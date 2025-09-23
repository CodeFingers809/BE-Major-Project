# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## BE Final Year Major Project
This folder contains the files for the final year major project for 4 year engineering students.
This project should be approached from a research perspective rather than a product making perspective.
We are going to have to write an entire research paper on this project after this is finished.

## Project Overview
Criminal face generation system that creates realistic faces from witness descriptions. The system follows a specific workflow: text description → sketch generation → sketch refinement → final colored image generation.

The project is optimized for Indian facial features and realistic mugshot-style images suitable for law enforcement use.

## Current Implementation
The prototype currently consists of:
- **Streamlit Web Application** (`streamlit_app.py`) - Main user interface
- **Command Line Demo** (`criminal_face_generator.py`) - Basic functionality testing
- **Interactive Demo** (`demo.py`) - Command line interface for testing

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit web app
streamlit run streamlit_app.py

# Or use the helper script
python run_app.py

# Run command line demo
python criminal_face_generator.py

# Interactive command line demo
python demo.py
```

## Technical Architecture

### Core Components
1. **CriminalFaceSketchGenerator** - Main class handling image generation
2. **Streamlit UI** - Three-column workflow interface
3. **API Integration** - Uses Pollinations.ai free image generation API

### Workflow Implementation
1. **Text to Sketch**: Generates black and white police sketches from descriptions
2. **Sketch Refinement**: Allows iterative improvements with additional details
3. **Sketch to Color**: Converts final sketch to realistic mugshot-style colored image

### Key Features
- Indian-specific facial feature selection (complexion, hair, facial hair, distinctive marks)
- Session state management for sketch history
- Image download functionality
- Real-time generation with progress indicators

## Prompt Engineering

### Sketch Generation Prompts
Use format: `"black and white pencil sketch of an Indian person, {description}, police sketch artist drawing, detailed facial features, South Asian features, realistic proportions, line art sketch on paper, monochrome drawing, criminal identification sketch"`

### Colored Image Prompts
Use format: `"police mugshot photograph of an Indian person, {description}, frontal view, neutral expression, harsh police station lighting, plain background, realistic Indian skin tone, South Asian facial features, criminal booking photo, high resolution, sharp focus, documentary photography style"`

## Important Constraints
- Focus on research/proof-of-concept rather than production-ready code
- TPU compatibility required for future ML components
- Generate realistic Indian faces with appropriate skin tones and features
- Maintain mugshot-style lighting and backgrounds (not studio quality)
- Context preservation for iterative face refinement is critical
- Avoid overly polished or AI-generated language in the interface

## API Dependencies
- **Pollinations.ai**: Free image generation API (no authentication required)
- **Streamlit**: Web application framework
- **PIL**: Image processing
- **Requests**: HTTP requests for API calls

## File Structure
```
/
├── streamlit_app.py          # Main Streamlit web application
├── criminal_face_generator.py # Core functionality and CLI demo
├── demo.py                   # Interactive command line demo
├── run_app.py               # Helper script to launch Streamlit
├── requirements.txt         # Python dependencies
└── CLAUDE.md               # This file
```
