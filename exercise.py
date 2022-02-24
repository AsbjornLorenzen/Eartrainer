from trainingmodes import trainer
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel,QWidget,QPushButton, QVBoxLayout,QHBoxLayout, QGridLayout
from PySide6.QtGui import QPixmap, QFont

class exercise():
    def __init__(self,main,mode,category,multiple=False):
        super().__init__()
        self.mode = mode
        self.category = category
        self.trainer = trainer(self.mode,self.category,multiple)
        self.main = main
        self.main.resize(600,600)
        if multiple:
            self.guesslist = []
        self.buildwindow()


    def buildwindow(self):
        self.central = QWidget()
        self.mainlo = QVBoxLayout()
        self.buildsucceededfailed()
        
        self.modeinfo = QLabel()
        self.modeinfo.setFont(QFont('Arial',20))
        self.modeinfo.setText('Practicing {mode}: {type}'.format(type=self.category,mode=self.mode))
        self.modeinfo.setAlignment(Qt.AlignCenter)
        self.mainlo.addWidget(self.modeinfo)
        
        self.statusholder = QHBoxLayout()
        self.statusholder.setAlignment(Qt.AlignCenter)
        self.statusicon = QLabel()
        self.statusicon.setAlignment(Qt.AlignRight)
        self.status = QLabel()
        self.status.setFont(QFont('Arial',16))
        self.status.setText('')
        self.status.setAlignment(Qt.AlignLeft)
        self.statusholder.addWidget(self.statusicon)
        self.statusholder.addWidget(self.status)
        self.mainlo.addLayout(self.statusholder)

        self.buildgrid(7) #passing amount of columns, the width of the app
        self.replaylo = QHBoxLayout()
        self.replay = QPushButton()
        self.replay.setText('Play again')
        self.replay.clicked.connect(self.trainer.playcurrent)

        self.arpeggiate = QPushButton()
        if self.mode =='solfa':
            self.arpeggiate.setText('Play cadence')
            self.arpeggiate.clicked.connect(lambda: self.trainer.playcadence())
        else:
            self.arpeggiate.setText('Arpeggiate')
            self.arpeggiate.clicked.connect(lambda *state,arp=True:self.trainer.playcurrent(arp))
        
        self.back_to_previous = QPushButton()
        self.back_to_previous.setText('Play previous')
        self.back_to_previous.clicked.connect(self.trainer.play_previous)
        self.back_to_previous.setEnabled(False)

        self.replaylo.addWidget(self.back_to_previous)
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
        self.succeeded.setText('Correct: {0}'.format(str(self.trainer.correctguesses)))

        self.failed = QLabel()
        self.failed.setAlignment(Qt.AlignCenter)
        self.failed.setFont(font)
        self.failed.setText('Incorrect: {0}'.format(str(self.trainer.incorrectguesses)))

        self.menubutton = QPushButton()
        self.menubutton.setText('Return to menu')
        self.menubutton.clicked.connect(self.main.returntomenu)

        self.counter.addWidget(self.succeeded)
        self.counter.addWidget(self.failed)
        self.counter.addWidget(self.menubutton)

        self.mainlo.addLayout(self.counter)

    def buildgrid(self,width):
        self.btns = []
        self.buttonholder = QGridLayout()
        currentrow = 0
        currentcolumn = 0
        for type in self.trainer.possibilities:
            if type == 'break':
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
        #Called when the user enters an answer. Records whether it is correct, and starts a new round
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
            self.back_to_previous.setEnabled(True) #Button is enabled after first round
            self.updatedata()
            self.trainer.delayed_newround()
        
    def makemultipleguess(self,guess):
        #Collects multiple guesses as a list and compares to the correct answer.
        self.guesslist.append(guess)
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
        self.succeeded.setText('Correct: {0}'.format(str(self.trainer.correctguesses)))
        self.failed.setText('Incorrect: {0}'.format(str(self.trainer.incorrectguesses)))