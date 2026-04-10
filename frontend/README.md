# ChurnAI Frontend

A modern React frontend for the ChurnAI customer churn prediction system.

## Features

- 🎨 Beautiful, responsive UI with Tailwind-inspired styling
- 📱 Mobile-friendly design
- ⚡ Fast predictions with Vite
- 🚀 Real-time API integration with FastAPI backend
- 📊 Visual prediction results and risk indicators

## Prerequisites

- Node.js 16+ and npm (or yarn/pnpm)
- Python 3.8+ with the ChurnAI API running (see parent README)

## Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

3. Make sure your FastAPI backend is running:

```bash
# In another terminal, from the parent directory
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── components/       # React components
│   │   ├── PredictionForm.jsx    # Customer data form
│   │   └── PredictionForm.css    # Form styling
│   ├── App.jsx          # Main app component
│   ├── App.css          # App styling
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies
└── README.md            # This file
```

## How to Use

1. Fill in the customer information form with relevant data
2. Click "Predict Churn" button
3. View the prediction results:
   - Churn probability percentage
   - Risk status (Likely to Churn / Not Likely to Churn)
   - Recommendation for action

## Building for Production

```bash
npm run build
```

The optimized production files will be in the `dist/` directory.

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client (configured but can be used for enhancements)
- **CSS3** - Styling with modern features

## Environment Configuration

The frontend automatically proxies API requests to the FastAPI backend. Modify `vite.config.js` if you need to change the backend URL.

## Troubleshooting

### Connection Error?

- Ensure the FastAPI backend is running: `uvicorn api:app --reload`
- Check the backend is on `http://127.0.0.1:8000`
- Browser console (F12) shows detailed error messages

### Port Already in Use?

- Development server uses port 5173 by default
- Change it in vite.config.js: `port: 5174`

## Contributing

Feel free to improve the frontend! Areas for enhancement:

- Advanced data visualization
- Historical prediction tracking
- CSV batch import feature
- Dark mode support
