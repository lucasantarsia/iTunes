import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

        self._bestSet = None
        self._bestScore = 0

    def buildGraph(self, d):
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap = {a.AlbumId: a for a in list(self._graph.nodes)}
        # for a in list(self._graph.nodes):
        #     self._idMap[a.AlbumId] = a
        edges = DAO.getEdges(self._idMap)

        self._graph.add_edges_from(edges)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._graph, v0)
        durataTOT = 0
        for album in conn:
            durataTOT += album.totD
        return len(conn), toMinutes(durataTOT)

    def getSetAlbum(self, a1, dTot):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._graph, a1)
        parziale = set([a1])  #???
        connessa.remove(a1)  # tolgo a1 da connesse visto che essendo in parziale non mi serve

        self._ricorsione(parziale, connessa, dTot)
        return self._bestSet, self.durataTot(self._bestSet)

    def _ricorsione(self, parziale, connessa, dTot):
        # Verificare se parziale è una soluzione ammissibile
        if self.durataTot(parziale) > dTot:  # se la durata è maggiore di dTot scarto questa soluzione
            return

        # Verificare che parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        # Ciclo su nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                self._ricorsione(parziale, connessa, dTot)
                parziale.remove(c)

    def durataTot(self, listOfNodes):
        dTot = 0
        for n in listOfNodes:
            dTot += n.totD
        return toMinutes(dTot)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)

    def getNodeI(self, i):
        return self._idMap[i]

def toMillisec(d):
    return d*60*1000

def toMinutes(d):
    return d/1000/60
