#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import struct

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
from extract_utils.utils import run_cmd

namespace_imports = [
    'device/redmi/begonia',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/mediatek/libaedv',
    'hardware/xiaomi',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None


def blob_fixup_symbolic(
    ctx: BlobFixupCtx,
    file: File,
    file_path: str,
    *args,
    **kwargs,
):
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())
    e_phoff = struct.unpack_from('<Q', data, 32)[0]
    e_phentsize, e_phnum = struct.unpack_from('<HH', data, 54)
    for i in range(e_phnum):
        p_off = e_phoff + i * e_phentsize
        p_type = struct.unpack_from('<I', data, p_off)[0]
        if p_type == 2:  # PT_DYNAMIC
            dyn_off, _, dyn_filesz = struct.unpack_from('<QQQ', data, p_off + 8)
            for pos in range(dyn_off, dyn_off + dyn_filesz, 16):
                d_tag, d_val = struct.unpack_from('<Qq', data, pos)
                if d_tag == 0:
                    break
                if d_tag in (15, 29):  # DT_RPATH, DT_RUNPATH -> DT_SYMBOLIC
                    struct.pack_into('<Qq', data, pos, 16, 0)
                elif d_tag == 30:  # DT_FLAGS |= DF_SYMBOLIC
                    struct.pack_into('<Qq', data, pos, 30, d_val | 0x2)
    with open(file_path, 'wb') as f:
        f.write(data)


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('libarmnn',
     'vendor.mediatek.hardware.camera.postproc@1.0',
     'vendor.mediatek.hardware.mms@1.0',
     'vendor.mediatek.hardware.mms@1.1',
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
        .add_needed('libshim_vtservice.so')
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

    'system/etc/init/init.vtservice.rc': blob_fixup()
        .regex_replace('/system_ext/bin/vtservice', '/system/bin/vtservice'),

    'system/lib64/libmtk_vt_service.so': blob_fixup()
        .add_needed('libshim_vtservice.so')
        .add_needed('libgui_shim.so'),

    'system/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),

    'system/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService/'),

    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),

    ('vendor/lib64/libalRnBRT_GL_GBWRAPPER.so',
     'vendor/lib64/libeffecthal.base.so',
     'vendor/lib64/libmtkcam_grallocutils.so',
     'vendor/lib64/libmtkcam_3rdparty.vidhance.so'): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),

    'vendor/lib64/libcam.hal3a.v3.so': blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so')
        .binary_regex_replace(
            b'\x68\x6b\x47\xb9\x68\x32\x00\xb9\x68\x6f\x47\xb9',
            b'\xa8\xfa\x4b\xb9\x68\x32\x00\xb9\x05\x00\x00\x14',
        ),

     'vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),

    'vendor/lib64/hw/hwcomposer.mt6785.so': blob_fixup()
        .binary_regex_replace(
            b'\x68\x00\x00\x34\x20\x00\x80\x52\x04\x00\x00\x14\x68\x62\x6f\x39\x1f\x01\x00\x71\xe0\x07\x9f\x1a',
            b'\x20\x00\x80\x52\xa8\x00\x00\x35\x68\x42\x40\xb9\x08\x15\x10\x12\x1f\x81\x41\x71\xe0\x17\x9f\x1a',
        )
        .binary_regex_replace(
            b'\x08\x60\x6e\x39\x48\x16\x00\x34\x08\xc0\x45\xf9',
            b'\x08\x40\x40\xb9\x48\x16\x90\x36\x08\xc0\x45\xf9',
        )
        .binary_regex_replace(
            b'\x09\x15\x10\x12\\\x3f\x81\x41\x71\x61\x00\x00\x54',
            b'\x09\x15\x10\x12\x3f\x81\x41\x71\x81\x14\x00\x54',
        )
        .binary_regex_replace(
            b'\x00\xe4\x00\x6f\x23\xfd\xff\x90\\\x24\xfd\xff\xd0\x25\xfd\xff\x90',
            b'\x0b\x40\xa0\x52\x5f\x01\x0b\x6b\x49\x02\x80\x52\x80\xff\xff\x54',
        )
        .binary_regex_replace(
            b'\x08\x15\x10\x12\x1f\x81\x41\x71\x61\x00\x00\x54\x35\x00\x80\x52\x09\x00\x00\x14',
            b'\x08\x15\x10\x12\x1f\x81\x41\x71\x61\x00\x00\x54\x35\x00\x80\x52\x29\x00\x00\x14',
        ),

    'vendor/lib64/libdpframework.so': blob_fixup()
        .binary_regex_replace(
            b'\xe0\x03\x80\x3d\xc1\x00\x00\x54\x81\x0e\x80\x52',
            b'\xe0\x03\x80\x3d\x1f\x20\x03\xd5\x81\x0e\x80\x52',
        )
        .binary_regex_replace(
            b'\x7f\x01\x0a\x6a\x80\xfb\xff\x54\x0a\x00\x8a\x52',
            b'\x7f\x01\x0a\x6a\xe0\xfa\xff\x54\x0a\x00\x8a\x52',
        )
        .binary_regex_replace(
            b'\xd8\x42\x02\x94\xe0\x03\x00\x91\xda\x42\x02\x94',
            b'\x20\x00\x80\x52\x1f\x20\x03\xd5\x1f\x20\x03\xd5',
        ),

    'vendor/lib64/libgpu_aux.so': blob_fixup()
        .binary_regex_replace(
            b'\xff\x03\x04\xd1\xfd\x7b\x0d\xa9\xfd\x43\x03\x91\xf6\x57\x0e\xa9',
            b'\x00\x00\x80\x52\xc0\x03\x5f\xd6\xfd\x43\x03\x91\xf6\x57\x0e\xa9',
        )
        .binary_regex_replace(
            b'\x9f\x02\x00\x72\xa9\x00\x80\x52\\\x29\x15\x9f\x1a\xe0\x03\x1f\x2a\x69\x02\x00\xb9',
            b'\x9f\x02\x00\x72\xa9\x00\x80\x52\x1f\x20\x03\xd5\xe0\x03\x1f\x2a\x69\x02\x00\xb9',
        ),

    'vendor/lib/libgpu_aux.so': blob_fixup()
        .binary_regex_replace(
            b'\x2d\xe9\xf0\x43\xb1\xb0\x04\x46\x25\x48\x14\\\x29',
            b'\x00\x20\x70\x47\xb1\xb0\x04\x46\x25\x48\x14\x29',
        )
        .binary_regex_replace(
            b'\x01\x22\x00\\\x28\x18\xbf\x03\x22\x0f\xe0\x01\x22\x00\\\x28\x18\xbf\x05\x22\x0a\xe0',
            b'\x03\x22\x00\x28\x00\xbf\x03\x22\x0f\xe0\x05\x22\x00\x28\x00\xbf\x05\x22\x0a\xe0',
        ),

    ('vendor/lib64/libalCFR.so',
     'vendor/lib64/libalLDC.so',
     'vendor/lib64/libalhLDC.so',
     'vendor/lib64/libapu-platform.so',
     'vendor/lib64/libneuron_platform.so'): blob_fixup()
        .call(blob_fixup_symbolic),

    'vendor/lib64/libmialgoengine.so': blob_fixup()
        .add_needed('libshim_camera.so'),


    'vendor/lib64/libmtkcam_3rdparty.customer.so': blob_fixup()
        .binary_regex_replace(b'\\\x3f\x91\\\x24\x71\x1a\x01\x89\x1a', b'\x29\x7d\x00\x11\x3a\x69\x1b\x12'),
    ('system/lib64/libcamera_algoup_jni.xiaomi.so',
     'system/lib64/libcamera_mianode_jni.xiaomi.so'): blob_fixup()
        .binary_regex_replace(
            b'\xe2\x03\x00\x91\xe0\x03\x13\xaa\x41\x00\x80\x52',
            b'\x60\x42\x00\x91\xa1\x01\x80\x52\x42\x00\x80\x52',
        )
        .binary_regex_replace(b'\x08\x9d\x40\xf9', b'\x68\x56\x40\xf9'),

    'system/lib64/libcamera_imagecodec_jni.xiaomi.so': blob_fixup()
        .add_needed('libui_shim.so')
        .binary_regex_replace(
            b'\xe2\x23\x00\x91\xe0\x03\x16\xaa\x81\x00\x80\x52\x08\x99\x40\xf9',
            b'\xc0\x42\x00\x91\xa1\x01\x80\x52\x82\x00\x80\x52\xc8\x56\x40\xf9',
        ),

    'system/lib64/libcamera_chroma_nr.xiaomi.so': blob_fixup()
        .binary_regex_replace(b'\x01\x06\x80\x52', b'\x61\x00\x80\x52'),

    'system/priv-app/MiuiCamera/MiuiCamera.apk': blob_fixup()
        .apktool_patch('blob-patches/MiuiCamera/')
        .call(lambda ctx, file, file_path, *args, **kwargs: run_cmd(['split', '--bytes=20M', '-d', file_path, f'{file_path}.part'])),
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
