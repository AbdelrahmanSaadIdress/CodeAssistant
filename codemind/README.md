# CodeMind — AI Code Intelligence Platform

> Full-stack AI code assistant with React frontend, Node.js proxy, and FastAPI/LangGraph backend.  
> **Portfolio-grade** — designed for top-tier engineering roles.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Vite, Zustand, Framer Motion, react-syntax-highlighter |
| **Proxy Server** | Node.js, Express, Multer, CORS |
| **Backend** | Python, FastAPI, LangGraph, OpenAI, HuggingFace |
| **AI Pipeline** | Multi-node LangGraph graph with intent classification, memory |

---

## Architecture

```
Browser (React + Vite)
        ↓  /api/*
Node.js Proxy (Express 4000)
        ↓  HTTP
FastAPI Backend (Uvicorn 8000)
        ↓  
LangGraph Pipeline → OpenAI
```

---

## Features

- **Intent Detection** — Classifies: generate, explain, debug, autocomplete, audit, refactor
- **Code Generation** — Creates production-ready Python code
- **Bug Detection** — Finds and fixes logical/syntax errors
- **Security Audit** — Detects injections, hard-coded secrets, unsafe patterns
- **Autocomplete** — Continues partial code snippets intelligently  
- **Code Refactor** — Adds docstrings, comments, improves structure
- **Project Upload** — `.rar` archive upload for codebase context
- **Syntax Highlighting** — GitHub-style code rendering with copy button
- **Session History** — Browse all prompts and responses

---

## Getting Started

### 1. FastAPI Backend

```bash
# Create .env in backend root — NEVER hardcode keys
cat > .env << EOF
APP_NAME="Code Assistant Chatbot"
APP_VERSION="0.1"
OPENAI_API_KEY=sk-...
GITHUB_AI_API_KEY=ghp_...
HF_TOKEN=hf_...
EOF

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Node.js Proxy Server

```bash
cd server
cp .env.example .env    # Edit if needed
npm install
npm run dev             # Starts on :4000
```

### 3. React Frontend

```bash
cd client
npm install
npm run dev             # Opens at http://localhost:5173
```

### One-command startup

```bash
npm install             # Install concurrently
npm run install:all     # Install server + client deps
npm run dev             # Start both simultaneously
```

---

## Project Structure

```
codemind/
├── server/                     # Node.js proxy
│   ├── index.js                
│   ├── .env.example            
│   └── package.json            
│
├── client/                     # React application
│   ├── src/
│   │   ├── App.jsx             # Root layout
│   │   ├── index.css           # Full design system (CSS tokens)
│   │   ├── store/
│   │   │   └── chatStore.js    # Zustand global state
│   │   ├── hooks/
│   │   │   └── useChat.js      # Chat logic hook
│   │   ├── utils/
│   │   │   └── api.js          # API layer
│   │   └── components/
│   │       ├── layout/         # Sidebar, Header
│   │       ├── chat/           # ChatPanel, Message, CodeBlock, etc.
│   │       ├── upload/         # UploadPanel
│   │       └── shared/         # Icons
│   └── package.json
│
└── README.md
```

---

## Backend Issues to Fix Before Production

These are issues in the FastAPI backend that **must** be fixed:

```python
# ❌ CRITICAL — Remove all hardcoded keys from node files
config = {"api_key": "ghp_..."}  # 8 files affected

# ✅ Fix: Inject from settings
from helpers import get_settings
settings = get_settings()
config = {"api_key": settings.GITHUB_AI_API_KEY}
```

```python
# ❌ BUG — call_llm_hf() has no return statement (silent None return)
data = parse_json_safe(response)
# return data  ← missing!

# ❌ BUG — generate_text() sends `prompt` as `messages` parameter
response = self.client.chat.completions.create(messages=prompt)
# Also has: chat_history.append(prompt) which mutates but is never used

# ❌ DESIGN — OpenAIProvider doesn't inherit BaseLLMProvider
# ❌ DESIGN — No try/except in any LangGraph node
# ❌ DESIGN — No tests (pytest)
```

---

## License

MIT © 2025
