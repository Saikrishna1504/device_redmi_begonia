/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.ui.components

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch
import org.lunaris.dolby.R
import org.lunaris.dolby.utils.*

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun EnhancedBottomNavigationBar(
    currentRoute: String,
    onNavigate: (String) -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 3.dp,
        shadowElevation = 8.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 12.dp)
                .windowInsetsPadding(WindowInsets.navigationBars),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            val isHomeSelected = currentRoute == "settings"
            val isEqualizerSelected = currentRoute == "equalizer"
            val isAdvancedSelected = currentRoute == "advanced"
            
            EnhancedNavItem(
                icon = Icons.Default.Home,
                label = stringResource(R.string.home),
                selected = isHomeSelected,
                onClick = { onNavigate("settings") },
                isMiddleItem = false,
                isSiblingSelected = isAdvancedSelected,
                modifier = Modifier.weight(1f)
            )
            
            EnhancedNavItem(
                icon = Icons.Default.GraphicEq,
                label = stringResource(R.string.equalizer),
                selected = isEqualizerSelected,
                onClick = { onNavigate("equalizer") },
                isEqualizer = true,
                isMiddleItem = true,
                isSiblingSelected = isHomeSelected || isAdvancedSelected,
                modifier = Modifier.weight(1f)
            )
            
            EnhancedNavItem(
                icon = Icons.Default.Settings,
                label = stringResource(R.string.advanced),
                selected = isAdvancedSelected,
                onClick = { onNavigate("advanced") },
                isMiddleItem = false,
                isSiblingSelected = isHomeSelected,
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun EnhancedNavItem(
    icon: ImageVector,
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    isEqualizer: Boolean = false,
    isMiddleItem: Boolean = false,
    isSiblingSelected: Boolean = false
) {
    val interactionSource = remember { MutableInteractionSource() }
    val haptic = rememberHapticFeedback()
    val scope = rememberCoroutineScope()
    
    var isBouncing by remember { mutableStateOf(false) }
    val bounceScale by animateFloatAsState(
        targetValue = if (isBouncing) 1.3f else 1f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessMedium
        ),
        finishedListener = { isBouncing = false },
        label = "bounce_scale"
    )
    
    val backgroundWidth by animateDpAsState(
        targetValue = if (selected) 120.dp else 52.dp,
        animationSpec = MaterialTheme.motionScheme.slowSpatialSpec(),
        label = "background_width"
    )
    
    val backgroundHeight by animateDpAsState(
        targetValue = if (selected) 52.dp else 48.dp,
        animationSpec = MaterialTheme.motionScheme.slowSpatialSpec(),
        label = "background_height"
    )
    
    val horizontalPadding by animateDpAsState(
        targetValue = when {
            isMiddleItem && isSiblingSelected -> 4.dp
            else -> 8.dp
        },
        animationSpec = MaterialTheme.motionScheme.slowSpatialSpec(),
        label = "horizontal_padding"
    )
    
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = horizontalPadding),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .height(backgroundHeight)
                .width(backgroundWidth)
                .clip(RoundedCornerShape(if (selected) 50.dp else 16.dp))
                .background(
                    color = if (selected) {
                        MaterialTheme.colorScheme.primaryContainer
                    } else {
                        MaterialTheme.colorScheme.surfaceContainerHighest
                    }
                )
                .clickable(
                    interactionSource = interactionSource,
                    indication = null
                ) {
                    scope.launch {
                        haptic.performHaptic(HapticFeedbackHelper.HapticIntensity.HEAVY_CLICK)
                    }
                    isBouncing = true
                    onClick()
                },
            contentAlignment = Alignment.Center
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Box(
                    modifier = Modifier.scale(bounceScale),
                    contentAlignment = Alignment.Center
                ) {
                    if (isEqualizer) {
                        AnimatedEqualizerIconDynamic(
                            color = if (selected) {
                                MaterialTheme.colorScheme.onPrimaryContainer
                            } else {
                                MaterialTheme.colorScheme.onSurfaceVariant
                            },
                            size = 24.dp
                        )
                    } else {
                        Icon(
                            imageVector = icon,
                            contentDescription = label,
                            tint = if (selected) {
                                MaterialTheme.colorScheme.onPrimaryContainer
                            } else {
                                MaterialTheme.colorScheme.onSurfaceVariant
                            },
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
                
                AnimatedVisibility(
                    visible = selected,
                    enter = fadeIn(
                        animationSpec = tween(300, delayMillis = 100)
                    ) + expandHorizontally(
                        animationSpec = MaterialTheme.motionScheme.slowSpatialSpec(),
                        expandFrom = Alignment.Start
                    ),
                    exit = fadeOut(
                        animationSpec = tween(200)
                    ) + shrinkHorizontally(
                        animationSpec = tween(300),
                        shrinkTowards = Alignment.Start
                    )
                ) {
                    Row {
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelLarge.copy(
                                fontSize = 13.sp
                            ),
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            maxLines = 1
                        )
                    }
                }
            }
        }
    }
}
