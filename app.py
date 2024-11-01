import os
import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

app = Flask(__name__)
CORS(app)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

def extract_video_id(youtube_url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL format")

@app.route('/transcript', methods=['POST'])
def get_youtube_transcript():
    data = request.get_json()
    youtube_url = data.get('url')
    logging.debug(f"Received URL: {youtube_url}")

    try:
        video_id = extract_video_id(youtube_url)
        logging.debug(f"Extracted video ID: {video_id}")
        
        # Attempt to get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logging.debug("Transcript successfully retrieved")

        cleaned_text = " ".join([entry['text'].replace('\n', ' ') for entry in transcript])
        
        return jsonify({"transcript": cleaned_text}), 200
    except TranscriptsDisabled:
        error_message = "Subtitles are disabled for this video"
        logging.error(error_message)
        return jsonify({"error": error_message}), 400
    except ValueError as ve:
        error_message = f"URL Error: {str(ve)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 400
    except Exception as e:
        error_message = f"Unexpected Error: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
