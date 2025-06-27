# 🎬 RipIt.YT — YouTube Video & Audio Downloader

> *Feeling down bad for that YouTube song?*  
> **Rip it. Clip it. Keep it.**

RipIt.YT is a lightweight, Streamlit-powered web app that lets you download **YouTube videos as MP4** or **extract audio as MP3**, all in a clean, no-nonsense interface.

---

## 🚀 Features

- 🎥 Download **YouTube videos in MP4**
- 🎧 Extract and download **audio in MP3**
- ⚡ Clean, fast interface using Streamlit
- 🛠 FFmpeg auto-detection with helpful setup guide
- 💾 Files saved locally with download button

---

## 🧠 How It Works

This app uses:
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) for downloading content
- [`FFmpeg`](https://ffmpeg.org/) for merging video/audio and converting formats
- [`Streamlit`](https://streamlit.io/) for the web UI

---

## 🖥️ Installation

### 1. Clone the Repo


git clone https://github.com/yourusername/ripit-yt.git
cd ripit-yt
2. Install Dependencies

pip install streamlit yt-dlp
3. Install FFmpeg (if not already installed)
📦 Windows:
Download static build from gyan.dev

Extract it (e.g., C:\ffmpeg)

Add C:\ffmpeg\bin to your System PATH

Restart your PC

Test it by running:

ffmpeg -version
🎯 Usage

streamlit run app.py
Paste a YouTube URL

Choose Video (MP4) or Audio (MP3)

Click Download

Boom 💥 — your file is ready!

Files are saved in the downloads/ folder inside your project directory.

🧃 Why "RipIt.YT"?
Because:

We’re ripping the vids (💀)

It sounds cool

.YT = YouTube vibes

Meme energy 💅

🤝 Contribute / Remix
PRs are welcome! Feel free to:

Add playlist support

Choose video resolutions

Deploy to the web

⚠️ Disclaimer
This tool is for educational and personal use only. Please respect YouTube's Terms of Service and do not use this tool to infringe copyright.


![alt text](image.png)

💬 Credits
Built with ❤️ by Varnit vishwakarma
Powered by yt-dlp, FFmpeg, and Streamlit









