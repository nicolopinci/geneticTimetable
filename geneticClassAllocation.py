#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:48:41 2020

@author: nicolo
"""

from random import randrange
import copy
import random
import math

class Event:
    def __init__(self, id, description, numberPeople):
        self.id = id
        self.description = description
        self.numberPeople = numberPeople
    
class Room:
    def __init__(self, id, description, capacity, isEmpty):
        self.id = id
        self.description = description
        self.isEmpty = isEmpty
        self.currentEvent = Event(0, "", 0)
        self.capacity = capacity
    
class Chromosome:
    def __init__(self, roomList):
        self.roomList = roomList
        
    def addEventToRoom(self, event, oldRoom):
        room = copy.deepcopy(oldRoom)
        
        added = False
        for r in self.roomList:
            if(r == room):
                room.currentEvent = event
                added = True
        
        if(added == False):
            room.currentEvent = event
            self.roomList.append(room)  
        room.isEmpty = False
            
    def deleteEvent(self, event):
        for room in self.roomList:
            if(room.currentEvent == event):
                room.isEmpty = True
        
    def __str__(self):
        out = ""
        for room in self.roomList:
            if(room.isEmpty == False):
                out += "Room " + room.id + ": " + room.currentEvent.id + "\n"
            
        return out
    
    def mutate(self):
        position1 = randrange(0, len(self.roomList))
        position2 = randrange(0, len(self.roomList))
        temp = self.roomList[position1].currentEvent
        self.roomList[position1].currentEvent = self.roomList[position2].currentEvent
        self.roomList[position2].currentEvent = temp
        
    def fitness(self):
        satisfiedPeople = 0
        for room in self.roomList:
            if(room.currentEvent.numberPeople <= room.capacity):
                satisfiedPeople += room.currentEvent.numberPeople
                
        return satisfiedPeople
        
    def crossover(self, otherChromosome):
    
        firstList = copy.copy(self.roomList)
        secondList = copy.copy(otherChromosome.roomList)
        
        firstList = sorted(firstList, key=lambda x: x.id, reverse = True)
        secondList = sorted(secondList, key=lambda x: x.id, reverse = True)
           
        # source: https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
    
        child = []
        childP0 = []
        childP1 = []
        childP2 = []
        
        geneA = int(randrange(0, len(firstList)-1))
        geneB = int(randrange(0, len(secondList)-1))
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
    
         
        print("...............::")
        if(len(firstList) == len(secondList)):
            print(startGene)
            print(endGene)
            print(self)
            print(otherChromosome)
            
        addedEvents = []
        
        for i in range(startGene, endGene):
            childP1.append(secondList[i])
            addedEvents.append(secondList[i].currentEvent)
            
        for i in range(0, startGene-1):
            found = False
            for j in range(0, len(firstList)):
                if(found == False):
                    if(firstList[j].currentEvent not in addedEvents):
                        firstList[i].currentEvent = firstList[j].currentEvent
                        addedEvents.append(firstList[j].currentEvent)
                        childP0.append(firstList[j])
                        found = True
            
                  
        for i in range(endGene+1, len(secondList)):
            found = False
            for j in range(0, len(firstList)):
                if(found == False):
                    if(firstList[j].currentEvent not in addedEvents):
                        firstList[i].currentEvent = firstList[j].currentEvent
                        addedEvents.append(firstList[j].currentEvent)
                        childP2.append(firstList[j])
                        found = True
    
        child = childP0 + childP1 + childP2
           
        newChromosome = Chromosome(child)
      
        print(newChromosome)
        print("::::::::::::::::::::::::")
        return newChromosome


    def fillRandom(self, events):
        listLength = len(events)
        permutation = list(range(listLength))
        permutation = random.sample(permutation, len(permutation))
        
        for p in range(0, len(permutation)):
            newRoom = Room("ROOM"+str(p), "", randrange(1, 100), True)
            newRoom.currentEvent = events[permutation[p]]
            newRoom.isEmpty = False
            
            self.roomList.append(newRoom)
                
                
#        position1 = randrange(0, len(firstList))
#        position2 = randrange(0, len(secondList))
#        
#        element1 = firstList[position1].currentEvent
#        element2 = secondList[position2].currentEvent
#        
#        position3 = 0
#        position4 = 0
#        
#        for a in range(0, len(firstList)):
#            if(firstList[a] == element2):
#                position3 = a
#                
#        
#         for b in range(0, len(secondList)):
#            if(secondList[b] == element1):
#                position4 = b
#                
#        temp = firstList[position1].currentEvent
#        firstList[position1].currentEvent = secondList[position2].currentEvent
#        secondList[position2].currentEvent = temp
#        
#        temp = firstList[position3].currentEvent
#        firstList[position3].currentEvent = secondList[position4].currentEvent
#        secondList[position4].currentEvent = temp
#        
        
mu = 0.5
chi = 0.5

rooms = []
events = []
chromosomes = []

totalPersons = 0

for e in range(0, 10):
    peopleEvent = randrange(1, 100)
    events.append(Event("EVENT"+str(e), "", peopleEvent))
    totalPersons += peopleEvent

for k in range(0, 5):
    chromosomes.append(Chromosome([]))
    chromosomes[k].fillRandom(events)
 
    
evolution = True

while(evolution):
    sortedChromosomes = sorted(chromosomes, key=lambda x:x.fitness(), reverse = True)
    
#    for s in range(0, len(sortedChromosomes)):
#        print(sortedChromosomes[s].fitness())
        
    toMutate = math.floor(mu*len(sortedChromosomes))
    toCrossover = math.floor(chi*len(sortedChromosomes)/2)*2

    print("Best solution so far:")
    print(str(sortedChromosomes[0].fitness()) + " on " + str(totalPersons))
    print(sortedChromosomes[0])
    print("=====================")
    
    elite = sortedChromosomes[0:toCrossover]
    worst = sortedChromosomes[toMutate:]
        
    childs = []
    
    for c in range(0, len(elite)-1):
        childs.append(elite[c].crossover(elite[c+1]))
            
    for m in range(0, len(worst)):
        worst[m].mutate()
        
    chromosomes = childs + sortedChromosomes
    
    if(sortedChromosomes[0].fitness() == totalPersons):
        evolution = False
#room1 = Room("VS7", "Study room", 100, True)
#event1 = Event("MAT001", "Math 001", 150)
#room2 = Room("VS9", "Lecture room", 200, True)
#event2 = Event("PHY001", "Physics 001", 10)
#
#room3 = Room("VS4", "Study room", 100, True)
#event3 = Event("MAT002", "Math 001", 150)
#room4 = Room("VS5", "Lecture room", 200, True)
#event4 = Event("PHY005", "Physics 001", 10)

#chromosome1 = Chromosome([])
#chromosome1.addEventToRoom(event1, room1)
#chromosome1.addEventToRoom(event2, room2)
#chromosome1.addEventToRoom(event3, room3)
#chromosome1.addEventToRoom(event4, room4)
#
#
#chromosome2 = Chromosome([])
#chromosome2.addEventToRoom(event1, room3)
#chromosome2.addEventToRoom(event2, room4)
#chromosome2.addEventToRoom(event3, room2)
#chromosome2.addEventToRoom(event4, room1)

#print(chromosome1.fitness())
#print(chromosome2.fitness())
