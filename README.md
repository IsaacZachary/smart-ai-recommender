# 📦 Smart AI Product Recommender with M-Pesa Integration

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourrepo/smart-ai-recommender/actions)
[![License](https://img.shields.io/github/license/yourrepo/smart-ai-recommender)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node.js-18.x-brightgreen)](https://nodejs.org/)
[![MySQL](https://img.shields.io/badge/database-MySQL-blue)](https://www.mysql.com/)

---

## 🚀 Overview

The **Smart AI Product Recommender** is a modular web application that harnesses the power of **AI** to deliver real-time product recommendations, tailored to user behavior. It is further enhanced with **M-Pesa STK Push** integration for seamless local payment processing.

The application follows a microservices architecture:
- 🧠 **Django (Python)**: Core AI logic, user and product management.
- 💳 **Express.js (Node.js)**: M-Pesa STK Push payments and asynchronous callback handling.

---

## 🛠️ Technologies Used

### Backend
- **Django** — AI logic, user authentication, admin dashboard
- **Express.js** — Payment endpoints and integration with Safaricom Daraja

### Database
- **MySQL 8+** — Centralized data storage for users, products, and transactions

### Key Libraries
- **Python**: `Django`, `requests`, `python-decouple`, `mysqlclient`
- **Node.js**: `express`, `axios`, `dotenv`, `uuid`

---

## 🗂️ Project Structure

```
smart-ai-recommender/
├── django_backend/
│   ├── ai_recommender/          # Django project files
│   ├── recommender_app/         # Business logic
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                     # Django environment variables
├── express_backend/
│   ├── controllers/
│   ├── routes/
│   ├── services/
│   ├── app.js
│   ├── package.json
│   └── .env                     # Express environment variables
├── README.md
└── .gitignore
```

---

## ✅ Core Features

- 🔍 AI-based product recommendation system
- 💸 M-Pesa STK Push payment gateway
- ⚡ Asynchronous payment verification and status tracking
- 📂 Persistent storage of transactions in MySQL
- 🛡️ CORS-enabled APIs for secure frontend communication
- 🧮 Django admin panel for analytics and control

---

## 🧰 Setup Instructions

### 1. Django Backend

```bash
cd django_backend
python -m venv env
source env/Scripts/activate  # Use `source env/bin/activate` on Unix
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Express Backend

```bash
cd express_backend
npm install
node app.js
```

### 3. Environment Variables
Create `.env` files in both Django and Express directories:

#### Django `.env`
```
DB_NAME=recommender
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
```

#### Express `.env`
```
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_PASSKEY=your_passkey
MPESA_SHORTCODE=174379
CALLBACK_URL=https://yourdomain.com/callback
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=recommender
```

---

## 🌐 API Endpoints

### `/pay` — Initiate STK Push
- **Method**: `POST`
- **Payload**:
```json
{
  "number": "254712345678",
  "amount": 150
}
```
- **Response**:
```json
{
  "message": "STK Push initiated successfully",
  "CheckoutRequestID": "ws_CO_123456789"
}
```

### `/callback` — Handle M-Pesa Confirmation
- **Method**: `POST`
- **Functionality**:
  - Extracts and saves `CallbackMetadata` to MySQL

---

## 🧮 Database Schema (MySQL)

```sql
CREATE TABLE payments (
    payment_id CHAR(36) PRIMARY KEY,
    number VARCHAR(15) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Security & Non-Functional Requirements

- 🌍 CORS configured for cross-origin access
- 📜 Logging of payment events and errors
- ✅ Status code handling (`200`, `400`, `500`)
- 💂 Secure credential handling via `.env`
- 📱 Input validation (number format, amount integrity)
- ⚙️ Scalable architecture for performance

---

## 🚀 Free Deployment Options

### Django Backend
- 🔹 [Render](https://render.com)
- 🔹 [Railway](https://railway.app)
- 🔹 [Replit](https://replit.com)

### Express Backend
- 🔸 [Render](https://render.com)
- 🔸 [Fly.io](https://fly.io)
- 🔸 [Glitch](https://glitch.com)

### MySQL Hosting
- 🗄️ [PlanetScale](https://planetscale.com)
- 🗄️ Google Cloud Free Tier
- 🗄️ ClearDB (Heroku)

---

## 🧪 Testing Tip

> Use `ngrok` to expose Express server during local development. M-Pesa requires a **public HTTPS URL** for callback functionality.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📬 Contact

Isaac Zachary — [izach.netlify.app](https://izach.netlify.app/)