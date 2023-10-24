# main.py

"""Simulate evolving DNA barcodes in clonal populations."""

import argparse, yaml, os
import matplotlib.pyplot as plt
import seaborn as sns
from utils import encode
from populate import simulate_population
from bootstrap import vectorize, generate_lineage_matrix

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, help="Output directory", default="./out")
    parser.add_argument("-c", "--config", type=str, help="Config file", default="./config.yaml")

    args = parser.parse_args()

    return args


def read_settings(config_f: str):
    """
    Generate settings dictionary from config YAML.
    """
    with open(config_f, "r") as f:
        print(f"Reading config file {config_f} ...")
        settings = yaml.safe_load(f)

    return settings


def simulate_tree(output_d, config_f: str) -> None:
    """
    Simulate a population of clones and reconstruct the lineage tree.
    """
    # Read settings from config file
    settings = read_settings(config_f)
    k = settings["k"]
    n = settings["n"]
    parity = settings["parity"]

    F = [[[] for i in range(100000)]]
    for i in range(k):
        print(f"Generation {i+1}")
        print("-----------------")
        # Generate population of clones
        print(f"Generating population of clones with {k} splits ...")
        G = simulate_population(F, n)
        # Flatten population
        H = []
        for g in G:
            E = [encode(tuple(x), parity) for x in g]
            H.append(E)

        # Generate lineage matrix
        print(f"Generating lineage matrix ...")
        A = generate_lineage_matrix(H, parity)
        F = G
        
        # Visualize lineage matrix
        print(f"Visualizing lineage matrix and saving to {output_d} ...")
        if not os.path.exists(output_d):
            os.makedirs(output_d)
        plt.figure()
        sns.heatmap(A, cmap = "mako")
        plt.savefig(f"{output_d}/tree-{i+1}.png", dpi=1000)
        plt.close()


if __name__ == "__main__":
    args = parse_args()
    simulate_tree(args.output, args.config)