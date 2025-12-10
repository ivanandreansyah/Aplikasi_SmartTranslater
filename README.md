# SmartTranslate

A simple AI-powered translator web app (Indonesian ↔ English) using HuggingFace MarianMT, Flask backend, and vanilla HTML/CSS/JS frontend. Includes history (localStorage), text-to-speech (hasil & input), voice-to-text via microphone, swap languages, and copy-to-clipboard.

## Fitur
- Terjemahan dua arah: Indonesia ↔ Inggris (model MarianMT Helsinki-NLP).
- UI responsif, modern, dengan swap bahasa.
- History tersimpan di `localStorage` (auto trim 10 entri).
- Text-to-Speech:
  - Hasil terjemahan (tombol 🔊).
  - Input text (tombol 🔊 di textarea).
- Voice-to-Text (speech recognition, tombol 🎤) untuk mengisi textarea.
- Copy hasil terjemahan (tombol 📋).

## Struktur Proyek
```
backend/
  app.py
frontend/
  index.html
  styles.css
  script.js
.gitignore
```

## Prasyarat
- Python 3.9+
- Browser modern (Chrome/Edge disarankan untuk speech recognition)
- Koneksi internet saat pertama kali (unduh model MarianMT)

## Setup Backend
```powershell
cd C:\smarttranslater\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install flask flask-cors torch transformers sentencepiece sacremoses
```

## Menjalankan Backend
```powershell
cd C:\smarttranslater\backend
.\.venv\Scripts\activate   # jika pakai venv
python app.py
# Server di http://127.0.0.1:5000
```

## Menjalankan Frontend
1. Buka `C:\smarttranslater\frontend\index.html` di browser (double-click atau `start index.html`).
2. Pastikan backend aktif di `http://127.0.0.1:5000`.

## Penggunaan Cepat
1. Pilih bahasa sumber & target (tidak boleh sama; swap dengan ↔).
2. Ketik teks atau rekam suara (🎤) → teks muncul di textarea.
3. (Opsional) Dengarkan input (🔊 di textarea).
4. Klik **Translate**.
5. Hasil muncul; bisa didengar (🔊) atau disalin (📋). Riwayat tersimpan otomatis.

## API
Endpoint: `POST /translate`
```json
{
  "text": "halo",
  "source": "id",
  "target": "en"
}
```
Respon:
```json
{ "result": "Hello." }
```
Arah yang didukung: `id-en`, `en-id`.

Contoh uji via PowerShell:
```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/translate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text":"halo","source":"id","target":"en"}'
```

## Catatan TTS & Voice
- TTS memakai `speechSynthesis`; voice recognition memakai `webkitSpeechRecognition/SpeechRecognition` (terbaik di Chrome/Edge).
- Browser akan minta izin microphone saat pertama klik 🎤.

## Deploy / Git
```powershell
cd C:\smarttranslater
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/ivanandreansyah/Aplikasi_SmartTranslater.git
git branch -M main
git push -u origin main
```

## Deploy Cepat
### Opsi A: Backend di Render, Frontend di GitHub Pages
- Pastikan `requirements.txt` sudah ada (sudah disertakan).
- Render (Web Service):
  - Build: `pip install -r requirements.txt`
  - Start: `python backend/app.py`
  - Gunakan Python 3.9+; biarkan `PORT` dari environment Render.
  - CORS sudah diaktifkan untuk `/translate`.
- GitHub Pages:
  - Aktifkan Pages dari Settings → Pages → sumber `main` ke folder `/frontend`.
  - Setelah backend live, set `API_URL` ke URL backend Render (mis. `https://your-service.onrender.com/translate`).  
    - Opsi: tambahkan sebelum `<script src="script.js">` di `index.html`:
      ```html
      <script>
        window.API_URL = "https://your-service.onrender.com/translate";
      </script>
      ```
    - Atau ganti langsung konstanta default di `frontend/script.js`.

### Opsi B: Backend + Frontend di satu VPS/Server
- Jalankan backend dengan `gunicorn` atau `waitress`, reverse proxy dengan Nginx ke port 5000.
- Sajikan folder `frontend` sebagai static site; set `API_URL` ke domain/backend Anda.

## Lisensi
MIT (atur sesuai kebutuhan Anda).

