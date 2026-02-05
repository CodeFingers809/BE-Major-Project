# Criminal Face Generation System

A Django-based research prototype for generating criminal face composites from witness descriptions, optimized for Indian facial features and law enforcement use.

## Overview

Comprehensive web application with detailed feature selection workflow:
1. **Feature Selection** - 13 detailed categories with 90+ Indian-specific facial features
2. **Real-time Composition** - Visual preview as features are selected
3. **Mugshot Generation** - AI creates realistic criminal mugshots using Flux Indo Realism

Built with Django backend and vanilla JavaScript frontend for maximum simplicity and control.

## Quick Start

### Prerequisites

- Python 3.10+
- macOS with Apple Silicon (M1/M2/M3/M4) - optimized for MLX
- 16GB+ RAM recommended
- ~20GB disk space for AI models
- Internet connection (for initial model download only)

### Installation & Running

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (including MFLUX for local AI generation)
pip install -r requirements.txt

# Login to Hugging Face (required for Flux model access)
huggingface-cli login --token YOUR_HF_TOKEN

# Accept Flux model license at: https://huggingface.co/black-forest-labs/FLUX.1-schnell

# Download models (one-time, ~19GB, takes 5-10 minutes)
python download_models.py

# Run migrations (first time only)
python manage.py migrate

# Populate feature database (first time only)
python manage.py populate_features

# Start Django development server
python manage.py runserver
```

Application runs on `http://127.0.0.1:8000`

**First Generation**: 5-10 minutes (downloads models)
**Subsequent Generations**: 15-20 seconds (local, no internet needed)

### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin` to manage features and view compositions.

Default credentials (if using the auto-created admin):
- Username: `admin`
- Password: `admin123`

### Legacy Applications (Deprecated)
```bash
# Old Streamlit interface (kept for reference)
streamlit run streamlit_app.py

# Command line demos
python criminal_face_generator.py
python demo.py
```

## Feature Categories (90+ Options)

### Comprehensive Indian Facial Feature Database

1. **Face Shape** (7 options) - Oval, Round, Square, Rectangular, Diamond, Heart-shaped, Triangular
2. **Complexion** (6 options) - Very Fair to Very Dark Indian skin tones
3. **Forehead** (5 options) - Broad, Narrow, Medium, Receding, Lined
4. **Eyes** (8 options) - Almond, Round, Deep-set, Hooded, Wide-set, Close-set, Droopy, Squinting
5. **Eyebrows** (6 options) - Thick & Straight, Thin & Arched, Unibrow, Sparse, Bushy, Angular
6. **Nose** (8 options) - Broad & Flat, Long & Narrow, Hooked, Bulbous, Thin, Crooked, Flared, Button
7. **Cheekbones** (5 options) - High & Prominent, Flat, Full & Round, Hollow, Average
8. **Mouth & Lips** (7 options) - Full, Thin, Wide, Small, Uneven, Downturned, Prominent Upper
9. **Jaw & Chin** (7 options) - Strong Square, Weak, Prominent, Pointed, Double, Cleft, Round
10. **Facial Hair** (8 options) - Clean Shaven, Full Beard, Stubble, Goatee, Mustache, Handlebar, Patchy, Sideburns
11. **Hair** (9 options) - Short, Medium, Receding, Bald, Partially Bald, Long, Curly, Slicked Back, Messy
12. **Distinctive Marks** (8 options) - Scars, Moles, Pockmarks, Birthmarks, Missing Tooth, etc.
13. **Age Features** (6 options) - Young 20s, Late 20s-30s, 40s, 50s+, Wrinkled, Eye Bags

## Workflow

1. **Select Features**: Choose one option from each category to build the face description
2. **Preview Canvas**: See selected features listed on the canvas in real-time
3. **Generate Mugshot**: AI creates realistic criminal mugshot using Flux Indo Realism model
4. **Download**: Save the generated face for law enforcement records

## Project Structure

```
criminal_face_app/           # Django project settings
  ├── settings.py            # Configuration
  ├── urls.py                # URL routing
  └── wsgi.py

face_generator/              # Main Django app
  ├── models.py              # Database models (Categories, Features, Compositions)
  ├── views.py               # API views and endpoints
  ├── serializers.py         # REST serializers
  ├── admin.py               # Admin interface configuration
  └── management/
      └── commands/
          └── populate_features.py  # Feature database population

templates/
  └── index.html             # Main frontend interface

static/
  └── app.js                 # Frontend JavaScript

requirements.txt             # Python dependencies
manage.py                    # Django management script
```

## Technical Stack

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Vanilla JavaScript, HTML5 Canvas
- **Database**: SQLite (development)
- **Image Processing**: PIL/Pillow
- **AI Generation**: MFLUX + Flux.1-Schnell + Indo-Realism LoRA (local, MLX-optimized for M4)
- **ML Framework**: Apple MLX (optimized for Apple Silicon)
- **HTTP**: Django CORS headers for API access

## Key Features

✅ **100% Local AI Generation** - Runs entirely on your M4 MacBook Air
✅ **Indo-Realism LoRA** - Specialized for Indian facial features
✅ **Copy Prompt Feature** - View and copy AI generation prompts
✅ **Pencil Sketch Style** - Authentic police sketch artist drawings
✅ **90+ Facial Features** - Comprehensive database of Indian features
✅ **Fast Generation** - 15-20 seconds after initial model download
✅ **Privacy First** - No data leaves your machine
✅ **Offline Capable** - Works without internet after setup

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