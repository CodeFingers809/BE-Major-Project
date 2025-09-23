# Criminal Face Generation System

A research-focused system for generating realistic criminal faces from witness descriptions, optimized for Indian facial features and law enforcement applications.

## Overview

This project implements a three-stage workflow for criminal face generation:
1. **Text to Sketch** - Generate black and white police sketches from descriptions
2. **Sketch Refinement** - Iteratively improve sketches with additional details
3. **Sketch to Color** - Convert final sketches to realistic mugshot-style colored images

The system is designed as a proof-of-concept for academic research rather than production deployment.

## Features

- 🎯 Optimized for Indian facial features and skin tones
- 📝 Natural language description input
- 🖼️ Three-stage image generation pipeline
- 🔄 Iterative sketch refinement
- 💾 Session state management and image downloads
- 🌐 Web interface built with Streamlit

## Quick Start

### Prerequisites

- Python 3.7+
- Internet connection (for Pollinations.ai API)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd BE\ PROJECT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Web Application
```bash
# Launch Streamlit web interface
streamlit run streamlit_app.py

# Or use helper script
python run_app.py
```

#### Command Line Interface
```bash
# Basic CLI demo
python criminal_face_generator.py

# Interactive demo
python demo.py
```

## Project Structure

```
├── streamlit_app.py          # Main Streamlit web application
├── criminal_face_generator.py # Core functionality and CLI demo
├── demo.py                   # Interactive command line demo
├── run_app.py               # Helper script to launch Streamlit
├── requirements.txt         # Python dependencies
├── CLAUDE.md               # Development guidelines
└── README.md               # This file
```

## Technical Details

### Architecture

- **Core Class**: `CriminalFaceSketchGenerator` handles image generation logic
- **API Backend**: Pollinations.ai free image generation service
- **Frontend**: Streamlit three-column workflow interface
- **Image Processing**: PIL for image handling and downloads

### Prompt Engineering

The system uses carefully crafted prompts for each generation stage:

- **Sketch Generation**: Focuses on police sketch aesthetics with Indian features
- **Color Generation**: Produces mugshot-style photographs with realistic lighting

### Key Dependencies

- `streamlit` - Web application framework
- `requests` - HTTP API communication
- `Pillow` - Image processing
- `pollinations.ai` - Image generation API (no auth required)

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