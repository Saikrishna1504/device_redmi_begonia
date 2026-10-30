#include <android/fdsan.h>
#include <android/sync.h>
#include <errno.h>
#include <limits.h>
#include <stdint.h>

extern "C" {

void _ZN7android5FenceC1Ei(int32_t* self, int fd) {
    self[0] = 0;
    self[1] = fd;
    if (fd >= 0) {
        uint64_t tag = android_fdsan_create_owner_tag(
            ANDROID_FDSAN_OWNER_TYPE_UNIQUE_FD, reinterpret_cast<uint64_t>(&self[1]));
        android_fdsan_exchange_owner_tag(fd, 0, tag);
    }
}

int _ZN7android5Fence4waitEi(const int32_t* self, int timeout) {
    return (self[1] != -1 && sync_wait(self[1], timeout) < 0) ? -errno : 0;
}

int64_t _ZNK7android5Fence13getSignalTimeEv(const int32_t* self) {
    if (self[1] == -1) return -1;
    auto* finfo = sync_file_info(self[1]);
    if (!finfo) return -1;
    if (finfo->status != 1) {
        int32_t status = finfo->status;
        sync_file_info_free(finfo);
        return status < 0 ? -1 : INT64_MAX;
    }
    uint64_t ts = 0;
    auto* pinfo = sync_get_fence_info(finfo);
    for (uint32_t i = 0; i < finfo->num_fences; i++) {
        if (pinfo[i].timestamp_ns > ts) ts = pinfo[i].timestamp_ns;
    }
    sync_file_info_free(finfo);
    return static_cast<int64_t>(ts);
}

} // extern "C"
