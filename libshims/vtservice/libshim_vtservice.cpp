#include <dlfcn.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <new>
#include <vector>

#include <binder/IBinder.h>
#include <binder/IInterface.h>
#include <gui/BufferItem.h>
#include <gui/HdrMetadata.h>
#include <gui/IConsumerListener.h>
#include <gui/IGraphicBufferConsumer.h>
#include <gui/OccupancyTracker.h>

namespace android {
class IGraphicBufferProducer;
}

#include <ui/Fence.h>
#include <ui/FenceTime.h>
#include <ui/GraphicBuffer.h>
#include <ui/PixelFormat.h>
#include <ui/Rect.h>
#include <ui/Region.h>
#include <utils/Errors.h>
#include <utils/NativeHandle.h>
#include <utils/RefBase.h>
#include <utils/String16.h>
#include <utils/String8.h>
#include <utils/StrongPointer.h>

namespace {

// Android 14 BufferItem layout (0x118 bytes, without mPictureProfileHandle at +0x98)
struct LegacyBufferItem {
    android::sp<android::GraphicBuffer> mGraphicBuffer;
    android::sp<android::Fence> mFence;
    std::shared_ptr<android::FenceTime> mFenceTime{android::FenceTime::NO_FENCE};
    android::Rect mCrop{android::Rect::INVALID_RECT};
    uint32_t mTransform{0};
    uint32_t mScalingMode{0};
    int64_t mTimestamp{0};
    bool mIsAutoTimestamp{false};
    android_dataspace mDataSpace{HAL_DATASPACE_UNKNOWN};
    android::HdrMetadata mHdrMetadata{};
    uint64_t mFrameNumber{0};
    int mSlot{android::BufferItem::INVALID_BUFFER_SLOT};
    bool mIsDroppable{false};
    bool mAcquireCalled{false};
    bool mTransformToDisplayInverse{false};
    android::Region mSurfaceDamage{};
    bool mAutoRefresh{false};
    bool mQueuedBuffer{true};
    bool mIsStale{false};
    int mApi{0};
};

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
static_assert(sizeof(LegacyBufferItem) == 0x118, "LegacyBufferItem must be 0x118 bytes");
static_assert(offsetof(LegacyBufferItem, mTimestamp) == 0x38, "mTimestamp offset mismatch");
static_assert(offsetof(LegacyBufferItem, mFrameNumber) == 0x98, "mFrameNumber offset mismatch");
static_assert(offsetof(LegacyBufferItem, mSlot) == 0xa0, "mSlot offset mismatch");
static_assert(offsetof(LegacyBufferItem, mSurfaceDamage) == 0xa8, "mSurfaceDamage offset mismatch");
static_assert(offsetof(LegacyBufferItem, mAutoRefresh) == 0x110, "mAutoRefresh offset mismatch");
#pragma clang diagnostic pop

// Android 14 IGraphicBufferConsumer inherited from IInterface (public virtual RefBase)
// and did not have getReleasedBuffersExtended, allowUnlimitedSlots, or the 2-arg
// setMaxAcquiredBufferCount virtual methods introduced in Android 15/16.
class LegacyBufferQueueConsumer : public android::IInterface {
public:
    explicit LegacyBufferQueueConsumer(const android::sp<android::IGraphicBufferConsumer>& consumer)
        : mConsumer(consumer) {}
    ~LegacyBufferQueueConsumer() override = default;

    // vptr + 0x10: IInterface::onAsBinder
    android::IBinder* onAsBinder() override { return nullptr; }

    // vptr + 0x18: IGraphicBufferConsumer::getInterfaceDescriptor
    virtual const android::String16& getInterfaceDescriptor() const { return mDescriptor; }

    // vptr + 0x20: acquireBuffer
    virtual android::status_t acquireBuffer(LegacyBufferItem* outBuffer, nsecs_t presentWhen,
                                            uint64_t maxFrameNumber = 0) {
        if (outBuffer == nullptr) {
            return android::BAD_VALUE;
        }
        using BufferItemFn = void (*)(void*);
        static auto realCtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemC1Ev"));
        static auto realDtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemD1Ev"));

        alignas(alignof(android::BufferItem)) uint8_t storage[sizeof(android::BufferItem)] = {};
        auto* realItem = reinterpret_cast<android::BufferItem*>(storage);
        realCtor(realItem);

        android::status_t err = mConsumer->acquireBuffer(realItem, presentWhen, maxFrameNumber);
        if (err == android::OK) {
            outBuffer->mGraphicBuffer = realItem->mGraphicBuffer;
            outBuffer->mFence = realItem->mFence;
            outBuffer->mFenceTime = realItem->mFenceTime;
            outBuffer->mCrop = realItem->mCrop;
            outBuffer->mTransform = realItem->mTransform;
            outBuffer->mScalingMode = realItem->mScalingMode;
            outBuffer->mTimestamp = realItem->mTimestamp;
            outBuffer->mIsAutoTimestamp = realItem->mIsAutoTimestamp;
            outBuffer->mDataSpace = realItem->mDataSpace;
            outBuffer->mHdrMetadata = realItem->mHdrMetadata;
            outBuffer->mFrameNumber = realItem->mFrameNumber;
            outBuffer->mSlot = realItem->mSlot;
            outBuffer->mIsDroppable = realItem->mIsDroppable;
            outBuffer->mAcquireCalled = realItem->mAcquireCalled;
            outBuffer->mTransformToDisplayInverse = realItem->mTransformToDisplayInverse;
            outBuffer->mSurfaceDamage = realItem->mSurfaceDamage;
            outBuffer->mAutoRefresh = realItem->mAutoRefresh;
            outBuffer->mQueuedBuffer = realItem->mQueuedBuffer;
            outBuffer->mIsStale = realItem->mIsStale;
            outBuffer->mApi = realItem->mApi;
        }

        realDtor(realItem);
        return err;
    }

    // vptr + 0x28: detachBuffer
    virtual android::status_t detachBuffer(int slot) {
        return mConsumer->detachBuffer(slot);
    }

    // vptr + 0x30: attachBuffer
    virtual android::status_t attachBuffer(int* outSlot,
                                           const android::sp<android::GraphicBuffer>& buffer) {
        return mConsumer->attachBuffer(outSlot, buffer);
    }

    // vptr + 0x38: releaseBuffer
    virtual android::status_t releaseBuffer(int buf, uint64_t frameNumber, EGLDisplay display,
                                            EGLSyncKHR fence,
                                            const android::sp<android::Fence>& releaseFence) {
        return mConsumer->releaseBuffer(buf, frameNumber, display, fence, releaseFence);
    }

    // vptr + 0x40: consumerConnect
    virtual android::status_t consumerConnect(
            const android::sp<android::IConsumerListener>& consumer, bool controlledByApp) {
        return mConsumer->consumerConnect(consumer, controlledByApp);
    }

    // vptr + 0x48: consumerDisconnect
    virtual android::status_t consumerDisconnect() {
        return mConsumer->consumerDisconnect();
    }

    // vptr + 0x50: getReleasedBuffers
    virtual android::status_t getReleasedBuffers(uint64_t* slotMask) {
        return mConsumer->getReleasedBuffers(slotMask);
    }

    // vptr + 0x58: setDefaultBufferSize
    virtual android::status_t setDefaultBufferSize(uint32_t w, uint32_t h) {
        return mConsumer->setDefaultBufferSize(w, h);
    }

    // vptr + 0x60: setMaxBufferCount
    virtual android::status_t setMaxBufferCount(int bufferCount) {
        return mConsumer->setMaxBufferCount(bufferCount);
    }

    // vptr + 0x68: setMaxAcquiredBufferCount
    virtual android::status_t setMaxAcquiredBufferCount(int maxAcquiredBuffers) {
        return mConsumer->setMaxAcquiredBufferCount(maxAcquiredBuffers);
    }

    // vptr + 0x70: setConsumerName
    virtual android::status_t setConsumerName(const android::String8& name) {
        return mConsumer->setConsumerName(name);
    }

    // vptr + 0x78: setDefaultBufferFormat
    virtual android::status_t setDefaultBufferFormat(android::PixelFormat defaultFormat) {
        return mConsumer->setDefaultBufferFormat(defaultFormat);
    }

    // vptr + 0x80: setDefaultBufferDataSpace
    virtual android::status_t setDefaultBufferDataSpace(android_dataspace defaultDataSpace) {
        return mConsumer->setDefaultBufferDataSpace(defaultDataSpace);
    }

    // vptr + 0x88: setConsumerUsageBits
    virtual android::status_t setConsumerUsageBits(uint64_t usage) {
        return mConsumer->setConsumerUsageBits(usage);
    }

    // vptr + 0x90: setConsumerIsProtected
    virtual android::status_t setConsumerIsProtected(bool isProtected) {
        return mConsumer->setConsumerIsProtected(isProtected);
    }

    // vptr + 0x98: setTransformHint
    virtual android::status_t setTransformHint(uint32_t hint) {
        return mConsumer->setTransformHint(hint);
    }

    // vptr + 0xa0: getSidebandStream
    virtual android::status_t getSidebandStream(
            android::sp<android::NativeHandle>* outStream) const {
        return mConsumer->getSidebandStream(outStream);
    }

    // vptr + 0xa8: getOccupancyHistory
    virtual android::status_t getOccupancyHistory(
            bool forceFlush, std::vector<android::OccupancyTracker::Segment>* outHistory) {
        return mConsumer->getOccupancyHistory(forceFlush, outHistory);
    }

    // vptr + 0xb0: discardFreeBuffers
    virtual android::status_t discardFreeBuffers() {
        return mConsumer->discardFreeBuffers();
    }

    // vptr + 0xb8: dumpState
    virtual android::status_t dumpState(const android::String8& prefix,
                                        android::String8* outResult) const {
        return mConsumer->dumpState(prefix, outResult);
    }

private:
    android::sp<android::IGraphicBufferConsumer> mConsumer;
    android::String16 mDescriptor;
};

} // namespace

static bool isCallerInLibgui(const void* retAddr) {
    Dl_info info{};
    if (dladdr(retAddr, &info) != 0 && info.dli_fname != nullptr) {
        return strstr(info.dli_fname, "libgui.so") != nullptr;
    }
    return false;
}

extern "C" {

void _ZN7android10BufferItemC1Ev(void* thisptr) {
    if (isCallerInLibgui(__builtin_return_address(0))) {
        using BufferItemFn = void (*)(void*);
        static auto realCtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemC1Ev"));
        realCtor(thisptr);
        return;
    }
    new (thisptr) LegacyBufferItem();
}

void _ZN7android10BufferItemC2Ev(void* thisptr) {
    if (isCallerInLibgui(__builtin_return_address(0))) {
        using BufferItemFn = void (*)(void*);
        static auto realCtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemC2Ev"));
        realCtor(thisptr);
        return;
    }
    new (thisptr) LegacyBufferItem();
}

void _ZN7android10BufferItemD1Ev(void* thisptr) {
    if (isCallerInLibgui(__builtin_return_address(0))) {
        using BufferItemFn = void (*)(void*);
        static auto realDtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemD1Ev"));
        realDtor(thisptr);
        return;
    }
    static_cast<LegacyBufferItem*>(thisptr)->~LegacyBufferItem();
}

void _ZN7android10BufferItemD2Ev(void* thisptr) {
    if (isCallerInLibgui(__builtin_return_address(0))) {
        using BufferItemFn = void (*)(void*);
        static auto realDtor = reinterpret_cast<BufferItemFn>(
                dlsym(RTLD_NEXT, "_ZN7android10BufferItemD2Ev"));
        realDtor(thisptr);
        return;
    }
    static_cast<LegacyBufferItem*>(thisptr)->~LegacyBufferItem();
}
void _ZN7android11BufferQueue17createBufferQueueEPNS_2spINS_22IGraphicBufferProducerEEEPNS1_INS_22IGraphicBufferConsumerEEEb(
        android::sp<android::IGraphicBufferProducer>* outProducer,
        android::sp<LegacyBufferQueueConsumer>* outConsumer,
        bool consumerIsSurfaceFlinger) {
    using CreateBqFn = void (*)(android::sp<android::IGraphicBufferProducer>*,
                                android::sp<android::IGraphicBufferConsumer>*, bool);
    static auto realCreateBq = reinterpret_cast<CreateBqFn>(dlsym(
            RTLD_NEXT,
            "_ZN7android11BufferQueue17createBufferQueueEPNS_2spINS_22IGraphicBufferProducerEEEPNS1_INS_22IGraphicBufferConsumerEEEb"));
    android::sp<android::IGraphicBufferConsumer> realConsumer;
    realCreateBq(outProducer, &realConsumer, consumerIsSurfaceFlinger);
    if (outConsumer != nullptr) {
        *outConsumer = (realConsumer != nullptr) ? new LegacyBufferQueueConsumer(realConsumer) : nullptr;
    }
}

} // extern "C"
