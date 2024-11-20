import unittest
from client import client, parser

class TestIperfClient(unittest.TestCase):

    def test_client_success(self):
        # Тест успішного підключення до сервера.
        server_ip = "192.168.1.2"
        result, error = client(server_ip)
        self.assertFalse(error, "Expected no errors, but got one.")
        self.assertIn("sec", result, "Expected iperf output to include 'sec' intervals.")

    def test_client_failure(self):
        # Тест підключення до недоступного сервера.
        server_ip = "192.168.2.1"  # Неправильна IP-адреса
        result, error = client(server_ip)
        self.assertTrue(error, "Expected an error, but got none.")
        self.assertRegex(error.lower(), r"(error|connect failed|timed out|no route to host)",
                        "Unexpected error message format.")

class TestIperfParser(unittest.TestCase):

    def test_parser_success(self):
        # Тест коректного парсингу виводу iperf.
        sample_output = (
            "2.00-3.00 sec  3.91 MBytes  32.8 Mbits/sec\n"
            "3.00-4.00 sec  1.50 MBytes  12.5 Mbits/sec\n"
        )
        expected_result = [
            {'Interval': '2.00-3.00 sec', 'Transfer': 3.91, 'Bitrate': 32.8},
            {'Interval': '3.00-4.00 sec', 'Transfer': 1.50, 'Bitrate': 12.5}
        ]
        parsed_data = parser(sample_output)
        self.assertEqual(parsed_data, expected_result, "Parser output does not match expected result.")

    def test_parser_invalid_format(self):
        # Тест для некоректного формату виводу.
        sample_output = "Invalid iperf output without intervals"
        parsed_data = parser(sample_output)
        self.assertEqual(parsed_data, [], "Parser should return an empty list for invalid output.")
    
    def test_parser_unit_conversion(self):
        # Тест конвертації одиниць (KBytes, Gbits).
        sample_output = (
            "2.00-3.00 sec  4.00 KBytes  32.0 Kbits/sec\n"
            "3.00-4.00 sec  2.00 GBytes  1.00 Gbits/sec\n"
        )
        expected_result = [
            {'Interval': '2.00-3.00 sec', 'Transfer': 0.00390625, 'Bitrate': 0.03125},  # Перетворення K -> M
            {'Interval': '3.00-4.00 sec', 'Transfer': 2048.0, 'Bitrate': 1024.0}       # Перетворення G -> M
        ]
        parsed_data = parser(sample_output)
        self.assertEqual(parsed_data, expected_result, "Unit conversion in parser is incorrect.")

if __name__ == "__main__":
    unittest.main()

