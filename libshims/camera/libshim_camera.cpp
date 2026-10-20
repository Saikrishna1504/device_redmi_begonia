#include <dlfcn.h>
#include <stdint.h>

extern "C" void _ZN7android7RefBaseD2Ev(void** self) {
    if (auto* refs = static_cast<int32_t*>(self ? self[1] : nullptr)) {
        if (refs[0] == (1 << 28) && refs[1] == 0) refs[4] |= 1;
    }
    using DtorFn = void (*)(void**);
    static DtorFn real = nullptr;
    if (!real) real = reinterpret_cast<DtorFn>(dlsym(RTLD_NEXT, "_ZN7android7RefBaseD2Ev"));
    if (real) real(self);
}
