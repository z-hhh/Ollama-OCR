import streamlit as st
from ocr_processor import OCRProcessor
import tempfile
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="OCR with Ollama",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
        border: 2px dashed #ccc;
        border-radius: 10px;
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_available_models():
    return ["llava:7b", "llama3.2-vision:11b"]

def main():
    # Header with cool emoji and styling
    st.markdown("<h1 style='text-align: center;'>🔍 Vision OCR Lab</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Powered by Ollama Vision Models</p>", unsafe_allow_html=True)

    # Sidebar with gradient background
    with st.sidebar:
        st.markdown("""
            <div style='background: linear-gradient(to right, #4CAF50, #45a049); padding: 1rem; border-radius: 5px; color: white;'>
                <h2 style='margin:0'>🎮 Controls</h2>
            </div>
        """, unsafe_allow_html=True)
        
        selected_model = st.selectbox(
            "🤖 Select Vision Model",
            get_available_models(),
            index=0,
        )
        
        format_type = st.selectbox(
            "📄 Output Format",
            ["markdown", "text", "json", "structured", "key_value"],
            help="Choose how you want the extracted text to be formatted"
        )
        
        st.markdown("---")
        
        # Model info box
        st.markdown(f"""
            <div style='background-color: #f1f3f4; padding: 1rem; border-radius: 5px;'>
                <h4>Selected Model: {selected_model}</h4>
                <p style='font-size: 0.9em; color: #666;'>
                    A powerful vision model for accurate text extraction
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Initialize OCR Processor
    processor = OCRProcessor(model_name=selected_model)

    # Main content area with tabs
    tab1, tab2 = st.tabs(["📸 Image Processing", "ℹ️ About"])
    
    with tab1:
        # File upload area with drag & drop
        uploaded_file = st.file_uploader(
            "Drop your image here",
            type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
            help="Supported formats: PNG, JPG, JPEG, TIFF, BMP"
        )

        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("<h3 style='text-align: center;'>📸 Input Image</h3>", unsafe_allow_html=True)
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                
                # Image info in a nice box
                st.markdown(f"""
                    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                        <h4>Image Details</h4>
                        <p>Size: {image.size}</p>
                        <p>Format: {image.format}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<h3 style='text-align: center;'>📝 Extracted Text</h3>", unsafe_allow_html=True)
                with st.spinner(f"✨ Magic happening with {selected_model}..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_path = tmp_file.name

                    try:
                        result = processor.process_image(temp_path, format_type)
                        
                        # Result container with styling
                        st.markdown("""
                            <div style='background-color: white; padding: 1rem; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        """, unsafe_allow_html=True)
                        
                        if format_type == "markdown":
                            st.markdown(result)
                        elif format_type == "json":
                            st.json(result)
                        else:
                            st.text_area("", value=result, height=400)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Download button with styling
                        st.download_button(
                            label="📥 Download Extracted Text",
                            data=result,
                            file_name=f"extracted_text_{format_type}.txt",
                            mime="text/plain",
                        )
                    finally:
                        os.unlink(temp_path)
        else:
            # Placeholder with nice styling
            st.markdown("""
                <div class='upload-text'>
                    <h3>👆 Upload an Image to Start</h3>
                    <p style='color: #666;'>Drag and drop your image here or click to browse</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
            <div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2>About Vision OCR Lab</h2>
                <p>This tool uses state-of-the-art vision models to extract text from images:</p>
                <ul>
                    <li><strong>llava:7b</strong> - A powerful vision-language model</li>
                    <li><strong>llama3.2-vision:11b</strong> - Advanced vision model with high accuracy</li>
                </ul>
                <h3>Output Formats</h3>
                <ul>
                    <li><strong>Markdown</strong> - Formatted text with headers and lists</li>
                    <li><strong>Text</strong> - Plain text extraction</li>
                    <li><strong>JSON</strong> - Structured data format</li>
                    <li><strong>Structured</strong> - Tables and organized data</li>
                    <li><strong>Key-Value</strong> - Paired information extraction</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()