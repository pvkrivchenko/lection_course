# Из набора тестов задания task_2 создайте один тест с параметрами, используя @pytest.mark.parametrize
# Промаркируйте 1 параметр из выборки как smokе, а 1 набор данных скипните

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


@pytest.mark.parametrize("a, b, expected", [
    pytest.param(10, 2, 5.0, marks=pytest.mark.smoke),  # smoke test
    (100, 5, 20.0),  # smoke test
    (30, 0, None),  # smoke test
    pytest.param(10, -1, -10.0, marks=pytest.mark.skip(reason="link_bug_report")),  # skip test
    (10, 4, 2.5)  # acceptance test
])
def test_all_division(a, b, expected):
    """
    Проверяет функцию all_division с различными параметрами.

    Проверяет, что результат деления a на b равен expected.
    """
    if b == 0:
        with pytest.raises(ZeroDivisionError):
            all_division(a, b)
    else:
        assert all_division(a, b) == expected