## Prerequisites

Before running this project, ensure you have:

- **Python 3.14+** - [Download](https://www.python.org/downloads/)
- **uv package manager** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url> python-test
cd python-test
```

### 2. Install Dependencies

The project uses `uv` as the package manager. Dependencies are automatically installed when you run the project:

```bash
# Option 1: Using make (recommended)
make run

# Option 2: Using uv directly
export PYTHONPATH=src:src/genpb && \
export PYTHONDONTWRITEBYTECODE=1 && \
uv run python src/app/main.py
```

The first time you run the project, `uv` will automatically:

- Install Python 3.14 (if not present)
- Install project dependencies (FastAPI, Uvicorn)
- Start the server

### 3. Access the API

Once running, the API will be available at:

```
http://localhost:8080/
```

API Documentation:

- **Interactive API Docs (Swagger UI):** <http://localhost:8080/docs>
- **Alternative API Docs (ReDoc):** <http://localhost:8080/redoc>
