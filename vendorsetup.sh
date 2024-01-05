rm -rf device/redmi
git clone --depth=1 https://github.com/Saikrishna1504/device_redmi_begonia -b elixir device/redmi/begonia

rm -rf device/mediatek
git clone --depth=1 https://github.com/Saikrishna1504/device_mediatek_sepolicy -b udc device/mediatek/sepolicy

rm -rf vendor/redmi
git clone --depth=1 https://github.com/Saikrishna1504/vendor_redmi_begonia -b udc vendor/redmi/begonia
git clone --depth=1 https://github.com/begonia-dev/android_vendor_redmi_begonia-ims -b 14.o vendor/redmi/begonia-ims
git clone --depth=1 https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware -b udc device/redmi/begonia-firmware

rm -rf kernel/xiaomi
git clone --depth=1 https://github.com/Saikrishna1504/kernel_xiaomi_mt6785 -b udc kernel/xiaomi/begonia

rm -rf hardware/mediatek
git clone https://github.com/Saikrishna1504/hardware_mediatek -b udc hardware/mediatek


