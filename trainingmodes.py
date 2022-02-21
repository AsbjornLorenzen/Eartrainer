from playnotes import piano
import random
import time
import sys
import threading

class trainer():
    #FIX SOLFA: Newround skal, hvis der er 0 gættede, spille kadence. Desuden, tilføj kadence knap ved arpeggio.
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
        if self.mode =='solfa' and ((self.correctguesses + self.incorrectguesses) == 0):
            #Plays cadence before first round of solfa
            self.firstthread = threading.Thread(target = self.playcadencethencurrent,args=())
            #self.piano.playcadence(self.key,True)
            self.firstthread.start()
        else:
            self.playthread = threading.Thread(target = self.piano.playsubject,args=(self.mode,self.subject,self.bottomnote,arpeggiate,self.octaves)) #REMEMBER: PASS MODE AS VARIABLE
            self.playthread.start()

    def playcadencethencurrent(self):
        self.piano.playcadence(self.key,True)
        self.piano.playsubject(self.mode,self.subject,self.bottomnote,octave=self.octaves)

    def playcadence(self):
        cthread = threading.Thread(target = self.piano.playcadence,args=(self.key,True))
        #self.piano.playcadence(self.key,True)
        cthread.start()
        #Maybe in an external thread

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
        print('Subjects selected: ',subjects)
        self.subject = list(map(lambda x: self.possibilities[x],subjects)) #creates list w/ the chosen subjects
        print('Subject: ',self.subject)
                
    def choosesubhelper(self,withininterval,prev):
        #Recursive function that ensures the next chosen note is not the same as previous and is still within the allowed notes.
        #Only returns difference between current and next, to ensure that the recursion works. The caller should always add the result to the prev number.
        print('Within;',withininterval,prev)
        print('possibilities: ',self.possibilities,len(self.possibilities))
        next = random.randint(-(withininterval),withininterval)
        if next == 0:
            next = self.choosesubhelper(withininterval,prev)
        if not 0 < next+prev < len(self.possibilities):
            next = self.choosesubhelper(withininterval,prev)
        print(next)
        return next
        
    #Below adds a small delay before playing the next subject.
    def delayed_newround(self):
        new = threading.Thread(target = self.delayed_newround_helper)
        new.start()

    def delayed_newround_helper(self):
        time.sleep(0.5)
        self.newround()

    def newround(self):
        self.choosesubject()
        #time.sleep(1)
        self.playcurrent()




















class chordtrainer(trainer):
    def __init__(self,category):
        super().__init__()
        self.allchords = self.piano.allchords
        self.category = category
        self.possibilities = self.category.chords

    def newround(self):
        #print('New round')
        self.choosesubject() #subject is the chord, interval, scale etc which is currently being played and tested. 
        self.playcurrent()

    def choosechord(self):
        #C3 is nr 17 in the notes, C5 is nr 41
        #notenr = random.randint(17,41)
        notenr = random.randint(17,28)
        self.bottomnote = self.piano.allnotes[notenr]
        while True:
            self.currentchord = random.choice(self.possibilities)
            if self.currentchord != 'break':
                break

class OLDchordtrainer():
    #NOTE: Piano is instantiated in the mode, remember to delete the instance when shutting down/changing modes to avoid having many threads running
    def __init__(self,category):
        #Category is the category of chords, fx dominant chords 
        print('init')
        self.piano = piano()
        self.allchords = self.piano.allchords
        self.arpeggiate = False
        self.category = category
        self.possibilities = self.category.chords
        self.correctguesses = 0
        self.incorrectguesses = 0
        #self.newround()

    def choosechord(self):
        #C3 is nr 17 in the notes, C5 is nr 41
        #notenr = random.randint(17,41)
        notenr = random.randint(17,28)
        self.bottomnote = self.piano.allnotes[notenr]
        while True:
            self.currentchord = random.choice(self.possibilities)
            if self.currentchord != 'break':
                break

    def playchord(self,type): #bottomnote=None
        """if not bottomnote:
            #C3 is nr 17 in the notes, C5 is nr 41
            notenr = random.randint(17,41)
            self.buttomnote == self.piano.allnotes[notenr]
        else:
            self.bottomnote = bottomnote"""
        self.piano.playchord(type,self.bottomnote,self.arpeggiate)

    def playcurrentchord(self,arpeggiate=None):
        if not arpeggiate:
            arpeggiate=self.arpeggiate
        self.playthread = threading.Thread(target = self.piano.playchord,args=(self.currentchord,self.bottomnote,arpeggiate))
        #self.piano.playchord(self.currentchord,self.bottomnote,self.arpeggiate)
        self.playthread.start()

""" 
    def newround(self):
        print('New round')
        #choose new chord
        self.choosechord()
        #
        self.playcurrentchord()

    def guesschord(self,guess):
        if guess == self.currentchord:
            self.correctguesses += 1
        else:
            self.incorrectguesses += 1 """

class intervaltrainer():
    def __init__(self,category): #No category is given. Might want to add ability to choose certain types of intervals later
        self.category = category
        self.piano = piano()
        self.allintervals = self.piano.allintervals
        self.allintervalslist = list(self.allintervals.keys())
        self.arpeggiate = False
        self.possibilities = self.category.intervals
        self.correctguesses = 0
        self.incorrectguesses = 0


    """def buildintervallist(self,category):
        intervallist = []
        self.intervalindex = {'fifth':(0,7),'octave':(0,12),'two octaves':(0,24)}
        a,b = self.intervalindex[category]
        for n in range(a,b):
            intervallist.append(self.allintervalslist[n])
        return intervallist"""
        
    def chooseinterval(self):
        notenr = random.randint(17,28)
        self.bottomnote = self.piano.allnotes[notenr]
        self.currentinterval = random.choice(self.possibilities)

    def playcurrentinterval(self,arpeggiate=None):
        if not arpeggiate:
            arpeggiate = self.arpeggiate
        self.playthread = threading.Thread(target = self.piano.playinterval,args=(self.currentinterval,self.bottomnote,arpeggiate))
        self.playthread.start()

    def guessinterval(self,guess):
        if guess == self.currentinterval:
            self.correctguesses += 1
        else:
            self.incorrectguesses += 1

    def newround(self):
        self.chooseinterval()
        self.playcurrentinterval(self.arpeggiate)


    

if __name__ == '__main__':
    c = chordtrainer()
    c.playchord('13#11','C4')
