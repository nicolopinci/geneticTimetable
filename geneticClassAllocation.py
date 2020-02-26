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
        
        firstList = sorted(firstList, key=lambda x:x.id)
        secondList = sorted(secondList, key=lambda x:x.id)
        
        crossedList = []
        addedEvents = []
        
        for i in range(0, len(firstList)):
            if((firstList[i].currentEvent not in addedEvents) and (secondList[i].currentEvent not in addedEvents)):
                casualElement = randrange(0,1)
                if(casualElement == 0):
                    crossedList.append(firstList[i])
                    addedEvents.append(firstList[i].currentEvent)
                else:
                    crossedList.append(secondList[i])
                    addedEvents.append(secondList[i].currentEvent)
            elif((firstList[i].currentEvent not in addedEvents) or (secondList[i].currentEvent not in addedEvents)):
                if(firstList[i].currentEvent not in addedEvents):
                    crossedList.append(firstList[i])
                    addedEvents.append(firstList[i].currentEvent)
                else:
                    crossedList.append(secondList[i])
                    addedEvents.append(secondList[i].currentEvent)
            else:
                j = 0
                while j<len(firstList):
                    if(firstList[j] not in addedEvents):
                        crossedList.append(firstList[j])
                        addedEvents.add(firstList[j])
                        j = len(firstList)
                    elif(secondList[j] not in addedEvents):
                        crossedList.append(secondList[j])
                        addedEvents.add(secondList[j])
                        j = len(firstList)
                    else:
                        j = j+1
    
        return Chromosome(crossedList)
                


    def fillRandom(self, events):
        listLength = len(events)
        permutation = list(range(listLength))
        permutation = random.sample(permutation, len(permutation))
        
        for p in range(0, len(permutation)):
            newRoom = Room("ROOM"+str(p), "", randrange(1, 100), True)
            newRoom.currentEvent = events[permutation[p]]
            newRoom.isEmpty = False
            
            self.roomList.append(newRoom)
                
                

  
        
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
