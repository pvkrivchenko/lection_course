import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN = "melartkon1"
PASSWORD = "melartkon11"
MESSAGE_TEXT = "Тестовое сообщение"

ADD_BUTTON = '[data-qa="sabyPage-addButton"]'
INPUT_FORM_MSG = '[data-qa="textEditor_slate_Field"]'
SEND_MSG = '[data-qa="msg-send-editor__send-button"]'
DIALOG_ITEM = '.msg-dialogs-item'
DELETE_MSG = '.controls-Menu__content[title="Удалить"]'
BUTTON_DELETE_YES = '[data-qa="controls-ConfirmationDialog__button-true"]'
BUTTON_DELETE_OK = '//*[normalize-space(text())="ОК"]'

options = Options()
options.add_experimental_option(
    "prefs",
    {"profile.default_content_setting_values.notifications": 2}
)
driver = webdriver.Chrome(options=options)
driver.maximize_window()


def wait_for(selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def wait_clickable(selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )


def visible_messages(text):
    elements = driver.find_elements(By.XPATH, f'//*[contains(text(), "{text}")]')
    return [
        el for el in elements
        if el.is_displayed() and el.tag_name not in ("script", "style", "noscript")
    ]


def dispatch_contextmenu(element):
    driver.execute_script("""
        const el = arguments[0];
        const rect = el.getBoundingClientRect();
        el.dispatchEvent(new MouseEvent('contextmenu', {
            bubbles: true, cancelable: true, view: window,
            button: 2, buttons: 2,
            clientX: rect.left + rect.width / 2,
            clientY: rect.top + rect.height / 2
        }));
    """, element)


try:
    driver.get("https://fix-online.sbis.ru/")
    time.sleep(2)

    login_field = wait_for('[data-qa="auth-AdaptiveLoginForm__login"] .controls-Field')
    login_field.send_keys(LOGIN)
    login_field.send_keys(Keys.ENTER)

    password_field = wait_for('[data-qa="auth-AdaptiveLoginForm__password"] .controls-Field')
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.ENTER)
    time.sleep(3)

    driver.get("https://fix-online.sbis.ru/page/people")
    time.sleep(3)

    add_button = wait_clickable(ADD_BUTTON, timeout=20)
    add_button.click()
    time.sleep(3)
    print("Создаём новый чат")

    input_field = wait_clickable(INPUT_FORM_MSG, timeout=20)
    input_field.click()
    input_field.send_keys(MESSAGE_TEXT)
    time.sleep(1)
    print(f'Сообщение: "{MESSAGE_TEXT}" - написано')

    send_button = wait_clickable(SEND_MSG)
    send_button.click()
    time.sleep(4)
    print(f'Сообщение: "{MESSAGE_TEXT}" - отправлено')

    if not visible_messages(MESSAGE_TEXT):
        raise Exception(f"Сообщение '{MESSAGE_TEXT}' не найдено в чате")
    print(f'Сообщение: "{MESSAGE_TEXT}" - отображается в чате')

    driver.get("https://fix-online.sbis.ru/page/people")
    time.sleep(3)

    dialogs = driver.find_elements(By.CSS_SELECTOR, DIALOG_ITEM)
    if not dialogs:
        raise Exception("Список диалогов пуст")

    dialogs[-1].click()
    time.sleep(3)
    wait_clickable(INPUT_FORM_MSG, timeout=20)
    print("Провалились в последний диалог")

    # Переиспользуем локатор на содержимое сообщения
    MESSAGE_CONTENT = '.msg-entity-layout__message-content'
    message_elements = driver.find_elements(By.CSS_SELECTOR, MESSAGE_CONTENT)
    if not message_elements:
        raise Exception("Сообщения в диалоге не найдены")

    last_message = message_elements[-1]
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", last_message
    )
    time.sleep(1)

    # Клик правой кнопкой по последнему сообщению
    ActionChains(driver).context_click(last_message).perform()
    time.sleep(2)

    # Клик на "Удалить"
    delete_item = wait_clickable(DELETE_MSG)
    delete_item.click()
    time.sleep(2)

    # Подтверждаем удаление
    confirm_button = wait_clickable(BUTTON_DELETE_YES)
    confirm_button.click()
    time.sleep(3)

    # Нажимаем "ОК" в финальном диалоге
    try:
        ok_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, BUTTON_DELETE_OK))
        )
        ok_button.click()
        time.sleep(2)
    except Exception:
        pass

    print(f'Сообщение: "{MESSAGE_TEXT}" - удалено')

    time.sleep(2)
    if visible_messages(MESSAGE_TEXT):
        raise Exception(f'Сообщение "{MESSAGE_TEXT}" всё ещё в чате')
    print(f'Сообщение: "{MESSAGE_TEXT}" - больше не отображается')

    print("ТЕСТ УСПЕШНО ПРОЙДЕН")

finally:
    time.sleep(2)
    driver.quit()