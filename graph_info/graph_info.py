import os

def analyze_hypergraph(file_path, output_folder, data_name):
    node_neighbors = {}
    node_degrees = {}
    edges = []
    edge_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            edge = line.strip().split(',')
            node_ids = set(map(int, edge))
            edges.append(node_ids)  # 엣지 리스트에 노드 ID 집합 추가
            edge_count += 1
            for node in node_ids:
                if node not in node_neighbors:
                    node_neighbors[node] = set()
                    node_degrees[node] = 0
                node_degrees[node] += 1
                node_neighbors[node].update(node_ids)

    # 각 노드의 이웃에서 자기 자신을 제거
    for node in node_neighbors:
        node_neighbors[node].discard(node)
    
    num_nodes = len(node_neighbors)
    total_nodes_in_edges = sum(len(edge) for edge in edges)  # 정확한 엣지 내 노드 수 계산
    avg_nodes_per_edge = total_nodes_in_edges / edge_count if edge_count > 0 else 0
    total_neighbors = sum(len(neighbors) for neighbors in node_neighbors.values())
    average_neighbor_size = total_neighbors / num_nodes
    average_degree = sum(degrees for degrees in node_degrees.values()) / num_nodes

    # 결과를 txt 파일로 저장
    output_path = os.path.join(output_folder, f'{data_name}.txt')
    with open(output_path, 'w') as output_file:
        output_file.write(f"Dataset: {data_name}\n")
        output_file.write(f"Number of nodes: {num_nodes}\n")
        output_file.write(f"Number of edges: {edge_count}\n")
        output_file.write(f"Average number of nodes per edge: {avg_nodes_per_edge:.2f}\n")
        output_file.write(f"Average Neighbor Size: {average_neighbor_size:.2f}\n")
        output_file.write(f"Average Degree: {average_degree:.2f}\n")

    print(f"Results written to {output_path}")

# 파일 경로 설정 및 함수 호출
data_name = 'aminer'
file_path = f'../ASAP_v5/dataset/real/{data_name}/network.hyp'
output_folder = './output'
analyze_hypergraph(file_path, output_folder, data_name)
