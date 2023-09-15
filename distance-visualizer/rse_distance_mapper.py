# Rucio Bulk RSE Distance Mapper
# Get distance information for all RSEs, map, and visualize the results
# Omari Paul, 2023

import argparse
import logging
import os
import sys
from time import sleep
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from rucio.client import Client as RucioClient

from rucio.client.rseclient import RSEClient

logging.basicConfig(format='%(asctime)-15s %(name)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('rbipi')

rse_objs = []
rse1 = []
rse2 = []
rse3 = []
rse_track = []
list1 = []
list2 = []
list3 = []
ranks = []

rses = {
"CCIN2P3_DATA_DISK" : 3,
"FRDF_STS_DISK" : 3,
"LANCS_DATA_DISK" : 2,
"LA_SERENA_DATA_DISK" : 2,
"RAL_ECHO_DATA_DISK" : 2,
"RAL_ECHO_TEST_DISK" : 2,
"SLAC_DATA_DISK" : 1,
"SLAC_STS_DISK" : 1,
"SLAC_TEST_DISK" : 1,
"SLAC_TTS_DISK" : 1,
"USDF_STS_DISK" : 1
}

def main():
        ranker = RSEClient()
        for rse1 in rses:
                for rse2 in rses:
                        if rse1 == rse2:
                                continue
                        else:
                                rse_obj = ranker.get_distance(rse1, rse2)
                                if rse_obj:
                                        rse_objs.append({'source': rse1, 'destination': rse2, 'rank': rse_obj[0]['ranking']})
        #print(rse_objs)



def sortRSEs():
        for rank in rse_objs:
                if rank['rank'] not in ranks:
                        ranks.append(rank['rank'])
        ranks.sort()


        for rse in rse_objs:
                if rse['rank'] == ranks[1]:
                        if rse['source'] not in rse2:
                                rse2.append(rse)
                                rse_track.append(rse['source'])
                elif rse['rank'] == ranks[0]:
                        rse3.append(rse)

        for rse in rse_objs:
                if rse['rank'] == 1:
                        if rse['source'] in rse_track and rse['destination'] in rse_track:
                                rse1.append(rse)

        for rse in rse1:
                if rse2[0]['source'] == rse['source'] or rse2[0]['source'] == rse['destination']:
                        list1.append(rse['destination'])
                else:
                        list2.append(rse['destination'])

        for rse in rse3:
                if rse['source'] not in list1 and rse['source'] not in list2 and rse['source'] not in list3:
                        list3.append(rse['source'])

        #print(ranks)
        #print(list1)
        #print(list2)
        #print(list3)



def plotRSEs():
        G = nx.DiGraph()
        nodes = np.arange(0, 3).tolist()
        G.add_nodes_from(nodes)
        G.add_edges_from([(0,1), (0,2), (1,2)])

        pos = {0:(10,10), 1:(7.5,7.5), 2:(12.5,7.5)}

        labels = {}
        lists = [list3, list2, list1]

        for i in range(len(lists)):
                label = {i:"\n".join(lists[i])}
                labels.update(label)

        sizes = [12000, 12000, 12000]

        nx.draw_networkx(G, pos = pos, labels = labels, arrows = False, bbox = dict(facecolor = "skyblue", boxstyle = "round", ec = "black", pad = 0.3), edge_color = "black")

        nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = {(0,1): '3', (0,2): '3', (1,2): '2'}, font_color = "black")

        plt.margins(0.3)
        plt.title("Data Facilities and RSE Mappings")
        plt.savefig('Mapping')
        print("Figure saved as Mapping.png")
        print("To visualize RSE mapping run the following command: python3 img_viewer.py Mapping.png")


if __name__ == '__main__':
    main()
    sortRSEs()
    plotRSEs()
