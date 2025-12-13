from flask import Flask, jsonify, request
import subprocess
import json
import os
import tempfile

app = Flask(__name__)

def get_cookie_file():
    try:
        import yt_cookies
        cookies = yt_cookies.youtube()
        if cookies:
            fd, path = tempfile.mkstemp(suffix='.txt')
            with os.fdopen(fd, 'w') as f:
                f.write(cookies)
            return path
    except:
        pass
    return None

def parse_duration(duration):
    if duration is None:
        return 0
    try:
        return int(float(duration))
    except:
        return 0

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
    
    cookie_file = None
    try:
        cookie_file = get_cookie_file()
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--no-warnings',
            '--quiet',
            '-j',
        ]
        if cookie_file:
            cmd.extend(['--cookies', cookie_file])
        cmd.append(f'ytsearch10:{query}')
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        results = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    video_id = data.get('id', '')
                    results.append({
                        'id': video_id,
                        'title': data.get('title', 'Unknown'),
                        'duration': parse_duration(data.get('duration')),
                        'thumbnail': f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                        'channel': data.get('channel') or data.get('uploader') or 'Unknown',
                    })
                except json.JSONDecodeError:
                    continue
        
        return jsonify({'results': results})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Search timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cookie_file and os.path.exists(cookie_file):
            os.unlink(cookie_file)

@app.route('/api/stream/<video_id>')
def stream(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    cookie_file = None
    
    try:
        cookie_file = get_cookie_file()
        cmd = [
            'yt-dlp',
            '--no-warnings',
            '--quiet',
            '-f', 'bestaudio[ext=m4a]/bestaudio/best',
            '-g',
            '--print', '%(title)s',
            '--print', '%(duration)s',
            '--print', '%(thumbnail)s',
            '--print', '%(channel)s',
        ]
        if cookie_file:
            cmd.extend(['--cookies', cookie_file])
        cmd.append(url)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return jsonify({'error': result.stderr or 'Failed to get stream'}), 500
        
        lines = result.stdout.strip().split('\n')
        if len(lines) < 5:
            return jsonify({'error': 'No audio stream available'}), 404
        
        title = lines[0]
        duration = parse_duration(lines[1])
        thumbnail = lines[2] if lines[2] != 'NA' else f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
        channel = lines[3] if lines[3] != 'NA' else 'Unknown'
        stream_url = lines[4]
        
        return jsonify({
            'title': title,
            'url': stream_url,
            'duration': duration,
            'thumbnail': thumbnail,
            'channel': channel,
        })
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Stream timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cookie_file and os.path.exists(cookie_file):
            os.unlink(cookie_file)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})
