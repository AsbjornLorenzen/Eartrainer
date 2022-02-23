from PySide6.QtWidgets import QLabel,QWidget,QPushButton,QHBoxLayout,QGridLayout,QCheckBox
from categories import *

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
        self.selected = [] #reset selected
        self.hide()

    def buildgrid(self,width):
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