import subprocess
import re

server_ip = '192.168.1.2'

def client(server_ip):
    """
    Підключення до сервера iperf та отримання результатів тесту.
    :param server_ip: IP-адреса сервера iperf
    :return: Вивід результатів команди та помилки
    """
    try:
        # Запуск команди iperf з підключенням до сервера
        process = subprocess.Popen(
            ["iperf", "-c", server_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Отримання виводу та помилок
        output, error = process.communicate()
        return output.decode("utf-8"), error.decode("utf-8")
    except Exception as e:
        return "", str(e)

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

# Виконання клієнтської функції та парсинг результату
result, error = client(server_ip)

if error:
    print("Помилка під час підключення до сервера:", error)
else:
    # Парсинг результату
    parsed_intervals = parser(result)
    
    # Фільтрація інтервалів відповідно до умов
    for value in parsed_intervals:
        if value['Transfer'] > 2 and value['Bitrate'] > 20:
            print(value)

