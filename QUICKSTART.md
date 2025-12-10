# ⚡ Quick Start - Deploy SmartTranslate

## 🎯 Tujuan
Deploy aplikasi SmartTranslate ke internet (GRATIS!)

## 📦 Yang Dibutuhkan
- ✅ Akun GitHub (sudah ada)
- ✅ Code sudah di GitHub (sudah push)
- ⏰ Waktu: ~20 menit

---

## 🚀 3 Langkah Mudah

### 1️⃣ BACKEND → Render.com
```
1. Buka: https://render.com/
2. Sign in dengan GitHub
3. New + → Web Service → Pilih repo Aplikasi_SmartTranslater
4. Konfigurasi:
   - Environment: Docker
   - Region: Singapore
   - Instance Type: Free
5. Deploy (tunggu 10-15 menit)
6. COPY URL yang diberikan
```

### 2️⃣ UPDATE CODE
```bash
# Jalankan script otomatis:
python update_api_url.py https://URL-RENDER-ANDA

# Atau edit manual: frontend/index.html baris 89

# Lalu commit:
git add frontend/index.html
git commit -m "Update API URL"
git push origin main
```

### 3️⃣ FRONTEND → Netlify.com
```
1. Buka: https://netlify.com/
2. Sign in
3. Add new site → Deploy manually
4. Drag folder "frontend" ke Netlify
5. SELESAI! Copy URL yang diberikan
```

---

## ✅ Test Aplikasi

Buka URL Netlify → Ketik "Halo" → Translate → Harusnya jadi "Hello"

---

## 📚 Dokumentasi Lengkap

- **Panduan Detail**: Baca `DEPLOY_NOW.md`
- **Troubleshooting**: Baca `DEPLOYMENT.md`
- **Workflow**: Baca `.agent/workflows/deploy.md`

---

## 🆘 Masalah?

1. Cek `DEPLOY_NOW.md` bagian Troubleshooting
2. Buka browser DevTools (F12) → Console
3. Screenshot error dan hubungi saya

---

**Good luck! 🚀**
