import copy
import itertools

from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._id_stati = {}
        self.percorso = []
        self.punteggio = 0

    def get_min_max(self):
        return DAO.get_min_max()

    def get_all_shapes(self):
        return DAO.get_all_shapes()

    def make_graph(self, lat, lon, shape):
        self._grafo.clear()
        nodi = DAO.get_nodi(lat, lon, shape)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            n.Neighbors = n.Neighbors.split(" ")
            print(n.Neighbors)
            self._id_stati[n.id] = n

        durate = DAO.get_durate(shape)


        for a in nodi:
            for vicino in a.Neighbors:
                b = self._id_stati.get(vicino)
                if b is not None and not self._grafo.has_edge(a, b):
                    self._grafo.add_edge(a, b, weight = (durate[a.id] + durate[b.id]))


    def dim_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_info(self):
        # 5 nodi di grado magiore e 5 archi di costo maggiore
        nodi = [(n, self._grafo.degree(n)) for n in self._grafo.nodes]
        archi = [(a, b, self._grafo[a][b]["weight"] ) for a, b in self._grafo.edges]

        nodi.sort(key=lambda x: x[1], reverse=True)
        archi.sort(key=lambda x: x[2], reverse=True)

        return nodi[0:5], archi[0:5]

    def get_percorso(self):
        self.percorso = []
        self.punteggio = 0
        for n in self._grafo:
            self._ricorsione([n], 0, 0)

        res = []

        for n in self.percorso:
            res.append((n, n.Population / n.Area))

        return res, self.punteggio



    def _ricorsione(self, parziale, peso_attuale, distanza_attuale):
        print("qui")
        if distanza_attuale != 0 and (peso_attuale/distanza_attuale) > self.punteggio:
            self.punteggio = (peso_attuale/distanza_attuale)
            self.percorso = copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            if self._controlla_step(parziale[-1], n):
                peso = self._grafo[parziale[-1]][n]["weight"]
                distanza = parziale[-1].distance_HV(n)
                parziale.append(n)
                self._ricorsione(parziale, peso_attuale+peso, distanza_attuale+distanza)
                parziale.pop()

    def _controlla_step(self, a, b):
        den_a = a.Population / a.Area
        den_b = b.Population / b.Area

        if den_b > den_a:
            return True

        return False
