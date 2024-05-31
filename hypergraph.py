#####
# v2, 2024/3/15, Zhu
# v3, 2024/5/19, Zhu

import pandas as pd

import itertools, functools

from collections import deque

def powerset(iterable):
    # copied from https://docs.python.org/ja/3/library/itertools.html
    # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"

    s = list(iterable)

    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

class Hypergraph:
    def __init__(self, hyperedge=None, index=None):
        self.edge = hyperedge   ## suppose to be a list of tuples
        self.index = index
        self.k = None
        self.E_map = None
        self.E_map_inverse = None
        self.v_list = None

    def __len__(self):
        return len(self.edge)

    def set_index(self, index):
        if index >= self.k:
            print(f"k = {self.k}, but index is set to be {index}, Error !!!")
            raise ValueError("error!") 
        self.index = index

    # def create_from_csv(self, csv_filename):
    #     self.edge = []
    #     hyperedge_list = pd.read_csv(csv_filename)
    #     self.k = len(hyperedge_list.columns)

    #     for i in range(len(hyperedge_list)):
    #         self.edge.append(tuple(hyperedge_list.loc[i]))

    def create_from_DataFrame(self, pd_dataframe):
        self.edge = []
        self.k = len(pd_dataframe.columns)

        for i in range(len(pd_dataframe)):
            self.edge.append(tuple(pd_dataframe.loc[i]))

    def create_from_edges(self, edge_list):
        self.edge = edge_list[:]
        self.k = len(self.edge[0])

    def get_vertices(self):
        self.v_list = set()
        for i in range(len(self.edge)):
            self.v_list.add(self.edge[i][self.index])

        return self.v_list
        
    def create_E_map(self):
        # create a Gamma function of neighbours
        if self.v_list is None:
            self.get_vertices()
        self.E_map = {v: set() for v in self.v_list}
        self.E_map_inverse = dict()
        for i in range(len(self.edge)):
            edge_tmp = list(self.edge[i][:])
            r = edge_tmp[self.index]
            edge_tmp.pop(self.index)
            edge_tmp = tuple(edge_tmp)
            self.E_map[r].add(edge_tmp)
            if edge_tmp not in self.E_map_inverse:
                self.E_map_inverse[edge_tmp] = set()
            self.E_map_inverse[edge_tmp].add(r)

        return self.E_map

    def check_clique(self, c):
        v_list_tmp = set(self.v_list)
        if len(c) == 1:
            for _c in c[0]:
                v_list_tmp &= self.E_map_inverse[(_c,)]
        else:
            for _c in itertools.product(*c):
                v_list_tmp &= self.E_map_inverse[_c]

        return list(v_list_tmp)

def find_biclique(H, l_now, r_now, candidate, visited):
    # This is a simple implementation of Algorithm MBEA in:
    # Y. Zhang et al. - On finding bicliques in bipartite graphs 
    #     a novel algorithm and its application to the integration 
    #     of diverse biological data types (2014). BMC Bioinformatics, 15(1):110, 2014,
    # that was adjusted for this problem

    r_candidate_list = []

    while len(candidate) > 0:
        p = candidate.popleft()

        r_new = r_now + [p]
        l_prime = H.E_map[p] & l_now

        l_prime_bar = l_now - l_prime
        C = [p]

        candidate_new = list()
        visited_new = list()

        is_maximal = True
        for q in visited:
            N_q = H.E_map[q] & l_prime
            if len(N_q) == len(l_prime):
                is_maximal = False
                break
            elif len(N_q) > 0:
                visited_new.append(q)

        if is_maximal:
            for v in candidate:
                if v == p:
                    continue
                N_v = l_prime & H.E_map[v]
                if len(N_v) == len(l_prime):
                    r_new.append(v)
                    if len(l_prime_bar & H.E_map[v]) == 0:
                        C.append(v)
                elif len(N_v) > 0:
                    candidate_new.append(v)

            r_candidate_list.append(r_new)

            if len(candidate_new) > 0:
                r_candidate_list_tmp = find_biclique(H, l_prime, r_new, deque(candidate_new), visited_new)
                r_candidate_list.extend(r_candidate_list_tmp)

        visited.extend(C)
        for c in C:
            if c != p:
                candidate.remove(c)

    return r_candidate_list

def find_maximal_solutions(k, H, theta_list, min_size, method="var2"):
    if len(H) < min_size:
        # impossible to get a k-hyperclique in the given situation
        return list()

    if H.k == 1:
        # margin case
        H.set_index(0)
        v_list = list(H.get_vertices())
        v_list.sort()
        return [[tuple(v_list)]]

    index_k = H.k - 1    ## maybe there is a better way to determine this

    H.set_index(index_k)
    v_list = H.get_vertices()
    E_map = H.create_E_map()
    new_min_size = min_size / theta_list[index_k]

    maximal_solutions_list_C = []

    if method == "org":
        # very slow, unrecommended
        BB = powerset(list(v_list))
        first_check_necessary = True
    # elif method == "var1":
    #     # a wrong method
    #     B = [[r] for r in list(v_list)]
    #     first_check_necessary = False
    elif method == "var2":
        # default method at now
        visited = []
        r_now = []
        candidate = deque(list(v_list))
        l_now = functools.reduce(lambda x, y: x | y, [E_map[v] for v in v_list])

        BB = find_biclique(H, l_now, r_now, candidate, visited)

        first_check_necessary = True

    for B in BB:   ### maybe there is a better way to select R

        if first_check_necessary and len(B) < theta_list[index_k]:
            # check the theta
            continue

        E_Sk_edge_list = list(functools.reduce(lambda x, y: x & y, [E_map[b] for b in B]))

        if len(E_Sk_edge_list) >= new_min_size:
            E_Sk = Hypergraph()
            E_Sk.create_from_edges(E_Sk_edge_list)

            hat_HH = find_maximal_solutions(k - 1, E_Sk, theta_list, new_min_size, method=method)

            for hat_H in hat_HH:
                Sk = H.check_clique(hat_H)

                ### L \cup R_new is provably a maximal solution once |R_new| >= \theta_k

                if len(Sk) >= theta_list[index_k]:
                    S = hat_H[:]
                    S.append(tuple(sorted(Sk)))

                    if S not in maximal_solutions_list_C:
                        # duplication is still possible
                        maximal_solutions_list_C.append(S)

    return maximal_solutions_list_C


class Hyperclique_Instance:
    def __init__(self, hypergraph=None, theta_list=None):
        self.hypergraph = hypergraph
        self.k = self.hypergraph.k if self.hypergraph is not None else None
        self.theta_list = theta_list[:] if theta_list is not None else None

    def set_instance(self, hypergraph, theta_list):
        self.hypergraph = hypergraph
        self.k = self.hypergraph.k
        self.theta_list = theta_list[:]

    def find_maximal_solutions(self, method="var2"):
        min_size = 1
        for _t in self.theta_list:
            min_size *= _t
        self.maximal_clique_list = find_maximal_solutions(self.k, self.hypergraph, self.theta_list, min_size, method=method)

        return self.maximal_clique_list

    def print_clique(self):
        for c in self.maximal_clique_list:
            for _c in c:
                print(_c)
            print()

