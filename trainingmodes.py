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

    def choosesubject(self):
        if self.mode == 'solfa' and self.multiple: #Multiple selection requires a different func.
            self.choosemulsubject()
        else:
            notenr = random.randint(17,28)
            self.bottomnote = self.piano.allnotes[notenr]
            self.subject = random.choice(self.possibilities)
            if self.subject == 'break':
                self.choosesubject() #break is usedf to organize the list of chords. 

    def choosemulsubject(self):
        #Selects the first element, then selects other that are within a third. This can later be edited, so that it isn't hardcoded.
        subjects = []
        self.octaves = '' #octaves can be hardcoded to be 0's, which will be everything in the bottom octave
        firstsubnr = random.randint(0,len(self.possibilities)-1) #Index of first subject
        self.octaves += str(random.randint(0,1))
        subjects.append(firstsubnr)
        withininterval = 4 #Notes are no more than 4 semitones away from eachother
        for n in range (self.multiple-1):
            subjects.append(self.choosesubhelper(withininterval,subjects[-1])+subjects[-1]) #within interval of the latest object in subjects.
            self.octaves += str(random.randint(0,1))
        self.subject = list(map(lambda x: self.possibilities[x],subjects)) #creates list w/ the chosen subjects
                
    def choosesubhelper(self,withininterval,prev):
        #Recursive function that ensures the next chosen note is not the same as previous and is still within the allowed notes.
        #Only returns difference between current and next, to ensure that the recursion works. The caller should always add the result to the prev number.
        next = random.randint(-(withininterval),withininterval)
        if next == 0:
            next = self.choosesubhelper(withininterval,prev)
        if not 0 < next+prev < len(self.possibilities):
            next = self.choosesubhelper(withininterval,prev)
        return next
        
    #Adds a small delay before playing the next subject.
    def delayed_newround(self):
        new = threading.Thread(target = self.delayed_newround_helper)
        new.start()

    def delayed_newround_helper(self):
        time.sleep(0.5)
        self.newround()

    def newround(self):
        self.choosesubject()
        if self.mode =='solfa' and ((self.correctguesses + self.incorrectguesses) == 0):
            self.firstthread = threading.Thread(target = self.playcadencethencurrent,args=())
            self.firstthread.start()
        else:
            self.playcurrent()
