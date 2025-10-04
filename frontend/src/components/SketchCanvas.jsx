import { useState, useRef } from 'react';
import axios from 'axios';
import SketchEditor from './SketchEditor';

function SketchCanvas({ compositeImage, selectedFeatures, onComplete, onBack }) {
  const [sketchImage, setSketchImage] = useState(null);
  const [description, setDescription] = useState('');
  const [additionalDetails, setAdditionalDetails] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [sketchHistory, setSketchHistory] = useState([]);
  const [editedSketch, setEditedSketch] = useState(null);
  const [showEditor, setShowEditor] = useState(false);
  const fileInputRef = useRef(null);

  // Build description from selected features
  const buildDescription = () => {
    const parts = [];
    if (selectedFeatures.complexion) parts.push(`${selectedFeatures.complexion} complexion`);
    if (selectedFeatures.faceShape) parts.push(`${selectedFeatures.faceShape} face shape`);
    if (selectedFeatures.eyeShape) parts.push(`${selectedFeatures.eyeShape} eyes`);
    if (selectedFeatures.noseType) parts.push(`${selectedFeatures.noseType} nose`);
    if (selectedFeatures.mouthShape) parts.push(`${selectedFeatures.mouthShape} lips`);
    if (selectedFeatures.eyebrows) parts.push(`${selectedFeatures.eyebrows} eyebrows`);
    if (selectedFeatures.hairType) parts.push(`${selectedFeatures.hairType} hair`);
    if (selectedFeatures.facialHair && selectedFeatures.facialHair !== 'clean shaven') {
      parts.push(selectedFeatures.facialHair);
    }
    if (selectedFeatures.distinctiveMarks && selectedFeatures.distinctiveMarks !== 'none') {
      parts.push(selectedFeatures.distinctiveMarks);
    }
    return parts.join(', ');
  };

  const generateSketch = async () => {
    const fullDescription = description || buildDescription();

    try {
      setIsGenerating(true);
      const response = await axios.post('/api/generate-sketch', {
        description: fullDescription,
        composite_image: compositeImage
      });

      const newSketch = {
        image: response.data.sketch_image,
        description: fullDescription,
        timestamp: Date.now()
      };

      setSketchImage(newSketch.image);
      setDescription(fullDescription);
      setSketchHistory([...sketchHistory, newSketch]);
    } catch (error) {
      console.error('Failed to generate sketch:', error);
      alert('Failed to generate sketch. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const refineSketch = async () => {
    if (!sketchImage || !additionalDetails.trim()) {
      alert('Please add additional details to refine the sketch');
      return;
    }

    try {
      setIsGenerating(true);
      const response = await axios.post('/api/refine-sketch', {
        current_sketch: sketchImage,
        original_description: description,
        additional_description: additionalDetails
      });

      const refinedSketch = {
        image: response.data.sketch_image,
        description: response.data.description,
        timestamp: Date.now()
      };

      setSketchImage(refinedSketch.image);
      setDescription(refinedSketch.description);
      setSketchHistory([...sketchHistory, refinedSketch]);
      setAdditionalDetails('');
    } catch (error) {
      console.error('Failed to refine sketch:', error);
      alert('Failed to refine sketch. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setEditedSketch(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const useEditedSketch = () => {
    if (editedSketch) {
      setSketchImage(editedSketch);
      alert('Edited sketch loaded successfully!');
    }
  };

  const openEditor = () => {
    if (sketchImage) {
      setShowEditor(true);
    }
  };

  const handleEditorSave = (editedImage) => {
    const editedVersion = {
      image: editedImage,
      description: description + ' (manually edited)',
      timestamp: Date.now()
    };
    setSketchImage(editedImage);
    setSketchHistory([...sketchHistory, editedVersion]);
    setShowEditor(false);
  };

  const handleEditorCancel = () => {
    setShowEditor(false);
  };

  const proceedToColorization = () => {
    if (sketchImage) {
      onComplete(sketchImage, description);
    } else {
      alert('Please generate a sketch first');
    }
  };

  const downloadSketch = () => {
    if (!sketchImage) return;

    const link = document.createElement('a');
    link.href = sketchImage;
    link.download = `sketch_${Date.now()}.png`;
    link.click();
  };

  return (
    <>
      {showEditor && (
        <SketchEditor
          initialImage={sketchImage}
          onSave={handleEditorSave}
          onCancel={handleEditorCancel}
        />
      )}

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Left Panel - Sketch Generation */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Generate Sketch
        </h2>

        {/* Description */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description (auto-generated from features)
          </label>
          <textarea
            value={description || buildDescription()}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            rows="4"
            placeholder="Description will be auto-generated from selected features"
          />
        </div>

        {/* Generate Button */}
        {!sketchImage && (
          <button
            onClick={generateSketch}
            disabled={isGenerating}
            className="w-full px-4 py-3 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-6"
          >
            {isGenerating ? (
              <span className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Generating Sketch...
              </span>
            ) : (
              'Generate Initial Sketch'
            )}
          </button>
        )}

        {/* Refinement Section */}
        {sketchImage && (
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add Details to Refine
              </label>
              <textarea
                value={additionalDetails}
                onChange={(e) => setAdditionalDetails(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                rows="3"
                placeholder="e.g., thick eyebrows, slightly crooked nose, scar on left cheek"
              />
            </div>
            <button
              onClick={refineSketch}
              disabled={isGenerating || !additionalDetails.trim()}
              className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? 'Refining...' : 'Refine Sketch'}
            </button>
          </div>
        )}

        {/* Manual Edit Section */}
        {sketchImage && (
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Manual Editing
            </h3>

            <button
              onClick={openEditor}
              className="w-full px-4 py-3 mb-3 text-white bg-purple-600 rounded-md hover:bg-purple-700 font-medium"
            >
              🎨 Open Sketch Editor (Add Scars, Tattoos, etc.)
            </button>

            <div className="text-center text-sm text-gray-500 mb-3">
              - OR -
            </div>

            <button
              onClick={downloadSketch}
              className="w-full px-4 py-2 mb-3 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              📥 Download Sketch to Edit Externally
            </button>

            <div className="mb-3">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current.click()}
                className="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                📤 Upload Edited Sketch
              </button>
            </div>

            {editedSketch && (
              <div className="mb-3">
                <div className="bg-gray-100 rounded p-2 mb-2">
                  <img
                    src={editedSketch}
                    alt="Edited sketch preview"
                    className="w-full rounded"
                  />
                </div>
                <button
                  onClick={useEditedSketch}
                  className="w-full px-4 py-2 text-white bg-green-600 rounded-md hover:bg-green-700"
                >
                  Use This Edited Sketch
                </button>
              </div>
            )}
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between items-center mt-6 pt-6 border-t">
          <button
            onClick={onBack}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            ← Back to Features
          </button>
          <button
            onClick={proceedToColorization}
            disabled={!sketchImage}
            className="px-6 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Proceed to Colorization →
          </button>
        </div>
      </div>

      {/* Right Panel - Preview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Sketch Preview
        </h2>

        {/* Current Sketch */}
        <div className="mb-6">
          <div className="bg-gray-100 rounded-lg p-4 aspect-square flex items-center justify-center">
            {sketchImage ? (
              <img
                src={sketchImage}
                alt="Generated sketch"
                className="max-w-full max-h-full rounded"
              />
            ) : (
              <div className="text-center">
                <p className="text-gray-400 mb-2">No sketch generated yet</p>
                <p className="text-sm text-gray-500">
                  Click "Generate Initial Sketch" to begin
                </p>
              </div>
            )}
          </div>
        </div>

        {/* History */}
        {sketchHistory.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Version History
            </h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {sketchHistory.map((sketch, index) => (
                <div
                  key={sketch.timestamp}
                  className="border border-gray-200 rounded-lg p-3 cursor-pointer hover:border-blue-400"
                  onClick={() => setSketchImage(sketch.image)}
                >
                  <div className="flex items-start space-x-3">
                    <img
                      src={sketch.image}
                      alt={`Version ${index + 1}`}
                      className="w-20 h-20 object-cover rounded"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">
                        Version {index + 1}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {sketch.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
    </>
  );
}

export default SketchCanvas;
