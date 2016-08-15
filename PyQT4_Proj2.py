#!/usr/bin/env python

import datetime
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class note():
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
        self.adddate = QPushButton("Add Date")
        column3.addWidget(self.adddate)
        self.addtime = QPushButton("Add Time")
        column3.addWidget(self.addtime)

        #last part
        lay = QVBoxLayout()
        lay.addLayout(column1)
        lay.addLayout(column2)
        lay.addLayout(column3)

        self.setWindowTitle("Easy Note")
        self.setLayout(lay)

    #controlling notes
    def add_note(self):
        self.notelist.append(note(self.title.text() , self.input.toPlainText()))
        self.record.addItem(QString(self.title.text()))

    def delete_note(self):
        self.notelist.pop(self.record.currentRow())
        self.record.takeItem(self.record.currentRow())

    def load_note(self):
        self.input.setPlainText(self.notelist[self.record.currentRow()].note_content)

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
    app = QApplication(sys.argv)

    obj = Easy_Note()
    obj.show()

    app.exec_()