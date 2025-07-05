# PersonaSense API Deployment Guide

This guide will help you deploy your PersonaSense API to free hosting platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Easiest)

**Steps:**
1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/personasense-api.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Create Web Service"
   - Your API will be deployed at: `https://your-app-name.onrender.com`

**Advantages:**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Custom domain support
- ✅ SSL certificate included
- ✅ Easy setup with render.yaml

### Option 2: Railway

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your repository
4. Railway will automatically detect it's a Python app
5. Deploy!

**Advantages:**
- ✅ Free tier available
- ✅ Very fast deployments
- ✅ Automatic environment detection

### Option 3: Fly.io

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. Deploy: `fly launch`
4. Follow the prompts

**Advantages:**
- ✅ Generous free tier
- ✅ Global edge deployment
- ✅ Custom domains

### Option 4: Heroku (Limited Free Tier)

**Steps:**
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Deploy: `git push heroku main`

**Note:** Heroku's free tier is limited, but it's still an option.

## 🔧 Environment Setup

Your app is already configured for deployment with:
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Heroku/Railway configuration  
- ✅ `runtime.txt` - Python version specification
- ✅ Environment variable handling for PORT

## 📝 Important Notes

### Model File Size
Your model file (`full_personality_prediction_pipeline.joblib`) might be large. If deployment fails due to size limits:

1. **Check model size:**
   ```bash
   ls -lh "Model Training/full_personality_prediction_pipeline.joblib"
   ```

2. **If too large (>100MB), consider:**
   - Using Git LFS (Large File Storage)
   - Hosting the model separately (AWS S3, Google Cloud Storage)
   - Compressing the model

### CORS Configuration
Your API already includes CORS middleware for:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)
- `https://personasense.netlify.app` (Your frontend)

**Update CORS origins** in `main.py` if your frontend URL changes.

## 🧪 Testing Your Deployment

After deployment, test your API:

```bash
# Health check
curl https://your-app-url.onrender.com/health

# Test prediction
curl -X POST https://your-app-url.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Social_event_attendance": 3,
    "Going_outside": 4,
    "Friends_circle_size": 2,
    "Post_frequency": 1,
    "Stage_fear": "Yes",
    "Drained_after_socializing": "Yes",
    "Time_spent_Alone": 5
  }'
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check if all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Model loading fails:**
   - Verify model file path is correct
   - Check if model file is included in repository

3. **CORS errors:**
   - Update CORS origins in `main.py`
   - Ensure frontend URL is correct

4. **Memory issues:**
   - Consider using a smaller model
   - Optimize dependencies

## 📊 Monitoring

Most platforms provide:
- ✅ Logs and error tracking
- ✅ Performance metrics
- ✅ Uptime monitoring

## 🎯 Next Steps

1. Choose your preferred platform
2. Follow the deployment steps
3. Update your frontend to use the new API URL
4. Test thoroughly
5. Monitor performance

Your API is ready for deployment! 🚀 