import streamlit as st
from PIL import Image
import os

# Try to use pytesseract if available, otherwise show installation instructions
try:
    import pytesseract
    
    # Check if Tesseract is available
    try:
        pytesseract.get_tesseract_version()
        tesseract_available = True
    except:
        tesseract_available = False
        
except ImportError:
    st.error("pytesseract not installed. Please add it to requirements.txt")
    st.stop()

st.title("Simple OCR App")

if not tesseract_available:
    st.error("""
    Tesseract-OCR is not available in this environment.
    
    For local development, install Tesseract:
    - **Linux**: `sudo apt-get install tesseract-ocr`
    - **Mac**: `brew install tesseract`
    - **Windows**: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
    
    For Streamlit Cloud deployment, use the alternative OCR option below.
    """)
    
    # Alternative: Use OCR.space API (free)
    st.info("Alternative: Using online OCR API (requires internet connection)")
    use_online_ocr = st.checkbox("Use online OCR API instead")
    
    if not use_online_ocr:
        st.stop()

# File upload
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            try:
                if tesseract_available:
                    # Use local Tesseract
                    text = pytesseract.image_to_string(image)
                else:
                    # Use online OCR fallback
                    text = extract_text_with_online_ocr(image)
                
                if text.strip():
                    st.success("Text extracted successfully!")
                    st.text_area("Extracted Text", text, height=200)
                else:
                    st.warning("No text found in the image")
            except Exception as e:
                st.error(f"Error: {e}")

# Online OCR fallback function
def extract_text_with_online_ocr(image):
    """Fallback to online OCR service"""
    try:
        import requests
        import base64
        from io import BytesIO
        
        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Use OCR.space API (free)
        payload = {
            'apikey': 'helloworld',  # Free key
            'base64Image': f'data:image/png;base64,{img_str}',
            'language': 'eng'
        }
        
        response = requests.post(
            'https://api.ocr.space/parse/image',
            data=payload,
            timeout=30
        )
        
        result = response.json()
        if result['IsErroredOnProcessing']:
            return "Error in OCR processing"
        
        return result['ParsedResults'][0]['ParsedText']
        
    except Exception as e:
        return f"Online OCR failed: {str(e)}"
