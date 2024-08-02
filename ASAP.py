import queue
import time
import functions
import copy
# from collections import Counter
# from sortedcontainers import SortedDict

# @profile
def ASAP(G, k, g, p):
    print(f"ASAP / k :{k}, g: {g}, p:{p}")
    #for test
    ng_time = 0
    ng_count = 0
    ng_len = 0
    nb_len = 0
    tot_len = 0
    nodelb_time = 0
    nodelb_count = 0
    edgelb_time = 0
    edgelb_count = 0
    less_k_nodelb_success = 0
    less_k_nodelb_fail = 0
    less_k_edgelb_success = 0
    less_k_edgelb_fail = 0
    ge_k_nodelb_fail = 0
    ge_k_edgelb_fail = 0
    #
    start = time.time()
    G1, S = functions.ASAP_kgcore(G, k, g)
    kg_time = time.time() - start
    num_kg_node = len(G1.nodes)
    num_kg_edge = len(G1.hyperedges)
    PQ = functions.PriorityQueue()
    VC = set()
    EC = set(G1.hyperedges.keys())
    M = {}
    for v in S:
        M[v] = {g: S[v]}
    # G1.initialize_Cnt() #노드 객체들 Nodecnt, EdgecntBag 초기화.
    init_time = time.time() - start
    m_time = time.time()
    while EC:
        for edge in EC:
            len_G1 = len(G1.hyperedges[edge])
            if len_G1 / len(G.hyperedges[edge]) < p:
                for v in G1.hyperedges[edge]:
                    if len_G1 -1 == 0:
                        break
                    G1.nodes[v].EdgeCnt = G1.nodes[v].EdgeCnt + 1
                    VC.add(v)
                G1.del_edge(edge)
        EC.clear()
        for v in VC:
            e_time = time.time()
            # print(f"v: {v}, M[v]: {M[v]}, Edgecnt: {G1.nodes[v].EdgeCnt}")
            a, M[v] = functions.getEdgeLB(G1.nodes[v], M[v], g)
            edgelb_time += time.time() - e_time; edgelb_count += 1
            # print(f"v: {v}, M[v]: {M[v]}, Edgecnt: {G1.nodes[v].EdgeCnt}")
            if a < k: #v의 객체, v의 map, g
                ng_init_time = time.time()
                ng, ng_l, nb_l, t_l = functions.getNbrMap(G1, v, g)
                ng_len += ng_l; nb_len += nb_l; tot_len += t_l
                ng_time += time.time() - ng_init_time
                ng_count += 1
                if len(ng) < k:
                    less_k_edgelb_success += 1
                    for e in G1.nodes[v].Edge:
                        EC.add(e)
                    G1.del_node(v)
                    if PQ.contains(v):
                        PQ.remove(v)
                    del M[v]
                    for w in ng:
                        G1.nodes[w].NodeCnt = G1.nodes[w].NodeCnt + 1
                        if PQ.contains(w):
                            PQ.remove(w)
                        PQ.push(w, G1.nodes[w].NodeCnt)
                else:
                    less_k_edgelb_fail += 1
                    M[v] = functions.updatesuptable(ng)
            else:
                ge_k_edgelb_fail += 1
        VC.clear()
        while not PQ.empty():
            v = PQ.pop()
            n_time = time.time()
            a = functions.getNodeLB(G1.nodes[v], M[v])
            nodelb_time += time.time() - n_time; nodelb_count += 1
            if a < k:
                ng_init_time = time.time()
                ng, ng_l, nb_l, t_l = functions.getNbrMap(G1, v, g)
                ng_len += ng_l; nb_len += nb_l; tot_len += t_l
                ng_time += time.time() - ng_init_time
                ng_count += 1
                if len(ng) < k:
                    less_k_nodelb_success += 1
                    for e in G1.nodes[v].Edge:
                        EC.add(e)
                    G1.del_node(v)
                    if PQ.contains(v):
                        PQ.remove(v)
                    del M[v]
                    for w in ng:
                        G1.nodes[w].NodeCnt = G1.nodes[w].NodeCnt + 1
                        if PQ.contains(w):
                            PQ.remove(w)
                        PQ.push(w, G1.nodes[w].NodeCnt)
                else:
                    less_k_nodelb_fail += 1
                    M[v] = functions.updatesuptable(ng)
            else:
                ge_k_nodelb_fail += 1
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
    result['NodeLB_Time'] = nodelb_time
    result['NodeLB_Count'] = nodelb_count
    result['Less_k_NodeLB_Success'] = less_k_nodelb_success
    result['Less_k_NodeLB_Fail'] = less_k_nodelb_fail
    result['Ge_k_NodeLB_Fail'] = ge_k_nodelb_fail
    result['EdgeLB_Time'] = edgelb_time
    result['EdgeLB_Count'] = edgelb_count
    result['Less_k_EdgeLB_Success'] = less_k_edgelb_success
    result['Less_k_EdgeLB_Fail'] = less_k_edgelb_fail
    result['Ge_k_EdgeLB_Fail'] = ge_k_edgelb_fail
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
    return G1, result




