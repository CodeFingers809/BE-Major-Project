#!/usr/bin/env python3
"""
Criminal Face Generation Prototype
A proof-of-concept for generating criminal faces from witness descriptions
using free image generation APIs.
"""

import requests
import json
import base64
import os
from typing import Dict, List, Optional
import time

class CriminalFaceGenerator:
    """
    Main class for generating criminal faces from text descriptions
    """

    def __init__(self):
        self.generated_faces = []
        self.face_database = []

    def generate_face_from_description(self, description: str) -> Dict:
        """
        Generate a face image from text description using Pollinations.ai free API
        """
        print(f"Generating face from description: {description}")

        # Using Pollinations.ai free API (no auth required)
        base_url = "https://image.pollinations.ai/prompt/"

        # Enhance the prompt for better face generation
        enhanced_prompt = f"realistic portrait photograph of a person, {description}, high quality, detailed facial features, professional headshot, neutral expression, photorealistic"

        # URL encode the prompt
        import urllib.parse
        encoded_prompt = urllib.parse.quote(enhanced_prompt)

        # Construct the full URL
        image_url = f"{base_url}{encoded_prompt}?width=512&height=512&seed=42"

        try:
            print("Requesting image generation...")
            response = requests.get(image_url, timeout=30)

            if response.status_code == 200:
                # Save the generated image
                timestamp = int(time.time())
                filename = f"generated_face_{timestamp}.jpg"

                with open(filename, "wb") as f:
                    f.write(response.content)

                face_data = {
                    "description": description,
                    "filename": filename,
                    "timestamp": timestamp,
                    "enhanced_prompt": enhanced_prompt
                }

                self.generated_faces.append(face_data)
                print(f"Face generated successfully: {filename}")
                return face_data

            else:
                print(f"Error generating image: {response.status_code}")
                return self._create_mock_face_data(description)

        except Exception as e:
            print(f"Error connecting to API: {e}")
            return self._create_mock_face_data(description)

    def _create_mock_face_data(self, description: str) -> Dict:
        """Create mock face data when API is unavailable"""
        timestamp = int(time.time())
        face_data = {
            "description": description,
            "filename": f"mock_face_{timestamp}.jpg",
            "timestamp": timestamp,
            "enhanced_prompt": f"Mock generated face for: {description}",
            "mock": True
        }
        self.generated_faces.append(face_data)
        print(f"Created mock face data for demo purposes")
        return face_data

    def refine_face(self, face_data: Dict, additional_description: str) -> Dict:
        """
        Refine an existing generated face with additional description
        """
        original_desc = face_data["description"]
        combined_description = f"{original_desc}, {additional_description}"

        print(f"Refining face with additional details: {additional_description}")
        return self.generate_face_from_description(combined_description)

    def search_similar_faces(self, target_description: str, crime_type: str = None, location: str = None) -> List[Dict]:
        """
        Mock implementation of face similarity search in criminal database
        """
        print(f"Searching for similar faces...")
        print(f"Target: {target_description}")
        if crime_type:
            print(f"Crime type filter: {crime_type}")
        if location:
            print(f"Location filter: {location}")

        # Mock criminal database
        mock_database = [
            {"id": 1, "description": "male, brown hair, beard, scar on left cheek", "crime_type": "robbery", "location": "downtown"},
            {"id": 2, "description": "female, blonde hair, blue eyes, small nose", "crime_type": "fraud", "location": "suburbs"},
            {"id": 3, "description": "male, black hair, brown eyes, thick eyebrows", "crime_type": "assault", "location": "downtown"},
            {"id": 4, "description": "male, grey hair, mustache, wrinkles", "crime_type": "robbery", "location": "city center"},
        ]

        # Simple keyword-based similarity (in real implementation, use facial recognition)
        similar_faces = []
        target_keywords = target_description.lower().split()

        for criminal in mock_database:
            # Apply filters
            if crime_type and criminal["crime_type"] != crime_type:
                continue
            if location and criminal["location"] != location:
                continue

            # Calculate simple similarity score
            criminal_keywords = criminal["description"].lower().split()
            common_keywords = set(target_keywords) & set(criminal_keywords)
            similarity_score = len(common_keywords) / len(set(target_keywords) | set(criminal_keywords))

            if similarity_score > 0.2:  # Threshold for similarity
                criminal["similarity_score"] = similarity_score
                similar_faces.append(criminal)

        # Sort by similarity score
        similar_faces.sort(key=lambda x: x["similarity_score"], reverse=True)

        print(f"Found {len(similar_faces)} similar faces in database")
        return similar_faces

    def demonstrate_workflow(self):
        """
        Demonstrate the complete workflow of the system
        """
        print("=== Criminal Face Generation System Demo ===\n")

        # Step 1: Generate face from witness description
        print("Step 1: Generating face from witness description")
        witness_description = "male, brown hair, beard, scar on left cheek, approximately 30 years old"
        generated_face = self.generate_face_from_description(witness_description)
        print(f"Generated face: {generated_face['filename']}\n")

        # Step 2: Refine the face with additional details
        print("Step 2: Refining face with additional witness details")
        additional_details = "thick eyebrows, slightly crooked nose"
        refined_face = self.refine_face(generated_face, additional_details)
        print(f"Refined face: {refined_face['filename']}\n")

        # Step 3: Search for similar faces in criminal database
        print("Step 3: Searching for similar faces in criminal database")
        similar_faces = self.search_similar_faces(
            target_description=refined_face["description"],
            crime_type="robbery",
            location="downtown"
        )

        print("\nSimilar faces found:")
        for i, face in enumerate(similar_faces[:3], 1):
            print(f"{i}. ID: {face['id']}, Similarity: {face['similarity_score']:.2f}")
            print(f"   Description: {face['description']}")
            print(f"   Crime: {face['crime_type']}, Location: {face['location']}\n")

        print("=== Demo Complete ===")
        return {
            "generated_face": generated_face,
            "refined_face": refined_face,
            "similar_faces": similar_faces
        }

def main():
    """Main function to run the demonstration"""
    generator = CriminalFaceGenerator()

    print("Criminal Face Generation Prototype")
    print("This is a proof-of-concept demonstration\n")

    try:
        # Run the complete demonstration
        results = generator.demonstrate_workflow()

        print(f"\nGenerated {len(generator.generated_faces)} faces during demo")
        print("Note: This is a research prototype for demonstration purposes only")

    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error during demo: {e}")

if __name__ == "__main__":
    main()