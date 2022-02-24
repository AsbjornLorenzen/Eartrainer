from playnotes import piano
import random
import time
import sys
import threading

class trainer():
    def __init__(self,mode,category,multiple=False):
        self.piano = piano()
        self.arpeggiate = False
        self.category = category
        self.correctguesses = 0
        self.incorrectguesses = 0
        self.mode = mode
        self.multiple = multiple
        self.previous_subject = None #will be added once the first round is done
        if self.mode == 'intervals':
            self.possibilities = self.category.intervals
        if self.mode == 'chords':
            self.possibilities = self.category.chords
        if self.mode == 'scales':
            self.possibilities = self.category.scales
        if self.mode == 'solfa':
            self.key = self.piano.allnotes[random.randint(17,28)]
            self.possibilities = self.category.solfa


    def playcurrent(self,arpeggiate=None):
        if not arpeggiate:
            arpeggiate = self.arpeggiate
        if not hasattr(self,'octaves'):
            self.octaves = '0000000'
        if self.mode == 'solfa':
            self.bottomnote = self.key #In solfa, bottomnote is the key
        self.playthread = threading.Thread(target = self.piano.playsubject,args=(self.mode,self.subject,self.bottomnote,arpeggiate,self.octaves)) #REMEMBER: PASS MODE AS VARIABLE
        self.playthread.start()

    def playcadencethencurrent(self):
        if not hasattr(self,'octaves'):
            self.octaves = '0000000'
        self.piano.playcadence(self.key,True)
        self.piano.playsubject(self.mode,self.subject,self.bottomnote,octave=self.octaves)

    def playcadence(self):
        cthread = threading.Thread(target = self.piano.playcadence,args=(self.key,True))
        cthread.start()

    def play_previous(self):
        #replays the previous subject - good for practicing and understanding mistakes
        temp = (self.subject,self.bottomnote)
        self.subject,self.bottomnote = self.previous_subject
        self.playcurrent()
        self.subject,self.bottomnote = temp


    def choosesubject(self):
        if self.mode == 'solfa' and self.multiple: #Multiple selection requires a different func.
            self.choosemulsubject()
        else:
            notenr = random.randint(17,28)
            self.bottomnote = self.piano.allnotes[notenr]
            self.subject = random.choice(self.possibilities)
            if self.subject == 'break':
                self.choosesubject() #break is used to organize the list of chords, should not be a subject. 

    def choosemulsubject(self):
        #Selects the first element, then selects other that are within 4 semitones
        subjects = [] #int list, index of subjects
        self.octaves = '' #octaves can be hardcoded to be 0's, placing everything in the bottom octave
        firstsubnr = random.randint(0,len(self.possibilities)-1) #Index of first subject
        self.octaves += str(random.randint(0,1))
        subjects.append(firstsubnr)
        withininterval = 4 #Notes are at most 4 semitones away from eachother
        for n in range (self.multiple-1):
            subjects.append(self.choosesubhelper(withininterval,subjects[-1]) + subjects[-1]) #within interval of the latest object in subjects.
            self.octaves += str(random.randint(0,1))
        self.subject = list(map(lambda x: self.possibilities[x],subjects)) #creates list w/ the chosen subjects
                
    def choosesubhelper(self,withininterval,prev):
        #Recursive function that ensures the next chosen note is not the same as previous and not out of bounds
        next = random.randint(-(withininterval),withininterval)
        #check if index is same as previous or is out of bounds
        if (next == 0) or (not 0 < next+prev < len(self.possibilities)):
            return self.choosesubhelper(withininterval,prev)
        return next #int indicating index of next subject compared to the first, e.g. 2 meaning 2 semitones above 1st subject
        

    #Adds a small delay before playing the next subject.
    def delayed_newround(self):
        new = threading.Thread(target = self.delayed_newround_helper)
        new.start()

    def delayed_newround_helper(self):
        time.sleep(0.5)
        self.newround()

    def newround(self):
        if (self.correctguesses + self.incorrectguesses > 0): 
            self.previous_subject = (self.subject,self.bottomnote)
        self.choosesubject()
        if self.mode =='solfa' and ((self.correctguesses + self.incorrectguesses) == 0):
            self.firstthread = threading.Thread(target = self.playcadencethencurrent,args=())
            self.firstthread.start()
        else:
            self.playcurrent()
