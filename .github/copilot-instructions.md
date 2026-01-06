# AI Coding Agent Instructions

## Project Context
This is a full-stack application with a **Django (Python)** backend and a **React (TypeScript)** frontend.
- **Root**: `z:\alhena`
- **Backend**: `backend/` (Django 6.0+)
- **Frontend**: `frontend/` (Vite + React 19 + Tailwind CSS 4)

## Architecture & Structure
- **Monorepo-style**: Backend and frontend are sibling directories.
- **Backend**: Standard Django project structure. `backend/aichatbot` is the config folder.
  - *Note*: This is a fresh project. You may need to create initial apps (e.g., `api`, `chat`) depending on requirements.
- **Frontend**: Vite project with shadcn/ui.
  - Components: `frontend/src/components` (shadcn in `ui/`).
  - Utils: `frontend/src/lib/utils.ts` (`cn` helper).
  - Styles: Tailwind CSS v4 managed via `@tailwindcss/vite` plugin.

## Technical Stack & Conventions

### Backend (Django)
- **Package Manager**: `uv` (faster pip alternative).
  - Install/Sync: `uv sync`
  - Add packages: `uv add <package>` (e.g., `django-rest-framework`, `django-cors-headers`)
  - Run commands: `uv run manage.py <command>`
- **Database**: Default SQLite (`db.sqlite3`). README suggests switching to MySQL/Postgres for production.
- **API**: Intended to be Django REST Framework (DRF).
- **Environment**: Use `django-environ` for settings management (needs setup).

### Frontend (React)
- **Package Manager**: `pnpm`.
  - Install: `pnpm install`
  - Dev Server: `pnpm dev`
- **Styling**: Tailwind CSS v4.
  - Config: Zero-config approach (CSS-first).
- **Components**: Functional components with TypeScript interfaces.
- **Imports**: Use `@/` alias for `src/` (e.g., `import { Button } from "@/components/ui/button"`).

## Critical Workflows

### 1. Setup & Run
**Backend**:
```bash
cd backend
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

**Frontend**:
```bash
cd frontend
pnpm install
pnpm dev
```

### 2. Integration
- Frontend acts as a SPA consuming the Backend API.
- **CORS**: Backend MUST configure `django-cors-headers` to allow `localhost:5173`.
- **Proxy**: Alternatively, configure `server.proxy` in `frontend/vite.config.ts`.

## Development Guidelines
- **Modularity**: Keep backend logic in dedicated apps (e.g., `chat`, `users`) inside `backend/`.
- **Types**: Ensure explicit TypeScript interfaces for all API responses in frontend.
- **Validation**: Use Pydantic or DRF Serializers for data validation on backend.
- **UI Components**: Reuse shadcn components from `@/components/ui`. do not reinvent standard UI elements.
