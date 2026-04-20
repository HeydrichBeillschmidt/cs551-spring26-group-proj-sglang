import os
import csv
import matplotlib.pyplot as plt

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLOT_DIR = os.path.join(REPO_ROOT, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# -----------------------------
# Dataset mapping
# -----------------------------
AWS_BASE = os.path.join(REPO_ROOT, "aws-daeun")
GCP_BASES = [
    os.path.join(REPO_ROOT, "gcp-roohee"),
    os.path.join(REPO_ROOT, "gcp-alina"),
]

DATASET_MAP = {
    "sharegpt": "sharegpt",
    "random": "random",
    "random-ids": "random-ids",
    "generated-shared-prefix": "generated-shared-prefix",
}

GCP_SPECIAL_NAMES = {
    "generated-shared-prefix": "generated-shared-prefix - 4096"
}

# -----------------------------
# Metrics to plot
# -----------------------------
METRICS = {
    "output_throughput": "Output Throughput (tokens/sec)",
    "p99_e2e_latency_ms": "P99 Latency (ms)",
    "energy_per_request_j": "Energy per Request (J)",
    "avg_power_w": "Average GPU Power (W)",
}

# -----------------------------
# Helper functions
# -----------------------------
def read_metric(csv_path):
    data = {}
    if not os.path.exists(csv_path):
        return data
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["metric"]] = float(row["value"])
    return data


def find_gcp_path(dataset):
    for base in GCP_BASES:
        name = GCP_SPECIAL_NAMES.get(dataset, dataset)
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    return None


def collect_data():
    results = {metric: {"AWS": [], "GCP": []} for metric in METRICS}

    datasets = list(DATASET_MAP.keys())

    for dataset in datasets:
        # AWS
        aws_path = os.path.join(AWS_BASE, DATASET_MAP[dataset])
        aws_perf = read_metric(os.path.join(aws_path, "bench_metrics.csv"))
        aws_energy = read_metric(os.path.join(aws_path, "dcgm_summary.csv"))

        # GCP
        gcp_base = find_gcp_path(dataset)
        if gcp_base:
            gcp_perf = read_metric(os.path.join(gcp_base, "bench_metrics.csv"))
            gcp_energy = read_metric(os.path.join(gcp_base, "dcgm_summary.csv"))
        else:
            gcp_perf, gcp_energy = {}, {}

        for metric in METRICS:
            if metric in aws_perf:
                results[metric]["AWS"].append(aws_perf[metric])
            elif metric in aws_energy:
                results[metric]["AWS"].append(aws_energy[metric])
            else:
                results[metric]["AWS"].append(0)

            if metric in gcp_perf:
                results[metric]["GCP"].append(gcp_perf[metric])
            elif metric in gcp_energy:
                results[metric]["GCP"].append(gcp_energy[metric])
            else:
                results[metric]["GCP"].append(0)

    return datasets, results


# -----------------------------
# Plotting
# -----------------------------
def plot_all():
    datasets, results = collect_data()
    x = range(len(datasets))

    for metric, title in METRICS.items():
        aws_vals = results[metric]["AWS"]
        gcp_vals = results[metric]["GCP"]

        width = 0.35

        plt.figure(figsize=(8, 5))
        plt.bar([i - width / 2 for i in x], aws_vals, width, label="AWS")
        plt.bar([i + width / 2 for i in x], gcp_vals, width, label="GCP")

        plt.xticks(x, datasets, rotation=20)
        plt.ylabel(title)
        plt.title(title)
        plt.legend()

        plt.tight_layout()
        save_path = os.path.join(PLOT_DIR, f"{metric}.png")
        plt.savefig(save_path)
        plt.close()

        print(f"Saved: {save_path}")


if __name__ == "__main__":
    plot_all()