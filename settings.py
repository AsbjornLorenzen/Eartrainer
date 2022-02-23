from ChordSelection import Ui_MainWindow as catsetup
from categories import *
from PySide6.QtWidgets import QMainWindow, QLabel,QWidget,QPushButton, QVBoxLayout,QHBoxLayout, QApplication, QGridLayout, QToolBar, QToolButton, QCheckBox, QComboBox
from customexercise import customexercisepopup

class settings(QMainWindow):
    #mode can be: chords, intervals, scales, solfa. As string
    def __init__(self,main,mode):
        super().__init__()
        self.main = main
        self.mode = mode
        self.newcategory = []
        self.setupcategories()
        self.ui = catsetup()
        self.setupui()
        self.editui()
        self.buildexitbutton() #exitbutton should be a part of the ui from the beginning. For now, it's built here
        self.ui.widget.hide()
        self.ui.toolButton.clicked.connect(self.handlepopup)
        self.main.setCentralWidget(self)

    def setupcategories(self):
        #Loads categories as intervalcategory objects, and adds them to the newcategory list
        if self.mode == 'chords':
            defaultcats = self.main.piano.defaultchords
        elif self.mode == 'intervals':
            defaultcats = self.main.piano.defaultintervals
        elif self.mode == 'scales':
            defaultcats = self.main.piano.defaultscales
        elif self.mode == 'solfa':
            defaultcats = self.main.piano.defaultsolfa
        for cat in defaultcats.keys():
            a,b = defaultcats[cat]
            catlist = []
            if self.mode == 'chords':
                for n in range(a,b):
                    catlist.append(self.main.piano.chordtypes[n])
                thiscat = chordcategory(cat,catlist) 
                #Note that the category object only contains the name of the interval, the specific notes have to be fetched from the piano's dict
            elif self.mode == 'intervals':
                for n in range(a,b):
                    catlist.append(self.main.piano.intervaltypes[n])
                thiscat = intervalcategory(cat,catlist)
            elif self.mode == 'scales':
                for n in range(a,b):
                    catlist.append(self.main.piano.scaletypes[n])
                thiscat = scalecategory(cat,catlist)
            elif self.mode == 'solfa':
                for n in range (a,b):
                    catlist.append(self.main.piano.solfatypes[n])
                thiscat = solfacategory(cat,catlist)
            self.newcategory.append(thiscat)

    def setupui(self):
        #Modifies the ui template for catsetup, in order to reuse the same template for intervals
        self.ui.setupUi(self)
        self.category = self.newcategory[0] #sets the first created category as default
        self.ui.pushButton.clicked.connect(self.openex)
        self.ui.comboBox.clear()
        for item in self.newcategory:
            self.ui.comboBox.addItem(str(item))
        self.ui.comboBox.currentIndexChanged.connect(self.categoryselector)

    def editui(self):
        #Edits the default ui to fit the current mode.
        if self.mode == 'intervals':
            self.ui.label.setText('Select interval type:')
            self.ui.checkBox.setText('Arpeggiate all intervals')
        elif self.mode == 'chords':
            pass #default ui is setup with chords
        elif self.mode == 'scales':
            self.ui.label.setText('Select scale type:')
            self.ui.checkBox.hide()
        elif self.mode == 'solfa':
            self.ui.label.setText('Select solfa type:')
            self.ui.checkBox.hide()
            self.ui.repbox = QComboBox()
            self.multiple = 1
            for n in range(5):
                self.ui.repbox.addItem(str(n+1))
            self.ui.repbox.currentIndexChanged.connect(self.multipleselector)
            self.ui.horizontalLayout_2.insertWidget(1,self.ui.repbox)

    def multipleselector(self,index):
        #Controlled by the comboBox self.ui.repbox
        self.multiple = index+1

    def buildexitbutton(self):
        self.exitbutton = QPushButton('Main Menu')
        self.exitbutton.clicked.connect(self.main.returntomenu)
        self.ui.verticalLayout.addWidget(self.exitbutton)

    def openex(self):
        #opens the exercise
        if self.mode == 'intervals':
            self.main.openintervalex(self.category)
        elif self.mode == 'chords':
            self.main.openchordex(self.category)
        elif self.mode == 'scales':
            self.main.openscaleex(self.category)
        elif self.mode == 'solfa':
            if self.multiple == 1:
                self.multiple = False
            self.main.opensolfaex(self.category,self.multiple)

    def categoryselector(self,index):
        self.category = self.newcategory[index]

    def handlepopup(self):
        self.popup = customexercisepopup(self,self.mode) #passes mode, and creates custom window
        self.popup.show()