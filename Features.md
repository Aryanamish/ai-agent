# Full-Stack AI Chat Assignment

## Overview

Build a simplified AI-powered customer support chat application using Django (backend) and React/Next.js (frontend). This assignment evaluates your ability to work with our tech stack and design patterns.

**Deadline:** 1 week from assignment date

**Note:** You can either deploy your application to a cloud platform (Heroku, Railway, Vercel, AWS, etc.) with a live URL, or provide clear instructions for running it locally with a live demo session.

## Project Requirements

### Backend (Django + Django REST Framework)

#### 1. Project Setup

-   Initialize a new Django project from scratch
-   Set up Django REST Framework
-   Configure local MySQL/PostgreSQL database
-   Implement proper environment variable management (use `django-environ` or similar)
-   Create a `requirements.txt` with all dependencies

#### 2. Database Models

Design and implement appropriate database models to support:

-   Multi-tenant organization management
-   Conversation/chat session tracking
-   Message history storage
-   User identification and session management
-   Conversation metadata

Your schema should support the functional requirements below and follow Django best practices.

#### 3. REST API Endpoints

Design and implement RESTful API endpoints to support:

**Minimum Required Endpoints:**

-   Create new conversation
-   Get conversation details
-   List all conversations (with filtering/search)
-   Send message and receive AI response
-   Get conversation message history
-   Update conversation status
-   Export conversation data

Follow REST best practices and include proper error handling, validation, and HTTP status codes.

#### 4. AI Agent Integration

Implement a simple agentic AI system:

-   Create an AI agent service/handler that processes user messages
-   Integrate with OpenAI API (GPT-4 or GPT-3.5-turbo)
-   Implement a **simple agent pattern** that:
    -   Analyzes user intent
    -   Maintains conversation context
    -   Provides relevant responses
    -   Can handle at least 2-3 different intents (e.g., "greeting", "product_inquiry", "support_request")

**Example Agent Flow:**

```python
class SupportAgent:
    def process_message(self, conversation, user_message):
        # 1. Analyze intent
        # 2. Retrieve conversation history
        # 3. Generate contextual response using LLM
        # 4. Save and return response
```

#### 5. Code Quality Requirements

-   Use Django class-based views or ViewSets
-   Implement proper serializers for all models
-   Add input validation and error handling
-   Follow Django best practices and PEP 8 style guide

### Frontend (React or Next.js)

#### 1. Project Setup

-   Initialize React (Create React App) or Next.js project
-   Set up proper folder structure (`components/`, `services/`, `hooks/`)
-   Configure environment variables for API endpoint

#### 2. Chat Interface Components

Build a functional chat UI with:

**Components Required:**

-   `ChatWidget` - Main container component
-   `MessageList` - Display conversation messages
-   `MessageInput` - User input field with send button
-   `Message` - Individual message component (user vs assistant styling)
-   `TypingIndicator` - Shows when AI is responding

#### 3. Features

**Chat Interface:**

-   Start new conversation on load
-   Send messages and receive AI responses in real-time
-   Display conversation history within current session
-   Show loading state while waiting for AI response
-   Handle errors gracefully with user-friendly messages
-   Responsive design (works on mobile and desktop)

**Conversation Management:**

-   View all past conversations (conversation history page)
-   Search and filter conversations by date, status, or content
-   View complete message history for any conversation

**QA/Admin Features:**

-   Admin dashboard to manage and review conversations
-   Ability to view, search, and filter all organization conversations
-   Export conversation data (JSON/CSV format)

#### 4. Code Quality Requirements

-   Use functional components with React Hooks
-   Implement proper state management (useState, useEffect, useContext)
-   Create reusable components
-   Use TypeScript (bonus points) or PropTypes for type checking
-   Follow React best practices and clean code principles
-   Add basic CSS/styled-components for a polished UI

### Database Setup

#### Requirements

-   Use MySQL 8.0+ or PostgreSQL 14+
-   Create database locally
-   Provide clear setup instructions in README
-   Include database migrations in the project

#### Setup Instructions to Provide

```bash
# Example for MySQL
mysql -u root -p
CREATE DATABASE ai_chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chat_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ai_chat_db.* TO 'chat_user'@'localhost';
```

### Project Structure

```
ai-chat-assignment/
├── backend/                    # Django project
│   ├── ai_chat/               # Main Django app
│   ├── conversations/         # Conversations app
│   ├── ai_agent/              # AI agent service
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/                   # React/Next.js project
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.js
│   ├── package.json
│   ├── .env.example
│   └── README.md
└── README.md                   # Main project README
```

## Submission Guidelines

### 1. GitHub Repository

-   Create a GitHub repository (public or private)
-   Initialize with a comprehensive README.md including:
    -   **Application Access** (Live URL or local setup instructions at the top)
    -   Project description
    -   Setup instructions (both backend and frontend)
    -   Environment variables needed
    -   How to run locally (detailed step-by-step)
    -   API documentation (endpoints, request/response examples)
    -   Database schema design and ERD
    -   Design decisions and architecture notes
    -   Known limitations or future improvements
    -   Deployment instructions (if deployed)

### 2. Pull Request

-   Create a `develop` branch from `main`
-   Do all your work in feature branches
-   Create a Pull Request from `develop` to `main` when complete
-   PR should include:
    -   **Application Access Info** (live URL or local demo instructions at the top)
    -   Clear description of implemented features
    -   Screenshots/GIFs of the working application
    -   Database schema/ERD diagram
    -   Any assumptions made and design decisions

### 3. Code Quality Checklist

Before submitting, ensure:

-   [ ] Code follows PEP 8 (backend) and ESLint rules (frontend)
-   [ ] No hardcoded credentials or API keys
-   [ ] `.env.example` files provided with all required variables
-   [ ] Database migrations are included and documented
-   [ ] README includes clear setup instructions
-   [ ] Application runs successfully on fresh clone
-   [ ] **Application is accessible (deployed OR ready for local demo)**
-   [ ] Database schema/ERD is documented
-   [ ] Git history is clean with meaningful commit messages

## Evaluation Criteria

### Technical Implementation (40%)

-   Django project structure and best practices
-   Database design and relationships
-   REST API design and implementation
-   AI agent implementation and logic
-   Frontend component architecture
-   Error handling and validation

### Code Quality (25%)

-   Clean, readable, and maintainable code
-   Proper use of design patterns
-   Code organization and structure
-   Type safety (TypeScript/PropTypes)
-   Following framework conventions

### Features & Functionality (20%)

-   All required features implemented
-   Conversation history and search
-   QA/Admin dashboard functionality
-   Data export capabilities

### Documentation (10%)

-   Clear README with setup instructions
-   API documentation
-   Database schema/ERD
-   Architecture decisions explained
-   Application accessibility (deployed or local demo ready)

### UI/UX (5%)

-   Functional and intuitive interface
-   Responsive design
-   Loading states and error handling
-   Visual polish

## Required Technologies

### Backend

-   Python 3.10+
-   Django 4.2+
-   Django REST Framework
-   MySQL 8.0+ or PostgreSQL 14+
-   OpenAI API (GPT-3.5-turbo minimum)

### Frontend

-   React 18+ or Next.js 14+
-   Modern JavaScript (ES6+) or TypeScript
-   CSS-in-JS, Tailwind, or Material-UI (your choice)

### Tools

-   Git & GitHub
-   Virtual environment (venv or virtualenv)
-   npm or yarn

## Environment Variables Required

### Backend (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost:3306/ai_chat_db
OPENAI_API_KEY=your-openai-api-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000/api
# or for Next.js
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Bonus Points (Optional)

-   Deploy application to cloud platform with live URL
-   Implement WebSocket for real-time chat updates
-   Advanced search capabilities (full-text search, semantic search)
-   Implement rate limiting on API endpoints
-   Add Docker configuration for easy setup
-   Add authentication (simple JWT auth)
-   Implement CI/CD pipeline (GitHub Actions)
-   Multi-language support (i18n)
-   Conversation sentiment analysis

## Submission

Submit your assignment by providing:

1. **GitHub Repository Access**

    - Create a GitHub repository (public or private)
    - If private, add reviewers as collaborators
    - Submit a Pull Request from `develop` to `main`
    - Ensure PR is ready for review

2. **Application Access** (Choose one or both)

    - **Option A:** Live Website URL - Deploy to any cloud platform (Heroku, Railway, Vercel, AWS, etc.)
    - **Option B:** Local Demo - Provide clear instructions for running locally and schedule a live demo session
    - Ensure both frontend and backend are fully functional

3. **Demo Video** (Optional but recommended)
    - 5-10 minute Loom/video walkthrough
    - Demonstrate all features including chat, history, and QA dashboard
    - Explain your design decisions

---
