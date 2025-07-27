# Depression Assessment Backend

A FastAPI-based backend service for depression assessment using CatBoost machine learning models.

## Features

- RESTful API for depression prediction
- Separate models for students and working professionals
- CORS support for frontend integration
- Health check endpoint
- Docker support for easy deployment

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /predict

Make a depression prediction based on user data.

### GET /health

Health check endpoint that returns the status of the service and whether models are loaded.

## Docker Deployment

### Build the Docker image:

```bash
docker build -t depression-backend .
```

### Run the container:

```bash
docker run -p 8000:8000 depression-backend
```

## Railway Deployment

### Prerequisites

- Railway account
- Railway CLI (optional)

### Deployment Steps

1. **Connect your repository to Railway:**

   - Go to [Railway](https://railway.app)
   - Create a new project
   - Connect your GitHub repository

2. **Configure environment variables (if needed):**

   - Railway automatically detects the PORT environment variable
   - Add any additional environment variables in the Railway dashboard

3. **Deploy:**
   - Railway will automatically detect the Dockerfile and deploy your application
   - The service will be available at the provided Railway domain

### Manual deployment with Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize and deploy
railway link
railway up
```

## Project Structure

```
.
├── models/
│   ├── catboost_model_s.cbm    # Student model
│   └── catboost_model_wf.cbm   # Working Professional model
├── pipeline/
│   └── pipeline.py             # Prediction pipeline
├── server.py                   # FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── railway.json               # Railway configuration
└── README.md                  # This file
```

## Environment Variables

- `PORT` - Port number for the application (automatically set by Railway)

## Health Check

The application includes a health check endpoint at `/health` that returns:

- Service status
- Model loading status

## CORS Configuration

The API is configured to accept requests from:

- `https://depression-frontend-zeta.vercel.app` (production frontend)
- `http://localhost:3000` (local development frontend)
