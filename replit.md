# YT Music Stream API

## Overview
YouTube Music streaming API using Flask, yt-dlp, and yt-cookies for automatic cookie generation.

## API Endpoints
- `GET /` - API info
- `GET /api/search?q=<query>` - Search tracks
- `GET /api/stream/<video_id>` - Get audio stream URL
- `GET /api/health` - Health check

## Dependencies
- flask - Web framework
- gunicorn - Production server
- yt-dlp - YouTube extraction
- yt-cookies - Auto cookie generation

## Local Dev
```bash
python main.py
```

## Render Deployment
Build: `pip install -r requirements.txt`
Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 60`
