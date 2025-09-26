import json
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
#%matplotlib inline

path = 'cs3220_2025f'

json_files = [os.path.join(root, name) 
              for root, dirs, files in os.walk(path) 
              for name in files 
              if name.endswith((".json"))] #If we needed to read several files extensions: if name.endswith((".ext1", ".ext2"))
print('Number of JSON files ready to be loaded: ' + str(len(json_files)))

json_files
print('Path to the first file: '+json_files[0])
with (open(json_files[0]) as f):
    json_data = json.load(f)

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
             yield person

    def __contains__(self, ch): # to check if the character belongs to the house (for ex., if person in house ...)
        for person in self.characters:
            if (ch == person):
                return True
        return False


    def __str__(self): # to print like print(house) - > displat the house's name
        printHouse = "This is a House of " + self._name + "!"
        return printHouse

    def getStrength(self): # return N of family members in this house (int)
        return len(self.characters)
    
class GameOfThronesGraph:
    def __init__(self, corpus):
        #initialisation of dictionary that will store all houses. They keys are Houses' (Dynasty) names, the values are Dynasty objects.
        self.houses = {}
        #Load the house corpus
        for data_item in corpus:
            house=Dynasty(data_item['name'])
            for characters in data_item['characters']:
                house.append(characters)
            self.houses[data_item['name']]=house
            

    def __iter__(self): # for the case like the following: for house in GameOfThronesHouses:
         for house in self.houses.values():
             yield house

    def __contains__(self, h): #Check if h (house's name) is a key in dict houses - the house is in the graph
        if h in self.houses:
            return True
        return False

#test 1
for data in json_data['groups']:
  house=Dynasty(data['name'])
  for character in data['characters']:
    house.append(character) 
  print(house)
  print("Our members:")
  for person in house:
    print(person)
  print(f"We have {house.getStrength()} family members!!!" + "\n") 
#test 2
corpus_data=json_data['groups']
GameOfThronesHouses=GameOfThronesGraph(corpus_data)
for house in GameOfThronesHouses:
   print(house)
#test 3
visualisationData={}
legendData=[]
for house in GameOfThronesHouses:
  print(house)
  print(f"Strength: {house.getStrength()}")
  visualisationData[house.name]=house.getStrength()
  legendData.append(house.name)
visualisationData
legendData

#Configure your x and y values from the dictionary:
x= list(visualisationData.keys())
y=list(visualisationData.values())

#Create the graph = create seaborn barplot
ax=sns.barplot(x=x,y=y)

#specfiy axis labels
ax.legend(legendData)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1.05, 1))
ax.set(xlabel='Houses',
       ylabel='Strength (N family members)',
       title='Strength of GameOfThronesHouses')

plt.xticks(rotation=45)
#display barplot
plt.show()

g=nx.Graph()

N_houses=0
colorKeys=[]
for house in GameOfThronesHouses:
    if house.name!="Include":
        N_houses+=1
        colorKeys.append(house.name)
sns.color_palette("husl", N_houses) # N_houses colors

nodeColors=dict(zip(colorKeys, [tuple(int(c*255) for c in cs) for cs in sns.color_palette("husl", N_houses)]))

for house in GameOfThronesHouses:
    if house.name!="Include":
        # add the house's name as a node to the graph g (houses's strength values is used as a node's size)
        g.add_node(house.name, size=house.getStrength())
        
for node, attributes in g.nodes(data=True): # run this code to check your code above
    print(f"Node: {node}, Attributes: {attributes}")

for house in GameOfThronesHouses:
    if house.name!="Include":
        # add each character as a node to the graph g 
        for character in house: #goes through every character in the house to add them one by one
            g.add_node(character)

for node, attributes in g.nodes(data=True): # run this code to check your code above
    print(f"Node: {node}, Attributes: {attributes}")

myEdges=[]

for house in GameOfThronesHouses:
    if house.name!="Include":
        for person in house:
            myEdges.append(person, house)
            

print("Connections between a House and its family members:") # run this code to check your code above
myEdges