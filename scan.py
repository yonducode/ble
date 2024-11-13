import asyncio
from bleak import BleakScanner
from typing import Set
import numpy as np

# Define constants for the distance estimation formula
txPower = -59  # RSSI at 1 meter distance, adjust based on beacon specs
n = 2.8001  # Path-loss exponent, typical values are between 2 and 4


tgt_mac = "DD340209CB26"
alphanumerical_charset = {
    c for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
}
assert len(alphanumerical_charset) == 26 * 2 + 10


def filter_in_chars(s: str, charset):
    return_chars = []
    for c in s:
        if c in charset:
            return_chars.append(c)
    return "".join(return_chars)


def estimate_distance(rssi, txPower, n=2):
    """
    Estimate the distance to the BLE beacon based on RSSI.

    Parameters:
    - rssi: Received Signal Strength Indicator
    - txPower: Expected RSSI value at 1 meter (calibrate as needed)
    - n: Path-loss exponent (environment factor, usually between 2 and 4)

    Returns:
    - Estimated distance in meters
    """
    return 10 ** ((txPower - rssi) / (10 * n))


async def scan_ble_devices():
    print("Scanning for BLE devices...")
    distances = []

    # Define a callback to process each discovered device
    def detection_callback(device, advertisement_data):
        if advertisement_data.rssi is not None:
            if filter_in_chars(str(device.address), alphanumerical_charset) == tgt_mac:
                distance = estimate_distance(advertisement_data.rssi, txPower, n)
                distances.append(distance)
                print(f"FOUND TGT BEACON")
                print(f"Device: {device.name} (MAC: {device.address})")
                print(
                    f"RSSI: {advertisement_data.rssi} dBm, Estimated Distance: {distance:.3f} meters\n"
                )

    # Start scanning and apply the callback for each device
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(60)  # Scan duration in seconds
    await scanner.stop()
    distances = np.array(distances)
    print(f"avg distance: {np.mean(distances)} | std distance: {np.std(distances)}")
    with open(f"distances.txt", "w") as f:
        f.write(str(distances.tolist()))


# Run the scan asynchronously
asyncio.run(scan_ble_devices())


# import asyncio
# from bleak import BleakScanner

# # Define constants for the distance estimation formula
# txPower = -59  # RSSI at 1 meter distance, adjust based on beacon specs
# n = 2  # Path-loss exponent, typical values are between 2 and 4


# def estimate_distance(rssi, txPower, n=2):
#     """
#     Estimate the distance to the BLE beacon based on RSSI.

#     Parameters:
#     - rssi: Received Signal Strength Indicator
#     - txPower: Expected RSSI value at 1 meter (calibrate as needed)
#     - n: Path-loss exponent (environment factor, usually between 2 and 4)

#     Returns:
#     - Estimated distance in meters
#     """
#     return 10 ** ((txPower - rssi) / (10 * n))


# async def scan_ble_devices():
#     print("Scanning for BLE devices...")

#     devices = await BleakScanner.discover()
#     for device in devices:
#         if device.rssi:
#             distance = estimate_distance(device.rssi, txPower, n)
#             print(f"Device: {device.name} (MAC: {device.address})")
#             print(
#                 f"RSSI: {device.rssi} dBm, Estimated Distance: {distance:.2f} meters\n"
#             )


# # Run the scan asynchronously
# asyncio.run(scan_ble_devices())
###
# import time

# from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter


# def callback(bt_addr, rssi, packet, additional_info):
#     print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))


# # scan for all TLM frames of beacons in the namespace "12345678901234678901"
# scanner = BeaconScanner(
#     callback,
#     # remove the following line to see packets from all beacons
#     device_filter=EddystoneFilter(namespace="12345678901234678901"),
#     packet_filter=EddystoneTLMFrame,
# )
# scanner.start()
# time.sleep(10)
# scanner.stop()
