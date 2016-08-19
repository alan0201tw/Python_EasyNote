#!/usr/bin/env python

import datetime
import sys
import atexit
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

    def write_file(self):
        file = open('note_file.txt' , 'w+')
        for note_ in self.notelist :
            file.write("Note Title : " + note_.note_title)
            file.write('\n\n')
            file.write("Note Content : " + note_.note_content)
            file.write('\n\n')

    def read_notes(self):
        try:
            file = open('note_file.txt' , 'r')
            content = file.read()
            tmp_list = content.split("\n\n")
            #print tmp_list
            #print len(tmp_list)
            i = 0
            while (i+1) < len(tmp_list) :
                self.notelist.append(note(tmp_list[i].replace("Note Title : " , "") , tmp_list[i+1].replace("Note Content : " , "")))
                self.record.addItem(QString(tmp_list[i].replace("Note Title : " , "")))
                i += 2
            #print "lalalalala"
            #print self.notelist[0].note_title
            #print self.notelist[0].note_content
        except Exception , ex:
            print str(ex)

    #controlling notes
    def add_note(self):
        self.notelist.append(note(self.title.text() , self.input.toPlainText()))
        self.record.addItem(QString(self.title.text()))

    def delete_note(self):
        self.notelist.pop(self.record.currentRow())
        self.record.takeItem(self.record.currentRow())

    def load_note(self):
        self.title.setText(self.notelist[self.record.currentRow()].note_title)
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

    obj.read_notes()
    app.exec_()

    obj.write_file()
