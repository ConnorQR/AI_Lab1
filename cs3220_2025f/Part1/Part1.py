import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width',100)
pd.set_option("display.max_colwidth", 135)

data = pd.read_csv("C:/Users/conno_52qz545/CS3220 AI/cs3220_2025f/data/game-of-thrones-battles.csv")
data.head()

data.info()

battles_df=data.loc[:,['name','attacker_king','defender_king','attacker_size','defender_size']]
battles_df.head()

battles_df.info()

battles_df_cleaned=battles_df.dropna()
battles_df_cleaned.info()

print(f"Attacking kings: {battles_df_cleaned.attacker_king.unique()}")

print(f"Defending kings: {battles_df_cleaned.defender_king.unique()}")

net5kings = Network(heading="Task1. Building Interactive Network of battles of War of 5",
                    bgcolor = "#242020",
                    font_color = "white",
                    height = "1000px",
                    width = "100%",
                    directed = True, # we have directed graph
                    notebook = True,
                    cdn_resources = "remote"
)

type(data['attacker_king'].values)

Kings_list=np.unique(np.concatenate((battles_df_cleaned['attacker_king'].values,battles_df_cleaned['defender_king'].values),0))
Kings_list

net5kings.add_nodes(Kings_list)
net5kings.nodes

edges = battles_df_cleaned.loc[:,["attacker_king", "defender_king"]].values.tolist()
edges[:]

edges_unique = []
for item in edges:
    if item not in edges_unique:
        edges_unique.append(item)
edges_unique

edge_weight = battles_df_cleaned.groupby(['attacker_king','defender_king']).size()
edge_weight

Titles = battles_df_cleaned.groupby(["attacker_king","defender_king"])['name'].agg(', '.join)
Titles

edge_weight_df = edge_weight.reset_index(name = 'count')
Titles_df = Titles.reset_index()
Data_df = pd.merge(edge_weight_df, Titles_df, on=['attacker_king', 'defender_king'], how='inner')

def format_row(row):
    return f"Attacking King: {row['attacker_king']}  Defending King: {row['defender_king']} N of Battles: {row['count']} Battle Names: {row['name']}"

attacks = Data_df.apply(format_row, axis=1)
print(attacks)
print("edges_weight: ", edge_weight_df['count'].tolist())

for index, row in Data_df.iterrows():
    net5kings.add_edge(row['attacker_king'], row['defender_king'], value=row['count'], title=row['name'])

def format_row(row):
    return f"The edge from '{row['attacker_king']}' to '{row['defender_king']}' with weight '{row['count']}' Title: '{row['name']}"

net5kings.edges

enemies_map = net5kings.get_adj_list()

for node in net5kings.nodes:
    node["value"] = len(enemies_map[node["id"]])+1

enemies_map

nodeColors={
    0:"blue",
    1:"green",
    2:"orange",
    3:"purple",
    4:"gold",
    5:"red"
}

for node in net5kings.nodes:
    node["color"] = nodeColors[node["value"]]

net5kings.nodes

net5kings.show("lab1-task1-net5kings.html", notebook = False)

