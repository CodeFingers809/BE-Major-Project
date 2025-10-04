import React, { useState } from 'react';
import FeatureSelector from './components/FeatureSelector';
import SketchCanvas from './components/SketchCanvas';
import ColorPanel from './components/ColorPanel';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [compositeImage, setCompositeImage] = useState(null);
  const [sketchImage, setSketchImage] = useState(null);
  const [sketchDescription, setSketchDescription] = useState('');
  const [finalImage, setFinalImage] = useState(null);

  const handleFeaturesComplete = (features, composite) => {
    setSelectedFeatures(features);
    setCompositeImage(composite);
    setCurrentStep(2);
  };

  const handleSketchComplete = (sketch, description) => {
    setSketchImage(sketch);
    setSketchDescription(description);
    setCurrentStep(3);
  };

  const handleColorComplete = (colored) => {
    setFinalImage(colored);
  };

  const resetWorkflow = () => {
    setCurrentStep(1);
    setSelectedFeatures({});
    setCompositeImage(null);
    setSketchImage(null);
    setSketchDescription('');
    setFinalImage(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Criminal Face Generation System
          </h1>
          <p className="mt-1 text-sm text-gray-600">
            Law enforcement facial composite generation
          </p>
        </div>
      </header>

      {/* Progress Indicator */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <StepIndicator step={1} currentStep={currentStep} label="Select Features" />
            <div className="h-0.5 w-16 bg-gray-300" />
            <StepIndicator step={2} currentStep={currentStep} label="Generate Sketch" />
            <div className="h-0.5 w-16 bg-gray-300" />
            <StepIndicator step={3} currentStep={currentStep} label="Colorize" />
          </div>
          <button
            onClick={resetWorkflow}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Start Over
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentStep === 1 && (
          <FeatureSelector onComplete={handleFeaturesComplete} />
        )}
        {currentStep === 2 && (
          <SketchCanvas
            compositeImage={compositeImage}
            selectedFeatures={selectedFeatures}
            onComplete={handleSketchComplete}
            onBack={() => setCurrentStep(1)}
          />
        )}
        {currentStep === 3 && (
          <ColorPanel
            sketchImage={sketchImage}
            description={sketchDescription}
            onComplete={handleColorComplete}
            onBack={() => setCurrentStep(2)}
          />
        )}
      </main>
    </div>
  );
}

function StepIndicator({ step, currentStep, label }) {
  const isActive = step === currentStep;
  const isCompleted = step < currentStep;

  return (
    <div className="flex items-center">
      <div
        className={`
          flex items-center justify-center w-10 h-10 rounded-full font-semibold
          ${isActive ? 'bg-blue-600 text-white' : ''}
          ${isCompleted ? 'bg-green-600 text-white' : ''}
          ${!isActive && !isCompleted ? 'bg-gray-200 text-gray-600' : ''}
        `}
      >
        {isCompleted ? '✓' : step}
      </div>
      <span
        className={`
          ml-2 text-sm font-medium
          ${isActive ? 'text-blue-600' : 'text-gray-600'}
        `}
      >
        {label}
      </span>
    </div>
  );
}

export default App;
