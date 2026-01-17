/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.utils

import android.content.Context
import android.widget.Toast

object ToastHelper {
    private var currentToast: Toast? = null
    
    fun showToast(context: Context, message: String, duration: Int = Toast.LENGTH_SHORT) {
        currentToast?.cancel()
        
        currentToast = Toast.makeText(context, message, duration)
        currentToast?.show()
    }
    
    fun showLongToast(context: Context, message: String) {
        showToast(context, message, Toast.LENGTH_LONG)
    }
}
