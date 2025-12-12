from flask import Flask, jsonify, request
from pytubefix import YouTube, Search
import re

app = Flask(__name__)

def sanitize_query(query):
    return re.sub(r'[<>"\']', '', query.strip())

@app.route('/')
def home():
    return jsonify({
        'service': 'YT Music Stream API',
        'endpoints': {
            '/api/search?q=<query>': 'Search for tracks',
            '/api/stream/<video_id>': 'Get stream URL',
            '/api/health': 'Health check'
        }
    })

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    query = sanitize_query(query)
    
    try:
        search_results = Search(query)
        results = []
        for video in search_results.videos[:10]:
            results.append({
                'id': video.video_id,
                'title': video.title,
                'duration': video.length,
                'thumbnail': f"https://i.ytimg.com/vi/{video.video_id}/mqdefault.jpg",
                'channel': video.author or 'Unknown',
            })
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream/<video_id>')
def stream(video_id):
    video_id = sanitize_query(video_id)
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            audio_stream = yt.streams.filter(progressive=True).order_by('abr').desc().first()
        
        if not audio_stream:
            return jsonify({'error': 'No audio stream available'}), 404
        
        return jsonify({
            'title': yt.title,
            'url': audio_stream.url,
            'duration': yt.length,
            'thumbnail': yt.thumbnail_url,
            'channel': yt.author or 'Unknown',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})
