# Official Mosey cloud component

Component revision 2, module version 0.4. This directory contains binary assets, an authenticated catalog and documentation only.

The app detects the required Wonder vendor interfaces instead of requiring an exact firmware build string or WLAN module digest. It still requires the supported ColorOS major version, Android 16 or newer, ARM64, compatible GMS/Mosey versions, system security types and an appropriate early-registration installer. Missing-component installation currently uses KSU/SukiSU initrc; Magisk/APatch installation is not implemented. A complete matching stock backend can be reused without installing this module.

The package contains six official files: Mosey APK, native server, FFI library and three declarations. No kernel, WLAN module or complete system-directory snapshot is included. Read-only additive overlays retain current system files, including new declarations added by an OTA. It does not guarantee compatibility with all ColorOS 17 devices.

ZIP size: 4,231,333 bytes. SHA-256: `3e39420a4c70f586168fd0c19090bfb3e1678729f27e5b2cb5e0d9deea2ec29f`.

The authenticated catalog was issued after complete downloads through twelve distinct CDN hosts were verified. Published revision ZIPs are immutable. The previous device-specific profile remains available for older clients.

OnePlus 15 acceptance: cloud installation, replacement of an older pending revision, reboot, system application registration, VINTF declaration, permissions, AIDL v3 and application enable succeeded. All 85 previously recorded declaration files remained visible. An isolated overlay test also preserved a simulated new OTA declaration. This revision has not yet repeated the prior revision's iPad bidirectional transfer test.

Before staging an update, the app retains separate backups of the active module and any earlier pending module. A staging failure restores the prior pending state. Disable through the app before managing the module; remove or disable the owned ROOT module and refresh its initrc through the ROOT manager, then reboot to remove its mounts. Do not delete metadata backing while mounted.
