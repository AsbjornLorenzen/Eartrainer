allnotes = ['G1','G#1','A1','A#1','B1',
        'C2','C#2','D2','D#2','E2','F2','F#2','G2','G#2','A2','A#2','B2',
        'C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3',
        'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
        'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
        'C6']
        
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