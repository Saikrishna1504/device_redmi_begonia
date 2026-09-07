/*
 * Copyright (C) 2024 LibreMobileOS Foundation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include "CameraProviderExtension.h"

#include <fstream>
#include <unistd.h>

static const std::string kTorchBrightnessPath =
        "/sys/devices/platform/flashlights_mt6360/torchbrightness";

template <typename T>
static void writeValue(const std::string& path, const T& value) {
    std::ofstream file(path);
    file << value;
}

template <typename T>
static T readValue(const std::string& path, const T& def) {
    std::ifstream file(path);
    T result;
    file >> result;
    return file.fail() ? def : result;
}

bool supportsTorchStrengthControlExt() {
    return access(kTorchBrightnessPath.c_str(), W_OK) == 0;
}

int32_t getTorchDefaultStrengthLevelExt() {
    return 3;
}

int32_t getTorchMaxStrengthLevelExt() {
    return 7;
}

int32_t getTorchStrengthLevelExt() {
    return readValue(kTorchBrightnessPath, 0);
}

void setTorchStrengthLevelExt(int32_t torchStrength, bool enabled) {
    writeValue(kTorchBrightnessPath, (enabled && torchStrength > 0) ? torchStrength : 0);
}
