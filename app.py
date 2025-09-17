import streamlit as st
import pytesseract
from PIL import Image
import subprocess

# Check if Tesseract is installed
def check_tesseract():
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Main app
st.title("Simple OCR App")

# Check Tesseract installation
if not check_tesseract():
    st.error("Tesseract-OCR is not installed. Please install it:")
    st.code("sudo apt-get update && sudo apt-get install -y tesseract-ocr")
    st.stop()

# File upload
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract text
    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            try:
                text = pytesseract.image_to_string(image)
                if text.strip():
                    st.success("Text extracted successfully!")
                    st.text_area("Extracted Text", text, height=200)
                else:
                    st.warning("No text found in the image")
            except Exception as e:
                st.error(f"Error: {e}")
