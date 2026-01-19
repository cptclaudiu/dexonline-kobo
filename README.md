# Romanian Dictionary for Kobo eReader

[![Downloads](https://img.shields.io/github/downloads/cptclaudiu/dexonline-kobo/total)](https://github.com/cptclaudiu/dexonline-kobo/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/cptclaudiu/dexonline-kobo?style=flat)](../../stargazers)
[![License](https://img.shields.io/badge/license-dexonline-blue)](https://dexonline.ro/licenta)

Romanian explanatory dictionary for Kobo devices, built from the [dexonline.ro](https://dexonline.ro) database.

## Contents

- 311,733 entries
- 1,355,230 inflected forms
- ~1,000,000 definitions
- Sources: DEX '98, DEX '09, NODEX, DOOM 2/3, DN, MDA2, DER, Scriban, Șăineanu

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
cp dicthtml-ro.zip /Volumes/KOBOeReader/.kobo/dict/
diskutil eject /Volumes/KOBOeReader
```

Linux:
```
cp dicthtml-ro.zip /media/$USER/KOBOeReader/.kobo/dict/
umount /media/$USER/KOBOeReader
```

Windows (PowerShell):
```
Copy-Item dicthtml-ro.zip -Destination "E:\.kobo\dict\" -Force
```

## License

Data provided by [dexonline.ro](https://dexonline.ro) under their [license](https://dexonline.ro/licenta).

## References

- [dexonline.ro](https://dexonline.ro)
- [pgaskin/dictutil](https://github.com/pgaskin/dictutil)
