[app]

# (str) Title of your application
title = Blackjack AI Genius

# (str) Package name
package.name = blackjack_ai_genius

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mario

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,txt

# (str) Application version
version = 0.1

# (list) Application requirements
# Librerie testate e compatibili con Python 3.10 e Kivy 2.3.0
requirements = python3,kivy==2.3.0,pyjnius==1.5.0,cython==0.29.36,requests,certifi,urllib3,idna,chardet

# (list) Permissions richiesti (necessari per rete, Telegram e scrittura file)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Supported orientations
orientation = portrait

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK / AAB will support
android.minapi = 21

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Indicate whether the screen should stay on
android.wakelock = True

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (bool) Allow app data auto backup (solo una riga)
android.allow_backup = True

# (bool) Use private data storage (più sicuro)
android.private_storage = True

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

# (str) Android entry point (default per Kivy)
android.entrypoint = org.kivy.android.PythonActivity

# (str) Bootstrap usato per Android build
p4a.bootstrap = sdl2

# (str) Percorso dove verranno salvati gli APK compilati
bin_dir = ~/apk_builds

# (list) Cartelle da escludere
source.exclude_dirs = tests,venv,__pycache__,.buildozer

# (bool) Non compila in bytecode (mantiene file leggibili)
#android.no-byte-compile-python = False

# (bool) App non in fullscreen
fullscreen = 0


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug completo)
log_level = 2

# (int) Display warning se buildozer è eseguito come root
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (APK)
bin_dir = ~/apk_builds
