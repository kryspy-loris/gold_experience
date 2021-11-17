import sys
import datetime
import sqlite3

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_window()

    def start_window(self):
        uic.loadUi('start_window.ui', self)
        self.move_seller_menu.clicked.connect(self.seller_menu)
        self.move_admin_menu.clicked.connect(self.pass_menu)
        # загрузка ui стартового окна
        self.pixmap = QPixmap('logo.jpg')
        # Загрузка логотипа в QPixmap
        self.logo.setPixmap(self.pixmap)

        db = sqlite3.connect('history.db')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS day_history(
                            item_type TEXT,
                            article TEXT,
                            cost TEXT,
                            calculation TEXT,
                            date_time TEXT
                        )""")
        # создание таблицы БД дневной истории

        cursor.execute("""CREATE TABLE IF NOT EXISTS history(
                                    item_type TEXT,
                                    article TEXT,
                                    cost TEXT,
                                    calculation TEXT,
                                    date_time TEXT
                                )""")
        # создание таблицы БД истории
        db.commit()
        db.close()

        db = sqlite3.connect('item.db')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS earrings(
                                    article TEXT,
                                    cost TEXT
                                )""")
        # создание таблицы БД с серьгами

        cursor.execute("""CREATE TABLE IF NOT EXISTS rings(
                                            article TEXT,
                                            cost TEXT
                                        )""")
        # создание таблицы БД с кольцами
        cursor.execute("""CREATE TABLE IF NOT EXISTS chains(
                                                    article TEXT,
                                                    cost TEXT
                                                )""")
        # создание таблицы БД с цепочками
        cursor.execute("""CREATE TABLE IF NOT EXISTS suspensions(
                                                    article TEXT,
                                                    cost TEXT
                                                )""")
        # создание таблицы БД с подвесками
        cursor.execute("""CREATE TABLE IF NOT EXISTS bracelet(
                                                    article TEXT,
                                                    cost TEXT
                        )""")
        # создание таблицы БД с браслетами
        db.commit()
        db.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            f = open('what_is_menu', mode='r', encoding='utf-8')
            s = list(map(str.strip, f.readlines()))
            if s[0] == "seller_menu":
                self.append_history()
            if s[0] == "itog_menu":
                self.zp_check()
            if s[0] == "pass_menu":
                self.pass_check()
            if s[0] == "add_menu":
                self.app_item_bd()
            if s[0] == "itog_menu":
                self.zp_check()
            f.close()


    def seller_menu(self):
        f = open('what_is_menu', mode='w', encoding='utf-8')
        print('seller_menu', file=f)
        f.close()
        uic.loadUi('seller_menu.ui', self)
        # загрузка меню продавца
        self.move_start_window.clicked.connect(self.start_window)
        # добавление действия кнопке(перемещение назад)
        self.itogo.clicked.connect(self.itog_menu)
        # добавление действия для перемещения в меню подсчета итога рабочего дня
        self.calculation.addItem('Наличный')
        self.calculation.addItem('Безналичный')
        self.calculation.addItem('Подарочный сертификат')
        # добавление выбора расчёта
        self.item_type.addItem('серьги')
        self.item_type.addItem('цепочка')
        self.item_type.addItem('кольцо')
        self.item_type.addItem('подвеска')
        self.item_type.addItem('браслет')

        self.append_item.clicked.connect(self.append_history)

    def append_history(self):
        #  этом меню также идёт проверка на наличие товара в БД
        try:
            if self.item_type.currentText() == 'кольцо':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM rings WHERE article = {self.articla_line_edit.text()}''').fetchall()
                result_c = cursor.execute(
                    f'''SELECT cost FROM rings WHERE article = {self.cost.text()}''').fetchall()
                self.dt_now = datetime.datetime.now()
                # узнаю дату и время сейчас
                db.commit()
                db.close()
                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    db = sqlite3.connect('history.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO day_history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                     self.articla_line_edit.text(),
                                                                                     self.cost.text(),
                                                                                     self.calculation.currentText(),
                                                                                     self.dt_now))
                    self.error.setText('')

                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    cursor.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                 self.articla_line_edit.text(),
                                                                                 self.cost.text(),
                                                                                 self.calculation.currentText(),
                                                                                 self.dt_now))
                    self.delete_item_db()
                    # запись данных в таблицу с общей историей
                    db.commit()
                    db.close()
                    # запись данных в таблицу с дневной историей
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
                else:
                    self.error.move(80, 430)
                    self.error.setText('такого товара не существует')
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
            if self.item_type.currentText() == 'серьги':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM earrings WHERE article = {self.articla_line_edit.text()}''').fetchall()
                result_c = cursor.execute(
                    f'''SELECT cost FROM earrings WHERE article = {self.cost.text()}''').fetchall()
                self.dt_now = datetime.datetime.now()
                # узнаю дату и время сейчас
                db.commit()
                db.close()
                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    db = sqlite3.connect('history.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO day_history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                     self.articla_line_edit.text(),
                                                                                     self.cost.text(),
                                                                                     self.calculation.currentText(),
                                                                                     self.dt_now))
                    self.error.setText('')

                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    cursor.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                 self.articla_line_edit.text(),
                                                                                 self.cost.text(),
                                                                                 self.calculation.currentText(),
                                                                                 self.dt_now))
                    self.delete_item_db()
                    # запись данных в таблицу с общей историей
                    db.commit()
                    db.close()
                    # запись данных в таблицу с дневной историей
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
                else:
                    self.error.move(80, 430)
                    self.error.setText('такого товара не существует')
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
            if self.item_type.currentText() == 'цепочка':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM chains WHERE article = {self.articla_line_edit.text()}''').fetchall()
                result_c = cursor.execute(
                    f'''SELECT cost FROM chains WHERE article = {self.cost.text()}''').fetchall()
                self.dt_now = datetime.datetime.now()
                # узнаю дату и время сейчас
                db.commit()
                db.close()
                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    db = sqlite3.connect('history.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO day_history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                     self.articla_line_edit.text(),
                                                                                     self.cost.text(),
                                                                                     self.calculation.currentText(),
                                                                                     self.dt_now))
                    self.error.setText('')

                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    cursor.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                 self.articla_line_edit.text(),
                                                                                 self.cost.text(),
                                                                                 self.calculation.currentText(),
                                                                                 self.dt_now))
                    self.delete_item_db()
                    # запись данных в таблицу с общей историей
                    db.commit()
                    db.close()
                    # запись данных в таблицу с дневной историей
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
                else:
                    self.error.move(80, 430)
                    self.error.setText('такого товара не существует')
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
            if self.item_type.currentText() == 'браслет':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM bracelet WHERE article = {self.articla_line_edit.text()}''').fetchall()
                result_c = cursor.execute(
                    f'''SELECT cost FROM bracelet WHERE article = {self.cost.text()}''').fetchall()
                self.dt_now = datetime.datetime.now()
                # узнаю дату и время сейчас
                db.commit()
                db.close()
                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    db = sqlite3.connect('history.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO day_history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                     self.articla_line_edit.text(),
                                                                                     self.cost.text(),
                                                                                     self.calculation.currentText(),
                                                                                     self.dt_now))
                    self.error.setText('')

                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    cursor.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                 self.articla_line_edit.text(),
                                                                                 self.cost.text(),
                                                                                 self.calculation.currentText(),
                                                                                 self.dt_now))
                    self.delete_item_db()
                    # запись данных в таблицу с общей историей
                    db.commit()
                    db.close()
                    # запись данных в таблицу с дневной историей
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
                else:
                    self.error.move(80, 430)
                    self.error.setText('такого товара не существует')
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
            if self.item_type.currentText() == 'подвеска':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM suspensions WHERE article = {self.articla_line_edit.text()}''').fetchall()
                result_c = cursor.execute(
                    f'''SELECT cost FROM suspensions WHERE article = {self.cost.text()}''').fetchall()
                self.dt_now = datetime.datetime.now()
                # узнаю дату и время сейчас
                db.commit()
                db.close()
                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    db = sqlite3.connect('history.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO day_history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                     self.articla_line_edit.text(),
                                                                                     self.cost.text(),
                                                                                     self.calculation.currentText(),
                                                                                     self.dt_now))
                    self.error.setText('')

                if self.articla_line_edit.text() != '' and self.cost.text() != '' and len(result) != 0 and len(
                        result_c) != 0:
                    cursor.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (self.item_type.currentText(),
                                                                                 self.articla_line_edit.text(),
                                                                                 self.cost.text(),
                                                                                 self.calculation.currentText(),
                                                                                 self.dt_now))
                    self.delete_item_db()
                    # запись данных в таблицу с общей историей
                    db.commit()
                    db.close()
                    # запись данных в таблицу с дневной историей
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
                else:
                    self.error.move(80, 430)
                    self.error.setText('такого товара не существует')
                    self.articla_line_edit.setText('')
                    self.cost.setText('')
        except sqlite3.OperationalError:
            self.error.move(180, 430)
            self.error.setText('введите число')

    def delete_item_db(self):
        if self.item_type.currentText() == 'кольцо':
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            cursor.execute(f'''
                            DELETE FROM rings
                            WHERE article = {self.articla_line_edit.text()}
                            ''').fetchone()
            db.commit()
            db.close()
            # запись данных в таблицу с кольцами
            self.articla_line_edit.setText('')
            # выставление значений по умолчанию

        if self.item_type.currentText() == 'серьги':
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            cursor.execute(f'''
                            DELETE FROM earrings
                            WHERE article = {self.articla_line_edit.text()}
                            ''').fetchone()
            db.commit()
            db.close()
            # запись данных в таблицу с кольцами
            self.articla_line_edit.setText('')
            # выставление значений по умолчанию
        if self.item_type.currentText() == 'подвеска':
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            cursor.execute(f'''
                                        DELETE FROM suspensions
                                        WHERE article = {self.articla_line_edit.text()}
                                        ''').fetchone()
            db.commit()
            db.close()
            # запись данных в таблицу с кольцами
            self.articla_line_edit.setText('')
            # выставление значений по умолчанию
        if self.item_type.currentText() == 'цепочка':
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            cursor.execute(f'''
                                        DELETE FROM chains
                                        WHERE article = {self.articla_line_edit.text()}
                                        ''').fetchone()
            db.commit()
            db.close()
            # запись данных в таблицу с кольцами
            self.articla_line_edit.setText('')
            # выставление значений по умолчанию
        if self.item_type.currentText() == 'браслет':
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            cursor.execute(f'''
                                        DELETE FROM bracelet
                                        WHERE article = {self.articla_line_edit.text()}
                                        ''').fetchone()
            db.commit()
            db.close()

    def itog_menu(self):
        f = open('what_is_menu', mode='w', encoding='utf-8')
        print('itog_menu', file=f)
        f.close()
        uic.loadUi('itog_menu.ui', self)
        # загрузка подсчета итога рабочего дня
        self.tableView.resize(515, 231)
        self.tableView.move(10, 60)
        self.move_seller_menu.clicked.connect(self.seller_menu)
        # добавление действия кнопке(перемещение назад)
        self.zp_seller.clicked.connect(self.zp_check)
        # добавление действий кнопке(перемещение назад)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('history.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('day_history')
        model.select()
        self.tableView.setModel(model)
        db.close()
        # отображаем дневную историю
        db = sqlite3.connect('history.db')
        cursor = db.cursor()
        bn_result = cursor.execute('''SELECT cost FROM day_history WHERE calculation = "Безналичный"''').fetchall()
        n_result = cursor.execute('''SELECT cost FROM day_history WHERE calculation = "Наличный"''').fetchall()
        ps_result = cursor.execute(
            '''SELECT cost FROM day_history WHERE calculation = "Подарочный сертификат"''').fetchall()
        # узнаём общую сумму, и сумму разных систем пасчёта
        bn_r = 0
        n_r = 0
        ps_r = 0
        for i in bn_result:
            for j in i:
                if j != '':
                    bn_r += int(j)
        for i in n_result:
            for j in i:
                if j != '':
                    n_r += int(j)
        for i in ps_result:
            for j in i:
                if j != '':
                    ps_r += int(j)
        all_r = bn_r + n_r + ps_r
        self.nal.setText(str(n_r))
        self.b_nal.setText(str(bn_r))
        self.ps.setText(str(ps_r))
        self.obsch_summ.setText(str(all_r))
        # расчитываем сумму всех операций

    def zp_check(self):
        db = sqlite3.connect('history.db')
        cursor = db.cursor()
        result = cursor.execute('''SELECT cost FROM day_history''').fetchall()
        day_sum = 0
        zarabot = 0
        for i in result:
            for j in i:
                day_sum += int(j)
        file = open('seller_stav.txt', mode='r', encoding='utf-8')
        file_1 = open('vihod', mode='r', encoding='utf-8')
        s = list(map(str.strip, file.readlines()))
        s_1 = list(map(str.strip, file_1.readlines()))
        zarabot = int(s_1[0]) + (day_sum * (int(s[0]) / 100))
        self.zar_plat.setText(f'Заработная плата составляет:{int(zarabot)} ₽')
        db.close()
        # отображение общих данных

    def pass_menu(self):
        f = open('what_is_menu', mode='w', encoding='utf-8')
        print('pass_menu', file=f)
        f.close()
        uic.loadUi('pass_menu.ui', self)
        # загрузка меню авторизации
        self.move_admin_pass.clicked.connect(self.start_window)
        # добавление действия кнопке(перемещение назад)
        self.login_btn.clicked.connect(self.pass_check)

    def pass_check(self):
        password = open('password.txt', mode='r', encoding='utf-8')
        password = list(map(str, password.readlines()))
        # получаем пароль
        if str(self.pass_input.text()) == str(password[0]):
            self.admin_menu()
            # если пароль верный, то впускаем в меню администратора
        elif str(self.pass_input.text()) == '':
            self.error.move(130, 340)
            self.error.setText('введите пароль')
            # если поле ввода пароля не заполнено, то выводится соответсвующая подсказка

        else:
            self.error.move(120, 340)
            self.error.setText('неверный пароль')
            # если пароль неверный, то выдаёём ошибку ввода

    def admin_menu(self):
        uic.loadUi('admin_menu.ui', self)
        # загрузка меню авторизации
        self.move_admin_pass.clicked.connect(self.start_window)
        # добавление действия кнопке(перемещение назад)
        self.additem_btn.clicked.connect(self.add_menu)
        # добавление действия кнопке(перемещение в меню вычета товара)
        self.removeitem_btn.clicked.connect(self.delete_menu)
        # добавление действия кнопке(перемещение в меню добавления товара)
        self.sell_hystory_btn.clicked.connect(self.sellhistory_menu)
        # добавление действия кнопке(перемещение в меню истории продаж)
        self.settings_btn.clicked.connect(self.settings_menu)
        # добавление действия кнопке(перемещение в меню истории продаж)
        self.item_list_btn.clicked.connect(self.nal_check_menu)
        # добавление действия кнопке(перемещение в меню проверки наличия)

    def add_menu(self):
        f = open('what_is_menu', mode='w', encoding='utf-8')
        print('add_menu', file=f)
        f.close()
        uic.loadUi('add_menu.ui', self)
        # загрузка меню добавления товара
        self.move_start_window.clicked.connect(self.admin_menu)
        # добавление действия кнопке(перемещение назад)
        self.append_item.clicked.connect(self.app_item_bd)
        self.item_combo_box.addItem('кольцо')
        self.item_combo_box.addItem("серьги")
        self.item_combo_box.addItem('подвеска')
        self.item_combo_box.addItem('цепочка')
        self.item_combo_box.addItem('браслет')

    def app_item_bd(self):
        try:
            self.error.setText('')
            if self.articla_line_edit.text() == '' or self.cost_line_edit.text() == '':
                self.error.resize(271, 41)
                self.error.move(125, 490)
                self.error.setText("заполните оба поля")
            if self.articla_line_edit.text() != '' and self.cost_line_edit.text() != '' \
                    and self.item_combo_box.currentText() == 'кольцо' and isinstance(int(self.articla_line_edit.text()),
                                                                                     int) and isinstance(
                int(self.cost_line_edit.text()), int):
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute('''SELECT article FROM rings''').fetchall()
                db.close()
                flag = True
                for i in result:
                    if self.articla_line_edit.text() in i:
                        flag = False
                if flag:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO rings VALUES(?, ?)", (self.articla_line_edit.text(),
                                                                      self.cost_line_edit.text()))
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.cost_line_edit.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.resize(371, 41)
                    self.error.move(70, 480)
                    self.error.setText('Такой товар уже существует')
            if self.articla_line_edit.text() != '' and self.cost_line_edit.text() != '' \
                    and self.item_combo_box.currentText() == 'серьги' and isinstance(int(self.articla_line_edit.text()),
                                                                                     int) and isinstance(
                int(self.cost_line_edit.text()), int):
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute('''SELECT article FROM earrings''').fetchall()
                db.close()
                flag = True
                for i in result:
                    if self.articla_line_edit.text() in i:
                        flag = False
                if flag:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO earrings VALUES(?, ?)", (self.articla_line_edit.text(),
                                                                         self.cost_line_edit.text()))
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.cost_line_edit.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.resize(371, 41)
                    self.error.move(70, 480)
                    self.error.setText('Такой товар уже существует')
            if self.articla_line_edit.text() != '' and self.cost_line_edit.text() != '' \
                    and self.item_combo_box.currentText() == 'подвеска' and isinstance(
                int(self.articla_line_edit.text()),
                int) and isinstance(
                int(self.cost_line_edit.text()), int):
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute('''SELECT article FROM suspensions''').fetchall()
                db.close()
                flag = True
                for i in result:
                    if self.articla_line_edit.text() in i:
                        flag = False
                if flag:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO suspensions VALUES(?, ?)", (self.articla_line_edit.text(),
                                                                            self.cost_line_edit.text()))
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.cost_line_edit.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.resize(371, 41)
                    self.error.move(70, 480)
                    self.error.setText('Такой товар уже существует')
            if self.articla_line_edit.text() != '' and self.cost_line_edit.text() != '' \
                    and self.item_combo_box.currentText() == 'цепочка' and isinstance(
                int(self.articla_line_edit.text()),
                int) and isinstance(
                int(self.cost_line_edit.text()), int):
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute('''SELECT article FROM chains''').fetchall()
                db.close()
                flag = True
                for i in result:
                    if self.articla_line_edit.text() in i:
                        flag = False
                if flag:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO chains VALUES(?, ?)", (self.articla_line_edit.text(),
                                                                       self.cost_line_edit.text()))
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.cost_line_edit.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.resize(371, 41)
                    self.error.move(70, 480)
                    self.error.setText('Такой товар уже существует')
            if self.articla_line_edit.text() != '' and self.cost_line_edit.text() != '' \
                    and self.item_combo_box.currentText() == 'браслет' and isinstance(
                int(self.articla_line_edit.text()),
                int) and isinstance(
                int(self.cost_line_edit.text()), int):
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute('''SELECT article FROM bracelet''').fetchall()
                db.close()
                flag = True
                for i in result:
                    if self.articla_line_edit.text() in i:
                        flag = False
                if flag:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO bracelet VALUES(?, ?)", (self.articla_line_edit.text(),
                                                                         self.cost_line_edit.text()))
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.cost_line_edit.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.resize(371, 41)
                    self.error.move(70, 480)
                    self.error.setText('Такой товар уже существует')
        except ValueError:
            self.error.move(150, 490)
            self.error.setText('введите число')

    def delete_menu(self):
        uic.loadUi('delete_menu.ui', self)
        # загрузка меню вычет товара
        self.move_start_window.clicked.connect(self.admin_menu)
        # добавление действия кнопке(перемещение назад)
        self.delete_item.clicked.connect(self.delete_item_bd)
        # добавление действия кнопке(удаление)
        self.item_combo_box.addItem('кольцо')
        self.item_combo_box.addItem("серьги")
        self.item_combo_box.addItem('подвеска')
        self.item_combo_box.addItem('цепочка')
        self.item_combo_box.addItem('браслет')

    def delete_item_bd(self):
        try:
            if self.item_combo_box.currentText() == 'кольцо' and self.articla_line_edit.text() != '':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM rings WHERE article = {self.articla_line_edit.text()}''').fetchall()
                db.commit()
                db.close()
                if len(result) != 0:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute(f'''
                                    DELETE FROM rings
                                    WHERE article = {self.articla_line_edit.text()}
                                    ''')
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.error.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.setText('Такого товара не существует')

            if self.item_combo_box.currentText() == 'серьги' and self.articla_line_edit.text() != '':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM earrings WHERE article = {self.articla_line_edit.text()}''').fetchall()
                db.commit()
                db.close()
                if len(result) != 0:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute(f'''
                                    DELETE FROM earrings
                                    WHERE article = {self.articla_line_edit.text()}
                                    ''')
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.error.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.setText('Такого товара не существует')
            if self.item_combo_box.currentText() == 'подвеска' and self.articla_line_edit.text() != '':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM suspensions WHERE article = {self.articla_line_edit.text()}''').fetchall()
                db.commit()
                db.close()
                if len(result) != 0:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute(f'''
                                    DELETE FROM suspensions
                                    WHERE article = {self.articla_line_edit.text()}
                                    ''')
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.error.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.setText('Такого товара не существует')
            if self.item_combo_box.currentText() == 'цепочка' and self.articla_line_edit.text() != '':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM chains WHERE article = {self.articla_line_edit.text()}''').fetchall()
                db.commit()
                db.close()
                if len(result) != 0:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute(f'''
                                    DELETE FROM chains
                                    WHERE article = {self.articla_line_edit.text()}
                                    ''')
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.error.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.setText('Такого товара не существует')
            if self.item_combo_box.currentText() == 'браслет' and self.articla_line_edit.text() != '':
                db = sqlite3.connect('item.db')
                cursor = db.cursor()
                result = cursor.execute(
                    f'''SELECT article FROM bracelet WHERE article = {self.articla_line_edit.text()}''').fetchall()
                db.commit()
                db.close()
                if len(result) != 0:
                    db = sqlite3.connect('item.db')
                    cursor = db.cursor()
                    cursor.execute(f'''
                                    DELETE FROM bracelet
                                    WHERE article = {self.articla_line_edit.text()}
                                    ''')
                    db.commit()
                    db.close()
                    # запись данных в таблицу с кольцами
                    self.articla_line_edit.setText('')
                    self.error.setText('')
                    # выставление значений по умолчанию
                else:
                    self.error.setText('Такого товара не существует')
        except sqlite3.OperationalError:
            self.error.setText('Введите число')

    def sellhistory_menu(self):
        uic.loadUi('sellhistory_menu.ui', self)
        # загрузка меню вычет товара
        self.tableView.resize(502, 321)
        self.tableView.move(17, 60)
        # изменение размера таблицы для отображения истории
        self.exit.clicked.connect(self.admin_menu)
        # добавление действия кнопке(перемещение назад)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('history.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('history')
        model.select()
        self.tableView.setModel(model)
        db.close()
        # отображаем дневную историю
        db = sqlite3.connect('history.db')
        cursor = db.cursor()
        result = cursor.execute('''SELECT cost FROM history''').fetchall()
        obsch_sum = 0
        for i in result:
            for j in i:
                obsch_sum += int(j)
        f = open('zakup', mode='r', encoding='utf-8')
        s = list(map(str.strip, f.readlines()))
        f.close()
        # открываем файл для чтения суммы закупа
        self.kol_tov.setText(str(len(result)))
        self.sum_tov.setText(str(obsch_sum))
        self.zakup.setText(s[0])
        db.close()
        # подсчитываем сумму продаж товара, кол-во проданного товара

    def settings_menu(self):
        uic.loadUi('settings_menu.ui', self)
        self.setWindowTitle('Client Program')
        # загрузка меню настроек
        self.exit.clicked.connect(self.admin_menu)
        # добавление действия кнопке(перемещение назад)
        self.change_pass.clicked.connect(self.change_password)
        self.clear_history.clicked.connect(self.clear_h)
        self.clear_day_history.clicked.connect(self.clear_h_day)
        # связь кнопок с функциями очистки
        self.sel_stav.clicked.connect(self.change_stav)
        self.change_zakup.clicked.connect(self.cng_zakup)
        self.sum_vihod.clicked.connect(self.cng_sum_vihod)

    def cng_sum_vihod(self):
        f = open('password.txt', 'r', encoding='utf-8')
        s = list(map(str.strip, f.readlines()))
        f.close()
        password, ok_pressed = QInputDialog.getText(self, "смена суммы за выход",
                                                    'для смены введите пароль')
        # вывод диалогового окна для смены пароля
        if ok_pressed and password == s[0]:
            new_vihod, ok_pressed = QInputDialog.getText(self, "Смена суммы за выход",
                                                         'введите сумму за выход')
            if ok_pressed:
                f = open('vihod', 'w')
                f.write(new_vihod)
                f.close()

    def cng_zakup(self):
        f = open('password.txt', 'r', encoding='utf-8')
        s = list(map(str.strip, f.readlines()))
        f.close()
        password, ok_pressed = QInputDialog.getText(self, "Смена суммы закупа",
                                                    'для смены введите пароль')
        # вывод диалогового окна для смены пароля
        if ok_pressed and password == s[0]:
            zakup, ok_pressed = QInputDialog.getText(self, "Смена суммы закупа",
                                                     'введите общую сумму товаров')
            if ok_pressed:
                f = open('zakup', 'w')
                f.write(zakup)
                f.close()

    def change_stav(self):
        f = open('password.txt', 'r', encoding='utf-8')
        s = list(map(str.strip, f.readlines()))
        f.close()
        password, ok_pressed = QInputDialog.getText(self, "Смена ставки",
                                                    'для смены ставки введите пароль')
        # вывод диалогового окна для смены пароля
        if ok_pressed and password == s[0]:
            stav, ok_pressed = QInputDialog.getText(self, "Смена ставки",
                                                    'введите новую ставку')
            if ok_pressed:
                f = open('seller_stav.txt', 'w')
                f.write(stav)
                f.close()

    def clear_h(self):
        file = open('password.txt', mode='r', encoding='utf-8')
        s = list(map(str.strip, file.readlines()))
        prove, ok_pressed = QInputDialog.getText(self, "очистка общей истории", "для очистки введите пароль")
        if ok_pressed and prove == s[0]:
            con = sqlite3.connect('history.db')
            cur = con.cursor()
            cur.execute('''
                            DELETE FROM history
                            ''')
            con.commit()
            con.close()
            # осичтка общей истории

    def clear_h_day(self):
        file = open('password.txt', mode='r', encoding='utf-8')
        s = list(map(str.strip, file.readlines()))
        prove, ok_pressed = QInputDialog.getText(self, "очистка дневной истории", "для очистки введите пароль")
        if ok_pressed and prove == s[0]:
            con = sqlite3.connect('history.db')
            cur = con.cursor()
            cur.execute('''
                                    DELETE FROM day_history
                                    ''')
            con.commit()
            con.close()
            # осичтка общей истории

    def change_password(self):
        f = open('password.txt', 'r', encoding='utf-8')
        s = list(map(str.strip, f.readlines()))
        f.close()
        password, ok_pressed = QInputDialog.getText(self, "Смена пароля",
                                                    'введите старый пароль')
        # вывод диалогового окна для смены пароля
        if ok_pressed and password == s[0]:
            new_password, ok_pressed = QInputDialog.getText(self, "Смена пароля",
                                                            'введите новый пароль')
            if ok_pressed:
                f = open('password.txt', 'w')
                f.write(new_password)
                f.close()

    # смена пароля при нажатии "ok"

    def nal_check_menu(self):
        uic.loadUi('nal_check_menu.ui', self)
        # загрузка меню проверки наличия
        self.tableView.resize(239, 291)
        self.exit.clicked.connect(self.admin_menu)
        # добавление действия кнопке(перемещение назад)
        self.item_combo_box.addItem('кольцо')
        self.item_combo_box.addItem("серьги")
        self.item_combo_box.addItem('подвеска')
        self.item_combo_box.addItem('цепочка')
        self.item_combo_box.addItem('браслет')

        self.nal_btn.clicked.connect(self.check)

    def check(self):
        if self.item_combo_box.currentText() == 'кольцо':
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('item.db')
            db.open()
            model = QSqlTableModel(self, db)
            model.setTable('rings')
            model.select()
            self.tableView.setModel(model)
            db.close()
            # отображение данных таблицы с кольцами
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            result = cursor.execute('''SELECT cost FROM rings''').fetchall()
            obsch_sum = 0
            for i in result:
                for j in i:
                    obsch_sum += int(j)
            self.kol_tov.setText(str(len(result)))
            self.sum_tov.setText(str(obsch_sum))
            db.close()
            # отображение общих данных

        if self.item_combo_box.currentText() == 'серьги':
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('item.db')
            db.open()
            model = QSqlTableModel(self, db)
            model.setTable('earrings')
            model.select()
            self.tableView.setModel(model)
            db.close()
            # отображение данных таблицы с серьгами
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            result = cursor.execute('''SELECT cost FROM earrings''').fetchall()
            obsch_sum = 0
            for i in result:
                for j in i:
                    obsch_sum += int(j)
            self.kol_tov.setText(str(len(result)))
            self.sum_tov.setText(str(obsch_sum))
            db.close()
            # отображение общих данных
        if self.item_combo_box.currentText() == 'подвеска':
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('item.db')
            db.open()
            model = QSqlTableModel(self, db)
            model.setTable('suspensions')
            model.select()
            self.tableView.setModel(model)
            db.close()
            # отображение данных таблицы с подвесками
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            result = cursor.execute('''SELECT cost FROM suspensions''').fetchall()
            obsch_sum = 0
            for i in result:
                for j in i:
                    obsch_sum += int(j)
            self.kol_tov.setText(str(len(result)))
            self.sum_tov.setText(str(obsch_sum))
            db.close()
            # отображение общих данных
        if self.item_combo_box.currentText() == 'цепочка':
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('item.db')
            db.open()
            model = QSqlTableModel(self, db)
            model.setTable('chains')
            model.select()
            self.tableView.setModel(model)
            db.close()
            # отображение данных таблицы с цепочками
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            result = cursor.execute('''SELECT cost FROM chains''').fetchall()
            obsch_sum = 0
            for i in result:
                for j in i:
                    obsch_sum += int(j)
            self.kol_tov.setText(str(len(result)))
            self.sum_tov.setText(str(obsch_sum))
            db.close()
            # отображение общих данных
        if self.item_combo_box.currentText() == 'браслет':
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('item.db')
            db.open()
            model = QSqlTableModel(self, db)
            model.setTable('bracelet')
            model.select()
            self.tableView.setModel(model)
            db.close()
            # отображение данных таблицы с браслетами
            db = sqlite3.connect('item.db')
            cursor = db.cursor()
            result = cursor.execute('''SELECT cost FROM bracelet''').fetchall()
            obsch_sum = 0
            for i in result:
                for j in i:
                    obsch_sum += int(j)
            self.kol_tov.setText(str(len(result)))
            self.sum_tov.setText(str(obsch_sum))
            db.close()
            # отображение общих данных


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
