# Перейти на https://sbis.ru/
# Перейти в раздел "Контакты"
# Найти баннер Тензор, кликнуть по нему
# Перейти на https://tensor.ru/
# Проверить, что есть блок новости "Сила в людях"
# Перейдите в этом блоке в "Подробнее" и убедитесь, что открывается https://tensor.ru/about
# Для сдачи задания пришлите код и запись с экрана прохождения теста

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# Инициализация веб-драйвера
driver = webdriver.Chrome()


class Selectors:
    BUTTON_CONTACT = '.sbisru-Header__container [href="/contacts"]'
    URL_SBISRU = "sbis.ru/"
    STAND_PROD = ''
    BANNER_LINK = '.sbisru-Contacts__border-left--border-xm [href="https://tensor.ru/"]'
    NEWS_POWER = '.tensor_ru-Index__block4-content .tensor_ru-Index__card-title'
    ABOUT_LINK = '.tensor_ru-Index__block4-content [href="/about"]'
    BLOCK_NEWS = '.tensor_ru-Index__block4-bg'
    ABOUT_COMPANY = '.tensor_ru-About__Banner-title'


class Texts:
    BLOCK_TEXT_POWER_IN_PEOPLE = 'Сила в людях'


def maximize_and_navigate(full_url):
    """
    Универсальный метод для перехода на страницу и максимизации окна браузера.

    :param full_url: Путь до страницы
    """
    driver.maximize_window()
    driver.get(full_url)  # Переход на указанную страницу


def switch_to_new_tab(tab_index):
    """
    Универсальный метод для переключения на новую вкладку браузера.

    :param tab_index: Индекс вкладки, на которую нужно переключиться (по умолчанию 1)
    """
    driver.switch_to.window(driver.window_handles[tab_index])


def finds_element(by, locator):
    """
    Универсальный метод для поиска элемента на странице.

    :param by: Метод поиска (например, By.CSS_SELECTOR)
    :param locator: Локатор элемента (например, "Selectors.ABOUT_LINK")
    :return: Найденный элемент или None, если элемент не найден
    """
    try:
        driver.find_element(by, locator)
    except NoSuchElementException:
        print(f"Элемент с локатором {locator} не найден")
        return None


def find_and_click_element(by, locator):
    """
    Универсальный метод для поиска элемента на странице и клика по нему.

    :param by: Метод поиска (например, By.CSS_SELECTOR)
    :param locator: Локатор элемента (например, "Selectors.ABOUT_LINK")
    :return: Найденный элемент или None, если элемент не найден
    """
    try:
        driver.find_element(by, locator).click()
    except NoSuchElementException:
        print(f"Элемент с локатором {locator} не найден")
        return None


def wait_for_element(timeout, by, locator):
    """
    Универсальная функция для ожидания появления элемента на странице.

    :param timeout: Время ожидания в секундах
    :param by: Метод поиска (например, By.CSS_SELECTOR)
    :param locator: Локатор элемента (например, "Selectors.BUTTON_CONTACT")
    :return: Найденный элемент или None, если элемент не найден
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((by, locator))
        )
        return element
    except TimeoutException:
        print(f"Элемент с локатором {locator} не найден в течение {timeout} секунд")
        return None


try:
    maximize_and_navigate(f'https://{Selectors.STAND_PROD}{Selectors.URL_SBISRU}')  # Переход на СБИС.РУ
    wait_for_element(10, By.CSS_SELECTOR, Selectors.BUTTON_CONTACT)  # Ожидание появления кнопки Контакты

    find_and_click_element(By.CSS_SELECTOR, Selectors.BUTTON_CONTACT)  # Переход на страницу "Контакты"
    wait_for_element(10, By.CSS_SELECTOR, Selectors.BANNER_LINK)  # Ожидание появления баннера

    find_and_click_element(By.CSS_SELECTOR, Selectors.BANNER_LINK)  # Переход по баннеру "Тензор"

    switch_to_new_tab(1)  # Акцент на таб в браузере
    action_chains = ActionChains(driver)
    action_chains.move_to_element(driver.find_element(By.CSS_SELECTOR, Selectors.BLOCK_NEWS))  # Окрол до объекта
    action_chains.perform()
    wait_for_element(10, By.CSS_SELECTOR, Selectors.NEWS_POWER)  # Ожидание появления Новости "Сила в людях"

    new_power = driver.find_element(By.CSS_SELECTOR, Selectors.NEWS_POWER)
    assert new_power.text == f"{Texts.BLOCK_TEXT_POWER_IN_PEOPLE}", f"Текст не соответствует ожидаемому'"  # Проверка блока
    wait_for_element(10, By.CSS_SELECTOR, Selectors.ABOUT_LINK)  # Ожидание появления кнопки Подробнее

    find_and_click_element(By.CSS_SELECTOR, Selectors.ABOUT_LINK)  # Переход на страницу tensor.ru/about
    wait_for_element(10, By.CSS_SELECTOR, Selectors.ABOUT_COMPANY)  # Ожидание появления кнопки Подробнее

    assert driver.current_url == "https://tensor.ru/about", "URL не соответствует ожидаемому"  # Проверка URL

    print("Тест успешно пройден")

finally:
    driver.quit()  # Закрытие браузера