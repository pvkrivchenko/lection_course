# Предварительные действия (Создайте эталонную задачу, заполнив обязательные поля)
# Авторизоваться на сайте https://fix-online.sbis.ru/
# Откройте эталонную задачу по прямой ссылке в новой вкладке браузера
# Убедитесь, что в заголовке вкладки отображается "Задача №НОМЕР от ДАТА", где ДАТА и НОМЕР - это ваши эталонные значения
# Проверьте, что поля: Исполнитель, дата, номер, описание и автор отображаются с эталонными значениями


from atf import *
from atf.ui import *
from pages_inside.libraries.EDWS3.Tasks.taskdialog import Dialog
from pages_inside.libraries.EDO3.Document.mainTabHeader import DateNumber, DocumentName
from pages_inside.login import LoginPage


class TestTask(TestCaseUI):
    url = 'https://fix-online.saby.ru/opendoc.html?guid=01a144be-b71e-74ce-89e9-fe77e0356f65&client=201629594'
    task_from_me = f'{Config().get("SITE")}/page/tasks-from-me/'
    date_task = '16 окт, пт'
    number_task = '2'
    description = 'Эталонная задача'
    executor = 'Мел Артем'
    responsible = 'Мел Артем'
    reglament = 'Задача'

    @classmethod
    def setUpClass(cls):
        cls.client = LoginPage(cls.driver).login_with_transit(cls.config.get('USER_NAME'), cls.config.get('PASSWORD'))
        cls.task_header = DateNumber(cls.driver)
        cls.document_name = DocumentName(cls.driver)
        cls.card_task = Dialog(cls.driver)

    def setUp(self):
        self.browser.open(self.task_from_me)

    def test_etalon_task(self):
        """Проверка открытия эталонной задачи по прямой ссылке"""

        init_browser = self.browser
        init_browser.switch_to_opened_window(init_browser.create_new_tab(self.url))
        self.document_name.check_regulation(self.reglament)

        with report.step(f'Проверяем отображение {self.reglament} №{self.number_task} от {self.date_task[:-4]}'):
            self.card_task.check_fields(exact=True, Исполнитель=self.executor,
                                        Описание=self.description, Ответственный=self.responsible,
                                        Дата=self.date_task, Номер=self.number_task)

    def tearDown(self):
        self.browser.close_windows_and_alert()
