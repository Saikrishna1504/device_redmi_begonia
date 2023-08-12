LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := Debloat
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_TAGS := optional
LOCAL_OVERRIDES_PACKAGES += AmbientSensePrebuilt AppDirectedSMSService arcore
LOCAL_OVERRIDES_PACKAGES += CarrierSetup ConnMO ConnMetrics
LOCAL_OVERRIDES_PACKAGES += DCMO  DiagnosticsToolPrebuilt DMService
LOCAL_OVERRIDES_PACKAGES += GCS GoogleCamera GoogleTTS Jelly
LOCAL_OVERRIDES_PACKAGES += MaestroPrebuilt Maps MyVerizonServices NovaBugReportWrapper Ornament OemDmTrigger OBDM_Perm obdm_stub
LOCAL_OVERRIDES_PACKAGES += Phonograph PixelLiveWallpaperPrebuilt
LOCAL_OVERRIDES_PACKAGES += RecorderPrebuilt
LOCAL_OVERRIDES_PACKAGES += SafetyHubPrebuilt SCONE ScribePrebuilt Showcase SimpleCalculator SimpleCalendar Snap SoundAmplifierPrebuilt SprintDM SprintHM
LOCAL_OVERRIDES_PACKAGES += Tag Tycho
LOCAL_OVERRIDES_PACKAGES += USCCDM
LOCAL_OVERRIDES_PACKAGES += Videos VZWAPNLib VzwOmaTrigger
LOCAL_OVERRIDES_PACKAGES += WallpapersBReel2020
LOCAL_OVERRIDES_PACKAGES += YouTubeMusicPrebuilt
LOCAL_UNINSTALLABLE_MODULE := true
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_SRC_FILES := /dev/null
include $(BUILD_PREBUILT)
