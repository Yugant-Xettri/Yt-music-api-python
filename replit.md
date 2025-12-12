# YT Music Stream API - Render Ready

## Overview
A YouTube Music streaming API built with Flask and yt-dlp. Designed for deployment on Render.

## Features
- Search YouTube tracks
- Get direct audio stream URLs
- Fast yt-dlp based extraction
- Optimized for Render deployment with gunicorn

## Project Structure
```
├── index.py               # Flask app with API endpoints
├── main.py                # Local development entry
├── requirements.txt       # Python dependencies
├── render.yaml            # Render configuration
└── pyproject.toml         # Python project config
```

## API Endpoints
- `GET /` - API info
- `GET /api/search?q=<query>` - Search for tracks (returns up to 10 results)
- `GET /api/stream/<video_id>` - Get stream URL for a track
- `GET /api/health` - Health check

## Local Development
```bash
python main.py
```
Runs on `http://localhost:5000`

## Render Deployment

### Via Dashboard
1. Push code to GitHub
2. Go to render.com → New → Web Service
3. Connect repository
4. Runtime: Python 3
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn index:app --bind 0.0.0.0:$PORT --workers 4 --timeout 60`
7. Deploy

### Using render.yaml
The render.yaml file is already configured for automatic deployment.

## Dependencies
- Flask - Web framework
- gunicorn - Production WSGI server
- yt-dlp - YouTube extraction

## How It Works
1. Search endpoint uses yt-dlp to search YouTube
2. Stream endpoint extracts direct audio URL using yt-dlp
3. Returns URLs that can be played directly in audio players

## Recent Changes
- 2025-12-12: Switched from pytubefix to yt-dlp for better bot detection handling
- 2025-12-12: Updated for Render deployment (from Vercel)
- 2025-12-12: Added gunicorn for production server
