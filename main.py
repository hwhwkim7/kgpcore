import argparse
import os
import time
import sys
import datetime
import functions
import ASAP
import naive

# python main.py --k 5 --g 5 --p 0.8 --algorithm naive --network ./dataset/real/house_bills/network.hyp
# python main.py --k 30 --g 30 --p 0.8 --algorithm ASAP --network ./dataset/real/house_bills/network.hyp
def get_base(file_path):
    path = os.path.dirname(file_path)
    return path+'/'
def get_user_param(args_set, _alg):
    ret = dict()
    if _alg == 'kgpcore':
        ret['k'] = args_set.k
        ret['g'] = args_set.g
        ret['p'] = args_set.p
    return ret

parser = argparse.ArgumentParser(description='value k')
parser.add_argument('--k', type=int, default=30,
                    help='user parameter k')

parser.add_argument('--g', type=int, default=30,
                    help='user parameter g')

parser.add_argument('--p', type=float, default=0.8,
                    help='threshold p of kgpcore or abpcore')

parser.add_argument('--algorithm', default='ASAP',
                    help='specify algorithm name')

parser.add_argument('--network', default="./dataset/real/house_bills/network.hyp",
                    help='a folder name containing network.dat')

parser.add_argument('--rec', default=0,
                    help='recursiv or not')

parser.add_argument('--mode', default='',
                    help='recursiv or not')

args = parser.parse_args()
user_params = get_user_param(args, args.algorithm)

if args.mode == 'single':
    if args.algorithm == 'kgcore':
        start_time = time.time()
        G = functions.Hypergraph()
        G.load_from_file(args.network)
        G, result = functions.ASAP_kgcore(G, args.k, args.g)
        print(result)
        print(f"Run time: {time.time() - start_time:.4f}")
        exit()
    if args.algorithm == 'ASAP':
        G = functions.Hypergraph()
        G.load_from_file(args.network)
        start_time = time.time()
        G, result = ASAP.ASAP(G, args.k, args.g, args.p)
        print(result)
        print(f"Run time: {time.time() - start_time:.4f}")
        exit()
    # python main.py --mode single --k 30 --g 30 --p 0.8  --algorithm naive --network ./dataset/real/house_bills/network.hyp
    if args.algorithm == 'naive':
        G = functions.Hypergraph()
        G.load_from_file(args.network)
        start_time = time.time()
        G, result = naive.naive(G, args.k, args.g, args.p)
        print(result)
        print(f"Run time: {time.time() - start_time:.4f}")
        exit()

# python main.py --mode compare --network ./dataset/real/house_bills/network.hyp
if args.mode == 'compare':
    output_dir = 'output'
    network_name = args.network.split('/')[-2]
    final_dir = os.path.join(output_dir, 'compare', network_name)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    tot = 0
    num_true = 0
    num_false = 0
    G = functions.Hypergraph()
    G.load_from_file(args.network)
    wrong = set()
    for i in range(1,4):
        for j in range(1,4):
            for k in [x * 0.1 for x in range(0, 4)]:
                tot += 1
                file_name = f"{args.network.split('/')[-2]}.txt"
                file_path = os.path.join(final_dir, file_name)
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                G1, _ = naive.naive(G, i, j, k)
                G2, _ = ASAP.ASAP(G, i, j, k)
                if G1.nodes.keys() == G2.nodes.keys() and G1.hyperedges.keys() == G2.hyperedges.keys():
                    num_true +=1
                else:
                    num_false +=1
                    wrong.add(f"k: {i}, g: {j}, p: {k}")
    results_to_write = [
        f"Date: {current_date}\n",
        f"compare: ASAPcompare\n",
        f"Tot: {tot}\n",
        f"num_true: {num_true}\n",
        f"num_false: {num_false}\n"
        f"wrong: {wrong}\n"
    ]
    with open(file_path, 'a') as file:
        file.writelines(results_to_write)
        file.write(f"\n")

    print(f"Results saved to {file_path}")
    exit()

# python main.py --k 30 --g 30 --p 0.8 --algorithm naive --network ./dataset/real/house_bills/network.hyp
#결과파일 저장 코드
output_dir = 'output'
algorithm_dir = os.path.join(output_dir, args.algorithm)
final_dir = os.path.join(algorithm_dir, args.network.split('/')[-2])

# 알고리즘별 결과 디렉토리 생성 (해당 디렉토리가 없을 경우)
if not os.path.exists(final_dir):
    os.makedirs(final_dir)

# 파일 이름 설정
file_name = f"{args.network.split('/')[-2]}_k{args.k}_g{args.g}_p{args.p}.txt"
file_path = os.path.join(final_dir, file_name)
current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#이미 결과 존재하면 건너뜀.
if os.path.exists(file_path):
    print("File already exists. Skipping the operation.")
    exit()

G = functions.Hypergraph()
G.load_from_file(args.network)

result = {}
result['python_file'] = ''
result['rec'] = 0
result['run_time'] = 0
result['init_time'] = 0
result['main_time'] = 0
result['edge_time'] = 0
result['cnt_time'] = 0
result['cnt_count'] = 0
result['avg_nb_len'] = 0 #nb의 수
result['avg_tot_occur'] = 0 #tot occur 중복 포함.
result['avg_ng_len'] = 0 #ng의 수
result['avg_frac_edge'] = 0
result['num_kg_node'] = 0
result['num_kg_edge'] = 0
result['num_remain_node'] = 0
result['num_remain_edge'] = 0
result['lower_time'] = 0
result['lower_count'] = 0

if args.algorithm == 'naive':
    _, result = naive.naive(G, args.k, args.g, args.p)
    result['python_file'] = 'naive.py'
    result['NodeLB_Time'] = 'N/A'
    result['NodeLB_Count'] = 'N/A'
    result['EdgeLB_Time'] = 'N/A'
    result['EdgeLB_Count'] = 'N/A'
    result['Less_k_NodeLB_Success'] = 'N/A'
    result['Less_k_NodeLB_Fail'] = 'N/A'
    result['Ge_k_NodeLB_Fail'] = 'N/A'
    result['Less_k_EdgeLB_Success'] = 'N/A'
    result['Less_k_EdgeLB_Fail'] = 'N/A'
    result['Ge_k_EdgeLB_Fail'] = 'N/A'

if args.algorithm == 'ASAP':
    _, result = ASAP.ASAP(G, args.k, args.g, args.p)
    result['python_file'] = 'ASAP.py'
    # print(f"nodeset: {G1.nodes.keys()}, hyperedgeset: {G1.hyperedges.keys()}")

results_to_write = [
    f"Date: {current_date}\n",
    f"Python_File: {result['python_file']}\n",
    f"Run_Time: {result['Run_Time']:.4f}\n",
    f"KG_Time: {result['KG_Time']:.4f}\n",
    f"Init_Time: {result['Init_Time']:.4f}\n",
    f"Main_Time: {result['Main_Time']:.4f}\n",
    f"N^g_Time: {result['N^g_Time']:.4f}\n",
    f"N^g_Count: {result['N^g_Count']}\n",
    f"Average_N^g_Length: {0 if result['Average_N^g_Length'] == 'cnt_count0' else format(float(result['Average_N^g_Length']), '.4f')}\n",
    f"Average_Nb_Length: {0 if result['Average_Nb_Length'] == 'cnt_count0' else format(float(result['Average_Nb_Length']), '.4f')}\n",
    f"Average_tot_occur: {0 if result['Average_tot_occur'] == 'cnt_count0' else format(float(result['Average_tot_occur']), '.4f')}\n",
    f"NodeLB_Time: {'N/A' if result['NodeLB_Time'] == 'N/A' else format(float(result['NodeLB_Time']), '.4f')}\n",
    # f"NodeLB_Time: {result['NodeLB_Time']:.4f}\n",
    f"NodeLB_Count: {result['NodeLB_Count']}\n",
    f"Less_k_NodeLB_Success: {result['Less_k_NodeLB_Success']}\n",
    f"Less_k_NodeLB_Fail: {result['Less_k_NodeLB_Fail']}\n",
    f"Ge_k_NodeLB_Fail: {result['Ge_k_NodeLB_Fail']}\n",
    # f"EdgeLB_Time: {result['EdgeLB_Time']:.4f}\n",
    f"EdgeLB_Time: {'N/A' if result['EdgeLB_Time'] == 'N/A' else format(float(result['EdgeLB_Time']), '.4f')}\n",
    f"EdgeLB_Count: {result['EdgeLB_Count']}\n",
    f"Less_k_EdgeLB_Success: {result['Less_k_EdgeLB_Success']}\n",
    f"Less_k_EdgeLB_Fail: {result['Less_k_EdgeLB_Fail']}\n",
    f"Ge_k_EdgeLB_Fail: {result['Ge_k_EdgeLB_Fail']}\n",
    f"Average_frac_edge: {0 if result['avg_frac_edge'] == 'no_hyperedge' else format(float(result['avg_frac_edge']), '.4f')}\n",
    f"num_kg_node: {result['num_kg_node']}\n",
    f"num_kg_edge: {result['num_kg_edge']}\n",
    f"num_remain_node: {result['num_remain_node']}\n",
    f"num_remain_edge: {result['num_remain_edge']}\n",
]


# 파일에 결과 데이터 쓰기
with open(file_path, 'a') as file:
    file.writelines(results_to_write)
    file.write(f"\n")

print(f"Results saved to {file_path}")