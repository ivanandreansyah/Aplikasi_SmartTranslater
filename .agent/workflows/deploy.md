---
description: Deploy SmartTranslate ke Railway (Backend) dan Vercel/Netlify (Frontend)
---

# Workflow Deploy SmartTranslate

Aplikasi ini terdiri dari:
- **Backend**: Flask API dengan model AI MarianMT (perlu server dengan Python)
- **Frontend**: Static HTML/CSS/JS (bisa di-host di mana saja)

## Opsi 1: Railway (Backend) + Vercel (Frontend) - RECOMMENDED

### A. Deploy Backend ke Railway

1. **Persiapan Repository**
   - Pastikan semua file sudah di-commit ke Git
   - Push ke GitHub repository: https://github.com/ivanandreansyah/Aplikasi_SmartTranslater.git

2. **Deploy di Railway**
   - Buka https://railway.app/
   - Login dengan GitHub
   - Klik "New Project" → "Deploy from GitHub repo"
   - Pilih repository `Aplikasi_SmartTranslater`
   - Railway akan otomatis mendeteksi Dockerfile
   - Tunggu build selesai (5-10 menit untuk download model pertama kali)
   - Setelah selesai, Railway akan memberikan URL publik (contoh: `https://smarttranslate-production.up.railway.app`)
   - **CATAT URL ini untuk langkah berikutnya**

3. **Konfigurasi Railway (Optional)**
   - Di Railway dashboard, buka tab "Settings"
   - Pastikan PORT sudah di-set (Railway otomatis set PORT environment variable)
   - Jika perlu, tambahkan environment variable `FLASK_ENV=production`

### B. Deploy Frontend ke Vercel

1. **Update API URL di Frontend**
   - Edit file `frontend/index.html`
   - Tambahkan script untuk set API URL sebelum tag `<script src="script.js">`
   - Ganti `YOUR_RAILWAY_URL` dengan URL Railway yang sudah dicatat

2. **Deploy ke Vercel**
   - Install Vercel CLI: `npm install -g vercel`
   - Login: `vercel login`
   - Masuk ke folder frontend: `cd frontend`
   - Deploy: `vercel --prod`
   - Ikuti instruksi (pilih scope, project name, dll)
   - Vercel akan memberikan URL production

### C. Testing
   - Buka URL Vercel di browser
   - Test fitur translate
   - Pastikan tidak ada error CORS

---

## Opsi 2: Render (Backend) + Netlify (Frontend)

### A. Deploy Backend ke Render

1. **Persiapan**
   - Push code ke GitHub

2. **Deploy di Render**
   - Buka https://render.com/
   - Login dengan GitHub
   - Klik "New +" → "Web Service"
   - Connect repository `Aplikasi_SmartTranslater`
   - Konfigurasi:
     - **Name**: smarttranslate-backend
     - **Environment**: Docker
     - **Region**: Singapore (terdekat dengan Indonesia)
     - **Instance Type**: Free (atau pilih yang berbayar untuk performa lebih baik)
   - Klik "Create Web Service"
   - Tunggu build selesai (10-15 menit)
   - Catat URL yang diberikan

### B. Deploy Frontend ke Netlify

1. **Update API URL**
   - Edit `frontend/index.html` dengan URL Render

2. **Deploy ke Netlify**
   - Buka https://netlify.com/
   - Login
   - Drag & drop folder `frontend` ke Netlify dashboard
   - Atau gunakan Netlify CLI:
     ```
     npm install -g netlify-cli
     netlify login
     cd frontend
     netlify deploy --prod
     ```

---

## Opsi 3: Heroku (All-in-One) - LEGACY

**Note**: Heroku tidak lagi gratis, tapi masih bisa digunakan dengan plan berbayar.

1. **Install Heroku CLI**
   ```
   # Download dari https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login dan Create App**
   ```
   heroku login
   heroku create smarttranslate-app
   ```

3. **Deploy**
   ```
   git push heroku main
   ```

4. **Open App**
   ```
   heroku open
   ```

---

## Troubleshooting

### Backend tidak bisa diakses
- Cek logs di Railway/Render dashboard
- Pastikan PORT environment variable sudah di-set
- Verifikasi Dockerfile build berhasil

### CORS Error
- Pastikan Flask CORS sudah dikonfigurasi dengan benar di `backend/app.py`
- Tambahkan domain frontend ke CORS allowed origins jika perlu

### Model loading lambat
- Pertama kali deploy akan download model (5-10 menit)
- Setelah itu, model akan di-cache
- Pertimbangkan upgrade ke instance berbayar untuk performa lebih baik

### Frontend tidak bisa connect ke Backend
- Pastikan API_URL di frontend sudah benar
- Cek Network tab di browser DevTools untuk lihat request/response
- Pastikan backend URL menggunakan HTTPS (bukan HTTP)
