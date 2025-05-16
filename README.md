# Secure Auth Demo – Final Version

This project is a complete demonstration of secure authentication and session management best practices using **Flask** (backend) and **Vue 3** (frontend). Originally developed as a hands-on lab for the **Advanced Information Security** course at UKIM, this finished version implements OWASP-compliant techniques and production-ready session flows.

---

## Features

- User registration with password strength validation
- Password hashing with bcrypt
- Account lockout after multiple failed login attempts
- Stateless session handling using JWT:
  - Access and refresh token issuance
  - Token refresh and expiration
  - Secure logout via cookie invalidation
- Secure cookies for storing JWTs (HTTP-only)
- HTTPS support with self-signed certificates
- CORS setup with credential handling

---

## Tech Stack

- **Backend:** Flask, Flask-JWT-Extended, SQLAlchemy, Flask-Bcrypt
- **Frontend:** Vue 3, Vite, Axios
- **Security:** JWT, Secure Cookies, HTTPS, Password Hashing
- **Config:** Environment variable loading with `python-dotenv`

---

## Getting Started

### 1. Clone the project

```bash
git clone https://github.com/your-username/secure-auth-demo-final.git
cd secure-auth-demo-final
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python app.py
```

### 3. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Access the App

- Frontend: [https://localhost:5173](https://localhost:5173)
- Backend API: [https://localhost:5000](https://localhost:5000)

> Note: Accept browser warnings for self-signed HTTPS certificates during local development.

---

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///auth.db
```

You can also refer to `.env.example` for the required variables.

---

## License

This project is developed for educational purposes and follows OWASP guidelines for secure session management.
