# Stage 1: Build React Frontend
FROM node:24-alpine AS frontend-builder

WORKDIR /app/frontend

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files first for better caching
COPY frontend/package.json frontend/pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy frontend source code
COPY frontend/ ./

# Build the React app (outputs to ../backend/staticfiles)
# We'll build to a local dist first, then copy in final stage
RUN NODE_ENV=production pnpm build


# Stage 2: Python Backend
FROM python:3.12-slim AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy backend requirements and install dependencies
COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --no-dev --frozen || uv sync --no-dev

# Copy backend source code
COPY backend/ ./

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/backend/staticfiles ./staticfiles/

# Collect Django static files (admin, DRF, etc.)
RUN uv run python manage.py collectstatic --noinput

# Create directory for SQLite databases
RUN mkdir -p /app/db

# Expose port
EXPOSE 8000

# Run with gunicorn for production
# Install gunicorn if not already in dependencies
RUN uv add gunicorn

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start the production server
CMD ["uv", "run", "gunicorn", "aichatbot.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
