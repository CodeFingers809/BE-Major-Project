import { useState } from 'react';
import axios from 'axios';

function ColorPanel({ sketchImage, description, onComplete, onBack }) {
  const [coloredImage, setColoredImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [colorDescription, setColorDescription] = useState('');

  const generateColoredImage = async () => {
    try {
      setIsGenerating(true);
      const response = await axios.post('/api/colorize-sketch', {
        sketch_image: sketchImage,
        description: colorDescription || description
      });

      setColoredImage(response.data.colored_image);
      onComplete(response.data.colored_image);
    } catch (error) {
      console.error('Failed to colorize sketch:', error);
      alert('Failed to colorize sketch. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadImage = (imageData, filename) => {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = filename;
    link.click();
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Left Panel - Colorization Controls */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Colorize Sketch
        </h2>

        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-4">
            The sketch will be colorized while preserving all details. Specify color preferences below.
          </p>

          <label className="block text-sm font-medium text-gray-700 mb-2">
            Color Description (optional)
          </label>
          <textarea
            value={colorDescription}
            onChange={(e) => setColorDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            rows="4"
            placeholder="e.g., dark brown eyes, black hair, wheatish skin tone, brown beard"
          />
          <p className="text-xs text-gray-500 mt-1">
            Leave empty to use the original description
          </p>
        </div>

        {!coloredImage && (
          <button
            onClick={generateColoredImage}
            disabled={isGenerating}
            className="w-full px-4 py-3 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-6"
          >
            {isGenerating ? (
              <span className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Colorizing Sketch...
              </span>
            ) : (
              'Colorize Sketch'
            )}
          </button>
        )}

        {coloredImage && (
          <div className="space-y-3 mb-6">
            <button
              onClick={() => downloadImage(coloredImage, `colored_face_${Date.now()}.png`)}
              className="w-full px-4 py-2 text-white bg-green-600 rounded-md hover:bg-green-700"
            >
              Download Colored Image
            </button>
            <button
              onClick={() => downloadImage(sketchImage, `final_sketch_${Date.now()}.png`)}
              className="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Download Sketch
            </button>
            <button
              onClick={() => {
                setColoredImage(null);
                setColorDescription('');
              }}
              className="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Regenerate
            </button>
          </div>
        )}

        {/* Information */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">
            Important
          </h3>
          <ul className="text-xs text-blue-800 space-y-1">
            <li>• The exact sketch structure will be preserved</li>
            <li>• Only colors will be applied, no new features generated</li>
            <li>• Colors will match realistic Indian skin tones</li>
            <li>• Result will be in mugshot photograph style</li>
          </ul>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center mt-6 pt-6 border-t">
          <button
            onClick={onBack}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            ← Back to Sketch
          </button>
        </div>
      </div>

      {/* Right Panel - Preview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Results
        </h2>

        {/* Sketch Preview */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Original Sketch
          </h3>
          <div className="bg-gray-100 rounded-lg p-4">
            <img
              src={sketchImage}
              alt="Original sketch"
              className="w-full rounded"
            />
          </div>
        </div>

        {/* Colored Image */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Colored Image
          </h3>
          <div className="bg-gray-100 rounded-lg p-4">
            {coloredImage ? (
              <img
                src={coloredImage}
                alt="Colored result"
                className="w-full rounded"
              />
            ) : (
              <div className="aspect-square flex items-center justify-center">
                <p className="text-gray-400">
                  Colored image will appear here
                </p>
              </div>
            )}
          </div>
        </div>

        {coloredImage && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm font-medium text-green-900">
              ✓ Generation Complete
            </p>
            <p className="text-xs text-green-700 mt-1">
              Download the images or regenerate with different colors
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ColorPanel;
