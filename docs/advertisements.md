# Advertisements

This is a registry of Bluetooth Low Energy Advertisements sent by BlueTrace
implementations, under what circumstances they appear, and how they are used.

These are used by `covidsafescan` to find devices running a BlueTrace
implementation (eg: COVIDSafe, TraceTogether) in peripheral mode.

## Service UUID (complete list, 128-bit)

**Example (production):** `11 07 f9 18 c2 4c 09 fe f0 80 6a 4f 95 15 fc b3 2a b8`

**Example (staging):** `11 07 d3 f4 43 76 56 2f e8 9f c9 4b 0e 49 d3 33 e0 17`

_Used by default_ in `covidsafescan`, disable with `--no-adv-uuids`.

* Service UUID, 128-bit (0x07)
  * Service ID:
    * Production version: `b82ab3fc-1595-4f6a-80f0-fe094cc218f9`
    * Staging version: `17e033d3-490e-4bc9-9fe8-2f567643f4d3`

Sent by the [Android][service-android] and [iOS][service-ios] peripheral
implementations.

This is used by the [Android][service-android-central] and
[iOS][service-ios-central] Central implementations to discover devices.

## Apple overflow area

**Example (production):** `14 ff 4c 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

**Example (staging):** `14 ff 4c 00 01 00 00 80 00 00 00 00 00 00 00 00 00 00 00 00 00`

_Not used by default_ in `covidsafescan`, enable with `--apple`.

* Manufacturer-specific data (0xff)
  * Company ID: Apple (0x004c)
    * Apple BLE frame type: 0x01 (overflow area)
      * Production version: byte 1, bit `0x01` is set
      * Staging version: byte 3, bit `0x80` is set
      * Values of other bits depend on what other apps are using peripheral mode
        on the device. If there are _no_ other uses, remaining bits are unset
        (0).

Sent [by the iOS platform][cbpm-startadvertising] when the peripheral
implementation is in the background.

Its use is part of the iOS platform, and is only used by other iOS centrals.

The value is a 128 bit mask (16 bytes). iOS hashes each Service UUID in use on
the system to a 7-bit value (0 - 127), and sets that bit offset high. 

There is a significant chance of collisions as service UUIDs it reduces each
16 or 128-bit Service UUID to 1 bit in the mask.

**More info:** [Hacking The Overflow Area][hacking-overflow]

## Withings

**Example:** `06 ff ff 03 __ __ __`

_Used by default_ in `covidsafescan`, disable with `--no-adv-manuf`.

* Manufacturer-specific data (0xff)
  * Company ID: Withings (0x3ff)
  * Value: up 3 random ASCII characters: `0` - `9`, `a` - `f`
    * _OpenTrace_ will send less bytes if the value is too large.
    * _COVIDSafe_ v1.0.16 and earlier [has a static value][au-static]
      (CVE-2020-12858), and will always send 3 bytes.

Sent by the [Android Peripheral implementation][withings-android] _only_.

This [is used by the iOS Central implementation][withings-ios-reader] to work
around a platform limitation where
[iOS exposes device identifiers using an opaque UUID][cbpeer-identifier]
(`CBPeripheral.identifier`) which changes even when the MAC address is the same.

## Transmit power level

**Example:** `02 0a ff`

_Not used_ in `covidsafescan`.

* Transmit power level (0x0a)
  * Level: full (0xff)

Sent explicitly by the [Android Peripheral implementation][txpower-android] 
_only_.

Because this is a generic field, this _alone_ can't determine if someone is
using a BlueTrace implementation.

This is used by the [Android][txpower-android-central] (on Android O and later)
and [iOS][txpower-ios-central] implementations.

[service-android]: https://github.com/opentrace-community/opentrace-android/blob/7e0cdd8f52f4560c4ed9bb37d55a0f820d1cb0ae/app/src/main/java/io/bluetrace/opentrace/bluetooth/BLEAdvertiser.kt#L98
[service-android-central]: https://github.com/opentrace-community/opentrace-android/blob/7e0cdd8f52f4560c4ed9bb37d55a0f820d1cb0ae/app/src/main/java/io/bluetrace/opentrace/bluetooth/BLEScanner.kt#L36
[service-ios]: https://github.com/opentrace-community/opentrace-ios/blob/75fc506bef34ba48a727f9758f94823b9b4a2286/OpenTrace/Bluetrace/PeripheralController.swift#L71
[service-ios-central]: https://github.com/opentrace-community/opentrace-ios/blob/75fc506bef34ba48a727f9758f94823b9b4a2286/OpenTrace/Bluetrace/CentralController.swift#L100
[withings-android]: https://github.com/opentrace-community/opentrace-android/blob/7e0cdd8f52f4560c4ed9bb37d55a0f820d1cb0ae/app/src/main/java/io/bluetrace/opentrace/bluetooth/BLEAdvertiser.kt#L99
[withings-ios-reader]: https://github.com/opentrace-community/opentrace-ios/blob/75fc506bef34ba48a727f9758f94823b9b4a2286/OpenTrace/Bluetrace/CentralController.swift#L164-L166
[cbpeer-identifier]: https://developer.apple.com/documentation/corebluetooth/cbpeer/1620687-identifier
[cbpm-startadvertising]: https://developer.apple.com/documentation/corebluetooth/cbperipheralmanager/1393252-startadvertising
[au-static]: https://github.com/covidsafewatch/covidsafe-android-decompiled/blob/232b8420fa792dc05e2b20f016073a8f04105e56/src/sources/au/gov/health/covidsafe/bluetooth/BLEAdvertiser.java#L85
[hacking-overflow]: http://www.davidgyoungtech.com/2020/05/07/hacking-the-overflow-area
[txpower-android]: https://github.com/opentrace-community/opentrace-android/blob/7e0cdd8f52f4560c4ed9bb37d55a0f820d1cb0ae/app/src/main/java/io/bluetrace/opentrace/bluetooth/BLEAdvertiser.kt#L97
[txpower-android-central]: https://github.com/opentrace-community/opentrace-android/blob/e8b68321d1c567f45898744c7210323c1660df6f/app/src/main/java/io/bluetrace/opentrace/streetpass/StreetPassScanner.kt#L85
[txpower-ios-central]: https://github.com/opentrace-community/opentrace-ios/blob/75fc506bef34ba48a727f9758f94823b9b4a2286/OpenTrace/Bluetrace/CentralController.swift#L173-L181
