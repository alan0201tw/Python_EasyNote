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
        print str(ex)
    finally:
        return reply

class note:
    def __init__(self):
        self.title = ""
        self.content = ""

    def __init__(self , title , content):
        self.note_title = str(title)
        self.note_content = str(content)

class Easy_Note (QWidget):
    def __init__(self , parent = None):
        super(Easy_Note, self).__init__(parent)
        self.create_layout()
        self.create_connect()
        self.resize(600,450)

    def create_layout(self):
        self.notelist = []

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
        self.add = QPushButton("Add")
        column2 = QHBoxLayout()
        column2.addWidget(self.load)
        column2.addWidget(self.delete)
        column2.addStretch(1)
        column2.addWidget(self.add)

        #tool-bar part
        column3 = QHBoxLayout()
        self.edit_tool_label = QLabel("Some Tools for Note Content :)")
        column3.addWidget(self.edit_tool_label)
        self.adddate = QPushButton("Add Today's Date")
        column3.addWidget(self.adddate)
        self.addtime = QPushButton("Add Time (Now)")
        column3.addWidget(self.addtime)

        #last part
        lay = QVBoxLayout()
        lay.addLayout(column1)
        lay.addLayout(column2)
        lay.addLayout(column3)

        self.setWindowTitle("Easy Note")
        self.setLayout(lay)

    def write_file(self):
        file = open('note_file.txt' , 'w+')
        for note_ in self.notelist :
            file.write(note_.note_title)
            file.write('---DevisionForProgram---')
            file.write(note_.note_content)
            file.write('---DevisionForProgram---')

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

    #controlling notes
    def add_note(self):
        self.notelist.append(note(self.title.text() , self.input.toPlainText()))
        self.record.addItem(QString(self.title.text()))

    def delete_note(self):
        reply = second_check_alert("Do you really want to delete note : " + self.notelist[self.record.currentRow()].note_title.decode('utf-8') + "?" )
        if reply == QMessageBox.Yes :
            self.notelist.pop(self.record.currentRow())
            self.record.takeItem(self.record.currentRow())

    def load_note(self):
        #add ".decode('utf-8')"
        self.title.setText(self.notelist[self.record.currentRow()].note_title.decode('utf-8'))
        #add ".decode('utf-8')"
        self.input.setPlainText(self.notelist[self.record.currentRow()].note_content.decode('utf-8'))

    #tools
    def add_date(self):
        self.input.appendPlainText(QString(str(datetime.date.today())))

    def add_time(self):
        self.input.appendPlainText(QString(str(datetime.datetime.now())))

    def create_connect(self):
        self.add.clicked.connect(self.add_note)
        self.load.clicked.connect(self.load_note)
        self.delete.clicked.connect(self.delete_note)

        self.addtime.clicked.connect(self.add_time)
        self.adddate.clicked.connect(self.add_date)


if __name__ == '__main__' :
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = QApplication(sys.argv)

    obj = Easy_Note()
    obj.show()

    obj.read_notes()
    app.exec_()

    obj.write_file()
