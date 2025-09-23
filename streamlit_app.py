import streamlit as st
import requests
import urllib.parse
from PIL import Image
import io
import time
import base64
from typing import Dict, Optional

class CriminalFaceSketchGenerator:
    """
    Criminal face sketch generator for Streamlit UI
    """

    def __init__(self):
        self.session_state = st.session_state
        if 'generated_sketches' not in self.session_state:
            self.session_state.generated_sketches = []
        if 'current_sketch' not in self.session_state:
            self.session_state.current_sketch = None
        if 'final_image' not in self.session_state:
            self.session_state.final_image = None

    def generate_sketch_from_description(self, description: str) -> Optional[Dict]:
        """
        Generate a black and white sketch from text description optimized for Indian faces
        """
        try:
            # Enhanced prompt for Indian criminal sketch generation
            sketch_prompt = f"black and white pencil sketch of an Indian person, {description}, police sketch artist drawing, detailed facial features, South Asian features, realistic proportions, line art sketch on paper, monochrome drawing, criminal identification sketch"

            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(sketch_prompt)

            # Using Pollinations.ai for sketch generation
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={int(time.time())}"

            with st.spinner("Generating sketch..."):
                response = requests.get(image_url, timeout=30)

            if response.status_code == 200:
                # Convert to PIL Image
                image = Image.open(io.BytesIO(response.content))

                sketch_data = {
                    "description": description,
                    "image": image,
                    "prompt": sketch_prompt,
                    "timestamp": int(time.time())
                }

                self.session_state.generated_sketches.append(sketch_data)
                self.session_state.current_sketch = sketch_data

                return sketch_data
            else:
                st.error(f"Failed to generate sketch. Status code: {response.status_code}")
                return None

        except Exception as e:
            st.error(f"Error generating sketch: {str(e)}")
            return None

    def refine_sketch(self, current_sketch: Dict, additional_description: str) -> Optional[Dict]:
        """
        Refine the current sketch with additional description
        """
        if not current_sketch:
            st.error("No current sketch to refine")
            return None

        original_desc = current_sketch["description"]
        combined_description = f"{original_desc}, {additional_description}"

        return self.generate_sketch_from_description(combined_description)

    def generate_colored_image(self, sketch_data: Dict) -> Optional[Dict]:
        """
        Generate a colored realistic mugshot-style image from the sketch description
        """
        try:
            # Enhanced prompt for realistic Indian criminal mugshot
            color_prompt = f"police mugshot photograph of an Indian person, {sketch_data['description']}, frontal view, neutral expression, harsh police station lighting, plain background, realistic Indian skin tone, South Asian facial features, criminal booking photo, high resolution, sharp focus, documentary photography style"

            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(color_prompt)

            # Using Pollinations.ai for colored image generation
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={sketch_data['timestamp']}"

            with st.spinner("Generating colored image..."):
                response = requests.get(image_url, timeout=30)

            if response.status_code == 200:
                # Convert to PIL Image
                image = Image.open(io.BytesIO(response.content))

                colored_data = {
                    "description": sketch_data["description"],
                    "image": image,
                    "prompt": color_prompt,
                    "timestamp": int(time.time()),
                    "based_on_sketch": True
                }

                self.session_state.final_image = colored_data

                return colored_data
            else:
                st.error(f"Failed to generate colored image. Status code: {response.status_code}")
                return None

        except Exception as e:
            st.error(f"Error generating colored image: {str(e)}")
            return None

def main():
    st.set_page_config(
        page_title="Criminal Face Generation System",
        layout="wide"
    )

    st.title("Criminal Face Generation System")
    st.markdown("Generate faces from witness descriptions for law enforcement")
    st.markdown("Workflow: Description → Sketch → Revisions → Final Image")

    # Initialize the generator
    generator = CriminalFaceSketchGenerator()

    # Create three columns for the workflow
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("1. Description to Sketch")

        # Text input for witness description
        description = st.text_area(
            "Enter witness description:",
            placeholder="e.g., male, dark hair, mustache, scar on forehead, around 35 years old, wheatish complexion",
            height=100
        )

        # Common facial features for quick selection
        st.subheader("Common Features")

        col1a, col1b = st.columns(2)

        with col1a:
            complexion = st.selectbox(
                "Complexion:",
                ["", "fair", "wheatish", "dusky", "dark"],
                index=0
            )

            facial_hair = st.selectbox(
                "Facial Hair:",
                ["", "clean shaven", "mustache", "beard", "goatee", "stubble"],
                index=0
            )

        with col1b:
            hair_type = st.selectbox(
                "Hair:",
                ["", "straight black hair", "curly hair", "wavy hair", "receding hairline", "bald"],
                index=0
            )

            distinctive_marks = st.selectbox(
                "Distinctive Marks:",
                ["", "scar on face", "mole on cheek", "broken nose", "missing tooth", "birthmark"],
                index=0
            )

        # Auto-append selected features to description
        feature_additions = []
        if complexion: feature_additions.append(f"{complexion} complexion")
        if facial_hair: feature_additions.append(facial_hair)
        if hair_type: feature_additions.append(hair_type)
        if distinctive_marks: feature_additions.append(distinctive_marks)

        if feature_additions:
            enhanced_description = description + ", " + ", ".join(feature_additions) if description else ", ".join(feature_additions)
        else:
            enhanced_description = description

        if st.button("Generate Sketch", type="primary"):
            if enhanced_description.strip():
                sketch_data = generator.generate_sketch_from_description(enhanced_description.strip())
                if sketch_data:
                    st.success("Sketch generated")
            else:
                st.warning("Please enter a description first")

        # Show the enhanced description being used
        if enhanced_description and enhanced_description != description:
            st.info(f"Using enhanced description: {enhanced_description}")

        # Display current sketch
        if generator.session_state.current_sketch:
            st.subheader("Current Sketch")
            st.image(
                generator.session_state.current_sketch["image"],
                caption=f"Sketch: {generator.session_state.current_sketch['description'][:50]}...",
                use_column_width=True
            )

    with col2:
        st.header("2. Sketch Refinement")

        if generator.session_state.current_sketch:
            st.write("**Current description:**")
            st.write(generator.session_state.current_sketch["description"])

            # Additional description for refinement
            additional_desc = st.text_area(
                "Add more details to refine the sketch:",
                placeholder="e.g., thick eyebrows, slightly crooked nose, deep-set eyes",
                height=80
            )

            if st.button("Refine Sketch"):
                if additional_desc.strip():
                    refined_sketch = generator.refine_sketch(
                        generator.session_state.current_sketch,
                        additional_desc.strip()
                    )
                    if refined_sketch:
                        st.success("Sketch refined")
                        st.rerun()
                else:
                    st.warning("Please enter additional details")

            # Show sketch history
            if len(generator.session_state.generated_sketches) > 1:
                st.subheader("Sketch History")
                for i, sketch in enumerate(reversed(generator.session_state.generated_sketches[-3:])):
                    with st.expander(f"Version {len(generator.session_state.generated_sketches) - i}"):
                        st.image(sketch["image"], use_column_width=True)
                        st.caption(sketch["description"][:100] + "...")
        else:
            st.info("Generate a sketch first to enable refinement")

    with col3:
        st.header("3. Generate Colored Image")

        if generator.session_state.current_sketch:
            st.write("**Ready to generate colored image from:**")
            st.write(generator.session_state.current_sketch["description"][:100] + "...")

            if st.button("Generate Colored Image", type="primary"):
                colored_image = generator.generate_colored_image(generator.session_state.current_sketch)
                if colored_image:
                    st.success("Final image generated")

            # Display final colored image
            if generator.session_state.final_image:
                st.subheader("Final Image")
                st.image(
                    generator.session_state.final_image["image"],
                    caption="Generated final image",
                    use_column_width=True
                )

                # Download button
                img_buffer = io.BytesIO()
                generator.session_state.final_image["image"].save(img_buffer, format="PNG")
                st.download_button(
                    label="Download Image",
                    data=img_buffer.getvalue(),
                    file_name=f"generated_face_{int(time.time())}.png",
                    mime="image/png"
                )
        else:
            st.info("Generate and refine a sketch first")

    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.markdown("""
        **About This System**

        This is a prototype system for generating criminal faces from witness descriptions.

        **How it works:**
        1. Enter witness description
        2. Select common facial features
        3. Generate initial sketch
        4. Refine with additional details
        5. Generate final colored image

        **Features:**
        - Text to sketch generation
        - Sketch refinement
        - Color image generation
        - Image download
        - Session history

        **Technical Details:**
        - Uses Pollinations.ai API
        - Built with Streamlit framework
        - Image processing with PIL
        - Real-time generation
        """)

        if st.button("Clear All", type="secondary"):
            # Clear session state
            generator.session_state.generated_sketches = []
            generator.session_state.current_sketch = None
            generator.session_state.final_image = None
            st.rerun()

        # Display session statistics
        st.subheader("Session Stats")
        st.metric("Sketches Generated", len(generator.session_state.generated_sketches))
        st.metric("Has Final Image", "Yes" if generator.session_state.final_image else "No")

if __name__ == "__main__":
    main()