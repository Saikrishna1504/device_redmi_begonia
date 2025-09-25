#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/redmi/begonia',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('libarmnn',
     'vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'system/lib/libsink-mtk.so': blob_fixup()
        .add_needed('libshim_vtservice.so'),

    'vendor/lib/hw/audio.primary.mt6785.so': blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v30.so')
        .add_needed('libshim_audio.so'),

    ('vendor/lib/hw/audio.usb.mt6785.so'): blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v30.so'),

    ('vendor/lib64/hw/android.hardware.thermal@2.0-impl.so',
     'vendor/lib64/hw/dfps.mt6785.so',
     'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.6-impl.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),

    'vendor/lib64/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v30.so'),

    ('vendor/bin/mnld',
     'vendor/lib/libaalservice.so',
     'vendor/lib/libcam.utils.sensorprovider.so',
     'vendor/lib64/libaalservice.so',
     'vendor/lib64/libcam.utils.sensorprovider.so'): blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),

    'vendor/bin/hw/android.hardware.keymaster@4.0-service.beanpod': blob_fixup()
        .add_needed('libshim_beanpod.so'),

    ('system/lib/libsource.so',
     'vendor/lib/libMtkOmxVdecEx.so'): blob_fixup()
        .add_needed('libui_shim.so'),

    'system/lib64/libem_support_jni.so': blob_fixup()
        .add_needed('libjni_shim.so'),

    ('vendor/lib/libwvhidl.so',
     'vendor/lib/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),

    'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron': blob_fixup()
        .add_needed('libbase_shim.so'),

    'vendor/lib/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),

    'system/lib/libmtk_vt_service.so': blob_fixup()
        .add_needed('libgui_shim.so'),

    'system/lib/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),

    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),

    ('vendor/lib64/libalRnBRT_GL_GBWRAPPER.so',
     'vendor/lib64/libcam.hal3a.v3.so',
     'vendor/lib64/libeffecthal.base.so',
     'vendor/lib64/libmtkcam_grallocutils.so',
     'vendor/lib64/libmtkcam_3rdparty.vidhance.so'): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'begonia',
    'redmi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
