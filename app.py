from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(youtube_url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.json
    youtube_url = data.get('youtube_url')
    
    if not youtube_url:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
