# Задание №1
# Авторизоваться на сайте https://fix-online.sbis.ru/
# Перейти в реестр Контакты
# Отправить сообщение самому себе
# Убедиться, что сообщение появилось в реестре
# Удалить это сообщение и убедиться, что удалили
# Для сдачи задания пришлите код и запись с экрана прохождения теста

from atf.ui import *
from atf import *
from pages_inside.login import LoginPage
from pages_inside.saby_pages.dialogs import Dialogs


class TestSendAndDeleteMsg(TestCaseUI):
    """Проверки таба Диалоги на вкладке Контакты"""

    @classmethod
    def setUpClass(cls):
        LoginPage(cls.driver).login_with_transit(cls.config.get('USER_NAME'), cls.config.get('PASSWORD'), 'Контакты')

        cls.dialog = Dialogs(cls.driver)

    def test01_delete_and_send_message(self):
        """Отправляем и проверяем пришедшее сообщение в диалогах.
        Удаляем пришедшее сообщение. Проверяем, что сообщение удалено."""

        self.dialog.select_tab('Диалоги')
        self.dialog.send_message(recipient='Мел Артем', message='Тестовое сообщение')
        self.dialog.delete_dialog('Тестовое сообщение')

        with report.step('Выставляем фильтр удаленные и проверяем что сообщение отображается в удаленных'):
            self.dialog.set_fast_filter(translate('Удаленные'))
            self.dialog.check_msg_in_dialogs('Тестовое сообщение')

    def tearDown(self):
        self.browser.close_windows_and_alert()
