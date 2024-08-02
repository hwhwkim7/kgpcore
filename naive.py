import queue
import time
import copy
import functions

# @profile
def naive(G, k,g,p):
    print(f"naive_kgpcore / k :{k}, g: {g}, p:{p}")
    #for test
    ng_time = 0
    ng_count = 0
    ng_len = 0
    nb_len = 0
    tot_len = 0
    #
    start = time.time()
    Q = queue.Queue()
    Q1 = set()
    G1, S = functions.ASAP_kgcore(G, k, g)
    kg_time = time.time() - start
    num_kg_node = len(G1.nodes)
    num_kg_edge = len(G1.hyperedges)
    EC = set(G1.hyperedges.keys())
    VC = set()
    init_time = time.time() - start
    m_time = time.time()
    while EC:
        for edge in EC:
            if len(G1.hyperedges[edge]) / len(G.hyperedges[edge]) < p:
                VC.update(G1.hyperedges[edge])
                G1.del_edge(edge)
        for v in VC:
            ng_init_time = time.time()
            ng, ng_l, nb_l, t_l = functions.getNbrMap(G1, v, g)
            ng_len += ng_l; nb_len += nb_l; tot_len += t_l
            ng_time += time.time() - ng_init_time
            ng_count += 1
            S[v] = len(ng)
            if S[v] < k:
                Q.put(v)
                Q1.add(v)
        VC.clear(); EC.clear()
        while not Q.empty():
            v = Q.get()
            Q1.remove(v)
            ng_init_time = time.time()
            ng, ng_l, nb_l, t_l = functions.getNbrMap(G1, v, g)
            ng_len += ng_l; nb_len += nb_l; tot_len += t_l
            ng_time += time.time() - ng_init_time
            ng_count += 1
            # EC = EC.union(G1.nodes[v].Edge)
            for e in G1.nodes[v].Edge:
                EC.add(e)
            G1.del_node(v)
            del S[v]
            for w in ng:
                if w not in Q1:
                    S[w] -= 1
                    if S[w] < k:
                        Q.put(w)
                        Q1.add(w)
    main_time = time.time() - m_time
    run_time = time.time() - start
    result = {}
    result['Run_Time'] = run_time
    result['KG_Time'] = kg_time
    result['Init_Time'] = init_time
    result['Main_Time'] = main_time
    result['N^g_Time'] = ng_time
    result['N^g_Count'] = ng_count
    if ng_count != 0:
        result['Average_N^g_Length'] = ng_len / ng_count
        result['Average_Nb_Length'] = nb_len / ng_count
        result['Average_tot_occur'] = tot_len / ng_count
    else:
        result['Average_N^g_Length'] = 'cnt_count0'
        result['Average_Nb_Length'] = 'cnt_count0'
        result['Average_tot_occur'] = 'cnt_count0'
    frac = 0.0
    for e in G1.hyperedges:
        frac += len(G1.hyperedges[e]) / len(G.hyperedges[e])  # 남은 edge의 fraction 평균.
    if len(G1.hyperedges) != 0:
        result['avg_frac_edge'] = frac / len(G1.hyperedges)
    else:
        result['avg_frac_edge'] = 'no_hyperedge'
    result['num_kg_node'] = num_kg_node
    result['num_kg_edge'] = num_kg_edge
    result['num_remain_node'] = len(G1.nodes)
    result['num_remain_edge'] = len(G1.hyperedges)
    # print(result)
    return G1, result

