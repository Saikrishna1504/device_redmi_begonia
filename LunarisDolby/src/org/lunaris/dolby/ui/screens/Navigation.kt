/*
 * Copyright (C) 2024-2025 Lunaris AOSP
 * SPDX-License-Identifier: Apache-2.0
 */

package org.lunaris.dolby.ui.screens

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import org.lunaris.dolby.ui.viewmodel.AppProfileViewModel
import org.lunaris.dolby.ui.viewmodel.DolbyViewModel
import org.lunaris.dolby.ui.viewmodel.EqualizerViewModel

sealed class Screen(val route: String) {
    object Settings : Screen("settings")
    object Equalizer : Screen("equalizer")
    object Advanced : Screen("advanced")
    object AppProfiles : Screen("app_profiles")
    object ImportExport : Screen("import_export")
}

@Composable
fun DolbyNavHost(
    dolbyViewModel: DolbyViewModel,
    equalizerViewModel: EqualizerViewModel
) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.Settings.route
    ) {
        composable(Screen.Settings.route) {
            ModernDolbySettingsScreen(
                viewModel = dolbyViewModel,
                navController = navController
            )
        }

        composable(Screen.Equalizer.route) {
            LaunchedEffect(Unit) {
                equalizerViewModel.loadEqualizer()
            }
            
            ModernEqualizerScreen(
                viewModel = equalizerViewModel,
                navController = navController
            )
        }

        composable(Screen.Advanced.route) {
            ModernAdvancedSettingsScreen(
                viewModel = dolbyViewModel,
                navController = navController
            )
        }
        
        composable(Screen.AppProfiles.route) {
            val context = LocalContext.current
            val appProfileViewModel: AppProfileViewModel = viewModel(
                factory = androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.getInstance(
                    context.applicationContext as android.app.Application
                )
            )
            
            AppProfileScreen(
                viewModel = appProfileViewModel,
                navController = navController
            )
        }
        
        composable(Screen.ImportExport.route) {
            PresetImportExportScreen(
                viewModel = equalizerViewModel,
                navController = navController
            )
        }
    }
}
