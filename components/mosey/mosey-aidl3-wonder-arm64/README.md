# Official Mosey cloud component

Component revision 3, module version 0.5. This directory contains binary assets, an authenticated catalog and documentation only.

The app detects the required Wonder vendor interfaces instead of requiring an exact firmware build string or WLAN module digest. It still requires the supported ColorOS major version, Android 16 or newer, ARM64, compatible GMS/Mosey versions, system security types and an appropriate early-registration installer. Missing-component installation currently uses KSU/SukiSU initrc; Magisk/APatch installation is not implemented. A complete matching stock backend can be reused without installing this module.

The package contains six official files: Mosey APK, native server, FFI library and three declarations. No kernel, WLAN module or complete system-directory snapshot is included. Read-only additive overlays retain current system files, including new declarations added by an OTA. It does not guarantee compatibility with all ColorOS 17 devices.

ZIP size: 4,232,113 bytes. SHA-256: `6e2fb5658cef412cd03d15c250a06a304cb37e1e82743609e7b4f320924cdfb6`.

The authenticated catalog was issued after complete downloads through thirteen distinct CDN hosts were verified. Published revision ZIPs are immutable. The previous device-specific profile remains available for older clients.

Revision 2 OnePlus 15 acceptance: cloud installation, replacement of an older pending revision, reboot, system application registration, VINTF declaration, permissions, AIDL v3 and application enable succeeded. All 85 previously recorded declaration files remained visible. An isolated overlay test also preserved a simulated new OTA declaration. This revision has not yet repeated the prior revision's iPad bidirectional transfer test.

Before staging an update, the app retains separate backups of the active module and any earlier pending module. A staging failure restores the prior pending state. Disable through the app before managing the module; remove or disable the owned ROOT module and refresh its initrc through the ROOT manager, then reboot to remove its mounts. Do not delete metadata backing while mounted.

Revision 3 integrates only the ColorOS CN GMS adjustment. Each boot it reads the current original `/my_product/etc/permissions/oplus_google_cn_gms_features.xml`, removes only the standalone `cn.google.services` declaration, and preserves every other line, including `com.google.android.feature.services_updater`. It does not include other manufacturers' settings or force-enable a tile. This adds one generated file bind at post-fs-data; it does not remount a partition. The app verifies the actual PackageManager feature state before enabling AirDrop. New clients require component revision 3 or newer and have additional catalog mirrors.

Isolated device tests verified CN removal, preservation of other and newly added OTA declarations, and rejection of unrecognized XML without masking the original. Twelve application policy tests, build and lint passed. Revision 3 reboot acceptance with the standalone Unlock CN GMS module disabled is still pending; prior revision acceptance is not presented as that result.
