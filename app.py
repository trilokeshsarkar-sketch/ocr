import streamlit as st
import pytesseract
from PIL import Image

# Configure PyTesseract if Tesseract-OCR is not in system PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

st.title("Image to Text OCR App")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Extracting text...")

    try:
        text = pytesseract.image_to_string(image)
        st.write("Extracted Text:")
        st.code(text)
    except pytesseract.TesseractNotFoundError:
        st.error("Tesseract-OCR is not installed or not found in your system's PATH. Please install it or configure pytesseract.pytesseract.tesseract_cmd.")
    except Exception as e:
        st.error(f"An error occurred during OCR: {e}")
