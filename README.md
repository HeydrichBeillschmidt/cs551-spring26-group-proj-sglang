# 🍃 Eco-Cloud: Multi-Cloud LLM Serving Benchmark

Eco-Cloud is a cloud-native system for deploying and benchmarking LLM inference across multiple cloud platforms, with a focus on performance and energy efficiency.

## What This Project Does

This project provides a reproducible pipeline to:

- Deploy LLM inference servers on Kubernetes (AWS EKS, GCP GKE)
- Generate controlled workloads for benchmarking
- Measure both performance (latency, throughput) and GPU power
- Compute energy efficiency metrics (energy per request / token)

The goal is to compare cloud platforms under identical conditions.

## System Architecture

The system is structured as an end-to-end measurement pipeline:
```

Client (benchmark)
│
▼
HTTP Requests
│
▼
SGLang Server (GPU)
├──► Performance Metrics (latency, throughput)
└──► DCGM Exporter (GPU power)
│
▼
Energy Computation

```

Each cloud environment includes:
- 1 GPU node (NVIDIA T4)
- Kubernetes-based deployment
- SGLang inference server
- DCGM-based power monitoring

## Repository Structure
```
.
├── sglang.yaml          # SkyPilot job configuration (deployment + serving)
├── scripts/             # Benchmarking and experiment scripts
├── local_datasets       # Datasets for experiments
├── results/             # Experiment outputs and plots
└── README.md

```

## Setup

### Prerequisites

- AWS or GCP account
- Kubernetes cluster (EKS or GKE)
- GPU node (T4 recommended)
- SkyPilot installed

### Deploy
```

sky launch -c <cluster-name> sglang.yaml

```

This will:
- Provision GPU resources
- Launch the SGLang server

## Running Experiments

1. Start the serving endpoint
2. Run benchmark workload:
```

python scripts/run_benchmark_with_energy.sh

```

3. Collect:
- Latency / throughput logs
- GPU power traces (DCGM)

> For full setup details and reproducibility guides, refer to:
>
> - **AWS Deployment Guide**  
>   https://docs.google.com/document/d/15jY7aPwVrCPzKFrQLaCZc2kiD11eEUarCw73KnBQ7CA/edit
>
> - **GCP Deployment Guide**  
>   https://docs.google.com/document/d/1dJAfKCjvCSUX1EEipI-17K0_qDSe8l3zHilxQP4505s/edit

## Metrics Collected

- Throughput (tokens/sec)
- Latency (E2E, P99)
- GPU power over time
- Energy per request / token

## Key Design Choices

- Single-GPU setup for fair comparison
- Identical configuration across clouds
- Separation of performance and energy measurement pipelines
- Explicit handling of idle power

## Results (Summary)

- AWS shows higher throughput and lower latency
- GCP shows higher tail latency
- Faster execution leads to lower energy per request on AWS

> **Detailed results and visualizations:**  
> See the plots in the repository for full comparisons and analysis:  
> https://github.com/HeydrichBeillschmidt/cs551-spring26-group-proj-sglang/tree/main/plots

## Team

Alina Li, Daeun Oh, Yaoxu Song, Roohee Urs













