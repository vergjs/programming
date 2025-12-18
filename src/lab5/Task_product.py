"""
Данная программа предназначена для чтения и обработки заказов,
хранящихся в текстовом файле orders.txt. Каждая строка входного файла
представляет собой отдельный заказ и содержит информацию о номере
заказа, наборе продуктов, данных заказчика, адресе доставки, номере
телефона и приоритете доставки.

В ходе работы программы выполняются следующие действия:
    1. Чтение заказов из входного файла.
    2. Проверка корректности адреса доставки и номера телефона.
    3. Формирование списка невалидных заказов с указанием типа ошибки.
    4. Форматирование списка продуктов с подсчётом количества
       одинаковых наименований.
    5. Сортировка валидных заказов по стране доставки и приоритету
       (от MAX к LOW).
    6. Запись результатов обработки в выходные файлы:
           - order_country.txt — файл с валидными заказами;
           - non_valid_orders.txt — файл с ошибками в заказах.

"""


import re
from collections import Counter


class Order:
    """
    Класс, описывающий один заказ продуктового онлайн-магазина.

    Содержит все данные, считанные из входного файла, а также поля,
    которые заполняются в процессе валидации и обработки заказа.

    Атрибуты:
        order_id (str): Номер заказа (пятизначное число).
        products (str): Строка с перечнем заказанных продуктов.
        fio (str): ФИО заказчика.
        address (str): Полный адрес доставки в формате:
            <Страна>. <Регион>. <Город>. <Улица>
        phone (str): Номер телефона заказчика.
        priority (str): Приоритет доставки (MAX, MIDDLE, LOW).

        country (str): Страна доставки (вычисляется после валидации).
        short_address (str): Адрес доставки без указания страны
            в формате: <Регион>. <Город>. <Улица>
    """

    def __init__(self, order_id, products, fio, address, phone, priority):
        """
        Инициализирует объект заказа.

        Параметры:
            order_id (str): Номер заказа.
            products (str): Список продуктов одной строкой.
            fio (str): ФИО заказчика.
            address (str): Полный адрес доставки.
            phone (str): Номер телефона.
            priority (str): Приоритет доставки.
        """
        self.order_id = order_id
        self.products = products
        self.fio = fio
        self.address = address
        self.phone = phone
        self.priority = priority

        self.country = None
        self.short_address = None


class OrderValidator:
    """
    Класс, отвечающий за проверку (валидацию) данных заказа.

    В рамках данной лабораторной работы выполняется проверка
    только двух атрибутов заказа:
        1. Адрес доставки
        2. Номер телефона

    Класс используется как отдельный объект, инкапсулирующий
    всю логику валидации данных.
    """

    def __init__(self):
        """
        Инициализирует объект валидатора заказа.

        При создании объекта компилируется регулярное выражение
        для проверки номера телефона.
        """
        self.phone_pattern = re.compile(
            r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
        )

    def validate_address(self, order):
        """
        Проверяет корректность адреса доставки заказа.

        Адрес считается корректным, если:
            - поле адреса не пустое;
            - адрес содержит ровно четыре части,
              разделённые точкой:
              <Страна>. <Регион>. <Город>. <Улица>

        В случае успешной проверки:
            - в объекте заказа сохраняется страна доставки;
            - формируется сокращённый адрес без страны.

        Параметры:
            order (Order): Объект заказа, адрес которого проверяется.

        Возвращает:
            tuple:
                (True, None) — если адрес корректен;
                (False, str) — если адрес некорректен,
                где str — проблемное значение или строка 'no data'.
        """
        if not order.address:
            return False, 'no data'

        parts = [p.strip() for p in order.address.split('.')]
        if len(parts) != 4:
            return False, order.address

        order.country = parts[0]
        order.short_address = f"{parts[1]}. {parts[2]}. {parts[3]}"
        return True, None

    def validate_phone(self, order):
        """
        Проверяет корректность номера телефона заказа.

        Номер телефона считается корректным, если:
            - поле не пустое;
            - номер соответствует шаблону +x-xxx-xxx-xx-xx.

        Параметры:
            order (Order): Объект заказа, номер телефона которого проверяется.

        Возвращает:
            tuple:
                (True, None) — если номер телефона корректен;
                (False, str) — если номер телефона некорректен,
                где str — проблемное значение или строка 'no data'.
        """
        if not order.phone:
            return False, 'no data'

        if not self.phone_pattern.match(order.phone):
            return False, order.phone

        return True, None


class OrderFormatter:
    """
    Класс, отвечающий за форматирование данных заказа.

    В рамках задания выполняется форматирование списка продуктов:
    одинаковые продукты группируются и дополняются количеством.
    """

    def format_products(self, products_str):
        """
        Форматирует строку с перечнем продуктов заказа.

        Исходная строка может содержать повторяющиеся наименования.
        В результате одинаковые продукты объединяются с указанием
        количества повторений.

        Пример:
            Входная строка:
                "Сыр, Колбаса, Сыр, Макароны"
            Результат:
                "Сыр x2, Колбаса, Макароны"

        Параметры:
            products_str (str): Исходная строка с продуктами.

        Возвращает:
            str: Отформатированная строка продуктов.
        """
        products = [p.strip() for p in products_str.split(',')]
        counter = Counter(products)

        result = []
        for product, count in counter.items():
            if count > 1:
                result.append(f"{product} x{count}")
            else:
                result.append(product)

        return ', '.join(result)


class OrderProcessor:
    """
    Главный управляющий класс программы.

    Отвечает за полный цикл обработки заказов:
        - чтение заказов из входного файла;
        - валидацию заказов;
        - сортировку корректных заказов;
        - запись результатов в выходные файлы.
    """

    PRIORITY_ORDER = {'MAX': 0, 'MIDDLE': 1, 'LOW': 2}

    def __init__(self, input_file):
        """
        Инициализирует обработчик заказов.

        Параметры:
            input_file (str): Имя входного файла с заказами.
        """
        self.input_file = input_file
        self.valid_orders = []
        self.invalid_orders = []

        self.validator = OrderValidator()
        self.formatter = OrderFormatter()

    def read_orders(self):
        """
        Считывает заказы из входного файла.

        Для каждой строки входного файла:
            - создаётся объект Order;
            - выполняется его проверка и обработка.
        """
        with open(self.input_file, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(';')
                if len(parts) != 6:
                    continue

                order = Order(*parts)
                self.process_order(order)

    def process_order(self, order):
        """
        Выполняет валидацию и обработку одного заказа.

        Если заказ содержит хотя бы одну ошибку:
            - информация об ошибке сохраняется;
            - заказ исключается из списка корректных.

        Параметры:
            order (Order): Объект обрабатываемого заказа.
        """
        has_error = False

        valid_address, addr_error = self.validator.validate_address(order)
        if not valid_address:
            self.invalid_orders.append(
                f"{order.order_id};1;{addr_error}"
            )
            has_error = True

        valid_phone, phone_error = self.validator.validate_phone(order)
        if not valid_phone:
            self.invalid_orders.append(
                f"{order.order_id};2;{phone_error}"
            )
            has_error = True

        if has_error:
            return

        order.products = self.formatter.format_products(order.products)
        self.valid_orders.append(order)

    def sort_orders(self):
        """
        Сортирует корректные заказы.

        Сортировка выполняется по двум критериям:
            1. По стране доставки
               (Россия и Российская Федерация располагаются первыми);
            2. По приоритету доставки в порядке:
               MAX → MIDDLE → LOW.
        """
        def country_key(order):
            if order.country in ('Россия', 'Российская Федерация'):
                return (0, '')
            return (1, order.country)

        self.valid_orders.sort(
            key=lambda o: (country_key(o), self.PRIORITY_ORDER[o.priority])
        )

    def write_valid_orders(self, filename):
        """
        Записывает корректные заказы в выходной файл.

        Формат записи одной строки:
            <Номер заказа>;
            <Набор продуктов>;
            <ФИО>;
            <Адрес доставки (без страны)>;
            <Номер телефона>;
            <Приоритет доставки>
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for o in self.valid_orders:
                file.write(
                    f"{o.order_id};{o.products};{o.fio};"
                    f"{o.short_address};{o.phone};{o.priority}\n"
                )

    def write_invalid_orders(self, filename):
        """
        Записывает информацию о невалидных заказах в файл.

        Каждая строка файла содержит:
            <Номер заказа>;<Тип ошибки>;<Проблемное значение>
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for err in self.invalid_orders:
                file.write(err + '\n')


if __name__ == '__main__':
    """
    Точка входа в программу.

    Создаёт объект OrderProcessor, запускает обработку заказов
    и формирует выходные файлы:
        - order_country.txt;
        - non_valid_orders.txt.
    """
    processor = OrderProcessor('orders.txt')
    processor.read_orders()
    processor.sort_orders()
    processor.write_valid_orders('order_country.txt')
    processor.write_invalid_orders('non_valid_orders.txt')

