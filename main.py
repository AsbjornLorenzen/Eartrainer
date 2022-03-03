from categories import *
from customexercise import customexercisepopup
from playnotes import piano
from trainingmodes import trainer
from exercise import exercise
from settings import settings
from MainMenu import Ui_mainmenu
from ChordSelection import Ui_MainWindow as catsetup

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QLabel,QWidget,QPushButton, QVBoxLayout,QHBoxLayout, QApplication, QGridLayout, QToolBar, QToolButton, QCheckBox, QComboBox
from PySide6.QtGui import QIcon, QAction, QPixmap

from functools import partial
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.piano = piano()
        self.centwidg = QWidget()
        self.setupmenu()

    def setupmenu(self):
        self.ui = Ui_mainmenu()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.openchordsettings)
        self.ui.pushButton.clicked.connect(self.openintervalsettings)
        self.ui.pushButton_3.clicked.connect(self.openscalesettings)
        self.ui.pushButton_4.clicked.connect(self.opensolfasettings)
        self.resize(300,300)

    def opensolfasettings(self):
        self.sols = settings(self,'solfa')

    def opensolfaex(self,category,multiple):
        self.solex = exercise(self,'solfa',category,multiple)

    def openscalesettings(self):
        self.ss = settings(self,'scales')

    def openscaleex(self,category):
        self.ex = exercise(self,'scales',category)

    def openchordsettings(self):
        self.cs = settings(self,'chords')

    def openchordex(self,category,arpeggiate=False):
        self.ex = exercise(self,'chords',category,arpeggiate=arpeggiate)
    
    def openintervalsettings(self):
        self.intervalsettings = settings(self,'intervals')

    def openintervalex(self,category,arpeggiate=False):
        self.ex = exercise(self,'intervals',category,arpeggiate=arpeggiate)
    
    def returntomenu(self):
        self.setupmenu()
        self.setCentralWidget(self.ui.verticalLayoutWidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

