import streamlit as st
import pytesseract
from PIL import Image
import io
import time
import subprocess
import sys
import os

# Set page configuration
st.set_page_config(
    page_title="OCR Text Extractor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to check if Tesseract is installed and install it if not
def install_tesseract():
    try:
        # Check if Tesseract is already installed
        subprocess.run(["tesseract", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        st.warning("Tesseract-OCR is not installed. Attempting to install...")
        
        try:
            # Update package list and install Tesseract
            subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True, capture_output=True)
            st.success("Tesseract-OCR installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to install Tesseract-OCR: {e}")
            return False

# Check and install Tesseract if needed
if install_tesseract():
    st.success("Tesseract-OCR is ready to use!")
else:
    st.error("""
    **Tesseract-OCR installation failed!**
    
    Please install Tesseract-OCR manually on your system:
    - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
    - **Mac**: `brew install tesseract`
    - **Linux**: `sudo apt-get install tesseract-ocr`
    """)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="main-header">📝 Image to Text OCR Extractor</h1>', unsafe_allow_html=True)
st.markdown("""
Upload an image containing text, and this app will extract the text using Optical Character Recognition (OCR) technology.
Supported formats: PNG, JPG, JPEG.
""")

# Sidebar for additional options
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    # OCR language selection
    languages = {
        "English": "eng",
        "Spanish": "spa",
        "French": "fra",
        "German": "deu",
        "Chinese": "chi_sim",
        "Japanese": "jpn",
        "Korean": "kor"
    }
    selected_lang = st.selectbox(
        "Select Language",
        options=list(languages.keys()),
        index=0,
        help="Select the language of the text in your image"
    )
    
    # OCR configuration options
    st.subheader("Advanced Options")
    use_advanced = st.checkbox("Show advanced options", value=False)
    
    if use_advanced:
        config_options = st.text_area(
            "Tesseract Configuration",
            value="--psm 6",
            help="Custom Tesseract configuration parameters"
        )
    else:
        config_options = "--psm 6"

# File upload section
st.markdown("---")
st.subheader("📤 Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Display image and processing
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Image info
        st.write(f"**Image format:** {image.format}")
        st.write(f"**Image size:** {image.size[0]} x {image.size[1]} pixels")
        st.write(f"**Image mode:** {image.mode}")

    with col2:
        st.subheader("📝 Extracted Text")
        
        # Progress bar and status
        with st.status("Processing image...", expanded=True) as status:
            st.write("Reading image...")
            time.sleep(0.5)
            
            st.write("Performing OCR...")
            progress_bar = st.progress(0)
            
            try:
                # Simulate progress
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Perform OCR with selected language
                text = pytesseract.image_to_string(
                    image, 
                    lang=languages[selected_lang],
                    config=config_options
                )
                
                status.update(label="OCR Complete!", state="complete", expanded=False)
                
            except pytesseract.TesseractNotFoundError:
                status.update(label="Error!", state="error")
                st.error("""
                **Tesseract-OCR not found!**
                
                Please install Tesseract-OCR on your system:
                - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
                - **Mac**: `brew install tesseract`
                - **Linux**: `sudo apt-get install tesseract-ocr`
                """)
                
            except Exception as e:
                status.update(label="Error!", state="error")
                st.error(f"An error occurred during OCR: {str(e)}")

        # Display extracted text if successful
        if 'text' in locals() and text.strip():
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.success("✅ Text successfully extracted!")
            
            # Text area for easy copying
            extracted_text = st.text_area(
                "Extracted Text:",
                value=text,
                height=300,
                label_visibility="collapsed"
            )
            
            # Text statistics
            st.write(f"**Character count:** {len(text)}")
            st.write(f"**Word count:** {len(text.split())}")
            st.write(f"**Line count:** {len(text.splitlines())}")
            
            # Download button for extracted text
            st.download_button(
                label="📥 Download Text",
                data=text,
                file_name="extracted_text.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        elif 'text' in locals():
            st.warning("⚠️ No text was detected in the image. Please try with a different image or adjust the language settings.")

# Add some helpful tips
with st.expander("💡 Tips for Better OCR Results"):
    st.markdown("""
    - Use high-quality images with good lighting
    - Ensure text is clear and not blurred
    - Use images with high contrast (black text on white background works best)
    - For handwritten text, use the appropriate language setting
    - If results are poor, try different PSM modes in advanced settings
    - For multi-language text, you may need to install additional language packs
    """)

# Footer
st.markdown("---")
st.caption("Built with Streamlit & PyTesseract | OCR Text Extraction Tool")
