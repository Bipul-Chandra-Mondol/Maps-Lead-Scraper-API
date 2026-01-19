# Maps-Lead-Scraper-API
Here is a clean, professional, production-ready **README.md** file for your GitHub repository:
**Maps Lead Scraper – Django REST API with Cookie-Based JWT Authentication**

You can copy-paste this into your repo as **README.md**.

---

# 🌍 Maps Lead Scraper API

### 🔐 Django REST API with Cookie-Based JWT Authentication (Access + Refresh Cookies)

This project is a **secure backend API** built using **Django REST Framework** with **SimpleJWT** using **HttpOnly Cookies** for authentication.

This architecture is the same used by production systems (banking, fintech, enterprise apps) because:

* Tokens are stored in **HttpOnly cookies** (XSS-protected)
* Frontend **never touches tokens**
* Refresh token creates new access token securely
* Cookies auto-send with every request
* Supports pure backend-driven authentication logic

---

# ⚙️ Features

### 🔐 Authentication System

* Email-based registration
* Login with HttpOnly cookie tokens
* Access + Refresh tokens stored securely in cookies
* Cookie-based refresh (`/token/refresh`)
* Protected API with custom authentication
* Logout with refresh token blacklist

### 🧰 Technologies

* Python
* Django / Django REST Framework
* SimpleJWT
* Cookie-based JWT strategy
* Postman-friendly API design

---

# 📁 Project Structure

```
maps-lead-scraper/
│── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── authentication.py
│   ├── urls.py
│── maps_lead_scraper/
│   ├── settings.py
│   ├── urls.py
│── venv/
│── manage.py
│── README.md
```

---

# 🚀 Installation Guide

## 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows:

```bash
venv\Scripts\activate
```

### Mac / Linux:

```bash
source venv/bin/activate
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have the file:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

---

## 3️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4️⃣ Run Server

```bash
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```

---

# 🔐 Authentication Endpoints

Base URL:

```
/api/auth/
```

### 🟢 1. Register (Email + Password + Confirm Password)

**POST** `/api/auth/register`

```json
{
  "email": "test@example.com",
  "password": "test1234",
  "confirm_password": "test1234"
}
```

---

### 🔵 2. Login (Sets Cookies)

**POST** `/api/auth/login`

Cookies set automatically:

* `access_token`
* `refresh_token`

---

### 🟣 3. Get Logged-in User

**GET** `/api/auth/me`

Response example:

```json
{
  "id": 1,
  "email": "test@example.com"
}
```

---

### 🟡 4. Refresh Access Token (Cookie-Based)

**POST** `/api/auth/token/refresh`

No body needed.

Cookies must include:

* `refresh_token`

Response:

```json
{
  "detail": "Access token refreshed successfully"
}
```

---

### 🔴 5. Logout

**POST** `/api/auth/logout`

Clears cookies + blacklists refresh token.

---

# 🔐 Authentication Flow Diagram

```
 ┌─────────────┐
 │   LOGIN     │
 └─────┬───────┘
       │
       ▼
 ┌────────────────────────┐
 │ access + refresh cookie│
 └─────────┬──────────────┘
           │
           ▼
 ┌────────────────────────┐
 │ Protected API request  │
 └─────────┬──────────────┘
           │
    Access token valid?
       ├── YES → Allow
       └── NO
             ▼
      /token/refresh
             │
    Refresh token valid?
       ├── YES → New access cookie
       └── NO → 401 Unauthorized
```

---

# 🛡️ Security Highlights

* HttpOnly cookies (JS cannot read tokens → prevents XSS)
* No localStorage/sessionStorage usage
* Refresh token rotation ready
* Token blacklist on logout
* Django custom user model (email only)
* Secure login flow

---

# 🧪 Postman Testing

### For cookies to work:

Enable:

✔ `Enable Cookie Jar`
✔ `Send Cookies Automatically`
✔ Use `POSTMAN` → Cookies (right side)

---

# 📌 Roadmap (Upcoming Features)

* Google OAuth Login
* CSRF Protection
* Device-based refresh token binding
* Brute force protection
* Lead scraping module (Google Maps, YellowPages, etc.)

---

# 🤝 Contributing

PRs welcome!
Submit issues, improvements, or new feature requests.

---

# 📄 License

MIT License — free to use & customize.
