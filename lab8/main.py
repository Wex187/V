import sys
import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox, QInputDialog, QAbstractItemView )


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_week_tab()
        self._create_teacher_tab()
        self._create_subject_tab()
        self._create_schedule_tab()


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="shedule3",
                                         user="postgres",
                                         password="12365477Suka",
                                         host="localhost",
                                         port="5432")
        self.cursor = self.conn.cursor()


    def _create_week_tab(self):
        self.week_tab = QWidget()
        self.tabs.addTab(self.week_tab, "Week")

        self.week_gbox = QGroupBox("Week")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.week_gbox)

        self._create_week_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.week_tab.setLayout(self.svbox)


    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")

        self.teacher_gbox = QGroupBox("Teachers")

        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()

        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)

        self.thbox1.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.add_shedule_button = QPushButton('Add')
        self.update_shedule_button2 = QPushButton("Update")
        self.thbox2.addWidget(self.update_shedule_button2)
        self.thbox2.addWidget(self.add_shedule_button)
        self.add_shedule_button.clicked.connect(self._add_shedule)
        self.update_shedule_button2.clicked.connect(self._update_shedule2)

        self.teacher_tab.setLayout(self.tvbox)


    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.subject_gbox = QGroupBox("Subjects")

        self.wvbox = QVBoxLayout()
        self.whbox1 = QHBoxLayout()
        self.whbox2 = QHBoxLayout()

        self.wvbox.addLayout(self.whbox1)
        self.wvbox.addLayout(self.whbox2)

        self.whbox1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.add_shedule_button2 = QPushButton("Add")
        self.update_shedule_button3 = QPushButton("Update")
        self.whbox2.addWidget(self.update_shedule_button3)
        self.whbox2.addWidget(self.add_shedule_button2)
        self.update_shedule_button3.clicked.connect(self._update_shedule3)
        self.add_shedule_button2.clicked.connect(self._add_shedule2)

        self.subject_tab.setLayout(self.wvbox)


    def _create_schedule_tab(self):
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Full schedule")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")

        self.fvbox = QVBoxLayout()
        self.fhbox1 = QHBoxLayout()
        self.fhbox2 = QHBoxLayout()
        self.fhbox3 = QHBoxLayout()

        self.fvbox.addLayout(self.fhbox1)
        self.fvbox.addLayout(self.fhbox2)
        self.fvbox.addLayout(self.fhbox3)

        self.fhbox1.addWidget(self.monday_gbox)
        self.fhbox2.addWidget(self.tuesday_gbox)
        self.fhbox3.addWidget(self.wednesday_gbox)
        self.fhbox1.addWidget(self.thursday_gbox)
        self.fhbox2.addWidget(self.friday_gbox)
        self.fhbox3.addWidget(self.saturday_gbox)

        self._create_schedule_table()
        self.schedule_tab.setLayout(self.fvbox)

    def _create_week_table(self):
        self.week_table = QTableWidget()
        self.week_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.week_table.setColumnCount(6)
        self.week_table.setHorizontalHeaderLabels(["Day", "Time", "Subject", "Auditorium", "", ""])

        self._update_week_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.week_table)
        self.week_gbox.setLayout(self.mvbox)

        self.week_table.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["Id", "Teacher", "Subject", "", ""])

        self._update_teacher_table()

        self.mvbox1 = QVBoxLayout()
        self.mvbox1.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox1)

        self.teacher_table.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["Id", "Subject", "", ""])

        self._update_subject_table()

        self.mvbox2 = QVBoxLayout()
        self.mvbox2.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox2)

        self.subject_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def _create_schedule_table(self):
        #Понедельник
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["Time", "Subject","Teacher", "Auditorium"])

        self._update_schedule_table()

        self.mvbox3 = QVBoxLayout()
        self.mvbox3.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox3)

        #Вторник
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(4)
        self.tuesday_table.setHorizontalHeaderLabels(["Time", "Subject", "Teacher", "Auditorium"])

        self._update_schedule_table2()

        self.mvbox4 = QVBoxLayout()
        self.mvbox4.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox4)

        #Среда
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(4)
        self.wednesday_table.setHorizontalHeaderLabels(["Time", "Subject","Teacher", "Auditorium"])

        self._update_schedule_table3()

        self.mvbox5 = QVBoxLayout()
        self.mvbox5.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox5)

        # Четверг
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(4)
        self.thursday_table.setHorizontalHeaderLabels(["Time", "Subject", "Teacher", "Auditorium"])

        self._update_schedule_table4()

        self.mvbox6 = QVBoxLayout()
        self.mvbox6.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox6)

        # Пятница
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(4)
        self.friday_table.setHorizontalHeaderLabels(["Time", "Subject", "Teacher", "Auditorium"])

        self._update_schedule_table5()

        self.mvbox8 = QVBoxLayout()
        self.mvbox8.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox8)

        # Суббота
        self.saturday_table = QTableWidget()
        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.saturday_table.setColumnCount(4)
        self.saturday_table.setHorizontalHeaderLabels(["Time", "Subject", "Teacher", "Auditorium"])

        self._update_schedule_table6()

        self.mvbox9 = QVBoxLayout()
        self.mvbox9.addWidget(self.saturday_table)
        self.saturday_gbox.setLayout(self.mvbox9)

        self.monday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tuesday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.wednesday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.thursday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.friday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.saturday_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def _update_week_table(self):
        self.cursor.execute("SELECT * FROM week ORDER BY id")
        records = list(self.cursor.fetchall())

        self.week_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton = QPushButton("change")
            stroke_deleteButton = QPushButton("delete")

            self.week_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.week_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.week_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.week_table.setItem(i, 3, QTableWidgetItem(str(r[4])))
            self.week_table.setCellWidget(i, 4, stroke_updateButton)
            self.week_table.setCellWidget(i, 5, stroke_deleteButton)

            d='Monday'
            stroke_updateButton.clicked.connect(lambda ch, num=i: self._change_day_from_week(num, d))
            stroke_deleteButton.clicked.connect(lambda ch, num=i: self._delete_day_from_week(num, d))
            stroke_deleteButton.clicked.connect(self._update_shedule)

        self.week_table.resizeRowsToContents()


    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records))
        'print(enumerate(records))'
        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton2 = QPushButton("change")
            stroke_deleteButton2 = QPushButton("delete")

            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, stroke_updateButton2)
            self.teacher_table.setCellWidget(i, 4, stroke_deleteButton2)

            d='teacher'
            stroke_updateButton2.clicked.connect(lambda ch, num=i: self._change_day_from_teacher(num, d))
            stroke_deleteButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_teacher(num, d))
            stroke_deleteButton2.clicked.connect(self._update_shedule2)

        self.teacher_table.resizeRowsToContents()


    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY id")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            stroke_deleteButton3 = QPushButton("delete")
            stroke_changeButton3 = QPushButton("change")

            self.subject_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, stroke_changeButton3)
            self.subject_table.setCellWidget(i, 3, stroke_deleteButton3)

            d='subject'
            stroke_deleteButton3.clicked.connect(lambda ch, num=i: self._delete_day_from_subject(num, d))
            stroke_changeButton3.clicked.connect(lambda ch, num=i: self._change_day_from_subject(num, d))
            stroke_deleteButton3.clicked.connect(self._update_shedule3)

        self.subject_table.resizeRowsToContents()

    def _update_schedule_table(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Понедельник\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.monday_table.resizeRowsToContents()

    def _update_schedule_table2(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Вторник\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.tuesday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.tuesday_table.resizeRowsToContents()

    def _update_schedule_table3(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Среда\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.wednesday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.wednesday_table.resizeRowsToContents()

    def _update_schedule_table4(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Четверг\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.thursday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.thursday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.thursday_table.resizeRowsToContents()

    def _update_schedule_table5(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Пятница\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.friday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.friday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.friday_table.resizeRowsToContents()

    def _update_schedule_table6(self):
        self.cursor.execute('SELECT week.day, week.time, week.subject, '
                            'teacher.name, week.room FROM week JOIN teacher ON week.subject = teacher.subject WHERE week.day = \'Суббота\' ORDER BY week.id;')
        records = list(self.cursor.fetchall())

        self.saturday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.saturday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.saturday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.saturday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.saturday_table.setItem(i, 3, QTableWidgetItem(str(r[4])))

        self.saturday_table.resizeRowsToContents()


    def _delete_day_from_week(self, rowNum, day):
        row = list()
        for i in range(self.week_table.columnCount()):
            try:
                row.append(self.week_table.item(rowNum, i).text())
                print(row)
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE week SET room = \'\', subject = \'\' WHERE day = \'{row[0]}\' AND time = \'{row[1]}\'')
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
        #self._update_shedule()


    def _delete_day_from_teacher(self, rowNum, day):
        row = list()
        row2 = list()
        for i in range(30):
            try:
                row2.append(self.week_table.item(i, 2).text())
            except:
                row2.append(None)
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        if row[2] in row2:
            QMessageBox.about(self, "!", "Нельзя удалить этого учителя")
            self._update_shedule2()
        else:
            self.cursor.execute(f'DELETE FROM teacher WHERE id = \'{row[0]}\'')
            self.conn.commit()
            self._update_shedule2()


    def _delete_day_from_subject(self, rowNum, day):
        row = list()
        row3 = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row3.append(self.teacher_table.item(i, 2).text())
            except:
                row3.append(None)
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        if row[1] in row3:
            QMessageBox.about(self, "!", "Данный предмет нельзя удалить")
            self._update_shedule3()
        else:
            self.cursor.execute(f'DELETE FROM subject WHERE id = \'{row[0]}\'')
            self.conn.commit()
            self._update_shedule3()


    def _change_day_from_week(self, rowNum, day):
        row = list()
        row2 = list()
        for i in range(40):
            try:
                row2.append(self.teacher_table.item(i, 2).text())
            except:
                row2.append(None)
        for i in range(self.week_table.columnCount()):
            try:
                row.append(self.week_table.item(rowNum, i).text())
            except:
                row.append(None)
        new_name, ok_pressed = QInputDialog.getText(self, "!",
                                                        "Введите новый предмет:")
        if not new_name in row2:
            QMessageBox.about(self, "!", "Либо данный предмет не существует, либо на него не назначен учитель")
        else:
            new_aud, ok_pressed = QInputDialog.getText(self, "!", "Введите аудиторию:")
            self.cursor.execute(
                f'UPDATE week SET room = \'{new_aud}\', subject = \'{new_name}\' WHERE day = \'{row[0]}\' AND time = \'{row[1]}\'')
            self.conn.commit()
            self._update_shedule()


    def _change_day_from_teacher(self, rowNum, day):
        r = list()
        row = list()
        row2 = list()
        row3 = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                r.append(self.teacher_table.item(rowNum, i).text())
            except:
                r.append(None)
        for i in range(30):
            try:
                row3.append(self.subject_table.item(i, 1).text())
                print(row3)
            except:
                row3.append(None)
        for i in range(30):
            try:
                row2.append(self.week_table.item(i, 2).text())
                print(row2)
            except:
                row2.append(None)
        for i in range(40):
            try:
                row.append(self.teacher_table.item(i, 2).text())
                print(row)
            except:
                row.append(None)
        print(r[2],row2)
        if r[2] in row2:
            new_name, ok_pressed = QInputDialog.getText(self, "!", "Данный предмет изменить нельзя\nвы можете изменить лишь имя учителя:")
            self.cursor.execute(
                f'UPDATE teacher SET name = \'{new_name}\' WHERE id = \'{r[0]}\'')
            self.conn.commit()
            self._update_shedule2()
        else:
            new_name, ok_pressed = QInputDialog.getText(self, "!", "Введите новое имя учителя:")
            new_subject, ok_pressed = QInputDialog.getText(self, "!", "Введите предмет этого учителя:")
            while True:
                if not new_subject in row3:
                    new_subject, ok_pressed = QInputDialog.getText(self, "!",
                                                                "Данного предмета нет в списке\nпопробуйте еще раз:")
                elif new_subject in row:
                    if new_subject == r[2]:
                        self.cursor.execute(
                            f'UPDATE teacher SET name = \'{new_name}\', subject = \'{new_subject}\' WHERE id = \'{r[0]}\'')
                        self.conn.commit()
                        self._update_shedule2()
                        break
                    else:
                        new_subject, ok_pressed = QInputDialog.getText(self, "!",
                                                                    "Данный предмет уже занят другим учителем\nпопробуйте еще раз:")
                else:
                    self.cursor.execute(
                        f'UPDATE teacher SET name = \'{new_name}\', subject = \'{new_subject}\' WHERE id = \'{r[0]}\'')
                    self.conn.commit()
                    self._update_shedule2()
                    break

    def _change_day_from_subject(self, rowNum, day):
        row = list()
        row2 = list()
        row3 = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row3.append(self.teacher_table.item(i, 2).text())
            except:
                row3.append(None)
        for i in range(self.subject_table.columnCount()):
            try:
                row2.append(self.subject_table.item(rowNum, i).text())
            except:
                row2.append(None)
        for i in range(40):
            try:
                row.append(self.subject_table.item(i, 1).text())
            except:
                row.append(None)
        if row2[1] in row3:
            QMessageBox.about(self, "!", "Данный предмет нельзя изменить")
            self._update_shedule3()
        else:
            new_subject, ok_pressed = QInputDialog.getText(self, "!", "Измените данный предмет:")
            while True:
                if new_subject in row:
                    new_subject, ok_pressed = QInputDialog.getText(self, "!",
                                                            "Такой предмет уже существует\nпопробуйте еще раз")
                else:
                    self.cursor.execute(f'UPDATE subject SET name = \'{new_subject}\' WHERE id = {row2[0]};')
                    self.conn.commit()
                    self._update_shedule3()
                    break

    def _update_shedule(self):
        self._update_week_table()
        self._update_schedule_table()
        self._update_schedule_table2()
        self._update_schedule_table3()
        self._update_schedule_table4()
        self._update_schedule_table5()
        self._update_schedule_table6()

    def _update_shedule2(self):
        self._update_teacher_table()
        self._update_schedule_table()
        self._update_schedule_table2()
        self._update_schedule_table3()
        self._update_schedule_table4()
        self._update_schedule_table5()
        self._update_schedule_table6()

    def _update_shedule3(self):
        self._update_subject_table()
        self._update_schedule_table()
        self._update_schedule_table2()
        self._update_schedule_table3()
        self._update_schedule_table4()
        self._update_schedule_table5()
        self._update_schedule_table6()


    def _add_shedule(self):
        row = list()
        row2 = list()
        for i in range(40):
            try:
                row2.append(self.subject_table.item(i, 1).text())
            except:
                row2.append(None)
                break
        for i in range(40):
            try:
                row.append(self.teacher_table.item(i, 2).text())
            except:
                row.append(None)
                break
        if len(row2) == len(row):
            QMessageBox.about(self, "!", "Нет доступных предметов")
        else:
            new_name, ok_pressed = QInputDialog.getText(self, "!", "Введите новое имя учителя:")
            new_subject, ok_pressed = QInputDialog.getText(self, "!", "Введите предмет этого учителя:")
            while True:
                if not new_subject in row2:
                    new_subject, ok_pressed = QInputDialog.getText(self, "!",
                                                                    "Данного предмета нет в списке\nпопробуйте еще раз:")
                elif new_subject in row:
                    new_subject, ok_pressed = QInputDialog.getText(self, "!", "Данный предмет уже занят другим учителем\nпопробуйте еще раз:")
                else:
                    self.cursor.execute(f'INSERT INTO teacher (name, subject) VALUES (\'{new_name}\', \'{new_subject}\');')
                    self.conn.commit()
                    self._update_shedule2()
                    break


    def _add_shedule2(self):
        row = list()
        for i in range(40):
            try:
                row.append(self.subject_table.item(i, 1).text())
            except:
                row.append(None)
        new_name, ok_pressed = QInputDialog.getText(self, "Привет", "Введите новое имя предмета:")
        while True:
            if new_name in row:
                new_name, ok_pressed = QInputDialog.getText(self, "!", "Данный предмет уже существутет\nпопробуйте еще раз")
            else:
                self.cursor.execute(f'INSERT INTO subject (name) VALUES (\'{new_name}\');')
                self.conn.commit()
                self._update_shedule3()
                break


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())