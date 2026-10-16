MIUI_CAM="vendor/redmi/begonia/proprietary/system/priv-app/MiuiCamera/MiuiCamera.apk"
if [ ! -f "$MIUI_CAM" ] || [ "${MIUI_CAM}.part00" -nt "$MIUI_CAM" ]; then
    cat "${MIUI_CAM}".part* > "$MIUI_CAM"
fi
