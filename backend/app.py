from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import io
import base64
from generator import SketchGenerator, ImageColorizer
from compositor import FacialFeatureCompositor

app = Flask(__name__)
CORS(app)

sketch_generator = SketchGenerator()
colorizer = ImageColorizer()
compositor = FacialFeatureCompositor()


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


@app.route('/api/composite-features', methods=['POST'])
def composite_features():
    """
    Composite layered facial features into a single base image
    Expected input: {"features": {"faceShape": "oval", "eyeShape": "almond", ...}}
    """
    try:
        data = request.json
        features = data.get('features', {})

        # Create composite image from selected features
        composite_image = compositor.create_composite(features)

        # Convert to base64
        img_buffer = io.BytesIO()
        composite_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return jsonify({
            "success": True,
            "composite_image": f"data:image/png;base64,{img_base64}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/generate-sketch', methods=['POST'])
def generate_sketch():
    """
    Generate sketch from description and optional composite image
    Expected input: {
        "description": "text description",
        "composite_image": "base64 image" (optional)
    }
    """
    try:
        data = request.json
        description = data.get('description', '')
        composite_b64 = data.get('composite_image', None)

        composite_image = None
        if composite_b64:
            # Decode base64 composite image
            if composite_b64.startswith('data:image'):
                composite_b64 = composite_b64.split(',')[1]
            composite_bytes = base64.b64decode(composite_b64)
            composite_image = Image.open(io.BytesIO(composite_bytes))

        # Generate sketch
        sketch_image = sketch_generator.generate_sketch(description, composite_image)

        # Convert to base64
        img_buffer = io.BytesIO()
        sketch_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return jsonify({
            "success": True,
            "sketch_image": f"data:image/png;base64,{img_base64}",
            "description": description
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/refine-sketch', methods=['POST'])
def refine_sketch():
    """
    Refine existing sketch with additional description
    Expected input: {
        "current_sketch": "base64 image",
        "original_description": "original text",
        "additional_description": "refinement text"
    }
    """
    try:
        data = request.json
        sketch_b64 = data.get('current_sketch', '')
        original_desc = data.get('original_description', '')
        additional_desc = data.get('additional_description', '')

        # Decode sketch image
        if sketch_b64.startswith('data:image'):
            sketch_b64 = sketch_b64.split(',')[1]
        sketch_bytes = base64.b64decode(sketch_b64)
        current_sketch = Image.open(io.BytesIO(sketch_bytes))

        # Combine descriptions
        combined_description = f"{original_desc}, {additional_desc}"

        # Generate refined sketch
        refined_sketch = sketch_generator.generate_sketch(combined_description, current_sketch)

        # Convert to base64
        img_buffer = io.BytesIO()
        refined_sketch.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return jsonify({
            "success": True,
            "sketch_image": f"data:image/png;base64,{img_base64}",
            "description": combined_description
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/colorize-sketch', methods=['POST'])
def colorize_sketch():
    """
    Colorize the final sketch (preserving sketch details exactly)
    Expected input: {
        "sketch_image": "base64 image",
        "description": "color description (skin tone, hair color, etc)"
    }
    """
    try:
        data = request.json
        sketch_b64 = data.get('sketch_image', '')
        description = data.get('description', '')

        # Decode sketch image
        if sketch_b64.startswith('data:image'):
            sketch_b64 = sketch_b64.split(',')[1]
        sketch_bytes = base64.b64decode(sketch_b64)
        sketch_image = Image.open(io.BytesIO(sketch_bytes))

        # Colorize sketch (preserving structure)
        colored_image = colorizer.colorize_sketch(sketch_image, description)

        # Convert to base64
        img_buffer = io.BytesIO()
        colored_image.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return jsonify({
            "success": True,
            "colored_image": f"data:image/png;base64,{img_base64}",
            "description": description
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
