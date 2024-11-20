import pytest 

def test_iperf_parsed_output(server, client):
    # Тест перевіряє розпарсений вивід iperf.

    # Перевірка, що фікстура клієнта повертає результат
    assert len(client) > 0, "Парсер не знайшов жодного результату"

    # Виведення повідомлення про початок перевірки
    print("Перевірка результатів клієнтського підключення iperf...")

    for result in client:
        interval = result["Interval"]
        transfer = result["Transfer"]
        bitrate = result["Bitrate"]

        # Виведення поточного результату на екран
        print(f"Інтервал: {interval}, Передано: {transfer} MB, Швидкість: {bitrate} Mbps")

        # Перевірка правильності значення "Transfer" і "Bitrate"
        assert transfer > 0, f"Невірне значення переданих даних: {transfer} MB"
        assert bitrate > 0, f"Невірне значення швидкості: {bitrate} Mbps"

        # Тест на позитивний результат:
        assert transfer > 2, f"Передано менше 2 MB: {transfer} MB"
        assert bitrate > 20, f"Пропускна здатність менше 20 Mbps: {bitrate} Mbps"

        # Тест на негативний результат (якщо значення повинно бути менше):
        # Для тестування можна вручну задати значення, які не проходять перевірку
        if transfer < 2:
            print(f"Тест не пройдено: Передано менше 2 MB - {transfer} MB")
        if bitrate < 20:
            print(f"Тест не пройдено: Пропускна здатність менше 20 Mbps - {bitrate} Mbps")

    print("Тест завершено успішно.")

