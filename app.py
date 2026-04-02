# app.py
# YouTube Downloader without FFmpeg

from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_info", methods=["POST"])
def get_info():
    url = request.form.get("url")

    if not url:
        return jsonify({"error": "Please enter a valid YouTube URL"})

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        data = {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "url": url
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    file_type = request.form.get("type")

    if not url:
        return "Invalid URL"

    unique_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

    try:
        if file_type == "audio":
            # Audio direct format me download hoga (m4a/webm etc.)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'quiet': True
            }
        else:
            # Best single file video choose karega
            # Isse FFmpeg ki need kam ho jati hai
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': output_template,
                'quiet': True
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        return f"Download Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)