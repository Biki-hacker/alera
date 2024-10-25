import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)

def extract_video_id(youtube_url):
    
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

@app.route('/transcript', methods=['POST'])
def get_youtube_transcript():
    
    data = request.get_json()
    youtube_url = data.get('url')
    try:
        
        video_id = extract_video_id(youtube_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
       
        cleaned_text = " ".join([entry['text'].replace('\n', ' ') for entry in transcript])
        
        
        return jsonify({"transcript": cleaned_text}), 200
    except Exception as e:
        
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run()
