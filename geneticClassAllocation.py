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

class Lecture:
    def __init__(self, id, description, numberPeople, timeslots, color):
        self.id = id
        self.description = description
        self.numberPeople = numberPeople
        self.timeslots = timeslots
        self.color = color
        
    def __str__(self):
        return str(self.id) + " - " + self.description + " - " + str(self.numberPeople) + " people - " + str(self.timeslots) + " timeslots"
        
    def transformIntoEvents(self):
        eventList = []
        for i in range(0, self.timeslots):
            eventList.append(Event(str(self.id) + "_" + str(i), self.description, self.numberPeople, i, self.id))
            
        return eventList
    
class Event:
    def __init__(self, id, description, numberPeople, fragmentNr, lecture):
        self.id = id
        self.description = description
        self.numberPeople = numberPeople
        self.fragmentNr = fragmentNr
        self.lecture = lecture
        
    def __str__(self):
        return str(self.id) + " - " + self.description + " - " + str(self.numberPeople) + " people, lecture " + str(self.lecture) + ", fragm " + str(self.fragmentNr)
    
    def findLecture(self, lectures):
        for l in lectures:
            if(l.id == self.lecture):
                return l
        return Lecture("","",0,0,"rgb(255,255,255)")
    
class Room:
    def __init__(self, id, description, capacity, isEmpty):
        self.id = id
        self.description = description
        self.isEmpty = isEmpty
        self.currentEvent = Event("", "", 0, 0, "")
        self.capacity = capacity
        
    def fillRandom(self, number):
        self.id = "ROOM"+str(number)
        self.description = ""
        self.capacity = randrange(1, 100)
        self.isEmpty = True

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
        
    def setRooms(self, rooms):
        self.roomList = copy.deepcopy(rooms)
        
#    def fillRandom(self, inEvents):
#        
#        events = copy.deepcopy(inEvents)
#        
#        listLength = len(events)
#        permutation = list(range(listLength))
#        permutation = random.sample(permutation, len(permutation))
#        
#        for r in range(0, len(self.roomList)):
#            self.roomList[r].currentEvent = events[permutation[r]]
#            self.roomList[r].isEmpty = False
                
                

def generateEvents(inEvents, roomList):
        
    outEvents = []
    
    events = copy.deepcopy(inEvents)
    
    listLength = len(events)
    permutation = list(range(listLength))
    permutation = random.sample(permutation, len(permutation))
    
    for r in range(0, len(roomList)):
        outEvents.append(events[permutation[r]])
    
    return outEvents
        
mu = 0.2
chi = 0.5

rooms = []
allEvents = []
lectures = []
timetable = []
chromosomes = []

maxChromosomes = 100
numberLectures = 100
availableTimeslots = 6
numberRooms = 100

totalSatisfied = 0
totalInvolved = 0

f = open("timetable.html","w")
f.write("<html>")
f.write("<head>")
f.write("</head>")
f.write("<body>")
f.write("<ul>")
for e in range(0, numberLectures):
    peopleLecture = randrange(1, 100)
    numberTimeslots = randrange(1, 10)
    red = str(randrange(100, 220))
    green = str(randrange(100, 220))
    blue = str(randrange(100, 220))
    color = "rgb("+red+","+green+","+blue+")"
    lectures.append(Lecture("LECTURE"+str(e), "", peopleLecture, numberTimeslots, color))
    f.write("<li>" + lectures[e].id + " - " + str(peopleLecture) + " people - " + str(numberTimeslots) + " timeslots</li>")
    allEvents += lectures[e].transformIntoEvents()
f.write("</ul>")
currentTS = 0

for r in range(0, numberRooms):
    room = Room("","",0,True)
    room.fillRandom(r)
    rooms.append(copy.deepcopy(room))
    
for c in range(0, maxChromosomes):
    chromosome = Chromosome([])
    chromosome.setRooms(rooms)
    chromosomes.append(chromosome)
    
for l in lectures:
    totalInvolved += l.numberPeople*l.timeslots

while(currentTS < availableTimeslots):
    
    currentTS += 1
    
    events = []
    totalPersons = 0
    count = 0
    
    
    for l in range(0, len(lectures)):
        minFragment = float('inf')
        minEvent = Event("","",0,0,"")
        
        for e in range(0, len(allEvents)):
            if(lectures[l].id == allEvents[e].lecture): 
                if(allEvents[e].fragmentNr < minFragment):
                    minFragment = allEvents[e].fragmentNr
                    minEvent = copy.deepcopy(allEvents[e])
        events.append(minEvent)
        totalPersons += minEvent.numberPeople
    

    newChromosomes = []
    
    for k in range(0, maxChromosomes):
        permutatedEvents = generateEvents(events, rooms)
        rooms = []
        for r in range(0,len(chromosomes[k].roomList)):
            newRoom = copy.deepcopy(chromosomes[k].roomList[r])
            newRoom.currentEvent = permutatedEvents[r]
            newRoom.isEmpty = False
            rooms.append(newRoom)
        newChromosomes.append(Chromosome(rooms))

    chromosomes = newChromosomes
    
    evolution = True
    
    numberEquals = 0
    previousFitness = 0
    
    while(evolution):
        count = count + 1
        sortedChromosomes = sorted(chromosomes, key=lambda x:x.fitness(), reverse = True)
        sortedChromosomes = sortedChromosomes[0:maxChromosomes]
        
        if(sortedChromosomes[0].fitness() == previousFitness):
            numberEquals += 1
        else:
            numberEquals = 0
        
        previousFitness = sortedChromosomes[0].fitness() 
        
        toMutate = math.floor(mu*len(sortedChromosomes))
        toCrossover = math.floor(chi*len(sortedChromosomes)/2)*2
    
        print("TS " + str(currentTS) + " - Generation " + str(count) + ": " + str(sortedChromosomes[0].fitness()) + " on " + str(totalPersons))
        print(sortedChromosomes[0])
        
        if(numberEquals == 5 or sortedChromosomes[0].fitness() == totalPersons):
                        
            timetableChromosome = copy.deepcopy(sortedChromosomes[0])
            timetable.append(timetableChromosome)
            evolution = False
            
            bestEvents = []
                        
            for r in range(0, len(sortedChromosomes[0].roomList)):
                if(sortedChromosomes[0].roomList[r].currentEvent.numberPeople <= sortedChromosomes[0].roomList[r].capacity):
                    bestEvents.append(sortedChromosomes[0].roomList[r].currentEvent)
            
                    totalSatisfied += sortedChromosomes[0].roomList[r].currentEvent.numberPeople
            
            newAllEvents = []
            for ev in range(0, len(allEvents)):
                foundEvent = False
                for be in range(0, len(bestEvents)):
                    if(allEvents[ev].id == bestEvents[be].id):
                        foundEvent = True
                if(foundEvent == False):
                    newAllEvents.append(allEvents[ev])
                    
            allEvents = newAllEvents
                        
        elite = copy.deepcopy(sortedChromosomes)
        elite = elite[0:toCrossover]
        worst = copy.deepcopy(sortedChromosomes[(len(sortedChromosomes) - toMutate):])
            
        childs = []
        
        for c in range(0, len(elite)-1):
            childs.append(elite[c].crossover(elite[c+1]))
        
        for m in range(0, len(worst)):
            worst[m].mutate()
                    
        chromosomes = childs + sortedChromosomes + worst
        

f.write("<table style=\"border-collapse: collapse; border: 1px solid black;\">")

for col in range(0, len(timetable[0].roomList)):
   f.write("<th style=\"border: 1px solid black; padding: 5px;\">")
   f.write(timetable[0].roomList[col].id)
   f.write("<br/>")
   f.write("<span style=\"font-size: small;\">")
   f.write("(max " + str(timetable[0].roomList[col].capacity) +" people)")
   f.write("</span>")
   f.write("</th>")
        
for row in range(0, len(timetable)):
    f.write("<tr style=\"border: 1px solid black;\">")
    for col in range(0, len(timetable[row].roomList)):
        f.write("<td style=\"border: 1px solid black; padding: 5px; ")
        if(timetable[row].roomList[col].currentEvent.numberPeople <= timetable[row].roomList[col].capacity):
            f.write("background-color: " + timetable[row].roomList[col].currentEvent.findLecture(lectures).color + ";\">")
            f.write(timetable[row].roomList[col].currentEvent.id)
            f.write("<br/>")
            f.write("<span style=\"font-size: small;\">")
            f.write("(" + str(timetable[row].roomList[col].currentEvent.numberPeople) +" people)")
            f.write("</span>")
        else:
            f.write("\">")
        f.write("</td>")
    f.write("</tr>")
f.write("</table>")
f.write("There are " + str(totalSatisfied) + " people satisfied on a total of " + str(totalInvolved))
f.write("</body>")
f.write("</html>")

f.close()