from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
import datetime
#import пружина

class Logon_Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        MainWindow.setStyleSheet("background-color: rgb(253, 234, 168);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, -5, 400, 51))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(125, 245, 150, 40))
        self.login_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.login_btn.setObjectName("login_btn")
        self.login = QtWidgets.QLineEdit(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(25, 145, 350, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.login.setFont(font)
        self.login.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.login.setObjectName("login")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(25, 195, 350, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.password.setObjectName("password")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 75, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Book")
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(135, 40, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 110, 150, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход в систему"))
        self.label.setText(_translate("MainWindow", "Вход в электронный дневник"))
        self.login_btn.setText(_translate("MainWindow", "Войти"))
        self.login.setPlaceholderText(_translate("MainWindow", "Введите логин"))
        self.password.setPlaceholderText(_translate("MainWindow", "Введите пароль"))
        self.label_2.setText(_translate("MainWindow", " Уже входили?"))
        self.label_3.setText(_translate("MainWindow", "Добро пожаловать!"))

class Logon_Logic(QMainWindow, Logon_Interface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.id = (1, )
        self.con = sqlite3.connect('DB_for_project.db')
        self.cur = self.con.cursor()
        self.comboBox.addItem('Выберите нужный логин и нажмите "Войти"')
        for i in self.cur.execute('SELECT login FROM mainTable').fetchall():
            self.comboBox.addItem(str(i[0]))
        self.login_btn.clicked.connect(self.check_add_logon)

    def check_add_logon(self):
        def addSubjectDB(s):
            soup = BeautifulSoup(s.get("https://edu.tatar.ru/user/diary/day", headers=header).text, features="lxml")
            urls = soup.find('div', {"class": "dsw"}).find_all('a')
            next_day = BeautifulSoup(s.get(urls[1].get("href"), headers=header).text, features="lxml")
            timeDB = []
            subject = []
            for i in next_day.find('tbody').find_all('td'):
                timeDB.append(i.text)
            d = "".join(timeDB).split("\n")
            for i in range(len(d)):
                if i % 6 == 0 and d[i] != "\r" and d[i] != "":
                    subject.append([d[i][11:], d[i + 2][32:]])
            for i in subject:
                print(i)

        def addTermDB():
            term = BeautifulSoup(s.get("https://edu.tatar.ru/user/diary/term", headers=header).text, features="lxml")
            termDB = []
            n = 1
            point = [0]
            for i in term.find('tbody').find_all('tr'):
                for j in i.text.split('\n'):
                    if "." in j:
                        point.append(i.text.split('\n').index(j) + 1)
            for i in term.find('tbody').find_all('tr'):
                if n != len(term.find('tbody').find_all('tr')):
                    termDB.append((i.text.split('\n'))[1:max(point)])
                n += 1
            for i in termDB:
                termDB[termDB.index(i)] = "__".join(i)
            self.cur.execute(f"UPDATE mainTable SET term = ? WHERE login = ?",
                             ('||'.join(termDB), datas['main_login2']))
            self.con.commit()

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/41.0.2272.101 Safari/537.36',
            'referer': 'https://edu.tatar.ru/logon'
        }
        link = 'https://edu.tatar.ru/logon'
        if self.comboBox.currentText() != 'Выберите нужный логин и нажмите "Войти"':
            datas = {
                'main_login2': self.comboBox.currentText(),
                'main_password2': self.cur.execute("SELECT password FROM mainTable WHERE login = ?",
                                              (self.comboBox.currentText(), )).fetchone()[0]
            }
        else:
            datas = {
                'main_login2': self.login.text(),
                'main_password2': self.password.text()
            }

        if requests.post(link, data=datas, headers=header).text == requests.get(link).text:
            QMessageBox.about(self, "Неправильные данные", "Неправильный логин или пароль")
        else:
            s = requests.Session()
            save_cookies = s.post(link, data=datas, headers=header)
            if self.cur.execute('SELECT id FROM mainTable WHERE login = ?',
                                (datas['main_login2'], )).fetchone() is None:
                self.cur.execute("INSERT INTO mainTable(login,password) VALUES(?,?)",
                            (datas['main_login2'],datas['main_password2']))
                self.con.commit()
            addSubjectDB(s)
            addTermDB()
            self.id = self.cur.execute("SELECT id FROM mainTable WHERE login = ?", (datas['main_login2'],)).fetchone()
            self.mainMenu()

    def mainMenu(self):
        global MainMenu_Logic, MainMenu_Logic_1
        MainMenu_Logic_1 = MainMenu_Logic()
        Logon_Logic_1.close()
        MainMenu_Logic_1.show()

class Grade_Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 600)
        MainWindow.setStyleSheet("background-color: rgb(253, 234, 168);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(30)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-38, 5, 101, 601))
        self.label_2.setStyleSheet("image: url(:/newPrefix/пружина.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(710, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.back_btn.setFont(font)
        self.back_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.back_btn.setObjectName("back_btn")
        self.lbl = QtWidgets.QLabel(self.centralwidget)
        self.lbl.setGeometry(QtCore.QRect(35, 45, 750, 545))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(17)
        font.setWeight(50)
        self.lbl.setFont(font)
        self.lbl.setLineWidth(1)
        self.lbl.setMidLineWidth(0)
        self.lbl.setObjectName("lbl")
        self.lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.lbl1.setGeometry(QtCore.QRect(740, 45, 60, 545))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(17)
        font.setWeight(50)
        self.lbl1.setFont(font)
        self.lbl1.setLineWidth(1)
        self.lbl1.setMidLineWidth(0)
        self.lbl1.setObjectName("lbl1")
        self.label_2.raise_()
        self.label.raise_()
        self.back_btn.raise_()
        self.lbl.raise_()
        self.lbl1.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Успеваемость"))
        self.label.setText(_translate("MainWindow", "Успеваемость:"))
        self.back_btn.setText(_translate("MainWindow", "Назад"))
        self.lbl.setText(_translate("MainWindow", ""))

class Grade_Logic(QMainWindow, Grade_Interface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cur = sqlite3.connect('DB_for_project.db').cursor()
        self.grade = self.cur.execute("SELECT term FROM mainTable WHERE id = ?", (Logon_Logic_1.id[0],)).fetchone()
        if self.grade == None:
            self.grade = ""
        else:
            self.grade = self.grade[0]
        self.subjects = []
        self.grades = []
        for i in self.grade.split("||"):
            self.subjects.append(" ".join(i.split('__')[:-1]))
            self.grades.append(" ".join(i.split('__')[-1]))
        self.lbl.setText("\n".join(self.subjects))
        self.lbl1.setText("\n".join(self.grades))
        self.back_btn.clicked.connect(self.back)

    def back(self):
        Grade_Logic_1.close()
        MainMenu_Logic_1.show()

class Homework_Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        MainWindow.setStyleSheet("background-color: rgb(253, 234, 168);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(30, 10, 270, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(25)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-38, 5, 101, 601))
        self.label_2.setStyleSheet("image: url(:/newPrefix/пружина.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(300, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.back_btn.setFont(font)
        self.back_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.back_btn.setObjectName("back_btn")
        self.label_2.raise_()
        self.label.raise_()
        self.back_btn.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Домашние задания"))
        self.label.setText(_translate("MainWindow", "Домашние задания"))
        self.back_btn.setText(_translate("MainWindow", "Назад"))

class Homework_Logic(QMainWindow, Homework_Interface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.back_btn.clicked.connect(self.back)

    def back(self):
        Homework_Logic_1.close()
        MainMenu_Logic_1.show()

class Planner_Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(253, 234, 168);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(30, 0, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-38, 5, 101, 601))
        self.label_2.setStyleSheet("image: url(:/newPrefix/пружина.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(270, 50, 170, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.timeEdit.setFont(font)
        self.timeEdit.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.timeEdit.setTime(QtCore.QTime(20, 00, 00))
        self.timeEdit.setObjectName("timeEdit")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(50, 50, 170, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dateEdit.setFont(font)
        self.dateEdit.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.dateEdit.setDate(QtCore.QDate(2022, 11, 10))
        self.dateEdit.setObjectName("dateEdit")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 140, 451, 371))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("background-color: rgb(255, 253, 208);")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(490, 10, 300, 580))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.plainTextEdit_2.setFont(font)
        self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 253, 208);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(55, 520, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(75, 100, 105, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(275, 100, 155, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.label_4.setObjectName("label_4")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(390, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.back_btn.setFont(font)
        self.back_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.back_btn.setObjectName("back_btn")
        self.label_2.raise_()
        self.label.raise_()
        self.timeEdit.raise_()
        self.dateEdit.raise_()
        self.plainTextEdit.raise_()
        self.plainTextEdit_2.raise_()
        self.pushButton.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.back_btn.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Планировщик"))
        self.label.setText(_translate("MainWindow", "Планировщик:"))
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow",
                                                         "Планы, сроки которых прошли, удаляются автоматически"))
        self.plainTextEdit_2.setPlainText(_translate("MainWindow", "Запланировано:"))
        self.pushButton.setText(_translate("MainWindow", "Запланировать"))
        self.label_3.setText(_translate("MainWindow", " ДД:ММ:ГГ"))
        self.label_4.setText(_translate("MainWindow", " ЧАСЫ:МИНУТЫ"))
        self.back_btn.setText(_translate("MainWindow", "Назад"))

class Planner_Logic(QMainWindow, Planner_Interface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('DB_for_project.db')
        self.cur = self.con.cursor()
        self.pln = self.cur.execute("SELECT memory FROM mainTable WHERE id = ?", (Logon_Logic_1.id[0],)).fetchone()
        if self.pln == None:
            self.pln = ""
        else:
            self.pln = self.pln[0]
        self.plan = [i for i in self.pln.split('\n')]
        timeNow = " ".join(str(datetime.datetime.now())[:16].split("-")).split(" ")
        self.plan.append(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||")
        self.plan.sort(key=lambda x: (x[6:10], x[3:5], x[0:2], x[11:16], x[17:]))
        self.plan = self.plan[self.plan.index(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||") + 1:]
        if self.plan == []:
            self.plainTextEdit_2.setPlainText("Запланировано:\n")
        else:
            self.plainTextEdit_2.setPlainText("Запланировано:\n" + "\n".join(self.plan[1:]))
        self.back_btn.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.toPlan)

    def toPlan(self):
        timeNow = " ".join(str(datetime.datetime.now())[:16].split("-")).split(" ")
        self.plan.append(self.dateEdit.text() + " " + self.timeEdit.text() + " " + self.plainTextEdit.toPlainText())
        self.plan.append(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||")
        self.plan.sort(key=lambda x: (x[6:10], x[3:5], x[0:2], x[11:16], x[17:]))
        self.plan = self.plan[self.plan.index(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||") + 1:]
        self.plainTextEdit_2.setPlainText("Запланировано:\n" + "\n".join(self.plan[1:]))
        self.cur.execute(f"UPDATE mainTable SET memory = ? WHERE id = ?", ("\n".join(self.plan), Logon_Logic_1.id[0]))
        self.con.commit()

    def back(self):
        global MainMenu_Logic, MainMenu_Logic_1
        MainMenu_Logic_1 = MainMenu_Logic()
        Planner_Logic_1.close()
        MainMenu_Logic_1.show()

class MainMenu_Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(400, 600)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(19)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(253, 234, 168);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(30, 10, 361, 110))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi Cond")
        font.setPointSize(40)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setObjectName("label")
        self.dz_btn = QtWidgets.QPushButton(self.centralwidget)
        self.dz_btn.setGeometry(QtCore.QRect(30, 130, 360, 85))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.dz_btn.setFont(font)
        self.dz_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.dz_btn.setObjectName("dz_btn")
        self.progress_btn = QtWidgets.QPushButton(self.centralwidget)
        self.progress_btn.setGeometry(QtCore.QRect(30, 230, 360, 85))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.progress_btn.setFont(font)
        self.progress_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.progress_btn.setObjectName("progress_btn")
        self.plan_btn = QtWidgets.QPushButton(self.centralwidget)
        self.plan_btn.setGeometry(QtCore.QRect(30, 330, 360, 85))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.plan_btn.setFont(font)
        self.plan_btn.setStyleSheet("background-color: rgb(205, 133, 63);")
        self.plan_btn.setObjectName("plan_btn")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-38, 5, 101, 601))
        self.label_2.setStyleSheet("image: url(:/newPrefix/пружина.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 430, 361, 161))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("background-color: rgb(255, 253, 208);")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_2.raise_()
        self.label.raise_()
        self.dz_btn.raise_()
        self.progress_btn.raise_()
        self.plan_btn.raise_()
        self.plainTextEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Школьный помощник"))
        self.label.setText(_translate("MainWindow", "Школьный\n"
"              помощник"))
        self.dz_btn.setText(_translate("MainWindow", "Домашние задания\n"
"на завтра"))
        self.progress_btn.setText(_translate("MainWindow", "Успеваемость"))
        self.plan_btn.setText(_translate("MainWindow", "Планировщик"))
        self.label_2.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/пружина.png\"/></p></body></html>"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Напоминалка:"))

class MainMenu_Logic(QMainWindow, MainMenu_Interface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('DB_for_project.db')
        self.cur = self.con.cursor()
        self.pln = self.cur.execute("SELECT memory FROM mainTable WHERE id = ?", (Logon_Logic_1.id[0],)).fetchone()
        if self.pln == None:
            self.pln = ""
        else:
            self.pln = self.pln[0]
        self.plan = [i for i in self.pln.split('\n')]
        timeNow = " ".join(str(datetime.datetime.now())[:16].split("-")).split(" ")
        self.plan.append(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||")
        self.plan.sort(key=lambda x: (x[6:10], x[3:5], x[0:2], x[11:16], x[17:]))
        self.plan = self.plan[self.plan.index(f"{timeNow[2]}.{timeNow[1]}.{timeNow[0]} {timeNow[3]} ||||") + 1:]
        self.plainTextEdit.setPlainText("Напоминалка:\n" + "\n".join(self.plan[1:]))
        self.dz_btn.clicked.connect(self.homework)
        self.progress_btn.clicked.connect(self.grade)
        self.plan_btn.clicked.connect(self.planner)

    def homework(self):
        global Homework_Logic, Homework_Logic_1
        Homework_Logic_1 = Homework_Logic()
        MainMenu_Logic_1.close()
        Homework_Logic_1.show()

    def grade(self):
        global Grade_Logic, Grade_Logic_1
        Grade_Logic_1 = Grade_Logic()
        MainMenu_Logic_1.close()
        Grade_Logic_1.show()


    def planner(self):
        global Planner_Logic, Planner_Logic_1
        Planner_Logic_1 = Planner_Logic()
        MainMenu_Logic_1.close()
        Planner_Logic_1.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Logon_Logic_1 = Logon_Logic()
    MainMenu_Logic_1 = MainMenu_Logic()
    Grade_Logic_1 = Grade_Logic()
    Homework_Logic_1 = Homework_Logic()
    Planner_Logic_1 = Planner_Logic()
    Logon_Logic_1.show()
    sys.exit(app.exec_())
