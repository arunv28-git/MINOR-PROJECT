# Complete Setup Guide - Tripster with Login Page

This guide will walk you through setting up and running the Tripster application with the login/registration page working properly.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.11 or 3.12** installed ([Download Python](https://www.python.org/downloads/))
- A code editor (VS Code, PyCharm, etc.)
- A web browser (Chrome, Firefox, Edge, etc.)
- **Windows PowerShell** (or Command Prompt)

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to the Backend Directory

Open PowerShell (or Command Prompt) and navigate to the project's backend folder:

```powershell
cd "C:\Users\Lenovo\OneDrive\Desktop\Tripster\backend"
```

**Note:** Adjust the path if your project is in a different location.

---

### Step 2: Create a Virtual Environment (Recommended)

This keeps your project dependencies isolated:

```powershell
# Create virtual environment
python -m venv venv

# Activate it (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` at the beginning of your command prompt.

---

### Step 3: Install Python Dependencies

Install all required packages:

```powershell
pip install -r requirements.txt
```

**Expected output:** You should see packages being installed (flask, flask-cors, flask-bcrypt, flask-jwt-extended, etc.)

**Troubleshooting:**
- If `pip` is not recognized, use `python -m pip` instead
- If installation fails, try upgrading pip: `python -m pip install --upgrade pip`

---

### Step 4: Create Environment Variables File

Create a `.env` file in the `backend` directory to store configuration:

**Option A: Using PowerShell**
```powershell
# Create the .env file
New-Item -Path .env -ItemType File -Force

# Open it in notepad
notepad .env
```

**Option B: Manually**
1. Open your file explorer
2. Navigate to `backend` folder
3. Create a new file named `.env` (make sure it starts with a dot)
4. Open it with any text editor

**Add the following content to `.env`:**

```env
SECRET_KEY=your-secret-key-change-this-in-production-12345
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production-67890
GOOGLE_PLACES_API_KEY=your-google-places-api-key-here
```

**Important Notes:**
- Replace the secret keys with your own random strings (you can use any random text)
- The `GOOGLE_PLACES_API_KEY` is optional - you can leave it empty if you don't have one
- **DO NOT** commit the `.env` file to git (it should already be in .gitignore)

**Example `.env` file:**
```env
SECRET_KEY=my-super-secret-key-2024-tripster
JWT_SECRET_KEY=my-jwt-secret-key-2024-tripster
GOOGLE_PLACES_API_KEY=
```

---

### Step 5: Start the Backend Server

Run the Flask application:

```powershell
python run.py
```

**Expected output:**
```
[Info] SQLite user database initialized.
[Info] Flask App created. Authentication available via SQLite.
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**✅ Success indicators:**
- You see "SQLite user database initialized"
- You see "Running on http://127.0.0.1:5000"
- No error messages

**Keep this terminal window open!** The server needs to keep running.

---

### Step 6: Open the Frontend

**Option A: Simple Method (Recommended for Testing)**

1. Open File Explorer
2. Navigate to: `C:\Users\Lenovo\OneDrive\Desktop\Tripster\frontend`
3. Double-click on `index.html`
4. It should open in your default browser

**Option B: Using a Local Server (Better for Development)**

Open a **NEW** PowerShell window (keep the backend server running in the first one):

```powershell
cd "C:\Users\Lenovo\OneDrive\Desktop\Tripster\frontend"
python -m http.server 8000
```

Then open your browser and go to: `http://localhost:8000`

---

### Step 7: Test the Login Page

1. **Click the "Login" button** in the top-right corner of the homepage
2. You should see the login/registration page

**Test Registration:**
1. Click the **"Register"** tab
2. Fill in the form:
   - Username: `testuser` (or any username you like)
   - Email: `test@example.com` (or any email)
   - Password: `password123` (minimum 6 characters)
   - Confirm Password: `password123`
3. Click **"Register"**
4. You should see a success message
5. The page will automatically switch to the Login tab after 2 seconds

**Test Login:**
1. In the **"Login"** tab, enter:
   - Username: `testuser` (the one you just registered)
   - Password: `password123`
2. Click **"Login"**
3. You should be redirected to the homepage
4. You should see **"Hello, testuser!"** in the header
5. The "Login" button should be replaced with a "Logout" button

**✅ If everything works:**
- You can register new users
- You can log in with registered users
- You can log out
- You can plan trips while logged in

---

## 🔍 Verification Checklist

After setup, verify these points:

- [ ] Backend server is running on `http://127.0.0.1:5000`
- [ ] Frontend page opens in browser
- [ ] Login page is accessible
- [ ] Can register a new user
- [ ] Can log in with registered credentials
- [ ] Username appears in header after login
- [ ] Can log out successfully
- [ ] Can plan trips (both logged in and logged out)

---

## 🐛 Troubleshooting

### Problem: "Module not found" error when running `python run.py`

**Solution:**
```powershell
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated (you should see (venv))
# If not, activate it:
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem: "Port 5000 already in use"

**Solution:**
- Another application is using port 5000
- Close other Flask applications or change the port in `run.py`:
  ```python
  app.run(debug=True, port=5001)  # Change to 5001 or any other port
  ```
- If you change the port, also update the frontend API URL in `frontend/assets/auth.js` and `frontend/assets/app.js`

---

### Problem: Login page shows "Could not connect to server"

**Solution:**
1. Make sure the backend server is running (check the first terminal window)
2. Check that it's running on `http://127.0.0.1:5000`
3. Open `http://127.0.0.1:5000/health` in your browser - it should return `{"status": "ok"}`
4. Check browser console (F12) for CORS errors
5. Make sure you're opening the frontend from `http://localhost:8000` or `file://` protocol

---

### Problem: "Authentication disabled" error

**Solution:**
- This shouldn't happen with SQLite, but if it does:
1. Check that `backend/app/db.py` exists
2. Check that `tripster.db` file is created in the `backend` folder
3. Restart the backend server

---

### Problem: Registration fails with "Username is already taken"

**Solution:**
- This is normal! The username already exists in the database
- Try a different username
- Or delete `backend/tripster.db` to start fresh (this will delete all users)

---

### Problem: Can't see the login page or styles are broken

**Solution:**
1. Make sure all files are in the correct locations:
   - `frontend/login.html` exists
   - `frontend/assets/auth.js` exists
   - `frontend/assets/app.js` exists
   - `frontend/assets/styles.css` exists
2. Check browser console (F12) for 404 errors
3. Try using a local server instead of opening the file directly:
   ```powershell
   cd frontend
   python -m http.server 8000
   ```

---

### Problem: Database errors

**Solution:**
- SQLite database is created automatically
- If you see database errors:
  1. Delete `backend/tripster.db` (if it exists)
  2. Restart the backend server
  3. The database will be recreated automatically

---

## 📁 File Structure Check

Make sure your project has this structure:

```
Tripster/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── db.py          ← Should exist (for SQLite auth)
│   │   ├── models.py
│   │   └── services.py
│   ├── run.py             ← Run this to start backend
│   ├── requirements.txt
│   ├── .env               ← Create this file
│   └── tripster.db        ← Created automatically
├── frontend/
│   ├── index.html
│   ├── login.html         ← Login page
│   └── assets/
│       ├── app.js
│       ├── auth.js        ← Authentication logic
│       └── styles.css
└── README.md
```

---

## 🎯 Quick Start Summary

For experienced users, here's the quick version:

```powershell
# 1. Navigate to backend
cd backend

# 2. Create and activate venv (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with SECRET_KEY and JWT_SECRET_KEY

# 5. Start backend
python run.py

# 6. In another terminal, start frontend server (optional)
cd frontend
python -m http.server 8000

# 7. Open http://localhost:8000 in browser
```

---

## ✅ Success!

If you've completed all steps and can:
- ✅ Register new users
- ✅ Log in successfully
- ✅ See your username in the header
- ✅ Log out
- ✅ Plan trips

**Congratulations! Your Tripster application with login is working correctly!** 🎉

---

## 📞 Need Help?

If you encounter issues not covered here:
1. Check the browser console (F12 → Console tab)
2. Check the backend terminal for error messages
3. Verify all files are in the correct locations
4. Make sure Python version is 3.11 or 3.12
5. Try deleting `tripster.db` and restarting the server

---

## 🔐 Security Notes

- The `.env` file contains sensitive keys - never commit it to git
- In production, use strong, random secret keys
- Change default secret keys before deploying
- SQLite is fine for development, but consider PostgreSQL or MongoDB for production

---

**Last Updated:** 2024
**Version:** 1.0





