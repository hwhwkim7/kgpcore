# (k,g,p)-core
This is the implementation of kgp-core algorithms, which is described in the following papaer:
- Beyond trivial edges: A fractional approach to cohesive subgraph detection in hypergraphs, KBS 2025.
- https://www.sciencedirect.com/science/article/pii/S0950705125005180

## How to use

### Algorithms
The implementation includes two algorithms for computing the (k,g,p)-core of a hypergraph:
- NPA(naive)
- ASAP


### Input parameters
  - k : g-neighbour size constraint
  - g : common hyperedge constraint
  - p : edge fraction constraint
  - Algorithm type: naive(NPA) or ASAP
  - Path of the hypergraph data

Example code
```
python main.py --k 5 --g 5 --p 0.8 --algorithm naive --network ./dataset/real/house_bills/network.hyp
python main.py --k 30 --g 30 --p 0.8 --algorithm ASAP --network ./dataset/real/house_bills/network.hyp
# the output file with result will be stored in ./output/{algorithm}/{network_name}/{network_name}_{k}_{g}_{p}.txt.
```

### Datasets
Due to size limitations, only the house_bills, gowalla, and kosarak datasets are uploaded.
You can download additional datasets from the following links:

Amazon : https://www.cs.cornell.edu/~arb/data/amazon-reviews/

Instacart : https://www.cs.cornell.edu/~arb/data/uchoice-Instacart/

Aminer : https://www.github.com/toggled/vldbsubmission


### Cite
```
@article{kim2025beyond,
  title={Beyond trivial edges: A fractional approach to cohesive subgraph detection in hypergraphs},
  author={Kim, Hyewon and Shin, Woocheol and Kim, Dahee and Kim, Junghoon and Lim, Sungsu and Jeong, Hyun Ji},
  journal={Knowledge-Based Systems},
  pages={113472},
  year={2025},
  publisher={Elsevier}
}
```
