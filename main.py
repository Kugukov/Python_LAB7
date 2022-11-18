#!/usr/bin/env python3
# coding=utf-8
import random
import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QButtonGroup
from PyQt5.QtCore import QTimer, QRect

answers = ['', '', '']  # 1 - form2, 2 - form3, 3 - form4


class Form1(QtWidgets.QMainWindow):
    # аргумент str говорит о том, что сигнал должен быть сторокового типа
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form1, self).__init__()
        uic.loadUi('uis/form1.ui', self)

        self.setWindowTitle('Приветствие')

        self.x = 50  # 477
        self.y = 13
        self.label_welcome_1.move(self.x, self.y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_label_left)
        self.timer.start(10)  # 100

        self.btn_exit.clicked.connect(self.close)
        self.btn_begin.clicked.connect(self.next)

    def move_label_left(self):
        if self.x <= -150:  # 477
            self.x = self.width()  # 477
            self.x -= 1
            self.label_welcome_1.move(self.x, self.height() - 30)
        else:
            self.x -= 1
            self.label_welcome_1.move(self.x, self.y)
        self.label_welcome_1.adjustSize()

    def next(self):
        self.switch_window.emit('1>2')


class Form2(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    # Смена картинок

    def __init__(self):
        super(Form2, self).__init__()
        uic.loadUi('uis/form2.ui', self)

        self.setWindowTitle('Детство')

        self.label_img.setPixmap(QPixmap('images/1.1.jpg'))

        self.label_img.setScaledContents(True)

        if answers[0] is not None:
            self.label_selected.setText('Выбрано: ' + answers[0])

        self.button_group = QButtonGroup()

        self.button_group.addButton(self.checkBox_1, 1)
        self.button_group.addButton(self.checkBox_2, 2)
        self.button_group.addButton(self.checkBox_3, 3)
        self.button_group.addButton(self.checkBox_4, 4)

        self.checkBox_1.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_1, 'images/1.1.jpg'))
        self.checkBox_2.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_2, 'images/1.2.jpg'))
        self.checkBox_3.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_3, 'images/1.3.jpg'))
        self.checkBox_4.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_4, 'images/1.4.jpg'))

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def onToggled(self, checkbox, image):
        if checkbox.isChecked():
            answers[0] = checkbox.text()
            self.label_selected.setText('Выбрано: ' + answers[0])
            self.label_img.setPixmap(QPixmap(image))

    def back(self):
        self.switch_window.emit('1<2')

    def next(self):
        self.switch_window.emit('2>3')


class Form3(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    # Анимация появления

    def __init__(self):
        super(Form3, self).__init__()
        uic.loadUi('uis/form3.ui', self)

        self.setWindowTitle('Отрочество')
        self.label_img.setPixmap(QPixmap('images/2.jpg'))
        self.label_img.setScaledContents(True)

        if answers[1] is not None:
            self.label_selected.setText('Выбрано: ' + answers[1])

        self.comboBox.activated.connect(self.handleActivated)
        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)
        self.start_animation()

    def handleActivated(self, index):
        answers[1] = self.comboBox.itemText(index)
        self.label_selected.setText('Выбрано: ' + answers[1])

    def start_animation(self):
        opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.label_img)
        self.label_img.setGraphicsEffect(opacity_effect)

        opacity_animation = QtCore.QPropertyAnimation(
            opacity_effect,
            b"opacity",
            duration=1000,
            startValue=0.0,
            endValue=1.0
        )

        group = QtCore.QParallelAnimationGroup(self.label_img)
        group.addAnimation(opacity_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def back(self):
        self.switch_window.emit('2<3')

    def next(self):
        self.switch_window.emit('3>4')


class Form4(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    # Постоянная анимация

    def __init__(self):
        super(Form4, self).__init__()
        uic.loadUi('uis/form4.ui', self)

        self.setWindowTitle('Юность')

        self.label_img.setPixmap(QPixmap('images/3.jpg'))
        self.label_img.setScaledContents(True)

        if answers[2] is not None:
            self.label_selected.setText('Выбрано: ' + answers[2])

        self.radioButton_1.toggled.connect(
            lambda: self.onToggled(self.radioButton_1))
        self.radioButton_2.toggled.connect(
            lambda: self.onToggled(self.radioButton_2))
        self.radioButton_3.toggled.connect(
            lambda: self.onToggled(self.radioButton_3))
        self.radioButton_4.toggled.connect(
            lambda: self.onToggled(self.radioButton_4))

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

        self.width = 100
        self.height = 100
        self.flag = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(100)

    def onToggled(self, radiobutton):
        if radiobutton.isChecked():
            answers[2] = radiobutton.text()
            self.label_selected.setText('Выбрано: ' + answers[2])

    def animation(self):
        if self.width < 200 and self.height < 200 and not self.flag:
            self.width += 2
            self.height += 2
            self.label_img.setGeometry(QRect(self.label_img.x(), self.label_img.y(), self.width, self.height))
        else:
            self.flag = True
            self.width -= 2
            self.height -= 2
            self.label_img.setGeometry(QRect(self.label_img.x(), self.label_img.y(), self.width, self.height))
            if self.width == 100 and self.height == 100:
                self.flag = False

    def back(self):
        self.switch_window.emit('3<4')

    def next(self):
        self.switch_window.emit('4>5')


class Form5(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    # Смена цветов анимированная

    def __init__(self):
        super(Form5, self).__init__()
        uic.loadUi('uis/form5.ui', self)

        self.setWindowTitle('Результат')

        # запрещаем редактирование таблицы
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # присваиваем значение ячейкам таблицы
        self.tableWidget.setItem(0, 0,
                                 QTableWidgetItem('Выберите любимую кашу'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(answers[0]))

        self.tableWidget.setItem(1, 0,
                                 QTableWidgetItem('Как вы учились в 5 классе'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(answers[1]))

        self.tableWidget.setItem(2, 0,
                                 QTableWidgetItem('Какое у вас образование'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(answers[2]))

        self.btn_back.clicked.connect(self.back)
        self.btn_exit.clicked.connect(self.close)

        self.list_of_colors = ["#000000", "#FF0000", "#008000", "#00FFFF", "#000080", "#008080", "#808000"]
        # Black, Red, Green, Aqua, Navy, Teal, Olive

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(1000)

    def animation(self):
        color_index = random.randint(0, 4)
        self.tableWidget.setStyleSheet("""
                    QTableWidget{
                        color: """ + self.list_of_colors[color_index] + """;
                    } """)
        self.tableWidget.horizontalHeaderItem(0).setForeground(QColor(self.list_of_colors[color_index]))
        self.tableWidget.horizontalHeaderItem(1).setForeground(QColor(self.list_of_colors[color_index]))
        self.label.setStyleSheet("""
                    QLabel{
                        color: """ + self.list_of_colors[color_index] + """;
                    } """)
        self.btn_back.setStyleSheet("""
                    QPushButton{
                        color: """ + self.list_of_colors[color_index] + """;
                    } """)
        self.btn_exit.setStyleSheet("""
                    QPushButton{
                        color: """ + self.list_of_colors[color_index] + """;
                    } """)

    def back(self):
        self.switch_window.emit("4<5")


class Controller:
    def __init__(self):
        pass

    def select_forms(self, text):
        if text == '1':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()

        if text == '1>2':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form1.close()

        if text == '2>3':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form2.close()

        if text == '3>4':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form3.close()

        if text == '4>5':
            self.form5 = Form5()
            self.form5.switch_window.connect(self.select_forms)
            self.form5.show()
            self.form4.close()

        if text == '4<5':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form5.close()

        if text == '3<4':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form4.close()

        if text == '2<3':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form3.close()

        if text == '1<2':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
            self.form2.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.select_forms("1")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
