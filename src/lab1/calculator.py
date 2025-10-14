"""
Простой калькулятор для подсчёта выражений состоящих из двух чисел, который может выполнять четыре базовые арифметические операции:
сложение, вычитание, умножение и деление.

Пользователь вводит выражение в виде строки.
Программа автоматически определяет операцию, выполняет вычисление и выводит результат.
"""

def calculate(expression):
    """
    Вычисляет простое арифметическое выражение.

    Поддерживаемые операции:
        - Сложение (+)
        - Вычитание (-)
        - Умножение (*)
        - Деление (/)

    Внутри функции:
        - x — первое число
        - y — второе число
        Оба значения извлекаются из строки `expression` и преобразуются в тип float.

    """
    expression = expression.replace(" ", "")  # удаляем пробелы

    if '+' in expression:
        x, y = expression.split('+')
        return float(x) + float(y)
    elif '-' in expression:
        x, y = expression.split('-')
        return float(x) - float(y)
    elif '*' in expression:
        x, y = expression.split('*')
        return float(x) * float(y)
    elif '/' in expression:
        x, y = expression.split('/')
        if float(y) == 0:
            return "Ошибка: деление на ноль!"
        return float(x) / float(y)
    else:
        return "Ошибка: операция не распознана!"


def main():
    """
    Запускает цикл, в котором пользователь может вводить выражения
    для вычисления.

    Для выхода из программы нужно ввести exit.
    """
    print("Калькулятор.")
    print('Для выхода из программы введите exit.')
    while True:
        expr = input("Введите выражение: ")
        if expr.lower() == 'exit':
            print("Выход из программы.")
            break

        result = calculate(expr)
        print(f"Результат: {result}\n")


if __name__ == "__main__":
    main()