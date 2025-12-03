"""
Программа для распределения респондентов по возрастным группам.

Пользователь вводит границы групп (например: 18 35 60 80), после чего программа
автоматически формирует диапазоны возрастов:

    0–18, 19–35, 36–60, 61–80, 101+

Каждый респондент вводится пользователем в виде строки "<ФИО>,<возраст>".
Все респонденты распределяются по соответствующим возрастным категориям.

Программа выводит группы в порядке от старших к младшим.
Внутри группы респонденты сортируются:
    • по возрасту — по убыванию
    • по ФИО — по возрастанию

Использование:
    1. Ввести границы возрастных групп
    2. Ввести респондентов (команда 'END' завершает ввод)
    3. Получить отсортированный вывод групп
"""

import sys

class Respondent:
    """
    Класс для хранения информации о респонденте.

    Атрибуты:
        full_name (str): Полное имя респондента.
        age (int): Возраст респондента.
    """
    def __init__(self, full_name: str, age: int):
        """
        Инициализация объекта Respondent.

        Args:
            full_name (str): Полное имя респондента.
            age (int): Возраст респондента.
        """
        self.full_name = full_name  # сохраняем ФИО
        self.age = age  # сохраняем возраст

    def __str__(self):
        """
        Преобразование респондента в строку вида:
        "<ФИО> (<возраст>)"
        """
        return f"{self.full_name} ({self.age})"


class AgeGroupManager:
    """
    Класс для управления возрастными группами и распределения респондентов по ним.

    Атрибуты:
        boundaries (list[int]): Границы возрастных групп.
        groups (list[tuple[int,int]]): Список кортежей с диапазонами групп.
        grouped (dict[tuple[int,int], list[Respondent]]): Словарь с группами и списками респондентов.
    """
    def __init__(self, boundaries: list[int]):
        """
        Инициализация менеджера групп.

        Args:
            boundaries (list[int]): Список границ возрастных групп.
        """
        self.boundaries = sorted(boundaries)
        self.groups = self._build_groups()
        self.grouped: dict[tuple[int,int], list] = {g: [] for g in self.groups}
    def _build_groups(self) -> list[tuple[int,int]]:
        """
        Формируем возрастные группы как кортежи (start, end).

        Верхняя группа фиксирована 101-123.

        Returns:
            list[tuple[int,int]]: список диапазонов возрастов
        """
        groups = []

        if self.boundaries:
            groups.append((0, self.boundaries[0]))

        for i in range(len(self.boundaries) - 1):
            groups.append((self.boundaries[i] + 1, self.boundaries[i + 1]))

        groups.append((101, 123))
        return groups

    def add_respondent(self, respondent: Respondent):
        """
        Добавление респондента в соответствующую возрастную группу.

        Args:
            respondent (Respondent): объект респондента
        """
        for (start, end) in self.groups:
            if start <= respondent.age <= end:
                self.grouped[(start, end)].append(respondent)
                break

    def get_sorted_groups(self):
        """
        Формируем отсортированные группы для вывода.
        Сортировка внутри группы:
            - возраст по убыванию
            - ФИО по возрастанию

        Returns:
            List[Tuple[str, List[Respondent]]]: список кортежей (название группы, список респондентов)
        """
        result = []

        for (start, end) in reversed(self.groups):
            respondents = self.grouped[(start, end)]
            if not respondents:
                continue

            respondents.sort(key=lambda r: (-r.age, r.full_name))

            if start == 101:
                name = "101+"
            else:
                name = f"{start}-{end}"

            result.append((name, respondents))

        return result

    def print_groups(self):
        """
        Печать групп в формате:
        <Группа>: <ФИО_1> (возраст_1), <ФИО_2> (возраст_2), …
        """
        for name, respondents in self.get_sorted_groups():
            line = ", ".join(str(r) for r in respondents)
            print(f"{name}: {line}")


def main():
    """
    Основная функция программы.
    1. Получает границы возрастных групп.
    2. Создаёт AgeGroupManager.
    3. Ввод респондентов через input.
    4. Распечатывает группы.
    """

    if len(sys.argv) > 1:
        try:
            boundaries = [int(x) for x in sys.argv[1:]]
        except ValueError:
            print("Границы должны быть числами.")
            return
    else:

        boundaries_input = input("Введите границы возрастных групп через пробел: ")
        boundaries = [int(x) for x in boundaries_input.split()]

    if not boundaries:
        print("Укажите хотя бы одну границу возрастных групп.")
        return

    manager = AgeGroupManager(boundaries)


    print("Введите респондентов в формате '<ФИО>,<возраст>', строка 'END' для завершения:")
    while True:
        line = input().strip()
        if line == "END":
            break
        if not line:
            continue

        try:
            full_name, age_str = line.split(",", 1)
            age = int(age_str)

            if not (0 <= age <= 123):
                print(f"Возраст должен быть от 0 до 123, пропущен: {line}")
                continue

            respondent = Respondent(full_name.strip(), age)
            manager.add_respondent(respondent)

        except ValueError:
            print(f"Некорректный ввод, пропущен: {line}")

    manager.print_groups()


if __name__ == "__main__":
    main()