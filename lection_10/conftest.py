import pytest
import time


@pytest.fixture(scope="class")
def class_fixture():
    """
    Фикстура для класса. Печатает время начала и окончания выполнения тестов класса.
    """
    start_time = time.time()
    print(f"\nНачало выполнения тестов класса: {time.ctime(start_time)}")

    yield

    end_time = time.time()
    print(f"\nОкончание выполнения тестов класса: {time.ctime(end_time)}")
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")


@pytest.fixture
def test_fixture():
    """
    Фикстура для конкретного теста. Печатает время выполнения теста.
    """
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"\nВремя выполнения теста: {end_time - start_time:.2f} секунд")