import unittest
from src.lab4.Task_opros import Respondent, AgeGroupManager

class AgeGroupManagerTest(unittest.TestCase):
    """
    Модульные тесты для AgeGroupManager и класса Respondent.
    """

    def setUp(self):
        """
        Создаём менеджер групп с границами для тестов
        """
        self.boundaries = [18, 25, 35, 45, 60, 80, 100]
        self.manager = AgeGroupManager(self.boundaries)

        # добавим тестовых респондентов
        self.respondents = [
            Respondent("Соколов Андрей Сергеевич", 15),
            Respondent("Егоров Алан Петрович", 7),
            Respondent("Ярилова Розалия Трофимовна", 29),
            Respondent("Старостин Ростислав Ермолаевич", 50),
            Respondent("Дьячков Нисон Иринеевич", 88),
            Respondent("Кошельков Захар Брониславович", 105),
            Respondent("Иванов Варлам Якунович", 88),
            Respondent("Алексеева Мария Ивановна", 29)
        ]

        for r in self.respondents:
            self.manager.add_respondent(r)

    def test_group_counts(self):
        """
        Проверка, что респонденты добавлены в правильные группы.
        """
        groups = self.manager.grouped
        # группа 0-18
        g_0_18 = groups[(0, 18)]
        self.assertEqual(len(g_0_18), 2)
        # группа 26-35
        g_26_35 = groups[(26, 35)]
        self.assertEqual(len(g_26_35), 2)
        # группа 46-60
        g_46_60 = groups[(46, 60)]
        self.assertEqual(len(g_46_60), 1)
        # группа 81-100
        g_81_100 = groups[(81, 100)]
        self.assertEqual(len(g_81_100), 2)
        # старшая группа 101+
        g_101 = groups[(101, 123)]
        self.assertEqual(len(g_101), 1)

    def test_sorting_within_groups(self):
        """
        Проверка сортировки респондентов по возрасту убыванию,
        при равном возрасте — по ФИО по возрастанию.
        """
        sorted_groups = self.manager.get_sorted_groups()
        # ищем группу 26-35
        for name, respondents in sorted_groups:
            if name == "26-35":
                # возраста должны быть 29,29
                self.assertEqual([r.age for r in respondents], [29, 29])
                # сортировка по ФИО
                self.assertEqual([r.full_name for r in respondents],
                                 ["Алексеева Мария Ивановна", "Ярилова Розалия Трофимовна"])

    def test_group_names_order(self):
        """
        Проверка, что группы возвращаются от старшей к младшей.
        """
        sorted_groups = self.manager.get_sorted_groups()
        names = [name for name, _ in sorted_groups]
        expected_order = ["101+", "81-100", "46-60", "26-35", "0-18"]
        self.assertEqual(names, expected_order)

    def test_print_groups_output(self):
        """
        Проверка формирования строкового вывода группы.
        """
        from io import StringIO
        import sys

        # перенаправляем stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        self.manager.print_groups()

        # возвращаем stdout обратно
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # проверим, что строки содержат ключевых респондентов
        self.assertIn("101+: Кошельков Захар Брониславович (105)", output)
        self.assertIn("81-100: Дьячков Нисон Иринеевич (88), Иванов Варлам Якунович (88)", output)
        self.assertIn("46-60: Старостин Ростислав Ермолаевич (50)", output)
        self.assertIn("26-35: Алексеева Мария Ивановна (29), Ярилова Розалия Трофимовна (29)", output)
        self.assertIn("0-18: Соколов Андрей Сергеевич (15), Егоров Алан Петрович (7)", output)


if __name__ == "__main__":
    unittest.main()
