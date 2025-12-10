# 🚀 Deployment Guide - SmartTranslate

## Quick Deploy (Recommended)

### Option 1: Railway (Backend) + Vercel (Frontend)

#### Step 1: Deploy Backend to Railway

1. **Go to Railway**
   - Visit https://railway.app/
   - Click "Login" and sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `ivanandreansyah/Aplikasi_SmartTranslater`
   - Railway will auto-detect the Dockerfile

3. **Wait for Build**
   - First build takes 5-10 minutes (downloading AI models)
   - Railway will provide a public URL like: `https://smarttranslate-production.up.railway.app`
   - **COPY THIS URL** - you'll need it for frontend

4. **Verify Backend**
   - Open the Railway URL in browser
   - You should see a 404 or method not allowed (this is normal)
   - Test the API with curl or Postman:
     ```bash
     curl -X POST https://YOUR-RAILWAY-URL.up.railway.app/translate \
       -H "Content-Type: application/json" \
       -d '{"text":"halo","source":"id","target":"en"}'
     ```

#### Step 2: Deploy Frontend to Vercel

1. **Update API URL**
   - Edit `frontend/index.html`
   - Find line 89: `window.API_URL = "http://127.0.0.1:5000/translate";`
   - Replace with your Railway URL:
     ```html
     <script>
       window.API_URL = "https://YOUR-RAILWAY-URL.up.railway.app/translate";
     </script>
     ```
   - Save and commit changes

2. **Deploy to Vercel**
   
   **Option A: Vercel Dashboard (Easiest)**
   - Go to https://vercel.com/
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Configure:
     - **Root Directory**: `frontend`
     - **Framework Preset**: Other
     - **Build Command**: (leave empty)
     - **Output Directory**: `.`
   - Click "Deploy"
   - Vercel will give you a URL like: `https://smarttranslate.vercel.app`

   **Option B: Vercel CLI**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Login
   vercel login
   
   # Deploy
   cd frontend
   vercel --prod
   ```

3. **Test Your App**
   - Open your Vercel URL
   - Try translating some text
   - Check browser console for any errors

---

### Option 2: Render (Backend) + Netlify (Frontend)

#### Step 1: Deploy Backend to Render

1. **Go to Render**
   - Visit https://render.com/
   - Sign in with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: smarttranslate-backend
     - **Environment**: Docker
     - **Region**: Singapore (closest to Indonesia)
     - **Instance Type**: Free (or paid for better performance)
   - Click "Create Web Service"

3. **Wait for Deployment**
   - Takes 10-15 minutes for first deploy
   - Copy the provided URL

#### Step 2: Deploy Frontend to Netlify

1. **Update API URL**
   - Same as Vercel option above
   - Use your Render URL instead

2. **Deploy to Netlify**
   
   **Option A: Drag & Drop**
   - Go to https://netlify.com/
   - Drag the `frontend` folder to Netlify dashboard
   - Done!

   **Option B: Netlify CLI**
   ```bash
   npm install -g netlify-cli
   netlify login
   cd frontend
   netlify deploy --prod
   ```

---

## Environment Variables

### Backend (Railway/Render)

Set these in your hosting platform's dashboard:

- `PORT`: Auto-set by platform (don't change)
- `FLASK_ENV`: `production`
- `SMARTTRANSLATE_MODEL_ID_EN`: (optional) Custom model path
- `SMARTTRANSLATE_MODEL_EN_ID`: (optional) Custom model path

---

## Troubleshooting

### Backend Issues

**Problem**: Build fails on Railway/Render
- **Solution**: Check logs in dashboard. Usually memory issue. Try paid tier.

**Problem**: Backend is slow
- **Solution**: First request loads models (slow). Subsequent requests are fast. Consider paid tier.

**Problem**: CORS errors
- **Solution**: Backend already has CORS enabled. Check if backend URL is correct in frontend.

### Frontend Issues

**Problem**: "Failed to fetch" error
- **Solution**: 
  1. Check if backend URL is correct in `index.html`
  2. Make sure backend is running (visit backend URL)
  3. Check browser console for exact error

**Problem**: Translation not working
- **Solution**:
  1. Open browser DevTools → Network tab
  2. Try translating
  3. Check if request is sent to correct URL
  4. Check response status and body

---

## Cost Estimates

### Free Tier (Recommended for Testing)
- **Railway**: 500 hours/month free, $5 credit
- **Vercel**: Unlimited deployments, generous bandwidth
- **Total**: FREE for small usage

### Paid Tier (For Production)
- **Railway**: ~$5-10/month for 1GB RAM
- **Vercel**: Free (or Pro at $20/month for team features)
- **Total**: ~$5-10/month

---

## Local Development

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r ../requirements.txt
python app.py

# Frontend
cd frontend
# Just open index.html in browser
# Or use a simple server:
python -m http.server 8000
```

---

## Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Railway: Add custom domain in settings
   - Vercel: Add custom domain in project settings

2. **Monitoring**
   - Check Railway/Render logs regularly
   - Monitor Vercel analytics

3. **Updates**
   - Push to GitHub → Auto-deploys on Railway/Vercel
   - No manual deployment needed!

---

## Support

If you encounter issues:
1. Check the logs in your hosting dashboard
2. Verify all URLs are correct
3. Test backend API directly with curl/Postman
4. Check browser console for frontend errors

Good luck! 🚀
