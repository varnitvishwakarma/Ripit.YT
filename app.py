import streamlit as st
import yt_dlp
import os
import shutil

# --- Configuration ---
DOWNLOAD_DIR = "downloads"

# --- Helper Functions ---
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
        title = info.get('title', '')
        # Find the correct .mp4 file
        for f in os.listdir(output_path):
            if f.endswith(".mp4") and title in f:
                return os.path.join(output_path, f)
    return None

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', '')
        for f in os.listdir(output_path):
            if f.endswith(".mp3") and title in f:
                return os.path.join(output_path, f)
    return None

# --- Streamlit App ---
st.set_page_config(page_title="YouTube Downloader", page_icon="📥")

st.title("📥 Ripit.YT")
st.markdown("Download any YouTube video as **MP4** or **MP3** with one click.")

if not check_ffmpeg_installed():
    st.error(
        "**FFmpeg not found!**\n\n"
        "This app requires FFmpeg to work.\n\n"
        "**Install steps (Windows):**\n"
        "1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)\n"
        "2. Extract it (e.g., to `C:\\ffmpeg`)\n"
        "3. Add `C:\\ffmpeg\\bin` to your system PATH\n"
        "4. Restart VS Code and this app"
    )
    st.stop()

url = st.text_input("🎬 Enter YouTube Video URL")

choice = st.radio("Download as:", ["Video (MP4)", "Audio (MP3)"])

if st.button("Download"):
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL.")
    else:
        # Create download folder if it doesn't exist
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        # Clear previous downloads
        for file in os.listdir(DOWNLOAD_DIR):
            try:
                os.remove(os.path.join(DOWNLOAD_DIR, file))
            except Exception:
                pass

        with st.spinner("⏳ Downloading... Please wait."):
            try:
                if choice == "Video (MP4)":
                    filepath = download_video(url, DOWNLOAD_DIR)
                else:
                    filepath = download_audio(url, DOWNLOAD_DIR)

                if filepath and os.path.exists(filepath):
                    st.success("✅ Download complete!")
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Click to download {os.path.basename(filepath)}",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="video/mp4" if choice == "Video (MP4)" else "audio/mpeg"
                        )
                else:
                    st.error("❌ File not found after download. Try another link.")

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and yt-dlp")
