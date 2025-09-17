#
# Copyright (C) 2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Release name
PRODUCT_RELEASE_NAME := begonia

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/product_launched_with_p.mk)

# Inherit from begonia device
$(call inherit-product, device/redmi/begonia/device.mk)

# Inherit some common LineageOS stuff
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit some extras stuff
$(call inherit-product-if-exists, vendor/extras/extras.mk)
$(call inherit-product-if-exists, hardware/dolby/dolby.mk)
$(call inherit-product-if-exists, vendor/MiuiCameraLeica/config.mk)

# Axion Stuff
AXION_CAMERA_REAR_INFO := 64,8,2,2
AXION_CAMERA_FRONT_INFO := 20
AXION_MAINTAINER := Sai_Krishna
AXION_PROCESSOR := MTK_Helio_G90T
TARGET_INCLUDES_LOS_PREBUILTS := true
PRODUCT_NO_CAMERA := false
BYPASS_CHARGE_SUPPORTED := true

# CPUsets configuration
AXION_CPU_BG := 0-3
AXION_CPU_FG := 0-7
AXION_CPU_LIMIT_BG := 0-2
AXION_CPU_UNLIMIT_UI := 0-7
AXION_CPU_LIMIT_UI := 0-5
AXION_CPU_DISPLAY := 6-7
AXION_CPU_AUDIO := 0-4

# Boot animation
TARGET_BOOT_ANIMATION_RES := 1920

## Device identifier. This must come after all inclusions
PRODUCT_DEVICE := begonia
PRODUCT_NAME := lineage_begonia
PRODUCT_BRAND := Redmi
PRODUCT_MODEL := Redmi Note 8 Pro
PRODUCT_MANUFACTURER := Xiaomi

BUILD_FINGERPRINT := "Redmi/begonia/begonia:11/RP1A.200720.011/V12.5.8.0.RGGMIXM:user/release-keys"

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="begonia-user 11 RP1A.200720.011 V12.5.8.0.RGGMIXM release-keys" \
    DeviceName="begonia"

PRODUCT_PROPERTY_OVERRIDES += \
    ro.build.fingerprint=$(BUILD_FINGERPRINT)

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi
