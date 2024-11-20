import re

REGEXP = r"([\d\.]+-[\d\.]+ sec)\s+([\d\.]+)\s+([KMG]?Bytes)\s+([\d\.]+)\s+([KMG]?bits/sec)"

def parser(output):
    # Парсинг результатів iperf-клієнта.
    matches = re.findall(REGEXP, output)
    result = []
    for match in matches:
        interval, transfer, transfer_unit, bitrate, bitrate_unit = match
        transfer_mb = convert_to_megabytes(float(transfer), transfer_unit)
        bitrate_mbps = convert_to_megabits(float(bitrate), bitrate_unit)
        result.append({
            "Interval": interval,
            "Transfer": transfer_mb,
            "Bitrate": bitrate_mbps
        })
    return result

def convert_to_megabytes(value, unit):
    # Конвертація значень у Мбайти.
    unit = unit.lower()
    if unit == "kbytes":
        return value / 1024
    if unit == "gbytes":
        return value * 1024
    return value

def convert_to_megabits(value, unit):
    # Конвертація значень у Мбіт/с.
    unit = unit.lower()
    if unit == "kbits/sec":
        return value / 1024
    if unit == "gbits/sec":
        return value * 1024
    return value
