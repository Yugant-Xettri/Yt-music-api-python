# Python Flask App - Vercel Ready

## Overview
This project is set up for deployment to Vercel as a Python serverless application using Flask.

## Project Structure
```
├── api/
│   └── index.py       # Main Flask app (Vercel entry point)
├── main.py            # Local development entry point
├── requirements.txt   # Python dependencies for Vercel
├── pyproject.toml     # Python project configuration
├── vercel.json        # Vercel deployment configuration
└── .gitignore         # Git ignore file
```

## Local Development
Run locally with:
```bash
python main.py
```
The server runs on `http://localhost:5000`

## Vercel Deployment

### Deploy via Vercel Dashboard
1. Push code to GitHub/GitLab/Bitbucket
2. Go to [vercel.com](https://vercel.com) → Add New → Project
3. Import your repository
4. Vercel auto-detects Python
5. Click Deploy

### Deploy via CLI
```bash
npm install -g vercel
vercel login
vercel           # Preview deployment
vercel --prod    # Production deployment
```

## API Endpoints
- `GET /` - Returns welcome message
- `GET /api` - Returns API status
- `GET /api/health` - Health check endpoint

## Dependencies
- Flask 3.0.0

## Notes
- Files in `/api` folder are exposed as serverless functions
- All routes are configured in `vercel.json` to route through `api/index.py`
- If you encounter build errors, try switching Node.js to 18.x in Vercel project settings
