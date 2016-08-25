#!/usr/bin/env python
#coding=utf-8
import datetime
import sys
import atexit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

#tools for developer
def second_check_alert(message):
    reply = None
    try:
        second_check = QMessageBox()
        second_check.setIcon(QMessageBox.Question)
        second_check.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        second_check.setWindowTitle("Second Check Message Box")
        second_check.setText(message)
        reply = second_check.exec_()
    except Exception , ex:
        alert_box(str(ex))
    finally:
        return reply

def alert_box(message):
    try:
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("Alert Box by EasyNote")
        box.setText(message)
        reply = box.exec_()
    except Exception , ex:
        print str(ex)

################################################################################

class note:
    def __init__(self):
        self.title = ""
        self.content = ""

    def __init__(self , title , content):
        self.note_title = str(title)
        self.note_content = str(content)

class Custom_Frame(QFrame):
    def __init__(self , parent = None):
        super(Custom_Frame , self).__init__(parent)
        self.custom_setting()

    def custom_setting(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 102, 102))
        self.setPalette(p)

        self.setStyleSheet(
            "QLabel {color:rgb(255,255,255)}" +
            "QPushButton {background-color: rgb(128, 0, 0); color:rgb(255,255,255)}" +
            "QListWidget{ background-color: rgb(128, 0, 0); color : rgb(255,255,255)}" +
            "QLineEdit { background-color: rgb(128, 0, 0); color : rgb(255,255,255)}"  +
            "QPlainTextEdit {background-color : rgb(128, 0, 0); color : rgb(255,255,255)}"
        );

################################################################################

class Easy_Note (Custom_Frame):
    def __init__(self , parent = None):
        super(Easy_Note, self).__init__(parent)
        self.create_layout()
        self.create_connect()
        self.read_notes()
        self.init_setting()

    def init_setting(self):
        try:
            self.setFixedSize(600,450) #size wont change
            self.set_font()
            self.setWindowIcon(QIcon("note_image.png"))
        except Exception , ex:
            alert_box(ex.message)

    def create_layout(self):
        self.notelist = []

        #col0 - settings
        self.font_size_label = QLabel("Font Size : ")
        self.font_size = QSlider(Qt.Horizontal)
        self.font_size.setMinimum(12)
        self.font_size.setMaximum(24)
        self.font_size.setValue(16)
        self.show_font_size = QLabel()
        column0 = QHBoxLayout()
        column0.addWidget(self.font_size_label)
        column0.addWidget(self.font_size)
        column0.addWidget(self.show_font_size)
        column0.addStretch(0.3)

        self.font_style = QFontComboBox()
        column0.addWidget(self.font_style)

        #col1
        self.record = QListWidget()
        self.title = QLineEdit("Note Title")
        self.input = QPlainTextEdit("Note Content")
        column1 = QHBoxLayout()
        col1_row1 = QVBoxLayout()
        column1.addWidget(self.record)
        col1_row1.addWidget(self.title)
        col1_row1.addWidget(self.input)
        column1.addLayout(col1_row1)

        #col2
        self.load = QPushButton("Load")
        self.delete = QPushButton("Delete")
        self.clear = QPushButton("Clear Note")
        self.add = QPushButton("Add")
        column2 = QHBoxLayout()
        column2.addWidget(self.load)
        column2.addWidget(self.delete)
        column2.addWidget(self.clear)
        column2.addStretch(1)#add space
        column2.addWidget(self.add)

        #col3 , tool-bar part
        column3 = QHBoxLayout()
        self.edit_tool_label = QLabel("Some Tools for Note Content :)")
        column3.addWidget(self.edit_tool_label)
        self.adddate = QPushButton("Add Today's Date")
        column3.addWidget(self.adddate)
        self.addtime = QPushButton("Add Time (Now)")
        column3.addWidget(self.addtime)

        #last part
        lay = QVBoxLayout()
        lay.addLayout(column0)
        lay.addLayout(column1)
        lay.addLayout(column2)
        lay.addLayout(column3)

        self.setWindowTitle("Easy Note")
        self.setLayout(lay)
    #save / load files
    def write_file(self):
        try:
            file = open('note_file.txt' , 'w+')
            for note_ in self.notelist :
                file.write(note_.note_title)
                file.write('---DevisionForProgram---')
                file.write(note_.note_content)
                file.write('---DevisionForProgram---')
        except Exception , ex:
            alert_box(str(ex))

    def read_notes(self):
        try:
            file = open('note_file.txt' , 'r')
            content = file.read()
            tmp_list = content.split("---DevisionForProgram---")

            i = 0
            while (i+1) < len(tmp_list) :
                tmp_list[i] = tmp_list[i].decode('utf-8')
                self.notelist.append(note(tmp_list[i], tmp_list[i+1]))
                self.record.addItem(QString(tmp_list[i]))
                i += 2

        except Exception , ex:
            print str(ex)

#controlling notes##############################################################
    def add_note(self):
        self.notelist.append(note(self.title.text() , self.input.toPlainText()))
        self.record.addItem(QString(self.title.text()))

    def delete_note(self):
        reply = second_check_alert("Do you really want to delete note : " + self.notelist[self.record.currentRow()].note_title.decode('utf-8') + "?" )
        if reply == QMessageBox.Yes :
            self.notelist.pop(self.record.currentRow())
            self.record.takeItem(self.record.currentRow())

    def clear_note(self):
        self.title.setText('')
        self.input.setPlainText('')

    def load_note(self):
        #add ".decode('utf-8')"
        self.title.setText(self.notelist[self.record.currentRow()].note_title.decode('utf-8'))
        #add ".decode('utf-8')"
        self.input.setPlainText(self.notelist[self.record.currentRow()].note_content.decode('utf-8'))

#TOOLS##########################################################################
    def add_date(self):
        self.input.appendPlainText(QString(str(datetime.date.today())))

    def add_time(self):
        self.input.appendPlainText(QString(str(datetime.datetime.now())))

#settings#######################################################################
    def set_font(self):
        #print self.font_size.value()
        self.show_font_size.setText(str(self.font_size.value()))
        try:
            font = QFont(self.font_style.currentFont())
            font.setPixelSize(self.font_size.value())

            all_widgets = self.findChildren(QLabel)
            all_widgets += self.findChildren(QLineEdit)
            all_widgets += self.findChildren(QPlainTextEdit)
            all_widgets += self.findChildren(QListWidget)
            all_widgets += self.findChildren(QPushButton)

            for widget in all_widgets :
                widget.setFont(font)
        except Exception , ex:
            alert_box(ex.message)

#For developer##################################################################
    def create_connect(self):
        #settings
        self.font_style.currentFontChanged.connect(self.set_font)
        #notes
        self.add.clicked.connect(self.add_note)
        self.load.clicked.connect(self.load_note)
        self.clear.clicked.connect(self.clear_note)
        self.delete.clicked.connect(self.delete_note)
        #tool
        self.addtime.clicked.connect(self.add_time)
        self.adddate.clicked.connect(self.add_date)
        #font_size
        self.font_size.valueChanged.connect(self.set_font)

    def on_disable(self):
        self.write_file()

################################################################################

if __name__ == '__main__' :
    reload(sys)
    sys.setdefaultencoding('utf-8')

    app = QApplication(sys.argv)

    obj = Easy_Note()
    obj.show()

    app.exec_()

    obj.on_disable()
