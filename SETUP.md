# Criminal Face Generator - Setup Guide

Complete setup instructions for running this criminal face generation research prototype.

## System Requirements

- **OS**: macOS, Linux, or Windows with WSL
- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher
- **RAM**: Minimum 8GB (16GB+ recommended for ComfyUI)
- **GPU**: NVIDIA GPU with 6GB+ VRAM recommended (for local ComfyUI)
- **Disk Space**: ~15GB for models and dependencies

---

## Quick Start (Without ComfyUI)

If you just want to test the app without local AI generation:

### 1. Clone Repository
```bash
git clone <repository-url>
cd "BE PROJECT"
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
# Backend runs on http://127.0.0.1:5001
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000 (or 3001 if 3000 is busy)
```

**Note**: Without ComfyUI, the app will use Pollinations.ai (free online API) but quality will be lower.

---

## Full Setup (With ComfyUI for Best Quality)

### Part 1: Backend Setup

#### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Requirements include**:
- Flask (REST API)
- Flask-CORS (Cross-origin requests)
- Pillow (Image processing)
- requests (HTTP client)

#### 2. Test Backend
```bash
python app.py
```
Should see:
```
 * Running on http://127.0.0.1:5001
```

---

### Part 2: ComfyUI Setup (Local AI Generation)

#### 1. Clone ComfyUI
```bash
cd "BE PROJECT"
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

#### 2. Install ComfyUI Dependencies
```bash
pip install -r requirements.txt
```

For NVIDIA GPUs:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

For Mac (M1/M2):
```bash
pip install torch torchvision torchaudio
```

For CPU-only:
```bash
pip install torch torchvision torchaudio
```

#### 3. Download Required Models

**a) Checkpoint Model** (Main generative model)
```bash
cd models/checkpoints
# Download Realistic Vision V6.0 B1
wget https://huggingface.co/SG161222/Realistic_Vision_V6.0_B1_noVAE/resolve/main/realisticVisionV60B1_v51VAE.safetensors -O realisticVisionV60B1.safetensors
```

Or download manually:
- Go to: https://huggingface.co/SG161222/Realistic_Vision_V6.0_B1_noVAE
- Download `realisticVisionV60B1_v51VAE.safetensors`
- Place in `ComfyUI/models/checkpoints/`
- Rename to `realisticVisionV60B1.safetensors`

**b) ControlNet Model** (For sketch preservation)
```bash
cd ../controlnet
# Download ControlNet Scribble
wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth -O control_v11p_sd15_scribble.safetensors
```

Or download manually:
- Go to: https://huggingface.co/lllyasviel/ControlNet-v1-1
- Download `control_v11p_sd15_scribble.pth`
- Place in `ComfyUI/models/controlnet/`
- Rename to `control_v11p_sd15_scribble.safetensors`

#### 4. Verify Model Locations
```bash
ls ComfyUI/models/checkpoints/
# Should show: realisticVisionV60B1.safetensors

ls ComfyUI/models/controlnet/
# Should show: control_v11p_sd15_scribble.safetensors
```

#### 5. Start ComfyUI
```bash
cd ComfyUI
python main.py
# Server runs on http://127.0.0.1:8188
```

Keep this running in a separate terminal.

---

### Part 3: Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

**Key Dependencies**:
- React 18
- Vite (Build tool)
- Tailwind CSS (Styling)
- Axios (HTTP client)

#### 2. Start Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000` or `http://localhost:3001`

---

## Running the Complete Stack

You need **3 terminals** running simultaneously:

### Terminal 1: Backend
```bash
cd "BE PROJECT/backend"
python app.py
# http://127.0.0.1:5001
```

### Terminal 2: ComfyUI (optional but recommended)
```bash
cd "BE PROJECT/ComfyUI"
python main.py
# http://127.0.0.1:8188
```

### Terminal 3: Frontend
```bash
cd "BE PROJECT/frontend"
npm run dev
# http://localhost:3000
```

---

## Workflow Overview

### 1. Feature Selection → Composite Generation
- User selects 9 facial features through UI
- Backend creates layered composite wireframe (`compositor.py`)
- Composite shows proper facial proportions

### 2. Sketch Generation (ComfyUI)
- Composite image → ComfyUI with ControlNet
- Generates B&W sketch following composite proportions
- Uses `comfyui_sketch_workflow.json`

### 3. Manual Editing (Optional)
- Built-in sketch editor (MS Paint-like)
- Add scars, tattoos, refine features
- Drawing tools: pen, eraser, undo/redo

### 4. Colorization (ComfyUI)
- Sketch → ComfyUI with ControlNet (0.98 strength)
- Preserves exact sketch structure
- Generates realistic mugshot
- Uses `comfyui_workflow.json`

---

## Project Structure

```
BE PROJECT/
├── backend/
│   ├── app.py                      # Flask REST API
│   ├── generator.py                # Sketch & colorization logic
│   ├── compositor.py               # Feature layering
│   ├── comfyui_client.py          # ComfyUI API client
│   ├── comfyui_workflow.json      # Colorization workflow
│   ├── comfyui_sketch_workflow.json # Sketch generation workflow
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FeatureSelector.jsx    # Step 1: Feature selection
│   │   │   ├── SketchCanvas.jsx       # Step 2: Sketch generation & editing
│   │   │   ├── SketchEditor.jsx       # Built-in drawing editor
│   │   │   └── ColorPanel.jsx         # Step 3: Colorization
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── ComfyUI/                       # AI generation engine
│   ├── models/
│   │   ├── checkpoints/           # Place realisticVisionV60B1.safetensors here
│   │   └── controlnet/            # Place control_v11p_sd15_scribble.safetensors here
│   └── main.py
├── CLAUDE.md                      # Project overview for Claude
└── SETUP.md                       # This file
```

---

## API Endpoints

### Backend (Flask) - Port 5001

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/composite-features` | POST | Generate composite from features |
| `/api/generate-sketch` | POST | Generate sketch from composite |
| `/api/refine-sketch` | POST | Refine existing sketch |
| `/api/colorize-sketch` | POST | Colorize final sketch |

### ComfyUI - Port 8188

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload/image` | POST | Upload reference image |
| `/prompt` | POST | Queue generation workflow |
| `/history/{id}` | GET | Get generation result |
| `/view` | GET | Download generated image |

---

## Troubleshooting

### Backend won't start
```bash
# Check port 5001
lsof -i:5001
# Kill process if needed
kill -9 <PID>
```

### ComfyUI errors
```bash
# "Model not found"
# → Check models are in correct folders with exact names

# CUDA out of memory
# → Reduce batch size or use CPU mode
# In comfyui_workflow.json, change "batch_size": 1

# Import errors
pip install -r requirements.txt --upgrade
```

### Frontend won't start
```bash
# Port conflict
# → Vite will auto-select next available port

# Module not found
npm install
npm cache clean --force
npm install
```

### ComfyUI not being used
```bash
# Check ComfyUI is running
curl http://127.0.0.1:8188

# Check backend logs
# Should see: "SketchGenerator: Using ComfyUI"
# If not, check ComfyUI server is accessible
```

### Low quality results
- **Without ComfyUI**: Uses Pollinations.ai (lower quality)
- **With ComfyUI**: Uses local ControlNet (high quality)
- Ensure models are downloaded correctly
- Check ControlNet strength in workflows (should be 0.85-0.98)

---

## Performance Tips

### For Limited Hardware
- Use CPU mode (slower but works)
- Close other applications
- Reduce steps in workflows (30 → 20)

### For GPU Systems
- Monitor VRAM usage
- Use `nvidia-smi` to check GPU
- Ensure CUDA drivers are installed

### Speed Optimization
- First generation takes longer (model loading)
- Subsequent generations are faster
- Keep ComfyUI running between requests

---

## Environment Variables (Optional)

Create `.env` in backend folder:
```bash
COMFYUI_URL=http://127.0.0.1:8188
FLASK_PORT=5001
FLASK_DEBUG=True
USE_COMFYUI=True  # Set to False to use Pollinations.ai only
```

---

## Testing the Setup

### 1. Test Backend
```bash
curl http://127.0.0.1:5001/api/health
# Should return: {"status": "ok"}
```

### 2. Test ComfyUI
```bash
curl http://127.0.0.1:8188
# Should return ComfyUI web UI HTML
```

### 3. Test Full Workflow
1. Open `http://localhost:3000`
2. Select all 9 features
3. Click "Complete Selection"
4. Wait for composite preview to generate
5. Click "Generate Initial Sketch"
6. Use sketch editor to add details
7. Click "Proceed to Colorization"
8. View final result

---

## Common Issues & Solutions

### "Address already in use"
Ports 5001 or 8188 are occupied:
```bash
# Find process
lsof -i:5001
lsof -i:8188
# Kill it
kill -9 <PID>
```

### "Failed to generate sketch"
- Check ComfyUI is running on port 8188
- Check models are downloaded
- Check backend can reach ComfyUI
- View backend logs for detailed errors

### "Sketch doesn't match composite"
- Increase ControlNet strength (0.85 → 0.95)
- Edit `comfyui_sketch_workflow.json`
- Line 42: `"strength": 0.95`

### "Colorization changes the face"
- Increase preservation strength
- Edit `comfyui_workflow.json`
- Already set to 0.98 (maximum preservation)
- Check negative prompt is being used

---

## Development Mode

### Hot Reload
- Frontend: Auto-reloads on file changes
- Backend: Restart manually after changes
- ComfyUI: Restart if workflows change

### Debugging
```bash
# Backend logs
python app.py  # Watch console output

# Frontend logs
npm run dev  # Watch browser console

# ComfyUI logs
python main.py  # Watch generation progress
```

---

## Production Deployment

**⚠️ Important**: This is a research prototype, not production-ready.

For production use, you would need:
- Authentication & authorization
- Rate limiting
- Model optimization
- Cloud GPU hosting
- Database for user sessions
- Security hardening
- API key management

---

## Credits & Models

- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Realistic Vision**: SG161222 on HuggingFace
- **ControlNet**: lllyasviel on HuggingFace
- **Pollinations.ai**: Free fallback API

---

## Support

If you encounter issues:
1. Check all 3 services are running
2. Verify model files exist and have correct names
3. Check console logs for errors
4. Ensure ports 5001, 8188, 3000 are available

For model downloads:
- Realistic Vision: ~2GB
- ControlNet: ~1.5GB
- Total: ~3.5GB download

---

## Next Steps After Setup

1. Test with sample features
2. Experiment with sketch editor
3. Try different feature combinations
4. Monitor generation quality
5. Adjust workflow parameters if needed

---

**Last Updated**: 2025-10-04
**Project**: BE Final Year Major - Criminal Face Generator
**Purpose**: Research prototype for law enforcement sketch generation
