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