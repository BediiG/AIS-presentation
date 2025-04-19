# JWT Authentication App

This is a demonstration project showcasing JWT-based authentication using a **Flask** backend and a **Vue.js** frontend. The app provides user registration, login, and access to a protected success page, with token-based authentication and refresh token functionality.

---

## Features

1. **User Authentication**:
   - Register with a username and password.
   - Login to receive **Access** and **Refresh Tokens**.

2. **Token Management**:
   - **Access Token**: Used for accessing protected resources (short-lived).
   - **Refresh Token**: Used to obtain a new access token when the current one expires (long-lived).

3. **Protected Routes**:
   - Access the success page only with a valid access token.
   - Automatically refresh access tokens when expired.

4. **Informative Success Page**:
   - Displays decoded token details:
     - Issued At 
     - Expiration Time
     - Remaining Time
     - Subject/User ID

5. **Token Refresh Flow**:
   - Automatically refreshes expired access tokens using the refresh token.

---

## Tech Stack

### Backend
- **Flask**
- **Flask-JWT-Extended**
- **Flask-SQLAlchemy**
- **Flask-CORS**
- **Bcrypt** for password hashing

### Frontend
- **Vue.js** (with `vue-router`)
- **Bootstrap 5** for styling
- **jwt-decode** for decoding tokens in the frontend
- **Axios** for HTTP requests

---

## Installation Instructions

### 1. Backend Setup
Navigate to the `login-jwt-backend` folder:

```bash
cd login-jwt-backend
```

Install the required Python dependencies:

```bash
pip install flask flask-bcrypt flask-jwt-extended flask-sqlalchemy flask-cors
```

Run the Flask app:

```bash
python app.py
```

The backend will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

### 2. Frontend Setup
Navigate to the `login-jwt` folder:

```bash
cd login-jwt
```

Install the required npm dependencies:

```bash
npm install
```

Run the Vue.js app:

```bash
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

---

## Usage

### 1. Sign Up
- Open the app at [http://localhost:5173](http://localhost:5173).
- Click "Sign Up" and create a new user account.

### 2. Login
- Log in using the username and password.
- On successful login, you’ll be redirected to the success page.

### 3. Success Page
- Displays the following:
  - Username
  - Human-readable token issuance and expiry times
  - Remaining time for token expiration
  - User ID (from token payload)

### 4. Logout
- Click the **Logout** button to clear tokens and return to the login page.

---

## Token Behavior

### Access Token
- **Duration**: Short-lived (e.g., 1 minute for demonstration purposes).
- **Usage**: Sent with `Authorization: Bearer` header for protected routes.

### Refresh Token
- **Duration**: Long-lived (e.g., 5 minutes for demonstration purposes).
- **Usage**: Used to request a new access token when the current one expires.

---

## Token Refresh Flow

1. When accessing a protected route:
   - If the **access token** is valid, access is granted.
   - If the **access token** is expired, the app sends the **refresh token** to the `/refresh` endpoint to obtain a new access token.
2. The app automatically retries the protected route with the new access token.

---

## Key Endpoints

### 1. `/register` (POST)
**Description**: Register a new user.  
**Request Body**:
```json
{
  "username": "example",
  "password": "password123"
}
```
**Response**:
```json
{
  "message": "User created successfully"
}
```

### 2. `/login` (POST)
**Description**: Authenticate a user and receive tokens.  
**Request Body**:
```json
{
  "username": "example",
  "password": "password123"
}
```
**Response**:
```json
{
  "message": "Login successful",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>"
}
```

### 3. `/protected` (GET)
**Description**: Access a protected route with a valid access token.  
**Headers**:
```http
Authorization: Bearer <access_token>
```
**Response**:
```json
{
  "message": "Hello username, welcome to the success page!"
}
```

### 4. `/refresh` (POST)
**Description**: Obtain a new access token using a refresh token.  
**Headers**:
```http
Authorization: Bearer <refresh_token>
```
**Response**:
```json
{
  "access_token": "<new_access_token>"
}
```




