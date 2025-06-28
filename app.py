import streamlit as st
import yt_dlp
import os
import shutil

DOWNLOAD_DIR = "downloads"

st.markdown("""
    <style>
    html, body, .stApp {
        background: #EFEEE8 !important;
        color: black !important;
    }
    label,
    .stTextInput > label,
    .stRadio > label {
        color: black !important;
    }
    [data-baseweb="radio"] label {
        color: black !important;
        opacity: 1 !important;
    }
    [data-baseweb="radio"] label[data-selected="true"] {
        font-weight: bold !important;
        color: black !important;
    }
    .stTextInput input {
        color: black !important;
        background-color: white !important;
        border-radius: 10px !important;
    }
    .stButton > button,
    .stDownloadButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        display: block;
        margin: 0 auto;
    }
    .centered-text {
        text-align: center;
        color: black;
        margin-top: 2rem;
    }
    .input-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    .stTextInput, .stRadio {
        flex: 1;
        min-width: 250px;
        max-width: 100%;
    }
    @media (max-width: 768px) {
        .input-container {
            flex-direction: column;
            align-items: stretch;
        }
    }
    </style>
""", unsafe_allow_html=True)


def check_ffmpeg_installed():
    return shutil.which("ffmpeg") is not None

def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        final_path = ydl.prepare_filename(info).replace(".webm", ".mp4")
        return final_path if os.path.exists(final_path) else None

def download_audio(url, output_path):
    downloaded_file = None

    def hook(d):
        nonlocal downloaded_file
        if d['status'] == 'finished':
            downloaded_file = d['filename'].replace('.webm', '.mp3').replace('.m4a', '.mp3')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'progress_hooks': [hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return downloaded_file if downloaded_file and os.path.exists(downloaded_file) else None

st.set_page_config(page_title="RipIt.YT", page_icon="📥")

st.markdown("""
<div class="centered-text">
    <h1>📥 RipIt.YT</h1>
    <p>Download any YouTube video as <strong>MP4</strong> or <strong>MP3</strong> with one click.</p>
</div>
""", unsafe_allow_html=True)

if not check_ffmpeg_installed():
    st.error(
        "**FFmpeg not found!**\n\n"
        "This app requires FFmpeg to work.\n\n"
        "**Install steps (Windows):**\n"
        "1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)\n"
        "2. Extract it (e.g., to `C:\\ffmpeg`)\n"
        "3. Add `C:\\ffmpeg\\bin` to your system PATH\n"
        "4. Restart your terminal or Streamlit"
    )
    st.stop()

st.markdown('<div class="input-container">', unsafe_allow_html=True)
url = st.text_input("🎬 YouTube URL", placeholder="https://youtu.be/...")
choice = st.radio("Format", ["Video (MP4)", "Audio (MP3)"])
st.markdown('</div>', unsafe_allow_html=True)

if st.button("⬇️ Download"):
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL.")
    else:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        for file in os.listdir(DOWNLOAD_DIR):
            try:
                os.remove(os.path.join(DOWNLOAD_DIR, file))
            except Exception:
                pass

        with st.spinner("⏳ Downloading... Please wait."):
            try:
                filepath = download_video(url, DOWNLOAD_DIR) if choice == "Video (MP4)" else download_audio(url, DOWNLOAD_DIR)

                if filepath and os.path.exists(filepath):
                    st.success("✅ Download complete!")
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"📥 Download {os.path.basename(filepath)}",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="video/mp4" if choice == "Video (MP4)" else "audio/mpeg"
                        )
                else:
                    st.error("❌ File not found after download. Try another link.")
            except Exception as e:
                error_msg = str(e)
                if "Sign in to confirm you’re not a bot" in error_msg or "--cookies" in error_msg:
                    st.warning("⚠️ This video requires sign-in or is age-restricted. Please try another link.")
                else:
                    st.error(f"❌ Error: {e}")

st.markdown("""
<div class="centered-text">
    <small>Made with ❤️ using Streamlit and yt-dlp</small>
</div>
""", unsafe_allow_html=True)
