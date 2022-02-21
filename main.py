from playnotes import piano
from trainingmodes import chordtrainer,intervaltrainer, trainer
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QLabel,QWidget,QPushButton, QVBoxLayout,QHBoxLayout, QApplication, QGridLayout, QToolBar, QToolButton, QCheckBox, QComboBox
from PySide6.QtGui import QIcon, QAction, QPixmap
from functools import partial
from MainMenu import Ui_mainmenu
from ChordSelection import Ui_MainWindow as catsetup
import threading

import random
import time
import sys

#STATUS:
#TODO: Tilføj en back to previous funktion - hvis man har gættet forkert, kan man altid gå tilbage og høre den forrige igen.

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
        self.sols = specificsettings(self,'solfa')

    def opensolfaex(self,category,multiple):
        self.solex = exercise(self,'solfa',category,multiple)

    def openscalesettings(self):
        self.ss = specificsettings(self,'scales')

    def openscaleex(self,category):
        self.ex = exercise(self,'scales',category)

    def openchordsettings(self):
        self.cs = specificsettings(self,'chords')

    def openchordex(self,category):
        self.ex = exercise(self,'chords',category)
    
    def openintervalsettings(self):
        self.intervalsettings = specificsettings(self,'intervals')

    def openintervalex(self,category):
        self.ex = exercise(self,'intervals',category)
    
    def returntomenu(self):
        self.setupmenu()
        self.setCentralWidget(self.ui.verticalLayoutWidget)

class specificsettings(QMainWindow):
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
                print(a,b)
                for n in range(a,b):
                    catlist.append(self.main.piano.chordtypes[n])
                thiscat = chordcategory(cat,catlist) #Note that the category object only contains the name of the interval, the specific notes have to be fetched from the piano's dict
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

class customexercisepopup(QWidget):
    def __init__(self,settings,type):
        #settings is the central widget of the main window, the parent that opens this popup
        #type is 'chords','intervals', and so on
        super().__init__()
        self.type = type
        self.selected = [] #Selected is a list of every individual chord/interval etc to be used. 
        self.parent = settings #settings is the parent of the popup. 
        self.mainLO = QHBoxLayout()
        self.desc = QLabel()
        self.desc.setText('Choose {type} for custom exercise'.format(type=self.type))
        self.mainLO.addWidget(self.desc)
        self.boxesLO = QGridLayout()
        self.buildgrid(7)
        self.mainLO.addLayout(self.boxesLO)
        self.submitbutton = QPushButton('Create Exercise')
        self.submitbutton.clicked.connect(self.submit)
        self.mainLO.addWidget(self.submitbutton)
        self.setLayout(self.mainLO)

    def submit(self):
        name = 'Custom category' #TODO: Create custom name input
        if self.type == 'chords':
            customcat = chordcategory(name,self.selected)
        if self.type == 'intervals':
            customcat = intervalcategory(name,self.selected)
        elif self.type == 'scales':
            customcat = scalecategory(name,self.selected)
        elif self.type == 'solfa':
            customcat = solfacategory(name,self.selected)
        self.parent.newcategory.append(customcat)
        self.parent.ui.comboBox.addItem(str(self.parent.newcategory[-1])) #Adds new cat to combobox
        combocount = self.parent.ui.comboBox.count()
        self.parent.ui.comboBox.setCurrentIndex(combocount-1) #Sets index to latest added item 
        print('Current count:',str(self.parent.ui.comboBox.count()))
        self.selected = [] #reset selected
        self.hide()

    def buildgrid(self,width):
        #TODO: This func can easily be generalized.
        currentcolumn = 0
        currentrow = 0
        self.checkboxes = []
        #pianotype is all possible subjects in a category, fx major, minor, aug, dim and so on
        if self.type == 'chords':
            pianotype = self.parent.main.piano.allchords
        if self.type == 'intervals':
            pianotype = self.parent.main.piano.allintervals 
        if self.type == 'scales':
            pianotype = self.parent.main.piano.allscales
        if self.type == 'solfa':
            pianotype = self.parent.main.piano.allsolfa
        for subject in pianotype:
            if pianotype[subject] == 'break': #break is used to group/organize subjects in subcategories
                currentrow += 1
                currentcolumn = 0
                continue
            addsubject = QCheckBox(subject)
            self.checkboxes.append(addsubject)
            self.boxesLO.addWidget(self.checkboxes[-1],currentcolumn,currentrow)
            self.checkboxes[-1].stateChanged.connect(lambda *state,subject=subject: self.togglebutton(subject))
            if currentcolumn == width-1:
                currentrow += 1
                currentcolumn = 0
            else:
                currentcolumn += 1


                    
    def togglebutton(self,topic):
        #topic is every specific chord or interval etc
        if topic not in self.selected:
            self.selected.append(topic)
        else:
            self.selected.remove(topic)

    def demo(self):
        demo = ['foo','bar','baz']
        self.checkboxes = []
        for type in demo:
            thisbox = QCheckBox(type)
            thisbox.stateChanged.connect(self.changed)
            self.checkboxes.append(thisbox)
            self.boxesLO.addWidget(thisbox)
        self.mainLO.addLayout(self.boxesLO)

class exercise(): #Instead if intervalguesser and chordguesser
    def __init__(self,main,mode,category,multiple=False):
        super().__init__()
        self.mode = mode
        self.category = category
        self.trainer = trainer(self.mode,self.category,multiple) #NOTE: These are only read when exercise is initialized.
        self.main = main
        self.main.resize(600,600)
        #TODO: REMOVE THIS
        multiple = True
        if multiple:
            self.guesslist = []
        self.buildwindow()


    def buildwindow(self):
        self.central = QWidget()
        self.mainlo = QVBoxLayout()
        self.buildsucceededfailed()
        self.statusholder = QHBoxLayout()
        self.statusholder.setAlignment(Qt.AlignCenter)
        self.statusicon = QLabel()
        #self.statusicon.setPixmap(QPixmap('images/tick.png'))
        self.statusicon.setAlignment(Qt.AlignRight)
        self.status = QLabel()
        self.status.setText('Guessing {type} {mode}'.format(type=self.category,mode=self.mode))
        self.status.setAlignment(Qt.AlignLeft)
        self.statusholder.addWidget(self.statusicon)
        self.statusholder.addWidget(self.status)
        #self.mainlo.addWidget(self.status)
        self.mainlo.addLayout(self.statusholder)
        self.buildgrid(7) #passing amount of columns, the width of the app
        self.replaylo = QHBoxLayout()
        self.replay = QPushButton()
        self.replay.setText('Play again')
        self.replay.clicked.connect(self.trainer.playcurrent)
        self.arpeggiate = QPushButton()
        if self.mode =='solfa':
            self.arpeggiate.setText('Play cadence')
            self.arpeggiate.clicked.connect(lambda: self.trainer.playcadence()) #syntax på lambda?
        else:
            self.arpeggiate.setText('Arpeggiate')
            self.arpeggiate.clicked.connect(lambda *state,arp=True:self.trainer.playcurrent(arp))
        self.replaylo.addWidget(self.replay)
        self.replaylo.addWidget(self.arpeggiate)
        self.mainlo.addLayout(self.replaylo)
        self.mainlo.addLayout(self.buttonholder)
        self.central.setLayout(self.mainlo)
        self.main.setCentralWidget(self.central)
        self.trainer.newround()

    def buildsucceededfailed(self):
        self.counter = QHBoxLayout()
        self.succeeded = QLabel()
        self.succeeded.setAlignment(Qt.AlignCenter)
        font = self.succeeded.font()
        font.setPointSize(20)
        self.succeeded.setFont(font)
        self.succeeded.setText(str(self.trainer.correctguesses))
        self.failed = QLabel()
        self.failed.setAlignment(Qt.AlignCenter)
        self.failed.setFont(font)
        self.failed.setText(str(self.trainer.incorrectguesses))
        self.counter.addWidget(self.succeeded)
        self.counter.addWidget(self.failed)
        self.menubutton = QPushButton()
        self.menubutton.setText('Return to menu')
        self.menubutton.clicked.connect(self.main.returntomenu)
        self.counter.addWidget(self.menubutton) #TEMPORARY PLACEMENT
        self.mainlo.addLayout(self.counter)

    def buildgrid(self,width):
        self.btns = []
        self.buttonholder = QGridLayout()
        currentrow = 0
        currentcolumn = 0
        for type in self.trainer.possibilities:
            if type == 'break': #Test: plejede at checke efter key val pairs i allpossible
                currentrow += 1
                currentcolumn = 0
                continue
            current = QPushButton()
            current.setText(str(type))
            self.btns.append(current)
            self.btns[-1].clicked.connect(lambda *state,type=type: self.makeguess(type))
            self.buttonholder.addWidget(self.btns[-1],currentcolumn,currentrow) 
            if currentcolumn == width-1:
                currentrow += 1
                currentcolumn = 0
            else:
                currentcolumn += 1

    def makeguess(self,guess):
        if self.trainer.multiple:
            self.makemultipleguess(guess)
        else:
            if guess == self.trainer.subject:
                self.status.setText('Correct!')
                self.statusicon.setPixmap(QPixmap('images/tick.png'))
                self.trainer.correctguesses += 1
            else:
                self.status.setText('Wrong! That was a {subject}'.format(subject=self.trainer.subject))
                self.statusicon.setPixmap(QPixmap('images/cross.png'))
                self.trainer.incorrectguesses += 1
            self.updatedata()
            self.trainer.delayed_newround()
        
    def makemultipleguess(self,guess):
        #Collects multiple guesses as a list and compares to the correct answer.
        self.guesslist.append(guess)
        print('Guesses, subject:',self.guesslist,self.trainer.subject)
        if len(self.guesslist) == self.trainer.multiple: #When the right amount of guesses have been made
            if self.guesslist == self.trainer.subject:
                self.status.setText('Correct!')
                self.statusicon.setPixmap(QPixmap('images/tick.png'))
                self.trainer.correctguesses += 1
            else:
                self.status.setText('Wrong! That was a {subject}'.format(subject=self.trainer.subject))
                self.statusicon.setPixmap(QPixmap('images/cross.png'))
                self.trainer.incorrectguesses += 1
            self.updatedata()
            self.guesslist = []
            self.trainer.delayed_newround()        

    def updatedata(self):
        self.succeeded.setText(str(self.trainer.correctguesses))
        self.failed.setText(str(self.trainer.incorrectguesses))

class chordcategory():
    def __init__(self,name,chords):
        #Chords are a list of all the possible chords in this category
        self.chords = chords
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class intervalcategory():
    def __init__(self,name,intervals):
        #Chords are a list of all the possible chords in this category
        self.intervals = intervals
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class scalecategory():
    def __init__(self,name,scales):
        #Chords are a list of all the possible chords in this category
        self.scales = scales
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class solfacategory():
    def __init__(self,name,solfa):
        self.solfa = solfa
        self.name = name
    
    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

