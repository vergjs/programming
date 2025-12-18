import unittest
import os
from src.lab5.Task_product import Order, OrderValidator, OrderFormatter, OrderProcessor

class OrderProcessingTest(unittest.TestCase):
    """
    Модульные тесты для обработки заказов продуктового магазина.
    """

    def setUp(self):
        """
        Создание временного файла с заказами для тестирования.
        """
        self.orders_file = "test_orders.txt"
        with open(self.orders_file, "w", encoding="utf-8") as f:
            # валидный заказ
            f.write("12345;Сыр, Хлеб, Сыр;Иванов Иван Иванович;Россия. Москва. Москва. Тверская;+7-999-888-77-66;MAX\n")
            # невалидный адрес
            f.write("12346;Молоко, Яблоки;Петров Петр;Россия. Москва. Москва;+7-999-777-66-55;MIDDLE\n")
            # невалидный телефон
            f.write("12347;Хлеб, Масло;Сидоров Сидор;Россия. Ленинградская область. Санкт-Петербург. Невский;+7-999-888-77;LOW\n")

        self.processor = OrderProcessor(self.orders_file)
        self.processor.read_orders()

    def tearDown(self):
        """
        Удаление временного файла после тестов.
        """
        os.remove(self.orders_file)
        if os.path.exists("test_valid.txt"):
            os.remove("test_valid.txt")
        if os.path.exists("test_invalid.txt"):
            os.remove("test_invalid.txt")

    def test_validate_address(self):
        """Проверка валидного и невалидного адреса"""
        valid_order = self.processor.valid_orders[0]
        validator = OrderValidator()
        result, error = validator.validate_address(valid_order)
        self.assertTrue(result)
        self.assertIsNone(error)

        invalid_order = Order("00001", "Продукт", "ФИО", "", "+7-111-222-33-44", "MAX")
        result, error = validator.validate_address(invalid_order)
        self.assertFalse(result)
        self.assertEqual(error, "no data")

    def test_validate_phone(self):
        """Проверка валидного и невалидного телефона"""
        valid_order = self.processor.valid_orders[0]
        validator = OrderValidator()
        result, error = validator.validate_phone(valid_order)
        self.assertTrue(result)
        self.assertIsNone(error)

        invalid_order = Order("00002", "Продукт", "ФИО", "Россия. Москва. Москва. Тверская", "+7-111-22-33", "MAX")
        result, error = validator.validate_phone(invalid_order)
        self.assertFalse(result)
        self.assertEqual(error, "+7-111-22-33")

    def test_format_products(self):
        """Проверка корректного форматирования продуктов"""
        formatter = OrderFormatter()
        products_str = "Сыр, Хлеб, Сыр, Масло, Масло, Масло"
        formatted = formatter.format_products(products_str)
        self.assertIn("Сыр x2", formatted)
        self.assertIn("Хлеб", formatted)
        self.assertIn("Масло x3", formatted)

    def test_process_orders_and_files(self):
        """Проверка обработки заказов и записи файлов"""
        self.processor.write_valid_orders("test_valid.txt")
        self.processor.write_invalid_orders("test_invalid.txt")

        with open("test_valid.txt", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertIn("Сыр x2", lines[0])  # проверка форматирования

        with open("test_invalid.txt", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # 2 ошибки: адрес + телефон

    def test_sort_orders(self):
        """Проверка сортировки заказов по стране и приоритету"""
        # добавим еще один валидный заказ для теста сортировки
        order = Order("12348", "Чай", "Кузнецов Кузьма", "Франция. Париж. Париж. Лувр", "+3-111-222-33-44", "LOW")
        self.processor.process_order(order)
        self.processor.sort_orders()

        # первый заказ должен быть из России
        self.assertTrue(self.processor.valid_orders[0].country.startswith("Россия"))
        # последний заказ — Франция
        self.assertEqual(self.processor.valid_orders[-1].country, "Франция")


if __name__ == "__main__":
    unittest.main()
