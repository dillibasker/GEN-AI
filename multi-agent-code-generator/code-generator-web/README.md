# Multi-Agent Code Generator - Web Interface

A clean, professional web interface for your 4-agent code generator.

## 📁 Project Structure

```
code-generator-web/
├── backend/
│   ├── server.js
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- Python 3
- Your existing `main.py` and `orchestrator/` folder

### Step 1: Place Your Python Code

1. Copy your existing project files (`main.py` and `orchestrator/` folder) to the **parent directory** of `code-generator-web/`

Your folder structure should look like:
```
your-project/
├── main.py
├── orchestrator/
│   └── orchestrator.py
└── code-generator-web/
    ├── backend/
    └── frontend/
```

**OR** if you want to keep them in the same folder:
- Place `main.py` and `orchestrator/` in the same directory as `code-generator-web/`
- Update line 24 in `backend/server.js` to: `const pythonScript = path.join(__dirname, '../main.py');`

### Step 2: Install Backend Dependencies

```bash
cd backend
npm install
```

### Step 3: Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

## 🏃 Running the Application

You need to run both backend and frontend servers.

### Terminal 1 - Backend Server

```bash
cd backend
npm start
```

Server will start at: `http://localhost:3001`

### Terminal 2 - Frontend Server

```bash
cd frontend
npm run dev
```

Server will start at: `http://localhost:3000`

### Open in Browser

Navigate to: **http://localhost:3000**

## 🎯 Usage

1. Enter your code requirement in the text area
2. Select target language (Python or JavaScript)
3. Click "Generate Code"
4. View results in four sections:
   - 📋 Plan
   - 🎨 Design
   - 💻 Generated Code
   - ✓ Test Result
5. Click "Copy" to copy any section to clipboard

## 🔧 Configuration

### Change Backend Port

Edit `backend/server.js` line 6:
```javascript
const PORT = 3001; // Change to your preferred port
```

Then update `frontend/src/App.jsx` line 22 to match.

### Change Frontend Port

Edit `frontend/vite.config.js`:
```javascript
server: {
  port: 3000 // Change to your preferred port
}
```

### Adjust Python Path

If your `main.py` is in a different location, edit `backend/server.js` line 24:
```javascript
const pythonScript = path.join(__dirname, 'path/to/your/main.py');
```

## 🐛 Troubleshooting

**Issue: Python script not found**
- Verify the path in `backend/server.js` line 24
- Ensure `main.py` is in the correct location

**Issue: CORS errors**
- Ensure backend is running on port 3001
- Check that frontend is making requests to the correct backend URL

**Issue: Port already in use**
- Change the port numbers in configuration files
- Kill the process using: `lsof -ti:3001 | xargs kill` (Mac/Linux)

## 📦 Production Build

### Build Frontend

```bash
cd frontend
npm run build
```

The build files will be in `frontend/dist/`

### Serve Production Build

You can serve the production build with the backend:

1. Add to `backend/server.js` before `app.listen()`:
```javascript
const path = require('path');
app.use(express.static(path.join(__dirname, '../frontend/dist')));
```

2. Run only the backend server:
```bash
cd backend
npm start
```

## 📝 Notes

- No database required - the app runs your existing Python code as-is
- Agent logic remains unchanged
- Clean, responsive UI works on mobile and desktop
- Results are parsed from your Python script's stdout

## 🎨 Customization

All styling is in `frontend/src/App.css`. The design uses:
- Clean gradients (purple theme)
- Professional spacing and typography
- Smooth animations
- Responsive layout

Feel free to modify colors, fonts, and layout to match your preferences!
