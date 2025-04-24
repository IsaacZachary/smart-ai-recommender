# 🖥️ AI Terminal Recommender System (AI-TRS)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAPI 3.0](https://img.shields.io/badge/OpenAPI-3.0-success.svg)](https://swagger.io/specification/)
[![Build Status](https://github.com/IsaacZachary/smart-ai-recommender/actions/workflows/ci.yml/badge.svg)](https://github.com/IsaacZachary/smart-ai-recommender/actions)
[![Codecov](https://img.shields.io/codecov/c/github/IsaacZachary/smart-ai-recommender)](https://codecov.io/gh/IsaacZachary/smart-ai-recommender)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/isaaczachary/ai-trs)
[![M-Pesa](https://img.shields.io/badge/payment-M--Pesa-orange.svg)](https://developer.safaricom.co.ke/)

> Terminal-style AI product recommender with natural language processing and M-Pesa tipping

---

## 🚀 Project Overview

AI-TRS is an open-source, AI-powered product recommendation platform with a command-line interface (CLI) aesthetic. It allows users to input product-related queries in any language, including slang or local dialects, and returns intelligent, contextual product suggestions from legitimate e-commerce sources. The system does not process purchases—it instead embeds product links and details. M-Pesa is integrated purely as a tipping feature for users who wish to appreciate the free service.

**Key Innovations:**
- 🤖 **Language-Agnostic Processing**: Understands queries in any language/dialect
- 🔒 **Zero-Auth Architecture**: Completely anonymous usage
- 💳 **Ethical Monetization**: Voluntary tipping only (no forced payments)

### 🎯 Core Objectives
- Provide frictionless product discovery with zero-auth requirements
- Deliver developer-friendly CLI aesthetic with modern UX principles
- Maintain privacy-first approach with no tracking
- Build open ecosystem with API-first design

---

## 🌐 System Architecture

```mermaid
graph TD
    A[React Frontend] -->|HTTPS| B(FastAPI Backend)
    B --> C{AI Processing}
    C --> D[OpenAI/Llama3]
    C --> E[Product APIs]
    B --> F[M-Pesa API]
    E --> G[Jumia/Amazon]
    F --> H[Safaricom Daraja]
```

---

## 🛠️ Tech Stack

### Core Components
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React 18, TypeScript, TailwindCSS | CLI-style UI |
| **Backend** | FastAPI (Python 3.10+) | API services |
| **AI Engine** | OpenAI GPT-4-turbo + Llama 3 fallback | NLP processing |
| **Payments** | Safaricom Daraja API | M-Pesa tipping |
| **Caching** | Redis | Session storage |

### Key Libraries
| Category | Libraries |
|----------|-----------|
| **Python** | FastAPI, httpx, langdetect, python-mpesa |
| **Frontend** | Framer Motion, Axios, react-markdown |
| **DevOps** | Docker, Prometheus, GitHub Actions |

### 🖥️ Frontend Specifications
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS with custom animations
- **Fonts**: JetBrains Mono (monospace terminal style)
- **Themes**: Dark (#0D0D0D) and Light (#F9FAFB) modes
- **Key Features**: Typing animations, command history

---

## 📂 Project Structure

```
ai-terminal-recommender/
├── app/                          # FastAPI application
│   ├── core/                     # Config and utilities
│   ├── models/                   # Pydantic schemas
│   ├── routes/                   # API endpoints
│   └── services/                 # Business logic
├── frontend/                     # React application
│   ├── public/                   # Static assets
│   └── src/                      # Source code
├── tests/                        # Pytest suite
├── docker/                       # Docker configs
├── .github/workflows/            # CI/CD pipelines
└── README.md                     # This file
```

---

## 🚀 Deployment

### Prerequisites
- Python 3.10+
- Node.js 18+
- Redis 6.2+
- Docker 20.10+

### Quick Start
```bash
# Clone repository
git clone https://github.com/IsaacZachary/smart-ai-recommender.git
cd smart-ai-recommender

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
npm run dev

# Run with Redis
docker-compose up -d
```

### Environment Variables
```ini
# Environment
ENVIRONMENT=development

# AI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview
LOCAL_LLM_ENABLED=false

# M-Pesa
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_ENV=sandbox

# Redis
REDIS_URL=redis://localhost:6379

# Product APIs
JUMIA_API_KEY=your_jumia_key
AMAZON_API_KEY=your_amazon_key

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

### Required Dependencies

#### Backend Dependencies
```ini
# Core
fastapi==0.109.2
uvicorn==0.27.1
pydantic==2.6.1
pydantic-settings==2.1.0

# HTTP and Database
httpx==0.26.0
redis==5.0.1
python-dotenv==1.0.1

# AI and NLP
openai==1.12.0
langdetect==1.0.9
beautifulsoup4==4.12.3

# M-Pesa Integration
python-mpesa==0.1.10

# Testing
pytest==8.0.0
pytest-asyncio==0.23.5
pytest-cov==4.1.0

# Monitoring and Server
sentry-sdk==1.39.1
gunicorn==21.2.0
python-multipart==0.0.9
locust==2.24.0
```

#### Frontend Dependencies
```json
{
  "dependencies": {
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-slot": "^1.0.2",
    "axios": "^1.6.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-react": "^0.323.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwind-merge": "^2.2.1",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

---

## 📡 API Documentation

### Interactive Docs
Access Swagger UI at `http://localhost:8000/docs` or Redoc at `http://localhost:8000/redoc`

### Key Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/recommend` | POST | Main recommendation endpoint |
| `/v1/clarify` | POST | Follow-up question handler |
| `/v1/tip/initiate` | POST | M-Pesa payment flow |
| `/v1/tip/status/{id}` | GET | Check transaction status |
| `/v1/tip/history/{phone}` | GET | View transaction history |

---

## 🔐 Security Considerations

1. **Data Protection**
   - End-to-end HTTPS encryption
   - No persistent user data storage

2. **Payment Security**
   - M-Pesa API signature verification
   - IP whitelisting for callbacks

3. **API Security**
   - Rate limiting (100 requests/min)
   - CORS restricted to frontend domains

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact

**Project Maintainer**  
Isaac Zachary - [izach.netlify.app](https://izach.netlify.app/)

**Project Link**  
[https://github.com/IsaacZachary/smart-ai-recommender](https://github.com/IsaacZachary/smart-ai-recommender)
