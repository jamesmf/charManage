# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 10:53:31 2015

@author: jmf
"""

import numpy as np
import cPickle
import json
from os.path import isfile

STATNAMES   = ["STRENGTH","DEXTERITY","CONSTITUTION","INTELLIGENCE","WISDOM","CHARISMA"]

class Char:
    
    def __init__(self,desc):
        self.atts   = {}
        self.mods   = {}
        self.profs  = {}
        self.desc   = desc.lower().strip()
        self.name   = self.getName()
        self.exists = self.hasSheet()
        self.getStats()
        self.jsonObj= self.toJSON()
        self.writeMe()
        
    def toJSON(self):
        ret     = {}
        ret["atts"] = self.atts
        ret["mods"] = self.mods
        ret["desc"] = self.desc
        ret["name"] = self.name
        ret["profs"]= self.profs  
        return ret
        
    def hasSheet(self):
        return isfile(self.name)
        
    def writeMe(self):
        with open("data/"+self.name,"wb") as f:
            json.dump(self.jsonObj,f)

    def getStats(self):
        if self.exists:
            with open(self.name,'rb') as f:
                me  = json.load(f)
            self.atts = me["atts"]
            self.mods = me["mods"]
        else:
           self.makeStats()
            
        
class PC(Char):
     
    
    def makeStats(self):
        attributes  = {}
        modifiers   = {}
        proficiencies={}
        rolls       = []
        for i in range(0,6):
            rolls.append(int(np.sum(sorted(np.ceil(np.random.rand(4)*6.),reverse=True)[:-1])))
        count = 0
        while len(rolls) > 0:
            print "Remaining Statistics:\n",rolls
            print "Please enter ",STATNAMES[count]," score, chosen from above"
            val     = raw_input("")
            if int(val) in rolls:
                rolls.pop(rolls.index(int(val)))
                attributes[STATNAMES[count]]    = int(val)
                modifiers[STATNAMES[count]]     = int(np.floor((int(val)-10)/2))
                count+=1         
        self.atts   = attributes
        self.mods   = modifiers
    
    def getName(self):
        return self.desc.lower().strip()
        
        
class Monster(Char):
     
    
    def makeStats(self):
        attributes  = {}
        modifiers   = {}
        rolls       = []
        for i in range(0,6):
            rolls.append(int(np.sum(sorted(np.ceil(np.random.rand(4)*6.),reverse=True)[:-1])))
        count = 0
        while len(attributes) < 6:
            print "Please enter ",STATNAMES[count]," score"
            val     = raw_input("")
            attributes[STATNAMES[count]]    = int(val)
            modifiers[STATNAMES[count]]     = np.floor((int(val)-10)/2)
            count+=1         
        self.atts   = attributes
        self.mods   = modifiers
    
    def getName(self):
        return self.desc.lower().strip()
        
        
        

pc  = PC("Jon_HU_BD")
#pc.makeStats()
print pc.atts
print pc.mods