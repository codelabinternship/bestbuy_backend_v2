# 🛍️ BestBuy Backend API

This is the Django REST Framework-based API for the BestBuy e-commerce platform.

## 🚀 Features

- User Registration & JWT Login
- Product & Category Management
- Reviews, Orders, Bot Configurations
- Activity Logs & SMS Campaigns
- Swagger / ReDoc API docs

## 🧩 API Endpoints

### 🔐 Authentication
- `POST /api/auth/register/` — Register a new user
- `POST /api/auth/login/` — Login and get access token
- `POST /api/token/` — Obtain JWT token

### 📦 Core APIs
- `GET/POST /products/` — List & create products
- `GET/POST /categories/` — Manage categories
- `GET/POST /users/` — User list and management
- `GET/POST /bot-configs/` — Telegram bot configuration
- `GET/POST /reviews/` — Product reviews
- `GET/POST /orderitem/` — Order item records
- `GET/POST /user-activity-logs/` — Track user actions
- `GET/POST /sms-campaigns/` — SMS campaign management
- `GET /rolechoices/` — Role choices (enum)

### 📚 API Docs
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## ⚙️ Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/bestbuy-backend.git
cd bestbuy-backend

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
# bestbuy_backend_v2
