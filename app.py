import streamlit as st
import subprocess
import os
import shutil
import zipfile
import io
import time
from PIL import Image

# Configuration
TOOL_PATH = "GeminiWatermarkTool.exe"
TEMP_DIR = "temp_uploads"

# Ensure temp directory exists (safely)
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
else:
    # Try to clean old files but don't fail if locked
    try:
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            try:
                if os.path.isfile(filepath):
                    os.unlink(filepath)
            except Exception:
                pass  # Skip locked files
    except Exception:
        pass

st.set_page_config(
    page_title="Gemini Watermark Remover",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS for Modern UI with Theme Support
def get_theme_css(dark_mode=False):
    if dark_mode:
        # Dark Theme
        return """
<style>
    /* Dark Neo Brutalism Theme */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
        font-family: 'Courier New', Courier, monospace;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    h1 {
        font-weight: 900;
        text-transform: uppercase;
        border: 4px solid #f1f5f9;
        padding: 1rem;
        background-color: #7c3aed;
        box-shadow: 8px 8px 0px #f1f5f9;
        color: #f1f5f9;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMarkdown p {
        font-size: 1.1rem;
        font-weight: 500;
        color: #e2e8f0;
    }
    .stButton button {
        background-color: #3b82f6;
        color: #f1f5f9;
        border: 3px solid #f1f5f9;
        border-radius: 0px;
        padding: 0.75rem 1.5rem;
        font-weight: 800;
        box-shadow: 5px 5px 0px #f1f5f9;
        transition: all 0.1s ease;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #f1f5f9;
        background-color: #2563eb;
        border-color: #f1f5f9;
    }
    .stButton button:active {
        transform: translate(2px, 2px);
        box-shadow: 3px 3px 0px #f1f5f9;
    }
    div[data-testid="stFileUploader"] {
        border: 3px solid #f1f5f9;
        background-color: #1e293b;
        box-shadow: 6px 6px 0px #f1f5f9;
        padding: 1rem;
        border-radius: 0px;
    }
    div[data-testid="stFileUploader"] label {
        color: #f1f5f9 !important;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    .stDownloadButton button {
        background-color: #10b981;
        border: 3px solid #f1f5f9;
        color: #f1f5f9;
        font-weight: 800;
        box-shadow: 5px 5px 0px #f1f5f9;
        border-radius: 0;
    }
    .stDownloadButton button:hover {
        box-shadow: 7px 7px 0px #f1f5f9;
        background-color: #059669;
        border-color: #f1f5f9;
    }
    img {
        border: 3px solid #f1f5f9;
        box-shadow: 5px 5px 0px #f1f5f9;
        border-radius: 0px;
    }
    /* Radio Button Style */
    div[role="radiogroup"] label {
        color: #f1f5f9 !important;
        font-weight: bold;
    }
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background-color: #fbbf24;
        border: 3px solid #f1f5f9;
        color: #0f172a;
        padding: 0.5rem;
        font-weight: bold;
        box-shadow: 4px 4px 0px #f1f5f9;
        cursor: pointer;
    }
    /* Subtitle box for dark mode */
    .subtitle-dark {
        border: 3px solid #f1f5f9;
        padding: 1rem;
        background-color: #1e293b;
        box-shadow: 6px 6px 0px #f1f5f9;
        margin-bottom: 2rem;
        color: #f1f5f9;
        font-weight: bold;
        text-align: center;
    }
    /* Text color fixes */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #f1f5f9 !important;
    }
    .stText {
        color: #f1f5f9 !important;
    }
    /* File uploader text */
    div[data-testid="stFileUploader"] > div > div > div > div {
        color: #f1f5f9 !important;
    }
    /* File uploader Browse button */
    div[data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #f1f5f9 !important;
        border: 3px solid #f1f5f9 !important;
        box-shadow: 4px 4px 0px #f1f5f9 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #2563eb !important;
        box-shadow: 5px 5px 0px #f1f5f9 !important;
    }
    /* File uploader small text */
    div[data-testid="stFileUploader"] small {
        color: #cbd5e1 !important;
    }
    /* Progress bar text */
    .stProgress > div > div > div {
        color: #f1f5f9 !important;
    }
    /* Info/Success/Error messages */
    .stAlert {
        border: 3px solid #f1f5f9;
        box-shadow: 4px 4px 0px #f1f5f9;
        border-radius: 0;
    }
    /* Divider */
    hr {
        border-color: #475569 !important;
    }
    /* Container borders */
    .element-container {
        color: #f1f5f9 !important;
    }
    /* Caption text */
    .caption {
        color: #cbd5e1 !important;
    }
    /* Radio button text (Language toggle) */
    div[role="radiogroup"] label p {
        color: #f1f5f9 !important;
    }
    div[role="radiogroup"] input[type="radio"] + div {
        color: #f1f5f9 !important;
    }
    /* Radio button selected state */
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #7c3aed !important;
        border-color: #f1f5f9 !important;
    }
    /* Header menu (hamburger menu) */
    button[kind="header"] {
        color: #f1f5f9 !important;
    }
    /* Header toolbar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    /* Sidebar menu items */
    .css-1544g2n, .css-1629p8f {
        color: #f1f5f9 !important;
    }
    /* Menu button */
    button[data-testid="baseButton-header"] {
        color: #f1f5f9 !important;
    }
    button[data-testid="baseButton-header"]:hover {
        background-color: #1e293b !important;
    }
</style>
"""
    else:
        # Light Theme
        return """
<style>
    /* Light Neo Brutalism Theme */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Courier New', Courier, monospace;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    h1 {
        font-weight: 900;
        text-transform: uppercase;
        border: 4px solid #000000;
        padding: 1rem;
        background-color: #fbbf24;
        box-shadow: 8px 8px 0px #000000;
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMarkdown p {
        font-size: 1.1rem;
        font-weight: 500;
        color: #1e293b;
    }
    .stButton button {
        background-color: #3b82f6;
        color: white;
        border: 3px solid #000000;
        border-radius: 0px;
        padding: 0.75rem 1.5rem;
        font-weight: 800;
        box-shadow: 5px 5px 0px #000000;
        transition: all 0.1s ease;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #000000;
        background-color: #2563eb;
        border-color: #000000;
    }
    .stButton button:active {
        transform: translate(2px, 2px);
        box-shadow: 3px 3px 0px #000000;
    }
    div[data-testid="stFileUploader"] {
        border: 3px solid #000000;
        background-color: #ffffff;
        box-shadow: 6px 6px 0px #000000;
        padding: 1rem;
        border-radius: 0px;
    }
    div[data-testid="stFileUploader"] label {
        color: #000000 !important;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    .stDownloadButton button {
        background-color: #10b981;
        border: 3px solid #000000;
        color: white;
        font-weight: 800;
        box-shadow: 5px 5px 0px #000000;
        border-radius: 0;
    }
    .stDownloadButton button:hover {
        box-shadow: 7px 7px 0px #000000;
        background-color: #059669;
        border-color: #000000;
    }
    img {
        border: 3px solid #000000;
        box-shadow: 5px 5px 0px #000000;
        border-radius: 0px;
    }
    /* Radio Button Style */
    div[role="radiogroup"] label {
        color: #000000 !important;
        font-weight: bold;
    }
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background-color: #0f172a;
        border: 3px solid #000000;
        color: #fbbf24;
        padding: 0.5rem;
        font-weight: bold;
        box-shadow: 4px 4px 0px #000000;
        cursor: pointer;
    }
    /* Subtitle box for light mode */
    .subtitle-light {
        border: 3px solid #000000;
        padding: 1rem;
        background-color: #1e293b;
        box-shadow: 6px 6px 0px #000000;
        margin-bottom: 2rem;
        color: #ffffff;
        font-weight: bold;
        text-align: center;
    }
    /* Text color fixes */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #0f172a !important;
    }
    .stText {
        color: #0f172a !important;
    }
    /* File uploader text */
    div[data-testid="stFileUploader"] > div > div > div > div {
        color: #000000 !important;
    }
    /* File uploader Browse button */
    div[data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: 3px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #2563eb !important;
        box-shadow: 5px 5px 0px #000000 !important;
    }
    /* File uploader small text */
    div[data-testid="stFileUploader"] small {
        color: #475569 !important;
    }
    /* Progress bar text */
    .stProgress > div > div > div {
        color: #000000 !important;
    }
    /* Info/Success/Error messages */
    .stAlert {
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        border-radius: 0;
    }
    /* Divider */
    hr {
        border-color: #64748b !important;
    }
    /* Container borders */
    .element-container {
        color: #0f172a !important;
    }
    /* Caption text */
    .caption {
        color: #475569 !important;
    }
    /* Radio button text (Language toggle) */
    div[role="radiogroup"] label p {
        color: #000000 !important;
    }
    div[role="radiogroup"] input[type="radio"] + div {
        color: #000000 !important;
    }
    /* Radio button selected state */
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #fbbf24 !important;
        border-color: #000000 !important;
    }
    /* Header menu (hamburger menu) */
    button[kind="header"] {
        color: #000000 !important;
    }
    /* Header toolbar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    /* Sidebar menu items */
    .css-1544g2n, .css-1629p8f {
        color: #000000 !important;
    }
    /* Menu button */
    button[data-testid="baseButton-header"] {
        color: #000000 !important;
    }
    button[data-testid="baseButton-header"]:hover {
        background-color: #e2e8f0 !important;
    }
    /* Specific text elements - NOT all divs */
    .stMarkdown strong {
        color: #000000 !important;
    }
    /* Link text */
    .stMarkdown a {
        color: #3b82f6 !important;
    }
    .stMarkdown a:hover {
        color: #2563eb !important;
    }
    /* Alert boxes - keep default backgrounds */
    div[data-baseweb="notification"] {
        border: 3px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }
    /* Info message text */
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: #0f172a !important;
    }
    /* Progress text */
    .stProgress [data-testid="stMarkdownContainer"] {
        color: #0f172a !important;
    }
    /* Status text */
    .stStatus [data-testid="stMarkdownContainer"] {
        color: #0f172a !important;
    }
    /* Image captions */
    .stImage > div > div {
        color: #475569 !important;
    }
    /* File uploader drag text - more specific */
    div[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
        color: #475569 !important;
    }
    /* File uploader file name */
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
        color: #000000 !important;
    }
    /* Ensure main background stays light */
    .main {
        background-color: #f8fafc !important;
    }
    /* Ensure containers don't override background */
    .block-container {
        background-color: transparent !important;
    }
    /* Text in markdown containers */
    [data-testid="stMarkdownContainer"] {
        color: inherit;
    }
    [data-testid="stMarkdownContainer"] p {
        color: #1e293b !important;
    }
    [data-testid="stMarkdownContainer"] h3 {
        color: #0f172a !important;
    }
</style>
"""

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Localization with theme toggle
LANGUAGES = {
    "ID": {
        "title": "✨ Penghapus Watermark Gemini",
        "subtitle": "Hapus watermark Gemini AI dari gambar Anda secara massal dengan presisi.",
        "upload_label": "Seret dan lepas gambar di sini",
        "selected_files": "### Terpilih {} gambar",
        "remove_btn": "✨ Hapus Watermark",
        "processing": "Memproses {}...",
        "complete": "Pemrosesan selesai!",
        "download_all": "📦 Unduh Semua (ZIP)",
        "preview_title": "### Pratinjau Hasil",
        "original": "Asli",
        "cleaned": "Bersih",
        "download_btn": "⬇️ Unduh",
        "more_images": "Dan {} gambar lagi... Unduh ZIP untuk melihat semua.",
        "reset_btn": "🔄 Reset",
        "error_process": "Gagal memproses {}: {}",
        "dark_mode": "🌙 Mode Gelap",
        "light_mode": "☀️ Mode Terang"
    },
    "EN": {
        "title": "✨ Gemini Watermark Remover",
        "subtitle": "Batch process your images to remove Gemini AI watermarks with precision.",
        "upload_label": "Drag and drop images here",
        "selected_files": "### Selected {} image(s)",
        "remove_btn": "✨ Remove Watermarks",
        "processing": "Processing {}...",
        "complete": "Processing complete!",
        "download_all": "📦 Download All (ZIP)",
        "preview_title": "### Preview Results",
        "original": "Original",
        "cleaned": "Cleaned",
        "download_btn": "⬇️ Download",
        "more_images": "And {} more images... Download the ZIP to see all.",
        "reset_btn": "🔄 Reset",
        "error_process": "Failed to process {}: {}",
        "dark_mode": "🌙 Dark Mode",
        "light_mode": "☀️ Light Mode"
    }
}

# Session State for Reset and Language
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0
if 'lang' not in st.session_state:
    st.session_state.lang = "ID"

def reset_app():
    st.session_state.uploader_key += 1
    # Try to clean up temp directory safely
    if os.path.exists(TEMP_DIR):
        try:
            # Try to remove files individually with retry
            for filename in os.listdir(TEMP_DIR):
                filepath = os.path.join(TEMP_DIR, filename)
                try:
                    if os.path.isfile(filepath):
                        os.unlink(filepath)
                except Exception:
                    pass  # Skip files that are in use
            # Try to remove the directory
            try:
                shutil.rmtree(TEMP_DIR)
            except Exception:
                pass  # Directory might still have locked files
        except Exception:
            pass  # If listing fails, just continue
    # Ensure directory exists
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

# Get current language texts
texts = LANGUAGES[st.session_state.lang]

# Language Toggle and Theme Toggle
col_theme, col_spacer, col_lang = st.columns([1, 4, 1])

with col_theme:
    theme_label = texts["light_mode"] if st.session_state.dark_mode else texts["dark_mode"]
    if st.button(theme_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with col_lang:
    lang_choice = st.radio("Bahasa / Language", ["ID", "EN"], horizontal=True, label_visibility="collapsed")
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

# Update texts after language change
texts = LANGUAGES[st.session_state.lang]

# Header with Reset Button
col_header, col_reset = st.columns([3, 1])
with col_header:
    st.title(texts["title"])
with col_reset:
    st.markdown("<br>", unsafe_allow_html=True) # Spacing
    st.button(texts["reset_btn"], on_click=reset_app, type="secondary")

st.markdown(f"""
    <div class="{'subtitle-dark' if st.session_state.dark_mode else 'subtitle-light'}">
        {texts["subtitle"]}
    </div>
""", unsafe_allow_html=True)

# File Uploader
uploaded_files = st.file_uploader(
    texts["upload_label"], 
    type=["jpg", "jpeg", "png", "webp", "bmp"], 
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded_files:
    st.markdown(texts["selected_files"].format(len(uploaded_files)))
    
    if st.button(texts["remove_btn"], type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        processed_images = []
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, uploaded_file in enumerate(uploaded_files):
                # Update status
                status_text.text(texts["processing"].format(uploaded_file.name))
                
                # Save input
                input_path = os.path.join(TEMP_DIR, uploaded_file.name)
                output_filename = f"cleaned_{uploaded_file.name}"
                output_path = os.path.join(TEMP_DIR, output_filename)
                
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Run Tool
                command = [TOOL_PATH, "-i", input_path, "-o", output_path]
                try:
                    subprocess.run(command, capture_output=True, check=True)
                    
                    if os.path.exists(output_path):
                        # Add to ZIP
                        zip_file.write(output_path, output_filename)
                        processed_images.append((input_path, output_path, uploaded_file.name))
                except Exception as e:
                    st.error(texts["error_process"].format(uploaded_file.name, e))
                
                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text(texts["complete"])
        progress_bar.empty()
        
        # Results Area
        st.markdown("---")
        
        # Download All Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label=texts["download_all"],
                data=zip_buffer.getvalue(),
                file_name="cleaned_images.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        st.markdown(texts["preview_title"])
        
        # Display Grid (limit to first 10 to avoid lag)
        for input_path, output_path, name in processed_images[:10]:
            with st.container():
                st.markdown(f"**{name}**")
                c1, c2 = st.columns(2)
                with c1:
                    st.image(input_path, caption=texts["original"], use_container_width=True)
                with c2:
                    st.image(output_path, caption=texts["cleaned"], use_container_width=True)
                    # Read file data once and store in memory
                    with open(output_path, "rb") as file:
                        file_data = file.read()
                    st.download_button(
                        label=texts["download_btn"],
                        data=file_data,
                        file_name=f"cleaned_{name}",
                        mime="image/png",
                        key=f"btn_{name}"
                    )
                st.divider()
        
        if len(processed_images) > 10:
            st.info(texts["more_images"].format(len(processed_images) - 10))

st.markdown("---")
st.markdown("Powered by [FYAN IT](https://fyan.web.id/)")
