# Bench360 – Local LLM Deployment Benchmark Suite

> ⚡ System Performance. 🔋 Energy Consumption. 🎯 Task Quality. One Benchmark.

**Bench360** is a modular benchmarking framework for evaluating **local LLM deployments** across backends, quantization formats, model architectures, and deployment scenarios.

It enables researchers and practitioners to analyze **latency, throughput, quality, efficiency, and cost** in real-world tasks like summarization, QA, and SQL generation—under both consumer and data center conditions.

![Bench360°](benchmark/docs/bench360.jpg)

---

## 🔍 Why Bench360?

When deploying LLMs locally, trade-offs between **model size**, **quantization**, and **inference engine** can drastically impact performance and feasibility. Bench360 helps answer the real-world questions that arise when resources are limited and requirements are strict:

### ❓ Should you run a **7B model in FP16**, a **13B in INT8**, or a **33B in INT4**?

Bench360 benchmarks across multiple quantization formats and model sizes—on the **same hardware** and **same tasks**—to help you understand the trade-offs between **quality**, **latency**, and **memory footprint**. Detailed telemetry (latency, throughput, energy/token) let you choose the sweet spot for your setup.

---

### ❓ Is **INT4 quantization good enough** for SQL generation or question answering?

Bench360 evaluates functional task quality—not just perplexity. For Text-to-SQL, it reports **execution accuracy** and **AST match**; for QA and summarization, it computes **F1**, **EM**, and **ROUGE**. You’ll see whether aggressive quantization introduces failure cases *that actually matter*.

---

### ❓  Which inference backend delivers the best performance for my use case?

Bench360 includes a workload controller that simulates different deployment scenarios:  
- 🧵 Single-stream  
- 📦 Offline batch  
- 🌐 Multi-user server (with Poisson query arrivals)

Engines like **vLLM**, **TGI**, **SGLang**, and **LMDeploy** can be tested under identical conditions.

---

## ⚙️ Features

| Category            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Tasks**           | Summarization, Question Answering (QA), Text-to-SQL                         |
| **Scenarios**       | `single`, `batch`, and `server` (Poisson arrival multi-threads)             |
| **Metrics**         | Latency (ATL/GL), Throughput (TPS, SPS), GPU/CPU util, Energy, Quality (F1, ROUGE, AST) |
| **Backends**        | vLLM, TGI, SGLang, LMDeploy                                                 |
| **Quantization**    | Support for FP16, INT8, INT4 (GPTQ, AWQ, GGUF)                              |
| **Cost Estimation** | Energy and amortized GPU cost per request                                   |
| **Output Format**   | CSV (run-level + per-sample details), logs, and visual plots ready          |

---

## 🧱 Installation

### Requirements

- OS: Ubuntu Linux
- NVIDIA GPU with NVML support
- CUDA 12.x
- Python 3.8+
- Docker

### Setup

Clone the repository:

```bash
git clone https://github.com/slinusc/fast_llm_inference.git
cd fast_llm_inference
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> System dependencies:
```bash
sudo apt update && sudo apt install -y \
  libssl-dev libcurl4 build-essential libllvm15 \
  nvidia-container-toolkit && \
  sudo nvidia-ctk runtime configure --runtime=docker && \
  sudo systemctl restart docker
```

Pull all official backend docker images:

```bash
docker pull lmsysorg/sglang:latest
docker pull openmmlab/lmdeploy:latest
docker pull vllm/vllm-openai:latest
docker pull ghcr.io/huggingface/text-generation-inference:latest
````

Export your Huggingface Token:
```bash
export HF_TOKEN=<your HF token>
````

---

## 🚀 Usage

### ✅ Single Run

```yaml
# config.yaml
backend: tgi
hf_model: mistralai/Mistral-7B-Instruct-v0.3
model_name: Mistral-7B
task: qa
scenario: single
samples: 256
```

---

### 🔁 Multi-run Sweep

Use **lists** to define a Cartesian product:

```yaml
backend: [tgi, vllm]
hf_model:
  - mistralai/Mistral-7B-Instruct-v0.3
  - Qwen/Qwen2.5-7B-Instruct
task: [summarization, sql, qa]
scenario: [single, batch, server]

samples: 256
batch_size: [16, 64]
run_time: 300
concurrent_users: [8, 16, 32]
requests_per_user_per_min: 12
```

```bash
python launch_benchmark.py config.yaml
```

---

## 📦 Output

Each experiment generates:

```
results_<timestamp>/
├── run_report/          # One CSV per experiment (summary)
├── details/             # Per-query logs
├── readings/            # GPU/CPU/power metrics
└── failed_runs.log      # List of failed configs
```

Each filename includes:

* backend
* model
* task
* scenario
* parameters (e.g. batch size, concurrent users)
* config hash

This enables reproducible comparisons & tracking.

---

## 🗂 Project Structure

```
fast_llm_inference/
├── benchmark/
│   ├── benchmark.py               # Main benchmarking logic
│   ├── inference_engine_client.py # Backend launcher
│   ├── tasks/                     # Task-specific eval logic
│   ├── backends/                  # Inference wrapper modules
├── launch_benchmark.py            # CLI entry point
├── utils_multi.py                 # Multi-run config handling
├── config.yaml                    # Example config file
└── requirements.txt
```

---

## 🧪 Contributing

Pull requests, bug reports, and ideas are welcome!
Fork the repo, create a feature branch, and submit your PR.

---

## 📄 License

Bench360 is released under the [MIT License](LICENSE).
