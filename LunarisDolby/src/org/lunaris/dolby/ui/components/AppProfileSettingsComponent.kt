/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.ui.components

import android.content.Context
import android.content.Intent
import android.provider.Settings
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.Crossfade
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import org.lunaris.dolby.R
import org.lunaris.dolby.service.AppProfileMonitorService

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AppProfileSettingsCard(
    onManageClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val prefs = context.getSharedPreferences("dolby_prefs", Context.MODE_PRIVATE)
    var isEnabled by remember { 
        mutableStateOf(prefs.getBoolean("app_profile_monitoring_enabled", false)) 
    }
    var showToasts by remember {
        mutableStateOf(prefs.getBoolean("app_profile_show_toasts", true))
    }
    var headphoneOnlyMode by remember {
        mutableStateOf(prefs.getBoolean("app_profile_headphone_only", false))
    }
    var showPermissionDialog by remember { mutableStateOf(false) }

    Card(
        modifier = modifier.fillMaxWidth(),
        shape = MaterialTheme.shapes.extraLarge,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceBright
        )
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(bottom = 16.dp)
            ) {
                Surface(
                    modifier = Modifier.size(40.dp),
                    shape = MaterialTheme.shapes.medium,
                    color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Default.Apps,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onPrimaryContainer,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
                
                Spacer(modifier = Modifier.width(12.dp))
                
                Text(
                    text = stringResource(R.string.app_profiles_title),
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            
            Text(
                text = stringResource(R.string.app_profiles_desc),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(bottom = 16.dp)
            )
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = stringResource(R.string.app_profiles_auto_switch),
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.onSurface
                )
                
                Switch(
                    checked = isEnabled,
                    onCheckedChange = { enabled ->
                        if (enabled && !hasUsageStatsPermission(context)) {
                            showPermissionDialog = true
                        } else {
                            isEnabled = enabled
                            prefs.edit().putBoolean("app_profile_monitoring_enabled", enabled).apply()
                            
                            if (enabled) {
                                AppProfileMonitorService.startMonitoring(context)
                            } else {
                                AppProfileMonitorService.stopMonitoring(context)
                            }
                        }
                    },
                    thumbContent = {
                        Crossfade(
                            targetState = isEnabled,
                            animationSpec = MaterialTheme.motionScheme.slowEffectsSpec(),
                            label = "switch_icon"
                        ) { isChecked ->
                            if (isChecked) {
                                Icon(
                                    imageVector = Icons.Filled.Check,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.Filled.Close,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                )
            }
            
            AnimatedVisibility(visible = isEnabled) {
                Column {
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = context.getString(R.string.app_profiles_headphone_only),
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.Medium,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Text(
                                text = context.getString(R.string.app_profiles_headphone_only_description),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(top = 2.dp)
                            )
                        }
                        
                        Spacer(modifier = Modifier.width(12.dp))
                        
                        Switch(
                            checked = headphoneOnlyMode,
                            onCheckedChange = { enabled ->
                                headphoneOnlyMode = enabled
                                prefs.edit().putBoolean("app_profile_headphone_only", enabled).apply()
                            },
                            thumbContent = {
                                Crossfade(
                                    targetState = headphoneOnlyMode,
                                    animationSpec = MaterialTheme.motionScheme.slowEffectsSpec(),
                                    label = "headphone_switch_icon"
                                ) { isChecked ->
                                    if (isChecked) {
                                        Icon(
                                            imageVector = Icons.Filled.Check,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    } else {
                                        Icon(
                                            imageVector = Icons.Filled.Close,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    }
                                }
                            }
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = stringResource(R.string.app_profiles_show_toasts),
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.Medium,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        
                        Switch(
                            checked = showToasts,
                            onCheckedChange = { show ->
                                showToasts = show
                                prefs.edit().putBoolean("app_profile_show_toasts", show).apply()
                            },
                            thumbContent = {
                                Crossfade(
                                    targetState = showToasts,
                                    animationSpec = MaterialTheme.motionScheme.slowEffectsSpec(),
                                    label = "toast_switch_icon"
                                ) { isChecked ->
                                    if (isChecked) {
                                        Icon(
                                            imageVector = Icons.Filled.Check,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    } else {
                                        Icon(
                                            imageVector = Icons.Filled.Close,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    }
                                }
                            }
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Button(
                onClick = onManageClick,
                modifier = Modifier.fillMaxWidth(),
                shape = MaterialTheme.shapes.medium,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                )
            ) {
                Icon(
                    Icons.Default.Apps,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(stringResource(R.string.app_profiles_manage))
            }
        }
    }
    
    if (showPermissionDialog) {
        AlertDialog(
            onDismissRequest = { showPermissionDialog = false },
            icon = {
                Icon(
                    Icons.Default.Security,
                    contentDescription = null,
                    modifier = Modifier.size(32.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            },
            title = { 
                Text(
                    stringResource(R.string.app_profiles_permission_required),
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                ) 
            },
            text = {
                Text(
                    stringResource(R.string.app_profiles_permission_required_details),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
                        context.startActivity(intent)
                        showPermissionDialog = false
                    },
                    shape = MaterialTheme.shapes.medium
                ) {
                    Text(stringResource(R.string.app_profiles_grant_permission))
                }
            },
            dismissButton = {
                TextButton(
                    onClick = { showPermissionDialog = false },
                    shape = MaterialTheme.shapes.medium
                ) {
                    Text(stringResource(R.string.cancel))
                }
            },
            shape = MaterialTheme.shapes.extraLarge
        )
    }
}

private fun hasUsageStatsPermission(context: Context): Boolean {
    val appOpsManager = context.getSystemService(Context.APP_OPS_SERVICE) as android.app.AppOpsManager
    val mode = appOpsManager.checkOpNoThrow(
        "android:get_usage_stats",
        android.os.Process.myUid(),
        context.packageName
    )
    return mode == android.app.AppOpsManager.MODE_ALLOWED
}
