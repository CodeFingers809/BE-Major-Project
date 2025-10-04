# CLAUDE.md

## BE Final Year Major Project
Criminal face generation research prototype for law enforcement. Creates faces from witness descriptions with Indian-optimized features. Research-focused, not production.

## Architecture
- **Frontend**: React + Vite + Tailwind (`/frontend`)
- **Backend**: Flask REST API (`/backend`)
- **Legacy**: Streamlit app (deprecated)

## Running the App

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py  # http://127.0.0.1:5001
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

## Workflow
1. **Feature Selection**: 9-step guided selection (face shape, eyes, nose, mouth, eyebrows, complexion, hair, facial hair, marks)
2. **Sketch Generation**: AI creates sketch from layered features + allows refinement and manual editing
3. **Colorization**: Colors final sketch (preserves structure, NO regeneration)

## Key Files
- `backend/app.py` - Flask API endpoints
- `backend/generator.py` - Sketch & color generation
- `backend/compositor.py` - Feature layering
- `frontend/src/components/FeatureSelector.jsx` - Step 1 UI
- `frontend/src/components/SketchCanvas.jsx` - Step 2 UI
- `frontend/src/components/ColorPanel.jsx` - Step 3 UI

## Tech Stack
- React 18, Vite, Tailwind CSS
- Flask, Flask-CORS
- PIL/Pillow
- Pollinations.ai API (free, no auth)

## Critical Constraints
- Research prototype, not production code
- Indian facial features optimization required
- Mugshot-style rendering (harsh lighting, plain background)
- Colorization MUST preserve sketch structure exactly
- TPU compatibility for future ML components

## Prompt Templates

**Sketch**: `"black and white pencil sketch of an Indian person, {description}, police sketch artist drawing, detailed facial features, South Asian features, realistic proportions, line art sketch on paper, monochrome drawing, criminal identification sketch"`

**Color**: `"police mugshot photograph of an Indian person, {description}, frontal view, neutral expression, harsh police station lighting, plain background, realistic Indian skin tone, South Asian facial features, criminal booking photo, high resolution, sharp focus, documentary photography style"`

## File Structure
```
backend/          # Flask API
frontend/         # React UI
streamlit_app.py  # [DEPRECATED]
*.py              # Legacy demos
```

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless absolutely necessary.
ALWAYS prefer editing existing files.
NEVER proactively create documentation files.
