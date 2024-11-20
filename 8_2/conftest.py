import pytest
import paramiko
import subprocess
import time
from parser import *

SERVER_IP = "192.168.1.2"
SSH_HOST = "192.168.1.2"
SSH_USER = "artem_lupashchenko_io14"
SSH_PASSWORD = "123"

@pytest.fixture(scope="module")
def server():
    # Фікстура для запуску iperф-сервера через SSH.
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

    try:
        # Запуск iperf-сервера
        stdin, stdout, stderr = client.exec_command("iperf -s -D")
        time.sleep(60)  # Час для запуску сервера
        yield
    finally:
        # Завершення роботи сервера
        client.exec_command("pkill -f 'iperf -s'")
        client.close()

@pytest.fixture(scope="function")
def client():
     # Фікстура для запуску iperf-клієнта.
    command = ["iperf", "-c", SERVER_IP]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=60
        )
        parsed_output = parser(result.stdout)  # Парсинг виводу через парсер
        yield parsed_output
    except subprocess.TimeoutExpired:
        raise Exception("iperf клієнт перевищив час виконання")

