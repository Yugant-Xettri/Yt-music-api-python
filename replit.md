# YT Music Stream - Vercel Ready

## Overview
A YouTube Music streaming web application built with Flask and pytubefix. Designed for deployment on Vercel as serverless functions.

## Features
- Search YouTube Music tracks
- Stream audio directly in browser
- Queue/playlist functionality
- Responsive modern UI
- No cookies or proxy setup required

## Project Structure
```
├── api/
│   └── index.py           # Flask app with API endpoints
├── templates/
│   └── index.html         # Frontend HTML
├── static/
│   ├── style.css          # Styles
│   └── app.js             # Frontend JavaScript
├── main.py                # Local development entry
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel configuration
└── pyproject.toml         # Python project config
```

## API Endpoints
- `GET /` - Serves the web UI
- `GET /api/search?q=<query>` - Search for tracks
- `GET /api/stream/<video_id>` - Get stream URL for a track
- `GET /api/health` - Health check

## Local Development
```bash
python main.py
```
Runs on `http://localhost:5000`

## Vercel Deployment

### Via Dashboard
1. Push code to GitHub
2. Go to vercel.com → Add New → Project
3. Import repository
4. Deploy

### Via CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

## Dependencies
- Flask 3.0.0
- pytubefix (lightweight, Vercel-compatible)

## How It Works
1. User searches for music
2. Backend uses pytubefix to search YouTube
3. User clicks a track
4. Backend extracts direct audio stream URL
5. Audio plays in browser's HTML5 player

## Notes
- pytubefix is lightweight (~1MB) and fits within Vercel's 50MB function size limit
- yt-dlp was too heavy for Vercel serverless functions
- Vercel function timeout is set to 60 seconds
- No proxy required - pytubefix handles extraction natively
