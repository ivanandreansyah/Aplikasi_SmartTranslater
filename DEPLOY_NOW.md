# 🚀 Deploy SmartTranslate - Render + Netlify

## Opsi yang Tersedia (Pilih Salah Satu)

### ✅ Opsi 1: Render (Backend) + Netlify (Frontend) - RECOMMENDED
**Gratis, mudah, dan reliable**

### ✅ Opsi 2: Vercel (All-in-One)
**Deploy backend dan frontend di satu tempat**

### ✅ Opsi 3: Heroku (Legacy)
**Berbayar tapi powerful**

---

## 📋 OPSI 1: Render + Netlify (RECOMMENDED)

### Part A: Deploy Backend ke Render

#### 1. Buka Render
- Kunjungi: https://render.com/
- Klik **"Get Started for Free"** atau **"Sign In"**
- Login dengan **GitHub**

#### 2. Create Web Service
- Setelah login, klik **"New +"** di pojok kanan atas
- Pilih **"Web Service"**
- Klik **"Connect account"** jika belum connect GitHub
- Cari dan pilih repository: **`Aplikasi_SmartTranslater`**
- Klik **"Connect"**

#### 3. Konfigurasi Service
Isi form dengan data berikut:

- **Name**: `smarttranslate-backend` (atau nama lain yang Anda suka)
- **Region**: **Singapore** (paling dekat dengan Indonesia)
- **Branch**: `main`
- **Root Directory**: (kosongkan)
- **Environment**: **Docker**
- **Instance Type**: **Free**

#### 4. Environment Variables (Optional)
Klik **"Advanced"** dan tambahkan:
- Key: `FLASK_ENV`, Value: `production`

#### 5. Deploy!
- Klik **"Create Web Service"**
- Tunggu 10-15 menit (download model AI pertama kali)
- Render akan memberikan URL seperti: `https://smarttranslate-backend.onrender.com`
- **CATAT URL INI!** Anda akan membutuhkannya untuk frontend

#### 6. Verifikasi Backend
- Buka URL Render di browser
- Anda akan melihat error 404 atau "Method Not Allowed" (ini NORMAL)
- Backend siap digunakan!

---

### Part B: Deploy Frontend ke Netlify

#### 1. Update API URL di Frontend

**PENTING**: Ganti URL backend dengan URL Render Anda!

Edit file `frontend/index.html` baris 89:

```html
<!-- SEBELUM -->
<script>
  window.API_URL = "http://127.0.0.1:5000/translate";
</script>

<!-- SESUDAH (ganti dengan URL Render Anda) -->
<script>
  window.API_URL = "https://smarttranslate-backend.onrender.com/translate";
</script>
```

Jangan lupa **commit dan push**:
```bash
git add frontend/index.html
git commit -m "Update API URL for production"
git push origin main
```

#### 2. Deploy ke Netlify

**Cara A: Drag & Drop (Paling Mudah)**

1. Buka: https://netlify.com/
2. Login dengan GitHub atau email
3. Klik **"Add new site"** → **"Deploy manually"**
4. **Drag folder `frontend`** ke area drop zone
5. Tunggu beberapa detik
6. Netlify akan memberikan URL seperti: `https://random-name-123.netlify.app`
7. **SELESAI!** Buka URL tersebut dan test aplikasi Anda

**Cara B: Connect to Git (Auto-deploy)**

1. Buka: https://netlify.com/
2. Klik **"Add new site"** → **"Import an existing project"**
3. Pilih **GitHub**
4. Pilih repository **`Aplikasi_SmartTranslater`**
5. Konfigurasi:
   - **Base directory**: `frontend`
   - **Build command**: (kosongkan)
   - **Publish directory**: `.`
6. Klik **"Deploy site"**
7. Setiap kali Anda push ke GitHub, Netlify akan auto-deploy!

---

## 📋 OPSI 2: Vercel (All-in-One)

Vercel bisa deploy backend Python dengan Serverless Functions!

### 1. Buat Vercel Configuration

Saya sudah buatkan file `vercel.json`, tapi kita perlu update untuk backend juga.

### 2. Deploy ke Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login:
```bash
vercel login
```

3. Deploy:
```bash
cd c:\smarttranslater
vercel --prod
```

4. Ikuti instruksi di terminal
5. Vercel akan memberikan URL production

**CATATAN**: Backend Python di Vercel ada limitasi (cold start, timeout). Lebih baik pakai Render untuk backend.

---

## 📋 OPSI 3: Heroku (Berbayar)

Heroku tidak lagi gratis, tapi masih bagus untuk production.

### 1. Install Heroku CLI
Download dari: https://devcenter.heroku.com/articles/heroku-cli

### 2. Login dan Deploy
```bash
heroku login
heroku create smarttranslate-app
git push heroku main
heroku open
```

**Biaya**: ~$7/month untuk Eco Dynos

---

## 🧪 Testing Setelah Deploy

### Test Backend
```bash
# Ganti URL dengan URL Render Anda
curl -X POST https://smarttranslate-backend.onrender.com/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"halo\",\"source\":\"id\",\"target\":\"en\"}"

# Harusnya return: {"result":"Hello."}
```

### Test Frontend
1. Buka URL Netlify/Vercel di browser
2. Ketik teks Indonesia, pilih target English
3. Klik **Translate**
4. Harusnya muncul hasil terjemahan

---

## ❗ Troubleshooting

### Backend Render lambat/timeout
- **Penyebab**: Free tier Render sleep setelah 15 menit tidak digunakan
- **Solusi**: Request pertama akan lambat (30-60 detik), request berikutnya cepat
- **Upgrade**: Pakai paid tier ($7/month) untuk always-on

### CORS Error
- **Penyebab**: Backend URL salah atau backend belum ready
- **Solusi**: 
  1. Cek URL di `frontend/index.html` sudah benar
  2. Pastikan backend sudah selesai deploy di Render
  3. Test backend langsung dengan curl

### Frontend tidak bisa connect
- **Solusi**:
  1. Buka DevTools (F12) → Console tab
  2. Lihat error message
  3. Pastikan API_URL sudah update dengan URL Render
  4. Pastikan URL pakai HTTPS (bukan HTTP)

---

## 💰 Biaya

### Free Tier
- **Render**: 750 jam/bulan gratis (cukup untuk 1 app)
- **Netlify**: Unlimited deployments, 100GB bandwidth/bulan
- **Total**: **GRATIS** untuk penggunaan normal

### Paid Tier (Jika Perlu)
- **Render**: $7/month (always-on, lebih cepat)
- **Netlify**: Gratis sudah cukup
- **Total**: ~$7/month

---

## 📝 Checklist Deployment

- [ ] Backend deployed di Render
- [ ] Copy URL Render
- [ ] Update `frontend/index.html` dengan URL Render
- [ ] Commit dan push perubahan
- [ ] Deploy frontend ke Netlify
- [ ] Test aplikasi di browser
- [ ] Cek tidak ada error di Console

---

## 🎉 Selesai!

Setelah deploy, Anda akan punya:
- **Backend**: https://smarttranslate-backend.onrender.com
- **Frontend**: https://your-app.netlify.app

Share URL frontend ke teman-teman Anda! 🚀
