APPEND_CERTS := $(DEVICE_PATH)/dtbo/append_certs.py
BOARD_DTBO_CFG := $(DTBO_OUT)/dtboimg.cfg
MKDTIMG := $(HOST_OUT_EXECUTABLES)/mkdtimg$(HOST_EXECUTABLE_SUFFIX)
MKDTBOIMG := $(HOST_OUT_EXECUTABLES)/mkdtboimg$(HOST_EXECUTABLE_SUFFIX)

$(BOARD_PREBUILT_DTBOIMAGE): $(DTC) $(MKDTIMG) $(MKDTBOIMG)
$(BOARD_PREBUILT_DTBOIMAGE):
	@echo "Building dtbo.img"
	$(call make-dtbo-target,$(KERNEL_DEFCONFIG))
	$(call make-dtbo-target,dtbs)
	@if [ ! -s $(BOARD_DTBO_CFG) ]; then \
		echo "dtboimg.cfg is empty! Generating a dummy DTBO overlay to satisfy BOARD_KERNEL_SEPARATED_DTBO..." ; \
		mkdir -p $(DTBO_OUT)/arch/$(KERNEL_ARCH)/boot/dts/mediatek ; \
		echo '/dts-v1/; /plugin/; / { fragment@0 { target-path = "/"; __overlay__ { dummy = <1>; }; }; };' > $(DTBO_OUT)/dummy.dts ; \
		$(DTC) -@ -I dts -O dtb -o $(DTBO_OUT)/arch/$(KERNEL_ARCH)/boot/dts/mediatek/dummy.dtbo $(DTBO_OUT)/dummy.dts ; \
		echo "mediatek/dummy.dtbo" > $(BOARD_DTBO_CFG) ; \
		echo " id=0" >> $(BOARD_DTBO_CFG) ; \
	fi
	$(MKDTBOIMG) cfg_create $@ $(BOARD_DTBO_CFG) -d $(DTBO_OUT)/arch/$(KERNEL_ARCH)/boot/dts
	$(APPEND_CERTS) --alignment 16 --cert1 $(DEVICE_PATH)/dtbo/cert1.der --cert2 $(DEVICE_PATH)/dtbo/cert2.der --dtbo $(BOARD_PREBUILT_DTBOIMAGE)
