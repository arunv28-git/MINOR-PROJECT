# 🚀 Quick Start - Tripster Login Setup

## ⚡ 5-Minute Setup

### Step 1: Backend Setup (Terminal 1)

```powershell
# Navigate to backend folder
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy this content)
# SECRET_KEY=my-secret-key-123
# JWT_SECRET_KEY=my-jwt-key-456

# Start server
python run.py
```

**✅ You should see:**
```
[Info] SQLite user database initialized.
[Info] Flask App created. Authentication available via SQLite.
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!**

---

### Step 2: Frontend Setup (Terminal 2 - Optional)

```powershell
# Open NEW terminal window
cd frontend
python -m http.server 8000
```

**OR** simply double-click `frontend/index.html` in File Explorer.

---

### Step 3: Test Login

1. Open browser → Go to `http://localhost:8000` (or open `index.html`)
2. Click **"Login"** button (top-right)
3. Click **"Register"** tab
4. Fill form:
   - Username: `testuser`
   - Email: `test@test.com`
   - Password: `password123`
5. Click **"Register"** → Should see success message
6. Click **"Login"** tab
7. Enter credentials → Click **"Login"**
8. ✅ Should see "Hello, testuser!" in header

---

## ✅ Checklist

- [ ] Backend running on port 5000
- [ ] Frontend opens in browser
- [ ] Can access login page
- [ ] Can register new user
- [ ] Can login successfully
- [ ] Username appears in header
- [ ] Can logout

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Close other Flask apps or change port in `run.py` |
| Module not found | Run `pip install -r requirements.txt` |
| Can't connect to server | Make sure backend is running in Terminal 1 |
| Login page not loading | Check browser console (F12) for errors |

---

## 📚 Need More Help?

See [SETUP.md](SETUP.md) for detailed instructions and troubleshooting.

---

**That's it! Your login page should be working now! 🎉**



