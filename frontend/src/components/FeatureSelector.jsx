import { useState } from 'react';
import axios from 'axios';
import { faceShapes, eyeShapes, noseTypes, mouthShapes, eyebrowTypes } from '../assets/faceShapes';

const FEATURE_OPTIONS = {
  faceShape: {
    label: 'Face Shape',
    options: ['oval', 'round', 'square', 'diamond', 'heart', 'oblong']
  },
  eyeShape: {
    label: 'Eye Shape',
    options: ['almond', 'round', 'hooded', 'upturned', 'downturned', 'monolid']
  },
  noseType: {
    label: 'Nose Type',
    options: ['straight', 'aquiline', 'button', 'broad', 'narrow', 'roman']
  },
  mouthShape: {
    label: 'Mouth Shape',
    options: ['full', 'thin', 'wide', 'small', 'bow', 'downturned']
  },
  eyebrows: {
    label: 'Eyebrows',
    options: ['straight', 'arched', 'rounded', 'angled', 'bushy', 'thin']
  },
  complexion: {
    label: 'Complexion',
    options: ['fair', 'wheatish', 'dusky', 'dark']
  },
  hairType: {
    label: 'Hair Type',
    options: ['straight black', 'curly', 'wavy', 'receding hairline', 'bald']
  },
  facialHair: {
    label: 'Facial Hair',
    options: ['clean shaven', 'mustache', 'beard', 'goatee', 'stubble']
  },
  distinctiveMarks: {
    label: 'Distinctive Marks',
    options: ['none', 'scar on face', 'mole on cheek', 'broken nose', 'missing tooth', 'birthmark']
  }
};

function FeatureSelector({ onComplete }) {
  const [currentFeature, setCurrentFeature] = useState(0);
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [compositePreview, setCompositePreview] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const featureKeys = Object.keys(FEATURE_OPTIONS);
  const currentFeatureKey = featureKeys[currentFeature];
  const currentFeatureData = FEATURE_OPTIONS[currentFeatureKey];

  const handleSelectOption = async (option) => {
    const newFeatures = {
      ...selectedFeatures,
      [currentFeatureKey]: option
    };
    setSelectedFeatures(newFeatures);

    // Generate composite preview for first 5 features (facial structure)
    if (currentFeature < 5) {
      try {
        setIsGenerating(true);
        const response = await axios.post('/api/composite-features', {
          features: newFeatures
        });
        setCompositePreview(response.data.composite_image);
      } catch (error) {
        console.error('Failed to generate composite:', error);
      } finally {
        setIsGenerating(false);
      }
    }

    // Move to next feature
    if (currentFeature < featureKeys.length - 1) {
      setCurrentFeature(currentFeature + 1);
    }
  };

  const handleBack = () => {
    if (currentFeature > 0) {
      setCurrentFeature(currentFeature - 1);
    }
  };

  const handleComplete = () => {
    onComplete(selectedFeatures, compositePreview);
  };

  const isLastFeature = currentFeature === featureKeys.length - 1;
  const hasSelectedCurrentFeature = selectedFeatures[currentFeatureKey] !== undefined;

  const getFeatureSVG = (featureKey, option) => {
    const svgMap = {
      faceShape: faceShapes,
      eyeShape: eyeShapes,
      noseType: noseTypes,
      mouthShape: mouthShapes,
      eyebrows: eyebrowTypes
    };
    return svgMap[featureKey]?.[option] || null;
  };

  const getFeatureEmoji = (featureKey) => {
    const emojiMap = {
      complexion: '🎨',
      hairType: '💇',
      facialHair: '🧔',
      distinctiveMarks: '⚠️'
    };
    return emojiMap[featureKey] || '👤';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Left Panel - Feature Selection */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-2xl font-bold text-gray-900">
              {currentFeatureData.label}
            </h2>
            <span className="text-sm text-gray-500">
              {currentFeature + 1} of {featureKeys.length}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentFeature + 1) / featureKeys.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Option Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {currentFeatureData.options.map((option) => {
            const svgContent = getFeatureSVG(currentFeatureKey, option);
            return (
              <button
                key={option}
                onClick={() => handleSelectOption(option)}
                className={`
                  p-4 rounded-lg border-2 transition-all duration-200
                  hover:border-blue-400 hover:shadow-md
                  ${selectedFeatures[currentFeatureKey] === option
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 bg-white'
                  }
                `}
              >
                <div className="text-center">
                  {svgContent ? (
                    <div
                      className="w-full h-24 mb-2 flex items-center justify-center"
                      dangerouslySetInnerHTML={{ __html: svgContent }}
                    />
                  ) : (
                    <div className="w-full h-24 bg-gray-100 rounded-md mb-2 flex items-center justify-center">
                      <span className="text-2xl text-gray-400">
                        {getFeatureEmoji(currentFeatureKey)}
                      </span>
                    </div>
                  )}
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {option}
                  </p>
                </div>
              </button>
            );
          })}
        </div>

        {/* Navigation Buttons */}
        <div className="flex justify-between items-center">
          <button
            onClick={handleBack}
            disabled={currentFeature === 0}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Back
          </button>

          {isLastFeature && hasSelectedCurrentFeature ? (
            <button
              onClick={handleComplete}
              className="px-6 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
            >
              Complete Selection →
            </button>
          ) : (
            <button
              onClick={() => handleSelectOption(selectedFeatures[currentFeatureKey])}
              disabled={!hasSelectedCurrentFeature}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          )}
        </div>
      </div>

      {/* Right Panel - Preview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Preview
        </h2>

        {/* Composite Preview */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Layered Composition
          </h3>
          <div className="bg-gray-100 rounded-lg p-4 aspect-square flex items-center justify-center">
            {isGenerating ? (
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-2"></div>
                <p className="text-sm text-gray-600">Generating preview...</p>
              </div>
            ) : compositePreview ? (
              <img
                src={compositePreview}
                alt="Composite preview"
                className="max-w-full max-h-full rounded"
              />
            ) : (
              <p className="text-gray-400">
                Preview will appear as you select features
              </p>
            )}
          </div>
        </div>

        {/* Selected Features Summary */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Selected Features
          </h3>
          <div className="space-y-2">
            {featureKeys.map((key) => (
              <div
                key={key}
                className={`
                  flex justify-between items-center p-2 rounded
                  ${selectedFeatures[key] ? 'bg-blue-50' : 'bg-gray-50'}
                `}
              >
                <span className="text-sm text-gray-700 capitalize">
                  {FEATURE_OPTIONS[key].label}:
                </span>
                <span className="text-sm font-medium text-gray-900 capitalize">
                  {selectedFeatures[key] || '-'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default FeatureSelector;
