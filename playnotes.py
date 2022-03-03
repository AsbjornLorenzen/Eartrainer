import pygame.mixer
import time
from os import walk, getcwd
from threading import Thread
from musictheory import allnotes, allchords, allintervals, allscales, allsolfa
import threading
import random
pygame.mixer.init()
pygame.init()
#fil nr 11 er G1, 64 er C6

class piano():
    def __init__(self):
        self.allnotes = allnotes
        self.allchords = allchords
        self.allintervals = allintervals
        self.allscales = allscales
        self.allsolfa = allsolfa
        self.chordtypes = list(self.allchords.keys())
        self.intervaltypes = list(self.allintervals.keys())
        self.scaletypes = list(self.allscales.keys())
        self.solfatypes = list(self.allsolfa.keys())
        self.filenames = self.readfiles()
        self.threads = []
        self.notes = self.notemap()
        self.builddefaultcats()

    def playsubject(self,mode,type,bottomnote,arpeggiate=False,octave='0000000',delay=3):
        self.mode = mode
        if mode == 'chords':
            notes = self.selectchordnotes(type,bottomnote)
            self.preparechordnotes(notes,delay)
        elif mode == 'intervals':
            notes = self.selectintervalnotes(type,bottomnote)
            self.prepareintervalnotes(notes)
        elif mode == 'scales':
            notes = self.selectscalenotes(type,bottomnote)
            self.preparescalenotes(notes)
            arpeggiate = True #scales are always arpeggiated
        elif mode == 'solfa':
            #if mode is solfa, subject is a list of notes as solfa strings
            rootindex = self.allnotes.index(bottomnote)
            if not isinstance(type,list):
                notes = [str(type)]
            else:
                notes = type
            self.preparesolfanotes(rootindex,notes,octave)
        self.playthreads(arpeggiate)

    def selectscalenotes(self,type,bottomnote):
        data = self.allscales[type]
        bottomindex = self.allnotes.index(bottomnote)
        notes = [[self.allnotes[bottomindex + x]] for x in data]
        return notes

    def selectintervalnotes(self,interval,bottomnote):
        _,b = self.allintervals[interval]
        bottomindex = self.allnotes.index(bottomnote)
        secondnote = self.allnotes[bottomindex+b]
        notelist = [[bottomnote],[secondnote]]
        return notelist

    def selectchordnotes(self,type,bottomnote,multiple=False):
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

    def preparesolfanotes(self,rootindex,notelist,octave,delay=1.0):
        del self.threads
        self.threads = [] 
        toplay = []
        for note in notelist:
            currentoct = int(octave[len(toplay)])
            toplay.append(self.allnotes[self.allsolfa[note]+rootindex+(currentoct*12)])
        self.threads.append(Thread(target = self.playnote, args=(toplay,delay,)))
        
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
                    s.play()
                    time.sleep(delay)
                    s.fadeout(500)
                    time.sleep(0.5)
                else:
                    time.sleep(float(delay)+0.5)

    def findroot(self,chord):
        #returns the root note of a chord
        note = chord[0]
        if len(chord) > 1:
            if chord[1] == '#':
                note += '#'
        return note

    def builddefaultcats(self):
        self.defaultintervals = {'thirds':(0,4),'first fifth':(0,7),'sixths':(7,9),'first octave':(0,12),'two octaves':(0,23)}
        self.defaultchords = {'triad':(1,7),'all':(1,62),'major':(23,35),'minor':(8,22),'dominant':(36,62)}
        self.defaultscales = {'major/minor':(0,2),'minor':(1,3),'all':(0,3)}
        self.defaultsolfa = {'fifth':(0,8),'octave':(0,12)} #More categories will be added later

    def playcadence(self,root,arpeggiate=False):
        #Plays a 2-5-1 cadence
        rootindex = self.allnotes.index(root)
        iivi = [(rootindex,'maj7'),(rootindex+2,'m7'),(rootindex+7,'7'),(rootindex,'maj7')]
        for chord in iivi:
            self.playsubject('chords',chord[1],self.allnotes[chord[0]],arpeggiate,delay=0.5)
            