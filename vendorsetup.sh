rm -rf device/redmi
git clone --depth=1 https://github.com/ProjectElixir-Devices/device_redmi_begonia -b UNO device/redmi/begonia

rm -rf device/mediatek
git clone --depth=1 https://github.com/Saikrishna1504/device_mediatek_sepolicy -b UNO device/mediatek/sepolicy

rm -rf vendor/redmi
git clone --depth=1 https://github.com/Saikrishna1504/vendor_redmi_begonia -b udc vendor/redmi/begonia
git clone --depth=1 https://github.com/Saikrishna1504/vendor_redmi_begonia-ims -b udc vendor/redmi/begonia-ims
git clone --depth=1 https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware -b udc vendor/redmi/begonia-firmware

rm -rf kernel/xiaomi
git clone --depth=1 https://github.com/Saikrishna1504/kernel_xiaomi_mt6785 -b udc kernel/xiaomi/mt6785

rm -rf hardware/mediatek
git clone https://github.com/Saikrishna1504/hardware_mediatek -b udc hardware/mediatek

rm -rf hardware/lineage/compat
git clone --depth=1 -b lineage-21.0 https://github.com/LineageOS/android_hardware_lineage_compat.git hardware/lineage/compat

rm -rf packages/apps/MtkFMRadio
git clone --depth=1 https://github.com/begonia-dev/android_packages_apps_MtkFMRadio packages/apps/MtkFMRadio

rm -rf vendor/MiuiCameraLeica
git clone --depth=1 https://bitbucket.org/saikrishna1504/vendor_miuicameraleica vendor/MiuiCameraLeica
