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
    'hardware/mediatek/libaedv',
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
    'vendor/lib/hw/audio.primary.mt6785.so': blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v30.so')
        .add_needed('libshim_audio.so'),

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

    'system/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),

    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v31.so')
        .replace_needed('libcodec2_hidl@1.2.so', 'libcodec2_hidl@1.2-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so'),

    'vendor/lib64/libcodec2_hidl@1.0-v31.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v33.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),

    'vendor/lib64/libcodec2_hidl@1.1-v31.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v33.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),

    'vendor/lib64/libcodec2_hidl@1.2-v31.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-v33.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v31.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),

    'vendor/lib64/libcodec2_hidl_plugin-v31.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so'),

    ('vendor/lib64/libcodec2_mtk_c2store.so',
     'vendor/lib64/libcodec2_vpp_qt_plugin.so',
     'vendor/lib64/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v31.so'),

    ('vendor/lib64/libcodec2_mtk_vdec.so',
     'vendor/lib64/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libformatter.so', 'libformatter_mtk.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v31.so')
        .replace_needed('libui.so', 'libui-v34.so'),

    'vendor/lib64/libcodec2_soft_common-v31.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v31.so'),

    'vendor/lib64/libcodec2_vndk-v31.so': blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),

    'vendor/lib64/libsfplugin_ccodec_utils-v31.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so'),

    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
        .regex_replace('1.1', '1.2'),

    ('vendor/lib/libwvhidl.so',
     'vendor/lib/mediadrm/libwvdrmengine.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),

    ('vendor/lib/libnvram.so',
    'vendor/lib/libsysenv.so',
    'vendor/lib64/libnvram.so',
    'vendor/lib64/libsysenv.so',
    'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron'): blob_fixup()
        .add_needed('libbase_shim.so'),

    'vendor/lib/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),

    'system/lib64/libmtk_vt_service.so': blob_fixup()
        .add_needed('libgui_shim.so'),

    'system/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),

    'system/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService/'),

    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),

    ('vendor/lib64/libalRnBRT_GL_GBWRAPPER.so',
     'vendor/lib64/libcam.hal3a.v3.so',
     'vendor/lib64/libeffecthal.base.so',
     'vendor/lib64/libmtkcam_grallocutils.so',
     'vendor/lib64/libmtkcam_3rdparty.vidhance.so'): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),

     'vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
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
