# Авторизоваться на сайте https://fix-online.saby.ru
# 1. Переместить запись в другую папку и проверить перемещение (убедиться в: наличии в папке и увеличении счётчика). И вернуть обратно.
# 2. Проверить, что дата сообщения в реестре Диалоги совпадает с датой в Чатах
# 3. Пометить сообщение эталонным тегом. Убедиться, что тег появился на сообщении, а счётчик тегов увеличился. Снять тег и проверить.

from atf import *
from pages_inside.login import LoginPage
from pages_inside.saby_pages.people import People
from pages_inside.saby_pages.dialogs import Dialogs
from controls import *
import helpers.dates


class TestContact(TestCaseUI):
    move_dialog = ControlsMoveDialog()
    msg = Config().get('MSG')
    my_folder = Config().get('MY_FOLDER')
    my_tag = Config().get('MY_TAG')
    all_messages = Config().get('ALL_MESSAGES')

    @classmethod
    def setUpClass(cls):
        cls.client = LoginPage(cls.driver).login_with_transit(cls.config.get('USER_NAME'), cls.config.get('PASSWORD'))
        cls.dialogs = Dialogs(cls.driver)
        cls.move_dialog = ControlsMoveDialog(cls.driver)
        cls.people = People(cls.driver)

    def setUp(self):
        self.dialogs.open()

    def test_move_msg_another_folder(self):
        """Перемещение записи в другую папку"""

        with (report.step('Проверить перемещение записи из корня в другую папку')):
            self.dialogs.send_message(recipient='Мел Артем', message=self.msg)
            self.dialogs.select_option_on_msg(self.msg, 'right_click', 'Перенести в папку')
            self.move_dialog.select(with_text=self.my_folder)
            self.dialogs.check_folder_counter(self.my_folder, 1)
            self.dialogs.open_folder(self.my_folder)
            self.dialogs.check_msg_in_dialogs(self.msg)

        with report.step('Проверить перемещение записи из другой папки в корень'):
            self.dialogs.select_option_on_msg(self.msg, 'right_click', 'Перенести в папку')
            self.move_dialog.move_root()
            self.dialogs.check_folder_counter(self.my_folder, 0)
            self.dialogs.open_folder(self.all_messages)
            self.dialogs.check_msg_in_dialogs(self.msg)

    def test_match_date_msg_on_tabs(self):
        """Проверка совпадения даты сообщения на вкладке Диалоги и Чаты"""

        with report.step('Проверить соответствие дат у сообщения на вкладке Диалоги и Чаты'):
            dialog_date = self.dialogs.get_date_msg(self.msg)
            format_date = f"{dialog_date.day} {helpers.dates.months_short[dialog_date.month - 1]}"
            self.people.open()
            info_message = self.people.check_message_exist(self.msg).text
            assert_that(format_date, equal_to(info_message.split('\n')[2][:-6]), desc='Дата НЕ соответствует эталону')

    def test_add_and_delete_tag_msg(self):
        """Проверка добавления и удаления тега на записи"""

        with (report.step('Проверить добавление тега на сообщение')):
            self.dialogs.open_create_tag_panel(self.msg)
            self.dialogs.tag_select_panel.select_tag(self.my_tag)
            self.dialogs.check_exist_tag_by_msg(self.msg, self.my_tag)
            self.dialogs.check_tag_count(self.my_tag, 1)

        with report.step('Проверить удаление тега с сообщения'):
            self.dialogs.open_create_tag_panel(self.msg)
            self.dialogs.tag_select_panel.unselect_tag(self.my_tag)
            self.dialogs.check_tag_count(self.my_tag, 0)
            self.dialogs.check_exist_tag_by_msg(self.msg, self.my_tag, tag_exist=False)

    def tearDown(self):
        self.browser.close_windows_and_alert()
