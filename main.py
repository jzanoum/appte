from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    # Get the parameters from the request
    url = request.args.get("url")
    format = request.args.get("format")
    folder = request.args.get("folder")

    # Create a YoutubeDL object with the desired options
    ydl_opts = {
        "format": format,
        "outtmpl": folder + "/%(title)s.%(ext)s",
        "quiet": True
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Try to download the video and return a JSON response
    try:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        return jsonify({"status": "success", "file": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
