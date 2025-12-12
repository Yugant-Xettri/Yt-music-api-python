from flask import Flask, jsonify, request
import yt_dlp
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
    search_url = f"ytsearch10:{query}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            results = []
            for entry in info.get('entries', []):
                if entry:
                    results.append({
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'duration': entry.get('duration'),
                        'thumbnail': f"https://i.ytimg.com/vi/{entry.get('id')}/mqdefault.jpg",
                        'channel': entry.get('channel') or entry.get('uploader', 'Unknown'),
                    })
            return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream/<video_id>')
def stream(video_id):
    video_id = sanitize_query(video_id)
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'channel': info.get('channel') or info.get('uploader', 'Unknown'),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})
