/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.data

import android.content.Context
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import org.lunaris.dolby.domain.models.BandGain
import org.lunaris.dolby.domain.models.BandMode
import org.lunaris.dolby.domain.models.EqualizerPreset
import java.io.*

class PresetExportManager(private val context: Context) {

    companion object {
        private const val PRESET_FILE_VERSION = 2
        private const val FILE_EXTENSION = ".ldp"
        private const val MIME_TYPE = "application/json"
    }

    suspend fun exportPresetToJson(preset: EqualizerPreset): String = withContext(Dispatchers.IO) {
        val json = JSONObject().apply {
            put("version", PRESET_FILE_VERSION)
            put("name", preset.name)
            put("timestamp", System.currentTimeMillis())
            put("createdBy", "Lunaris Dolby Manager")
            put("bandMode", preset.bandMode.value)
            put("bandCount", preset.bandMode.bandCount)
            val gainsArray = JSONArray()
            preset.bandGains.forEach { bandGain ->
                gainsArray.put(JSONObject().apply {
                    put("frequency", bandGain.frequency)
                    put("gain", bandGain.gain)
                })
            }
            put("bandGains", gainsArray)
        }
        json.toString(2)
    }

    suspend fun importPresetFromJson(jsonString: String): EqualizerPreset = withContext(Dispatchers.IO) {
        val json = JSONObject(jsonString)
        
        val version = json.optInt("version", 1)
        if (version > PRESET_FILE_VERSION) {
            throw IllegalArgumentException("Preset version not supported")
        }
        val name = json.getString("name")
        val bandMode = if (json.has("bandMode")) {
            BandMode.fromValue(json.getString("bandMode"))
        } else {
            BandMode.TEN_BAND
        }
        
        val gainsArray = json.getJSONArray("bandGains")
        val bandGains = mutableListOf<BandGain>()
        for (i in 0 until gainsArray.length()) {
            val gainObj = gainsArray.getJSONObject(i)
            bandGains.add(BandGain(
                frequency = gainObj.getInt("frequency"),
                gain = gainObj.getInt("gain")
            ))
        }
        
        val expectedCount = bandMode.bandCount
        if (bandGains.size != expectedCount) {
            throw IllegalArgumentException(
                "Band count mismatch: expected $expectedCount, got ${bandGains.size}"
            )
        }
        
        EqualizerPreset(
            name = name,
            bandGains = bandGains,
            isUserDefined = true,
            bandMode = bandMode
        )
    }

    suspend fun exportPresetToFile(preset: EqualizerPreset, uri: Uri): Result<Unit> = 
        withContext(Dispatchers.IO) {
            try {
                val json = exportPresetToJson(preset)
                context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                    BufferedWriter(OutputStreamWriter(outputStream, Charsets.UTF_8)).use { writer ->
                        writer.write(json)
                    }
                }
                Result.success(Unit)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun importPresetFromFile(uri: Uri): Result<EqualizerPreset> = 
        withContext(Dispatchers.IO) {
            try {
                val json = context.contentResolver.openInputStream(uri)?.use { inputStream ->
                    BufferedReader(InputStreamReader(inputStream, Charsets.UTF_8)).use { reader ->
                        reader.readText()
                    }
                } ?: throw IOException("Cannot open file")
                val preset = importPresetFromJson(json)
                Result.success(preset)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun exportMultiplePresets(
        presets: List<EqualizerPreset>,
        uri: Uri
    ): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val json = JSONObject().apply {
                put("version", PRESET_FILE_VERSION)
                put("count", presets.size)
                put("timestamp", System.currentTimeMillis())
                put("supportsBandModes", true)
                
                val presetsArray = JSONArray()
                presets.forEach { preset ->
                    presetsArray.put(JSONObject(exportPresetToJson(preset)))
                }
                put("presets", presetsArray)
            }
            context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                BufferedWriter(OutputStreamWriter(outputStream, Charsets.UTF_8)).use { writer ->
                    writer.write(json.toString(2))
                }
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun importMultiplePresets(uri: Uri): Result<List<EqualizerPreset>> = 
        withContext(Dispatchers.IO) {
            try {
                val json = context.contentResolver.openInputStream(uri)?.use { inputStream ->
                    BufferedReader(InputStreamReader(inputStream, Charsets.UTF_8)).use { reader ->
                        reader.readText()
                    }
                } ?: throw IOException("Cannot open file")
                val jsonObject = JSONObject(json)
                val presetsArray = jsonObject.getJSONArray("presets")
                val presets = mutableListOf<EqualizerPreset>()
                for (i in 0 until presetsArray.length()) {
                    val presetJson = presetsArray.getJSONObject(i).toString()
                    presets.add(importPresetFromJson(presetJson))
                }
                Result.success(presets)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun createShareIntent(preset: EqualizerPreset): Result<android.content.Intent> = 
        withContext(Dispatchers.IO) {
            try {
                val json = exportPresetToJson(preset)
                val fileName = "${preset.name.replace(" ", "_")}_${preset.bandMode.value}band$FILE_EXTENSION"
                val cacheDir = File(context.cacheDir, "shared_presets")
                cacheDir.mkdirs()
                val file = File(cacheDir, fileName)
                
                FileOutputStream(file).use { fos ->
                    BufferedWriter(OutputStreamWriter(fos, Charsets.UTF_8)).use { writer ->
                        writer.write(json)
                    }
                }
                val uri = androidx.core.content.FileProvider.getUriForFile(
                    context,
                    "${context.packageName}.fileprovider",
                    file
                )
                val intent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                    type = MIME_TYPE
                    putExtra(android.content.Intent.EXTRA_STREAM, uri)
                    putExtra(android.content.Intent.EXTRA_SUBJECT, 
                        "Dolby Preset: ${preset.name} (${preset.bandMode.displayName})")
                    putExtra(android.content.Intent.EXTRA_TEXT, 
                        "Check out this custom Dolby ${preset.bandMode.displayName} audio preset!")
                    addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                Result.success(android.content.Intent.createChooser(intent, "Share Preset"))
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun copyPresetToClipboard(preset: EqualizerPreset): Result<Unit> = 
        withContext(Dispatchers.IO) {
            try {
                val json = exportPresetToJson(preset)
                val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) 
                    as android.content.ClipboardManager
                val clip = android.content.ClipData.newPlainText(
                    "Dolby Preset: ${preset.name} (${preset.bandMode.displayName})", 
                    json
                )
                clipboard.setPrimaryClip(clip)
                Result.success(Unit)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun importPresetFromClipboard(): Result<EqualizerPreset> = 
        withContext(Dispatchers.IO) {
            try {
                val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) 
                    as android.content.ClipboardManager
                val clip = clipboard.primaryClip
                
                if (clip != null && clip.itemCount > 0) {
                    val text = clip.getItemAt(0).text.toString()
                    val preset = importPresetFromJson(text)
                    Result.success(preset)
                } else {
                    Result.failure(IllegalStateException("No data in clipboard"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
}
