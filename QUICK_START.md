# 🚀 Quick Start Guide

## ✅ Setup Complete!
- ✅ API key configured in `backend/.env`
- ✅ Frontend configured to use local backend in `frontend/.env`

## 📋 Step-by-Step Instructions

### Step 1: Install Backend Dependencies

Open a terminal and run:

```powershell
cd d:\startup\backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

In the same terminal (or a new one):

```powershell
cd d:\startup\backend
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

✅ Backend is now running on `http://localhost:5000`

### Step 3: Install Node.js (If Not Already Installed)

**If you see "npm is not recognized" error:**

1. Download Node.js from: https://nodejs.org/
2. Install the LTS version (recommended)
3. **Restart your terminal/IDE** after installation
4. Verify installation:
   ```powershell
   node --version
   npm --version
   ```

### Step 4: Install Frontend Dependencies

Open a **NEW terminal** (keep backend running):

```powershell
cd d:\startup\frontend
npm install
```

### Step 5: Start the Frontend Server

In the same frontend terminal:

```powershell
npm start
```

**Expected output:**
```
Compiled successfully!
You can now view startup-evaluator-frontend in the browser.
  Local:            http://localhost:3000
```

✅ Frontend will automatically open in your browser at `http://localhost:3000`

## 🎯 Using the Application

1. Open `http://localhost:3000` in your browser
2. Enter your startup idea in the text box
3. Click "Evaluate Startup"
4. View the comprehensive analysis with charts and scores!

## 🔧 Troubleshooting

### Backend Issues:
- **Port 5000 already in use?** Change port in `backend/app.py` line 114
- **Module not found?** Run `pip install -r requirements.txt` again

### Frontend Issues:
- **npm not found?** Install Node.js and restart terminal
- **Port 3000 already in use?** React will ask to use a different port
- **Network error?** Make sure backend is running on port 5000

### API Connection:
- Frontend is configured to use `http://localhost:5000`
- Check `frontend/.env` file if connection fails
- Verify backend is running by visiting `http://localhost:5000` in browser

## 📝 Notes

- Keep **both terminals open** while using the app
- Backend must be running before frontend can make API calls
- The API key is stored in `backend/.env` (not committed to git)

