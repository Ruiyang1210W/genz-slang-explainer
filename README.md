# Gen Z Slang Explainer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)

A fine-tuned LLM that explains Gen Z internet slang with definitions and examples. Built with **TinyLlama-1.1B** and **LoRA** fine-tuning on 1,779 slang terms.

## Overview

This project fine-tunes **TinyLlama-1.1B** using **LoRA (Low-Rank Adaptation)** on a dataset of 1,779 Gen Z slang terms. The model learns to generate accurate definitions and usage examples for internet slang. This project is seperated from my personal project: https://github.com/memeorigin/memeorigin 

## Features

- **Fine-tuned LLM**: TinyLlama-1.1B specialized for Gen Z slang explanation
- **Efficient Training**: LoRA adapters (~8MB) instead of full model retraining
- **FastAPI Service**: RESTful API for real-time slang explanations
- **RAG-Enhanced**: Retrieval-augmented generation with fallback to knowledge base
- **Interactive Comparison**: Compare base model vs fine-tuned model performance

## Tech Stack

- **Model**: TinyLlama-1.1B-Chat-v1.0
- **Fine-tuning**: LoRA (Parameter-Efficient Fine-Tuning)
- **Framework**: Transformers, PEFT, PyTorch
- **API**: FastAPI
- **Training**: Google Colab (T4 GPU)

## Project Structure

```
genz-slang-explainer/
├── training/                           # Model training
│   ├── Train_TinyLlama_GenZ_Slang.ipynb
│   └── genz_slang_training_v2.jsonl   # 1,779 training examples
├── api/                                # FastAPI service
│   ├── src/
│   │   ├── router.py                  # API endpoints
│   │   ├── inference.py               # Model inference
│   │   ├── retrieval.py               # RAG retrieval
│   │   └── postprocess.py             # Output parsing
│   ├── data/
│   │   └── slang_pairs.jsonl          # Knowledge base
│   └── pyproject.toml
├── models/
│   └── adapters/
│       └── tinyllama-lora@2025-10-29/ # Fine-tuned LoRA weights
├── demo/                               # Comparison scripts
│   ├── compare_base_vs_finetuned.py
│   └── demo_comparison.py
└── README.md
```

## Quick Start

### Option 1: Docker

```bash
# Clone the repository
git clone https://github.com/Ruiyang1210W/genz-slang-explainer.git
cd genz-slang-explainer

# Run with Docker Compose
docker-compose up
```

**Note:** First startup downloads TinyLlama model (~2.2GB) and takes 5-15 minutes. The model is cached to `~/.cache/huggingface` on your host, so subsequent runs start in ~30 seconds.

The API will be available at `http://localhost:8000`

### Option 2: Local Installation

**Prerequisites:**
- Python 3.10+
- 8GB+ RAM (for CPU inference)
- GPU recommended for training

```bash
# Clone the repository
git clone https://github.com/Ruiyang1210W/genz-slang-explainer.git
cd genz-slang-explainer

# Install dependencies
pip install -r requirements.txt

# Or install with dev dependencies for testing
pip install -r requirements-dev.txt
```

## Usage

### 1. Run the FastAPI Service

```bash
cd api
uvicorn src.router:app --host 0.0.0.0 --port 8000 --reload
```

Then visit `http://localhost:8000/docs` for the interactive API documentation.

**Try these tested terms:** u, stan, jk, sis, lmao, ngl, irl, idc, asap, ez, idk, nsfw, ootd, plz, ppl, sry, ty

### 2. Compare Base vs Fine-Tuned Model

```bash
python demo/compare_base_vs_finetuned.py
```

This interactive script lets you test any slang term and see how the base model compares to the fine-tuned version (With Lora)./

demo video: https://youtu.be/lkPemg-hO2U

### 3. Run Demo Script
Test : Model vs Dataset
```bash
python demo/demo_comparison.py
```

## Training

The model was trained using Google Colab with the following configuration:

- **Epochs**: 3
- **Batch Size**: 4 (with gradient accumulation)
- **Learning Rate**: 2e-4
- **LoRA Rank**: 16
- **Training Time**: ~30-60 minutes on T4 GPU
- **Dataset**: 1,779 slang terms with definitions and examples

To retrain the model:

1. Upload `training/genz_slang_training_v2.jsonl` to Google Colab
2. Open `training/Train_TinyLlama_GenZ_Slang.ipynb`
3. Run all cells
4. Download the generated LoRA adapters
5. Replace files in `models/adapters/`

## API Endpoints

### Testing the API (Interactive Documentation) ⭐

**The easiest way to test the API** is through the built-in interactive documentation:

1. Start the API server (see Usage section above)
2. Open your browser to: **http://localhost:8000/docs**
3. Click on **POST /v1/explain**
4. Click **"Try it out"**
5. Enter a slang term in the request body:
   ```json
   {
     "term": "jk"
   }
   ```
6. Click **"Execute"**

**Try these tested terms:** `u`, `stan`, `jk`, `sis`, `lmao`, `ngl`, `irl`, `idc`, `asap`, `ez`, `idk`, `nsfw`, `ootd`, `plz`, `ppl`, `sry`, `ty`

---

### `POST /v1/explain`

Explain a slang term with AI-generated definition and example.

**Example Response:**
```json
{
  "term": "jk",
  "definition": "Just kidding",
  "example": "I'm not going to tell you, but jk!",
  "source": "lora"
}
```

**Response Fields:**
- `term` - The normalized slang term
- `definition` - AI-generated definition
- `example` - AI-generated usage example
- `source` - Where the data came from (`lora`, `lora+baseline`, or `lora_raw`)

---

### Using cURL (Advanced)

For command-line testing:

```bash
# Basic usage
curl -X POST "http://localhost:8000/v1/explain" \
  -H "Content-Type: application/json" \
  -d '{"term": "jk"}'

# More examples
curl -X POST "http://localhost:8000/v1/explain" \
  -H "Content-Type: application/json" \
  -d '{"term": "ngl"}'

curl -X POST "http://localhost:8000/v1/explain" \
  -H "Content-Type: application/json" \
  -d '{"term": "lmao"}'
```

---

### Other Endpoints

- **`GET /`** - Service information
- **`GET /health`** - Health check endpoint
- **`GET /docs`** - Interactive API documentation (Swagger UI) ⭐
- **`GET /redoc`** - Alternative API documentation (ReDoc)

## How It Works

1. **Retrieval**: First checks knowledge base for exact match
2. **Generation**: If no match, uses fine-tuned LLM to generate explanation
3. **Post-processing**: Parses output into structured definition + example
4. **Fallback**: Returns retrieval result if generation fails

## Training Data Format

Each training example follows this format:

```
Task: Explain the internet slang.
Term: w

Definition: Shorthand for win or winning
Example: Got the job today, big W!
```

## Testing

Run the test suite to ensure everything works correctly:

```bash
# Navigate to API directory
cd api

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_router.py -v

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

**Test Coverage:**
- API endpoint tests (router)
- Model inference tests
- Retrieval system tests
- Output parsing tests

## Model Performance

The fine-tuned model demonstrates:
- **Accurate Definitions**: Generates contextually appropriate explanations
- **Proper Format**: Consistently follows definition + example structure
- **Generalization**: Can explain slang terms not in training data
- **Comparison**: Significantly outperforms base TinyLlama on slang understanding

### Deployment

**Docker Deployment:**
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs (useful for monitoring first-time model download)
docker-compose logs -f

# Stop the service
docker-compose down
```

**Performance Notes:**
- First run: Downloads TinyLlama-1.1B (~2.2GB) - takes 5-15 minutes
- Subsequent runs: Uses cached model from `~/.cache/huggingface` - starts in ~30 seconds
- The cache persists on your host machine, speeding up container restarts

**Manual Deployment:**
```bash
cd api
uvicorn src.router:app --host 0.0.0.0 --port 8000 --workers 4
```

## Key Features Showcase

### 🚀 Production-Ready
- RESTful API with FastAPI
- Comprehensive error handling and logging
- Health checks and monitoring
- Docker containerization

### 🧪 Well-Tested
- Unit tests for all components
- >80% code coverage
- CI/CD pipeline with GitHub Actions
- Automated linting and formatting

### 🎯 Smart Architecture
- RAG (Retrieval-Augmented Generation) with fallback
- Efficient LoRA adapters (~8MB vs full model retrain)
- CPU-friendly inference
- Structured output parsing

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see LICENSE file for details


AI Assistance Diclosure: This project used Claude.ai to help with debug and polish README.md
