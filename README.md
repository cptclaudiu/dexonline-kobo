# Romanian Dictionary for Kobo eReader

[![Downloads](https://img.shields.io/github/downloads/cptclaudiu/dexonline-kobo/total)](https://github.com/cptclaudiu/dexonline-kobo/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/cptclaudiu/dexonline-kobo?style=flat)](../../stargazers)
[![License](https://img.shields.io/badge/license-dexonline-blue)](https://dexonline.ro/licenta)

Romanian explanatory dictionary for Kobo devices, built from the [dexonline.ro](https://dexonline.ro) database.

## Contents

- 113,827 entries with complete definitions
- 1,175,035 inflected forms for lookup
- Sources: DEX '98, DEX '96

The dictionary includes all inflected forms (declined nouns, conjugated verbs, adjectives), enabling direct lookup of any word form encountered in text.

## Installation

1. Download `dicthtml-ro.zip` from [Releases](../../releases/latest)
2. Connect your Kobo to computer via USB
3. Copy the file to `.kobo/dict/` (hidden folder on device)
4. Eject and disconnect the device

The `.kobo` folder is hidden by default:
- Windows: View → Hidden items
- macOS: `Cmd + Shift + .`

## Terminal installation

macOS:
```
curl -L -o dicthtml-ro.zip https://github.com/cptclaudiu/dexonline-kobo/releases/latest/download/dicthtml-ro.zip
cp dicthtml-ro.zip /Volumes/KOBOeReader/.kobo/dict/
diskutil eject /Volumes/KOBOeReader
```

Linux:
```
curl -L -o dicthtml-ro.zip https://github.com/cptclaudiu/dexonline-kobo/releases/latest/download/dicthtml-ro.zip
cp dicthtml-ro.zip /media/$USER/KOBOeReader/.kobo/dict/
umount /media/$USER/KOBOeReader
```

Windows (PowerShell):
```
Invoke-WebRequest -Uri "https://github.com/cptclaudiu/dexonline-kobo/releases/latest/download/dicthtml-ro.zip" -OutFile "dicthtml-ro.zip"
Copy-Item dicthtml-ro.zip -Destination "E:\.kobo\dict\" -Force
```

## License

Data provided by [dexonline.ro](https://dexonline.ro) under their [license](https://dexonline.ro/licenta).

## References

- [dexonline.ro](https://dexonline.ro)
- [pgaskin/dictutil](https://github.com/pgaskin/dictutil)
