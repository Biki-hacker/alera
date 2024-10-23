import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

# Function to extract video_id from YouTube URL
def extract_video_id(youtube_url):
    video_id_match = re.match(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

@app.route('/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    youtube_url = data.get('youtube_url')

    # Extract video_id from YouTube URL
    video_id = extract_video_id(youtube_url)

    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    try:
        # Use the YouTubeTranscriptApi to fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment variable or use 5000
    app.run(host='0.0.0.0', port=port)
