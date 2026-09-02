# Напишите 5 тестов на функцию all_division. Обязательно должен быть тест деления на ноль.
# Промаркируйте часть тестов. Например, smoke.
# В консоли с помощью pytest сделайте вызов:
# 1) Всех тестов
# 2) Только с маркером smoke
# 3) По маске. Выберите такую маску, чтобы под неё подпадали не все тесты, но больше одного
# Пришлите на проверку файл с тестами и скрины с вызовами и их результаты

import pytest


def all_division(*arg1):
    """
    Выполняет последовательное деление аргументов.

    Функция принимает произвольное количество аргументов и последовательно выполняет деление
    первого аргумента на все последующие. Возвращает результат деления.

    :param Числовые значения для деления. Должно быть как минимум два аргумента.
    :return: float: Результат деления первого аргумента на все последующие.
    """
    division = arg1[0]
    for i in arg1[1:]:
        division /= i
    return division


@pytest.mark.smoke
def test_division_by_two():
    """
    Проверяет, что результат деления 10 на 2 равен 5.0.
    """
    assert all_division(10, 2) == 5.0


@pytest.mark.smoke
def test_division_by_multiple_numbers():
    """
    Проверяет, что результат деления 100 на 5 и затем на 2 равен 10.0.
    """
    assert all_division(100, 5, 2) == 10.0


@pytest.mark.smoke
def test_division_by_zero():
    """
    Проверяет, что при делении 30 на 0 возникает исключение ZeroDivisionError.
    """
    with pytest.raises(ZeroDivisionError):
        all_division(30, 0)


@pytest.mark.skip(reason="division by -one")
def test_division_by_one():
    """
    Проверяет, что результат деления 10 на -1 равен -10.0.
    """
    assert all_division(10, -1) == -10.0


@pytest.mark.acceptance
def test_division_resulting_in_fraction():
    """
    Проверяет, что результат деления 10 на 4 равен 2.5.
    """
    assert all_division(10, 4) == 2.5