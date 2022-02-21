import pygame.mixer
import time
from os import walk, getcwd
from threading import Thread
import threading
import random
pygame.mixer.init()
pygame.init()
#fil nr 11 er G1, 64 er C6

class piano():
    allnotes = ['G1','G#1','A1','A#1','B1',
            'C2','C#2','D2','D#2','E2','F2','F#2','G2','G#2','A2','A#2','B2',
            'C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3',
            'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
            'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
            'C6']

    allchordsOLD = {    
    '':(0, 4, 7),
    'maj': (0, 4, 7),
    'm': (0, 3, 7),
    'min': (0, 3, 7),
    '-': (0, 3, 7),
    'dim': (0, 3, 6),
    'aug': (0, 4, 8),
    'sus2': (0, 2, 7),
    'sus4': (0, 5, 7),
    'sus': (0, 5, 7),
    'm7': (0, 3, 7, 10),
    'M7': (0,4,7,11),
    '7': (0,4,7,10)}

#TODO: Organiser disse i under-dicts med kategorier, fx dominanter, mb5 akkorder, osv
    allchords = {
        '5':(0, 7),
        'maj':(0, 4, 7),
        'min':(0, 3, 7),
        'dim':(0, 3, 6),
        'aug':(0, 4, 8),
        'sus2':(0, 2, 7),
        'sus4':(0, 5, 7),
        'break':'break',
        'm6':(0, 3, 7, 9), #minor is 8-21
        'm7':(0, 3, 7, 10), 
        'madd4':(0, 3, 5, 7),
        'madd9':(0, 3, 7, 14),
        'm69':(0, 3, 7, 9, 14),
        'mM7':(0, 3, 7, 11),
        'm9':(0, 3, 7, 10, 14),
        'm7add11':(0, 3, 7, 10, 17),
        'mM7add11':(0, 3, 7, 11, 17),
        'm7b5':(0, 3, 6, 10),
        'm7#5':(0, 3, 8, 10),
        'm7b9b5':(0, 3, 6, 10, 13),
        'dim6':(0, 3, 6, 8),
        'dim7':(0, 3, 6, 9),
        'break2':'break',
        'maj7':(0, 4, 7, 11), #major is 23-34
        'M7+5':(0, 4, 8, 11),
        'add4':(0, 4, 5, 7),
        'add11':(0, 4, 7, 17),
        'add9':(0, 4, 7, 14),
        '6':(0, 4, 7, 9),
        '69':(0, 4, 7, 9, 14),
        'M9':(0, 4, 7, 11, 14),
        'maj9':(0, 4, 7, 11, 14),
        'M7#11':(0, 4, 7, 11, 18),
        'M7add11':(0, 4, 7, 11, 17),
        'M13':(0, 4, 7, 9, 11, 14),
        'break3':'break',
        '7':(0, 4, 7, 10), #dominant is 36 ->
        '7b5':(0, 4, 6, 10),
        '7#5':(0, 4, 8, 10),
        '7sus4':(0, 5, 7, 10),
        '9':(-12, 4, 7, 10, 14),
        '7b9':(-12, 4, 7, 10, 13),
        '7#9':(-12, 4, 7, 10, 15),
        '9sus4':(-12, 5, 7, 10, 14),
        '11':(-12, 7, 10, 14, 17),
        '7#11':(-12, 4, 7, 10, 18),
        '13':(-12, 4, 7, 10, 14, 21),
        '7b13':(-12, 4, 7, 10, 20),
        'break4':'break',
        #'9b5':(-12,-2,4, 6, 14),   #rest of dominants are 49+  NOTE: COMMENTED THIS OUT, MIGHT GIVE PROBS
        '9#5':(-12, -2,4, 8, 14),
        '9#11':(-12, -2,4, 7, 14, 18),
        '7#9b5':(-12, -2,4, 6, 15),
        '7#9#5':(-12, -2,4, 8, 15),
        '7b9b5':(-12, -2,4, 6, 13),
        '7b9#5':(-12, -2,4, 8, 13),
        '7b9#9':(-12, -2,4, 7, 13, 15),
        '7b9#11':(-12, -2,4, 7, 13, 18),
        '7#9#11':(-12, -2,4, 7, 15, 18),
        '7b9b13':(-12, -2,4, 7, 13, 17, 20),
        '13b9':(-12, -2,4, 7, 13, 21),
        '13#9':(-12, -2,4, 7,15, 21),
        '13#11':(-12, -2,4, 7, 18, 21),
        }


    allintervals = {
        #'Unison':(0,0),
        'Minor second':(0,1),
        'Major second':(0,2),
        'Minor third':(0,3),
        'Major third':(0,4),
        'Perfect fourth':(0,5),
        'Diminished fifth':(0,6),
        'Perfect fifth':(0,7),
        'Minor sixth':(0,8),
        'Major sixth':(0,9),
        'Minor seventh':(0,10),
        'Major seventh':(0,11),
        'Octave':(0,12),
        'Minor ninth':(0,13),
        'Major ninth':(0,14),
        'Minor tenth':(0,15),
        'Major tenth':(0,16),
        'Perfect eleventh':(0,17),
        'Augmented eleventh':(0,18),
        'Perfect twelfth':(0,19),
        'Minor thirteenth':(0,20),
        'Major thirteenth':(0,21),
        'Minor forteenth':(0,22),
        'Major fourteenth':(0,23),
        'Two octaves':(0,24)
    }

    allscales = {
        'Major':(0,2,4,5,7,9,11,12),
        'Minor':(0,2,3,5,7,8,10,12),
        'Melodic Minor':(0,2,3,5,7,9,11,12),
    }

    allsolfa = {
        'Do':0,
        'Ra':1,
        'Re':2,
        'Me':3,
        'Mi':4,
        'Fa':5,
        'Fi':6,
        'So':7,
        'Le':8,
        'La':9,
        'Te':10,
        'Ti':11
    }

    def __init__(self):
        self.filenames = self.readfiles()
        self.threads = []
        self.notes = self.notemap()
        #TODO: These types below could be made redundant
        self.chordtypes = list(self.allchords.keys())
        self.intervaltypes = list(self.allintervals.keys())
        self.scaletypes = list(self.allscales.keys())
        self.solfatypes = list(self.allsolfa.keys())
        #self.chordindex = {'triad':(1,7),'all':(1,62),'major':(23,35),'minor':(8,22),'dominant':(36,62)} #Should not be used - see defaultcats
        self.builddefaultcats()

    def playchord(self,type,bottomnote,arpeggiate=False):
        notes = self.selectnotesfromtype(type,bottomnote)
        print(notes)
        self.preparechordnotes(notes)
        self.playthreads(arpeggiate)

    def playinterval(self,intervaltype,bottomnote,arpeggiate=False):
        notes = self.selectintervalnotes(intervaltype,bottomnote)
        #Notes are returned as a list, and are passed to prepareintervalnotes
        self.prepareintervalnotes(notes)
        self.playthreads(arpeggiate)

    def playsubject(self,mode,type,bottomnote,arpeggiate=False,octave='0000000'):
        self.mode = mode
        if mode == 'chords':
            notes = self.selectnotesfromtype(type,bottomnote) #TODO: Generalize selectnotes
            self.preparechordnotes(notes)
        elif mode == 'intervals':
            notes = self.selectintervalnotes(type,bottomnote)
            self.prepareintervalnotes(notes)
        elif mode == 'scales':
            notes = self.selectscalenotes(type,bottomnote)
            self.preparescalenotes(notes)
            arpeggiate = True #scales should always be arpeggiated
        elif mode == 'solfa':
            #if mode is solfa, subject should be a list of notes as solfa strings
            rootindex = self.allnotes.index(bottomnote)
            if not isinstance(type,list):
                notes = [str(type)]
            else:
                notes = type
            self.preparesolfanotes(rootindex,notes,octave)
        self.playthreads(arpeggiate)

    def preparesolfanotes(self,rootindex,notelist,octave,delay=1.0):
        toplay = []
        #if len(notelist) == 1:
        #    toplay.append(self.allnotes[self.allsolfa[notelist]+rootindex])
        counter = 0
        for note in notelist:
            currentoct = int(octave[counter])
            toplay.append(self.allnotes[self.allsolfa[note]+rootindex+(currentoct*12)])
            counter += 1
        del self.threads
        self.threads = []
        self.threads.append(Thread(target = self.playnote, args=(toplay,delay,)))


    def selectnotes(self):
        pass
        """To be a generla note selector. When implementing, remember to change bottomnote from trainingmodes, so the bottomnote is simply the int index of the note, instead of translating to string and bakc again.
        Also, is list of lists too much/not needed?
        """

    def playspecifiednotes(self,notelist,arpeggiate=False):
        #Currently not in use. Can play any list of notes as chords
        self.preparechordnotes(notelist)
        self.playthreads(arpeggiate)

    def playchordstest(self,chords,arpeggiate):
        #Chords is a list of chordname strings, arpeggiate is a boolean
        notestoplay = self.selectnotes(chords)
        print(notestoplay)
        self.preparechordnotes(notestoplay)
        self.playthreads(arpeggiate)

    def selectscalenotes(self,type,bottomnote):
        data = self.allscales[type]
        bottomindex = self.allnotes.index(bottomnote)
        notes = [[self.allnotes[bottomindex + x]] for x in data]
        print('DEMO OF NOTES',notes)
        return notes

    def selectintervalnotes(self,interval,bottomnote):
        _,b = self.allintervals[interval]
        bottomindex = self.allnotes.index(bottomnote)
        secondnote = self.allnotes[bottomindex+b]
        notelist = [[bottomnote],[secondnote]]
        return notelist

    def selectnotesfromtype(self,type,bottomnote,multiple=False):
        #notelist should perhaps be optimized for when only single chord playing is requsted - list of lists is redundant in this use.
        notelist = [[],[],[],[],[],[]]
        #Finds chord data and the starting(bottom) note, and returns the notelist with every note to be playedl.
        #multiple is only for loading and playing several chords.
        chorddata = self.allchords[type]
        startnr = self.allnotes.index(bottomnote)
        for n in range(len(notelist)):
            if n < len(chorddata):
                notelist[n].append(self.allnotes[startnr+chorddata[n]])
            else:
                notelist[n].append(None)
        return notelist

    def preparechordnotes(self,notelist,delay=3):
        #notelist is a list of tuples, where notelist[0] is the bottomvoice, notelist[1] is the second lowest voice, and so on.
        #If only one chord is played, the tuple only has one value.
        #the rest of notelist is filled with None values, so if the notes aren't specified, playnote won't return an out of range error, but will simply do nothing
        del self.threads
        self.threads = []
        for n in range(6):
            self.threads.append(Thread(target = self.playnote, args=(notelist[n],delay,)))

    def prepareintervalnotes(self,notelist):
        del self.threads
        self.threads = []
        self.threads.append(Thread(target = self.playnote, args=(notelist[0],)))
        self.threads.append(Thread(target = self.playnote, args=(notelist[1],)))

    def preparescalenotes(self,notelist):
        del self.threads
        self.threads = []
        for note in notelist:
            self.threads.append(Thread(target = self.playnote,args=(note,)))
        
    def playthreads(self,arpeggiate=False):
        for thread in self.threads:
            thread.start()
            if arpeggiate:
                time.sleep(0.2)
        for thread in self.threads:
            thread.join()

    def readfiles(self):
        folder = getcwd() + '/notes/'
        _, _, filenames = next(walk(folder))
        filenames.sort()
        try:
            filenames.remove('.DS_Store') #necessary on macOS
        except:
            pass
        dirnames = []
        for file in filenames:
            dir = folder + file
            dirnames.append(dir)
        return dirnames

    def notemap(self):
        notemap = dict(zip(self.allnotes,self.filenames))
        return notemap

    def playnote(self,notes=None,delay=3):
        #plays notes. if the notes aren't specified, does nothing.
        if notes != []:
            for note in notes:
                if note != None:
                    notefile = self.notes[note]
                    s = pygame.mixer.Sound(notefile)
                    print(notefile)
                    s.play()
                    time.sleep(delay)
                    s.fadeout(500)
                    time.sleep(0.5)
                else:
                    time.sleep(float(delay)+0.5)

    def findroot(self,chord):
        print(chord)
        note = chord[0]
        if len(chord) > 1:
            if chord[1] == '#':
                note += '#'
        return note

    def builddefaultcats(self):
        self.defaultintervals = {'thirds':(0,4),'first fifth':(0,7),'sixths':(7,9),'first octave':(0,12),'two octaves':(0,23)}
        self.defaultchords = {'triad':(1,7),'all':(1,62),'major':(23,35),'minor':(8,22),'dominant':(36,62)}
        self.defaultscales = {'major/minor':(0,2),'minor':(1,3),'all':(0,3)}
        self.defaultsolfa = {'fifth':(0,8),'octave':(0,12)} #TODO: these should be better, and there should be more

    def playcadence(self,root,first=False,arpeggiate=False):
        #Plays a 2-5-1 cadence
        rootindex = self.allnotes.index(root)
        iivi = [(rootindex,'maj7'),(rootindex+2,'m7'),(rootindex+7,'7'),(rootindex,'maj7')]
        for chord in iivi:
            notes = self.selectnotesfromtype(chord[1],self.allnotes[chord[0]])
            self.preparechordnotes(notes,delay=0.5)
            self.playthreads(arpeggiate)

            