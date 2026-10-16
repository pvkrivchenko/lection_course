# Задание №2
# Авторизоваться на сайте https://fix-online.sbis.ru/
# Перейти в реестр Задачи на вкладку "В работе"
# Убедиться, что выделена папка "Входящие" и стоит маркер.
# Убедиться, что папка не пустая (в реестре есть задачи)
# Перейти в другую папку, убедиться, что теперь она выделена, а со "Входящие" выделение снято
# Создать новую папку и перейти в неё
# Убедиться, что она пустая
# Удалить новую папку, проверить, что её нет в списке папок


from atf.ui import *
from atf import *
from pages_inside.login import LoginPage
from pages_inside.saby_pages.tasks_in_work import TasksInWork
from pages_inside.libraries.EDWS3.Utils.userFolder import ConstructionDialog
from pages_eo.libraries.EORegistry.remove import Dialog


class TestTasks(TestCaseUI):
    """Проверка перехода в реестр Задачи. Создание, удаление папок"""

    new_folder = 'Новая папка'
    other_folder = 'Другая папка'
    main_folder = 'Входящие'

    @classmethod
    def setUpClass(cls):
        LoginPage(cls.driver).login_with_transit(cls.config.get('USER_NAME'), cls.config.get('PASSWORD'), 'Задачи')

        cls.task_in_work = TasksInWork(cls.driver)
        cls.popup_set_folder = ConstructionDialog(cls.driver)

    def test_tasks(self):
        """Проверка работы реестра Задачи на вкладке 'В работе'"""

        with report.step('Перейти в Задачи на мне'):
            self.task_in_work.open('Задачи', 'В работе')
            self.task_in_work.check_folder_marker(self.main_folder)
            self.task_in_work.check_docs_count(3)
            self.task_in_work.folder_click(self.other_folder)
            self.task_in_work.check_folder_marker(self.other_folder)
            self.task_in_work.check_folder_marker(self.main_folder, displayed=False)

        with report.step('Создать новую папку'):
            self.task_in_work.add_folder()
            self.popup_set_folder.set_name(self.new_folder)
            self.popup_set_folder.save()
            self.task_in_work.open_folder(self.new_folder)
            self.task_in_work.check_docs_count(0)

        with report.step('Удалить созданную папку'):
            self.task_in_work.folder_hover_operation(self.new_folder, 'Удалить папку')
            self.task_in_work.popup_confirmation.confirm()
            self.task_in_work.check_folder_exists(self.new_folder, exist=False)

    def tearDown(self):
        self.browser.close_windows_and_alert()
