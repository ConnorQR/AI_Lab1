import json
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

path="data/game-of-thrones-characters-groups.json"

json_files = [os.path.join(root, name) 
              for root, dirs, files in os.walk(path) 
              for name in files 
              if name.endswith((".json"))] #If we needed to read several files extensions: if name.endswith((".ext1", ".ext2"))
print('Number of JSON files ready to be loaded: ' + str(len(json_files)))

#print('Path to the first file: '+json_files[0])
with (open(path) as f):
    json_data = path

'''
with (open(json_files[0]) as f):
    json_data = json.load(f)
'''

class Dynasty:
    def __init__(self,name):
        self._name=name # House name, for.ex."Martell"
        self.characters=[] # Family members ("Doran Martell","Ellaria Sand","Nymeria Sand",...)


    @property
    def name(self): # getter for the private instance attribute _name
        return self._name
       

    @name.setter
    def name(self, value):
        if value!="": #making sure the value isn't a null string
            self._name=value
      

    def append(self, ch): # to append character to the House (during reading data from JSON-file)
        if (isinstance(ch, str)):
            self.characters.append(ch)
        #this code will check if character is an instance
         #of the String class. If not, an exception will be raised


    def __iter__(self): # to loop throw the list of characters via IN operator (for ex. for person in house: ....)
         for person in self.characters:
             print(person + "\n")

    def __contains__(self, ch): # to check if the character belongs to the house (for ex., if person in house ...)
        for person in self.characters:
            if (ch == person):
                return True
        return False


    def __str__(self): # to print like print(house) - > displat the house's name
        print(self._name)
    
    def getStrength(self): # return N of family members in this house (int)
        return len(self.characters)
    
class GameOfThronesGraph:
    def __init__(self, corpus):
        #initialisation of dictionary that will store all houses. They keys are Houses' (Dynasty) names, the values are Dynasty objects.
        self.houses = {}
        #Load the house corpus
        for data_item in corpus:
            house=Dynasty(data_item)
            for characters in house:
                house.append(characters)
            self.houses[data_item]=house
            

    def __iter__(self): # for the case like the following: for house in GameOfThronesHouses:
         for house in self.houses.values():
             print(house)

    def __contains__(self, h): #Check if h (house's name) is a key in dict houses - the house is in the graph
        if h in self.houses:
            return True
        return False
'''
for data in json_data['groups']:
  house=Dynasty(data['name'])
  for character in data['characters']:
    house.append(character)
  print(house)
  print("Our members:")
  for person in house:
    print(person)
  print(f"We have {house.getStrength()} family members!!!")

corpus_data=json_data['groups']
GameOfThronesHouses=GameOfThronesGraph(corpus_data)
for house in GameOfThronesHouses:
   print(house)

visualisationData={}
legendData=[]
for house in GameOfThronesHouses:
  print(house)
  print(f"Strength: {house.getStrength()}")
  visualisationData[house.name]=house.getStrength()
  legendData.append(house.name)
visualisationData
legendData

#%matplotlib inline
'''