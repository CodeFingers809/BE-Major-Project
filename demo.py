#!/usr/bin/env python3
"""
Simple demo script to test the criminal face generator
"""

from criminal_face_generator import CriminalFaceGenerator

def interactive_demo():
    """Interactive demo allowing user input"""
    generator = CriminalFaceGenerator()

    print("=== Interactive Criminal Face Generator Demo ===")
    print("Enter witness descriptions to generate faces\n")

    while True:
        print("\nOptions:")
        print("1. Generate face from description")
        print("2. Search similar faces")
        print("3. Run full demo")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            description = input("Enter witness description: ").strip()
            if description:
                face_data = generator.generate_face_from_description(description)
                print(f"Generated face saved as: {face_data['filename']}")

        elif choice == "2":
            description = input("Enter description to search for: ").strip()
            crime_type = input("Enter crime type (optional): ").strip() or None
            location = input("Enter location (optional): ").strip() or None

            similar_faces = generator.search_similar_faces(description, crime_type, location)

            if similar_faces:
                print(f"\nFound {len(similar_faces)} similar faces:")
                for i, face in enumerate(similar_faces, 1):
                    print(f"{i}. Similarity: {face['similarity_score']:.2f}")
                    print(f"   Description: {face['description']}")
            else:
                print("No similar faces found")

        elif choice == "3":
            generator.demonstrate_workflow()

        elif choice == "4":
            print("Exiting demo...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    interactive_demo()