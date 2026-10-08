# Авторизоваться на сайте https://fix-online.sbis.ru/
# Перейти в реестр Контакты
# Отправить сообщение самому себе
# Убедиться, что сообщение появилось в реестре
# Удалить это сообщение и убедиться, что удалили
# Для сдачи задания пришлите код и запись с экрана прохождения теста

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Texts:
    LOGIN = "melartkon1"
    PASSWORD = "melartkon11"
    MESSAGE_TEXT = "Тестовое сообщение"


class Selectors:
    ADD_BUTTON = '[data-qa="sabyPage-addButton"]'
    INPUT_FORM_MSG = '[data-qa="textEditor_slate_Field"]'
    SEND_MSG = '[data-qa="msg-send-editor__send-button"]'
    DIALOG_ITEM = '.msg-dialogs-item'
    DELETE_MSG = '.controls-Menu__content[title="Удалить"]'
    BUTTON_DELETE_YES = '[data-qa="controls-ConfirmationDialog__button-true"]'
    BUTTON_DELETE_OK = '//*[normalize-space(text())="ОК"]'
    MESSAGE_CONTENT = '.msg-entity-layout__message-content'
    LOGIN_FIELD = '[data-qa="auth-AdaptiveLoginForm__login"] .controls-Field'
    PASSWORD_FIELD = '[data-qa="auth-AdaptiveLoginForm__password"] .controls-Field'


options = Options()
options.add_experimental_option(
    "prefs",
    {"profile.default_content_setting_values.notifications": 2}
)
driver = webdriver.Chrome(options=options)
driver.maximize_window()


def wait_for(selector, timeout=15):
    """
    Ждет, пока элемент появится на странице.

    :param selector: CSS-селектор элемента (например, ".my-class" или "#my-id").
    :param timeout: сколько секунд ждать (по умолчанию 15).
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def wait_clickable(selector, timeout=15):
    """
    Ждет, пока по элементу можно будет кликнуть.

    Просто ждать появления мало, элемент может быть скрыт или перекрыт
    другими элементами. Эта функция ждет, пока он станет полностью
    доступным для клика.

    :param selector: CSS-селектор элемента.
    :param timeout: сколько секунд ждать (по умолчанию 15).
    """
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )


def visible_messages(text):
    """
    Ищет на странице все видимые элементы, в которых есть нужный текст.

    :param text: текст, который мы ищем (или его часть).
    """
    elements = driver.find_elements(By.XPATH, f'//*[contains(text(), "{text}")]')
    return [
        el for el in elements
        if el.is_displayed() and el.tag_name not in ("script", "style", "noscript")
    ]


try:
    driver.get("https://fix-online.sbis.ru/page/people")
    # time.sleep(2)

    login_field = wait_for(Selectors.LOGIN_FIELD)
    login_field.send_keys(Texts.LOGIN)
    login_field.send_keys(Keys.ENTER)

    password_field = wait_for(Selectors.PASSWORD_FIELD)
    password_field.send_keys(Texts.PASSWORD)
    password_field.send_keys(Keys.ENTER)
    # time.sleep(3)

    # driver.get("https://fix-online.sbis.ru/page/people")
    # time.sleep(3)

    add_button = wait_clickable(Selectors.ADD_BUTTON)
    add_button.click()
    time.sleep(3)

    input_field = wait_clickable(Selectors.INPUT_FORM_MSG)
    input_field.click()
    input_field.send_keys(Texts.MESSAGE_TEXT)
    time.sleep(1)

    send_button = wait_clickable(Selectors.SEND_MSG)
    send_button.click()
    time.sleep(1)

    if not visible_messages(Texts.MESSAGE_TEXT):
        raise Exception(f"Сообщение '{Texts.MESSAGE_TEXT}' не найдено в чате")

    time.sleep(3)

    dialogs = driver.find_elements(By.CSS_SELECTOR, Selectors.DIALOG_ITEM)
    if not dialogs:
        raise Exception("Список диалогов пуст")

    message_elements = driver.find_elements(By.CSS_SELECTOR, Selectors.MESSAGE_CONTENT)
    if not message_elements:
        raise Exception("Сообщения в диалоге не найдены")

    last_message = message_elements[-1]
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", last_message
    )
    time.sleep(1)

    ActionChains(driver).context_click(last_message).perform()
    time.sleep(2)

    delete_item = wait_clickable(Selectors.DELETE_MSG)
    delete_item.click()
    time.sleep(2)

    confirm_button = wait_clickable(Selectors.BUTTON_DELETE_YES)
    confirm_button.click()
    time.sleep(3)

    try:
        ok_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, Selectors.BUTTON_DELETE_OK))
        )
        ok_button.click()
        time.sleep(2)
    except Exception:
        pass

    time.sleep(2)
    if visible_messages(Texts.MESSAGE_TEXT):
        raise Exception(f'Сообщение "{Texts.MESSAGE_TEXT}" всё ещё в чате')


finally:
    time.sleep(2)
    driver.quit()
