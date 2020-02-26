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
                out += "Room " + room.id + " (" + str(room.capacity) + " people): " + room.currentEvent.id + " (" + str(room.currentEvent.numberPeople) + " people)"
                if(room.capacity < room.currentEvent.numberPeople):
                    out += " (*)"
                out += "\n"
                
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
        
        firstList = copy.deepcopy(self.roomList)
        secondList = copy.deepcopy(otherChromosome.roomList)
        
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
                
                

  
        
mu = 0.01
chi = 0.5

rooms = []
events = []
chromosomes = []

totalPersons = 0
count = 0
maxChromosomes = 100
numberEvents = 30

for e in range(0, numberEvents):
    peopleEvent = randrange(1, 100)
    events.append(Event("EVENT"+str(e), "", peopleEvent))
    totalPersons += peopleEvent

for k in range(0, maxChromosomes):
    chromosomes.append(Chromosome([]))
    chromosomes[k].fillRandom(events)
 
    
evolution = True

while(evolution):
    count = count + 1
    sortedChromosomes = sorted(chromosomes, key=lambda x:x.fitness(), reverse = True)
    sortedChromosomes = sortedChromosomes[0:maxChromosomes]
    
    toMutate = math.floor(mu*len(sortedChromosomes))
    toCrossover = math.floor(chi*len(sortedChromosomes)/2)*2

    print("Generation " + str(count) + ": " + str(sortedChromosomes[0].fitness()) + " on " + str(totalPersons))
    print(sortedChromosomes[0])
    
    if(sortedChromosomes[0].fitness() == totalPersons):
        evolution = False
#    print(sortedChromosomes[0])
#    print("=====================")
    
    elite = copy.deepcopy(sortedChromosomes)
    elite = elite[0:toCrossover]
    worst = copy.deepcopy(sortedChromosomes[(len(sortedChromosomes) - toMutate):])
        
    childs = []
    
#    print("==========00001============")
#    for s in range(0, len(sortedChromosomes)):
#        print(sortedChromosomes[s].fitness())
    
    for c in range(0, len(elite)-1):
        childs.append(elite[c].crossover(elite[c+1]))
       
#    print("==========00002============")
#    for s in range(0, len(sortedChromosomes)):
#        print(sortedChromosomes[s].fitness())
    
    for m in range(0, len(worst)):
        worst[m].mutate()
        
#    print("==========00003============")
#    for s in range(0, len(sortedChromosomes)):
#        print(sortedChromosomes[s].fitness())
        
    chromosomes = childs + sortedChromosomes + worst
#    
#    print("==========00004============")
#    for s in range(0, len(sortedChromosomes)):
#        print(sortedChromosomes[s].fitness())
        
#    if(count == 1):
#        evolution = False