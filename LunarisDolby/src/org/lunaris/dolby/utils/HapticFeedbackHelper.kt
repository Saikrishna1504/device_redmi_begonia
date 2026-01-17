/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.utils

import android.content.Context
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.asCoroutineDispatcher
import kotlinx.coroutines.withContext
import java.util.concurrent.Executors

object HapticFeedbackHelper {
    
    private val executor = Executors.newSingleThreadExecutor().asCoroutineDispatcher()
    
    enum class HapticIntensity(val value: Int) {
        TEXTURE_TICK(1),
        TICK(2),
        CLICK(3),
        DOUBLE_CLICK(4),
        HEAVY_CLICK(5)
    }
    
    suspend fun triggerVibration(context: Context, intensity: HapticIntensity) {
        withContext(executor) {
            try {
                val vibrator = getVibrator(context) ?: return@withContext
                
                if (!vibrator.hasVibrator()) {
                    return@withContext
                }
                
                val effect = createVibrationEffect(intensity) ?: return@withContext
                
                vibrator.cancel()
                vibrator.vibrate(effect)
            } catch (e: Exception) {
            }
        }
    }
    
    private fun getVibrator(context: Context): Vibrator? {
        return try {
            val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
            vibratorManager?.defaultVibrator
        } catch (e: Exception) {
            null
        }
    }
    
    private fun createVibrationEffect(intensity: HapticIntensity): VibrationEffect? {
        return try {
            when (intensity) {
                HapticIntensity.TEXTURE_TICK -> 
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_TEXTURE_TICK)
                HapticIntensity.TICK -> 
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_TICK)
                HapticIntensity.CLICK -> 
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK)
                HapticIntensity.DOUBLE_CLICK -> 
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_DOUBLE_CLICK)
                HapticIntensity.HEAVY_CLICK -> 
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK)
            }
        } catch (e: Exception) {
            null
        }
    }
}

@Composable
fun rememberHapticFeedback(): HapticFeedback {
    val context = LocalContext.current
    return remember { HapticFeedback(context) }
}

class HapticFeedback(private val context: Context) {
    
    suspend fun performHaptic(intensity: HapticFeedbackHelper.HapticIntensity) {
        HapticFeedbackHelper.triggerVibration(context, intensity)
    }
    
    suspend fun click() = performHaptic(HapticFeedbackHelper.HapticIntensity.CLICK)
    suspend fun doubleClick() = performHaptic(HapticFeedbackHelper.HapticIntensity.DOUBLE_CLICK)
    suspend fun heavyClick() = performHaptic(HapticFeedbackHelper.HapticIntensity.HEAVY_CLICK)
    suspend fun tick() = performHaptic(HapticFeedbackHelper.HapticIntensity.TICK)
    suspend fun textureTick() = performHaptic(HapticFeedbackHelper.HapticIntensity.TEXTURE_TICK)
}
