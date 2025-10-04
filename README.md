# Criminal Face Generation System

A research prototype for generating criminal face composites from witness descriptions, optimized for Indian facial features and law enforcement use.

## Overview

Modern web application with a guided workflow:
1. **Feature Selection** - Step-by-step selection of 9 facial characteristics
2. **Sketch Generation** - AI creates sketch from layered features with refinement options
3. **Colorization** - Applies realistic colors while preserving exact sketch structure

The system uses a React frontend with a Flask backend API, replacing the deprecated Streamlit interface.

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- Internet connection (for Pollinations.ai API)

### Installation & Running

#### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend API runs on `http://localhost:5000`

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

Open `http://localhost:3000` in your browser to use the application.

### Legacy Applications (Deprecated)
```bash
# Old Streamlit interface (kept for reference)
streamlit run streamlit_app.py

# Command line demos
python criminal_face_generator.py
python demo.py
```

## Workflow

### 1. Feature Selection
User selects options across 9 categories:
- Face shape (oval, round, square, diamond, heart, oblong)
- Eye shape (almond, round, hooded, upturned, downturned, monolid)
- Nose type (straight, aquiline, button, broad, narrow, roman)
- Mouth shape (full, thin, wide, small, bow, downturned)
- Eyebrows (straight, arched, rounded, angled, bushy, thin)
- Complexion (fair, wheatish, dusky, dark)
- Hair type (straight black, curly, wavy, receding, bald)
- Facial hair (clean shaven, mustache, beard, goatee, stubble)
- Distinctive marks (scars, moles, birthmarks, etc.)

Selected features are layered into a composite base image.

### 2. Sketch Generation
- AI generates initial sketch from composite + description
- Text-based refinement with additional details
- Manual editing: download sketch → edit externally → re-upload
- Version history tracks all iterations

### 3. Colorization
- Final approved sketch is colorized
- Preserves exact sketch structure (critical)
- Applies realistic Indian skin tones and mugshot-style rendering
- No face regeneration, only colorization

## Project Structure

```
/backend                      # Flask REST API
  ├── app.py                 # API endpoints
  ├── generator.py           # Sketch & colorization logic
  ├── compositor.py          # Feature layering
  └── requirements.txt       # Python dependencies

/frontend                     # React + Vite UI
  ├── src/
  │   ├── components/
  │   │   ├── FeatureSelector.jsx
  │   │   ├── SketchCanvas.jsx
  │   │   └── ColorPanel.jsx
  │   ├── App.jsx
  │   └── main.jsx
  ├── package.json
  └── vite.config.js

streamlit_app.py             # [DEPRECATED] Legacy Streamlit UI
criminal_face_generator.py   # Legacy CLI demo
requirements.txt             # Root dependencies
CLAUDE.md                    # Detailed technical docs
```

## Technical Stack

- **Frontend**: React 18, Vite, Tailwind CSS
- **Backend**: Flask, Flask-CORS
- **Image Processing**: PIL/Pillow
- **API**: Pollinations.ai (free, no auth)
- **HTTP Client**: Axios (frontend), Requests (backend)

## Research Context

This project is developed as a final year engineering research project. The implementation prioritizes:

- Research methodology over production readiness
- Indian demographic representation
- Academic documentation and reproducibility
- Future integration with ML/TPU components

## Limitations

- Requires internet connectivity for image generation
- Limited to Pollinations.ai API capabilities
- Prototype-level error handling
- No authentication or user management

## Future Enhancements

- Local ML model integration
- Enhanced facial feature control
- Batch processing capabilities
- Advanced sketch refinement tools
- Performance optimization for TPU deployment

## License

This project is developed for academic research purposes.

## Citation

If you use this work in your research, please cite:
```
[Citation format to be added upon publication]
```

## Contact

For questions regarding this research project, please contact the development team.