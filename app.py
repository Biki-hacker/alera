from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)


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

    
    video_id = extract_video_id(youtube_url)

    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
