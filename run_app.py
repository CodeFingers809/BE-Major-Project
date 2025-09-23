#!/usr/bin/env python3
"""
Simple script to run the Streamlit app
"""

import subprocess
import sys

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        print("Starting Criminal Face Generation System...")
        print("The app will open in your browser automatically.")
        print("Press Ctrl+C to stop the application.")

        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])

    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    run_streamlit_app()