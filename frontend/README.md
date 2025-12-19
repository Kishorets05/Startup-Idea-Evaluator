# Startup Evaluator - Frontend

React frontend application for the Startup Evaluator.

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Configure API URL (optional):**
   - Create `.env` file in the frontend directory
   - Add: `REACT_APP_API_URL=https://startup-idea-evaluator-bryf.onrender.com`
   - Default is `https://startup-idea-evaluator-bryf.onrender.com`

3. **Run the development server:**
```bash
npm start
```

The app will open at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Features

- Modern React UI with responsive design
- Real-time startup idea evaluation
- Interactive charts and visualizations
- Expandable evaluation sections
- PDF report generation
- Error handling and loading states

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── IdeaInput.js
│   │   ├── EvaluationResults.js
│   │   ├── ScoreDisplay.js
│   │   ├── Charts.js
│   │   ├── EvaluationSections.js
│   │   ├── PDFDownload.js
│   │   └── LoadingSpinner.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
└── package.json
```

