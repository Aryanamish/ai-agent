# Backend API

This is the Django backend for the AI Chat application.

## Setup

For full project instructions (including frontend), see the [root README](../README.md).

### Quick Start

**Using `uv` (Recommended):**

```bash
# Install dependencies
uv sync

# Run migrations
uv run manage.py migrate

# Start server
uv run manage.py runserver
```

**Using `pip`:**

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Install & Run
pip install .
python manage.py migrate
python manage.py runserver
```
