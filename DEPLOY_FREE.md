# 🆓 Deploy SmartTranslate - 100% GRATIS

## ⚠️ Update: Railway & Render Berbayar
Railway dan Render sekarang sudah tidak gratis lagi. Berikut alternatif yang **BENAR-BENAR GRATIS**:

---

## 🎯 OPSI 1: PythonAnywhere + Netlify (RECOMMENDED)

### ✅ Kelebihan:
- **100% GRATIS SELAMANYA**
- Mudah setup
- Khusus untuk Python apps
- Reliable

### Part A: Deploy Backend ke PythonAnywhere

#### 1. Buat Akun PythonAnywhere
- Buka: https://www.pythonanywhere.com/
- Klik **"Start running Python online in less than a minute!"**
- Pilih **"Create a Beginner account"** (GRATIS)
- Isi form registrasi

#### 2. Upload Code

**Cara 1: Via Git (Recommended)**
```bash
# Di PythonAnywhere Console (Bash):
git clone https://github.com/ivanandreansyah/Aplikasi_SmartTranslater.git
cd Aplikasi_SmartTranslater
```

**Cara 2: Upload Manual**
- Klik tab **"Files"**
- Upload folder `backend`

#### 3. Install Dependencies
```bash
# Di Console:
cd Aplikasi_SmartTranslater/backend
pip3.10 install --user flask flask-cors torch transformers sentencepiece sacremoses
```

#### 4. Setup Web App
- Klik tab **"Web"**
- Klik **"Add a new web app"**
- Pilih **"Manual configuration"**
- Python version: **3.10**

#### 5. Konfigurasi WSGI
- Di tab Web, klik **"WSGI configuration file"**
- Ganti isi file dengan:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/Aplikasi_SmartTranslater/backend'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import flask app
from app import app as application
```

Ganti `YOUR_USERNAME` dengan username PythonAnywhere Anda.

#### 6. Reload & Get URL
- Klik **"Reload"** (tombol hijau)
- URL Anda: `https://YOUR_USERNAME.pythonanywhere.com`
- **COPY URL INI!**

#### 7. Test Backend
```bash
curl -X POST https://YOUR_USERNAME.pythonanywhere.com/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"halo","source":"id","target":"en"}'
```

### Part B: Deploy Frontend ke Netlify

Sama seperti panduan sebelumnya:

1. Update API URL di `frontend/index.html`:
```html
<script>
  window.API_URL = "https://YOUR_USERNAME.pythonanywhere.com/translate";
</script>
```

2. Commit & push:
```bash
git add frontend/index.html
git commit -m "Update API URL for PythonAnywhere"
git push origin main
```

3. Deploy ke Netlify:
- Buka https://netlify.com/
- Drag & drop folder `frontend`
- SELESAI!

---

## 🎯 OPSI 2: Hugging Face Spaces + Netlify

### ✅ Kelebihan:
- **100% GRATIS**
- Cocok untuk AI/ML apps
- Auto-scaling
- Community support

### Part A: Deploy Backend ke Hugging Face Spaces

#### 1. Buat Akun
- Buka: https://huggingface.co/
- Sign up gratis

#### 2. Create Space
- Klik **"New"** → **"Space"**
- Name: `smarttranslate`
- SDK: **Gradio** atau **Docker**
- Visibility: **Public**

#### 3. Buat File untuk Gradio

Buat file `app_gradio.py`:

```python
import gradio as gr
from transformers import MarianMTModel, MarianTokenizer

# Load models
tokenizer_id_en = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-id-en")
model_id_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-id-en")

tokenizer_en_id = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-id")
model_en_id = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-id")

def translate(text, source, target):
    if source == target:
        return "Source and target must be different"
    
    direction = f"{source}-{target}"
    
    if direction == "id-en":
        tokenizer, model = tokenizer_id_en, model_id_en
    elif direction == "en-id":
        tokenizer, model = tokenizer_en_id, model_en_id
    else:
        return f"Unsupported direction: {direction}"
    
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**tokens)
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    
    return result

# Create Gradio interface
demo = gr.Interface(
    fn=translate,
    inputs=[
        gr.Textbox(label="Text to translate", lines=3),
        gr.Radio(["id", "en"], label="Source Language", value="id"),
        gr.Radio(["id", "en"], label="Target Language", value="en")
    ],
    outputs=gr.Textbox(label="Translation Result"),
    title="SmartTranslate",
    description="AI-powered Indonesian ↔ English translator using MarianMT"
)

if __name__ == "__main__":
    demo.launch()
```

#### 4. Upload ke Space
- Upload `app_gradio.py` ke Space Anda
- Buat `requirements.txt`:
```
transformers
torch
sentencepiece
sacremoses
gradio
```

#### 5. Get URL
- Hugging Face akan auto-deploy
- URL: `https://huggingface.co/spaces/YOUR_USERNAME/smarttranslate`

**CATATAN**: Dengan Gradio, Anda sudah punya UI, jadi tidak perlu frontend terpisah!

---

## 🎯 OPSI 3: Vercel Serverless (Dengan Limitasi)

### ⚠️ Limitasi:
- Timeout 10 detik (hobby plan)
- Cold start lambat
- Model AI mungkin terlalu besar

### Setup

Buat file `api/translate.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)
CORS(app)

# Models akan di-cache
models = {}

def get_model(direction):
    if direction not in models:
        model_name = f"Helsinki-NLP/opus-mt-{direction}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        models[direction] = (tokenizer, model)
    return models[direction]

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '').strip()
    source = data.get('source', '').lower()
    target = data.get('target', '').lower()
    
    direction = f"{source}-{target}"
    
    try:
        tokenizer, model = get_model(direction)
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**tokens)
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

Buat `vercel.json`:
```json
{
  "functions": {
    "api/*.py": {
      "runtime": "python3.9",
      "maxDuration": 10
    }
  }
}
```

Deploy:
```bash
npm install -g vercel
vercel --prod
```

**CATATAN**: Mungkin tidak work karena model terlalu besar dan timeout.

---

## 📊 Perbandingan Opsi

| Platform | Gratis? | Kecepatan | Mudah? | Limitasi |
|----------|---------|-----------|--------|----------|
| **PythonAnywhere** | ✅ Selamanya | ⭐⭐⭐ | ⭐⭐⭐⭐ | CPU terbatas |
| **Hugging Face** | ✅ Selamanya | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Public only |
| **Vercel** | ✅ Hobby | ⭐⭐ | ⭐⭐⭐ | Timeout 10s |
| Railway | ❌ Berbayar | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $5/bulan |
| Render | ❌ Berbayar | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $7/bulan |

---

## 🏆 REKOMENDASI SAYA

### Untuk Pemula: **Hugging Face Spaces**
- Paling mudah
- Sudah include UI (Gradio)
- Tidak perlu setup frontend terpisah
- Perfect untuk AI apps

### Untuk Full Control: **PythonAnywhere + Netlify**
- Gratis selamanya
- Bisa custom UI
- Lebih fleksibel

---

## 🚀 Quick Start - Hugging Face (TERMUDAH!)

1. **Buat akun** di https://huggingface.co/
2. **Create Space**: New → Space → Gradio
3. **Upload files**:
   - `app_gradio.py` (lihat kode di atas)
   - `requirements.txt`
4. **Tunggu deploy** (5-10 menit)
5. **SELESAI!** Buka URL Space Anda

---

## 💡 Tips

### PythonAnywhere
- Free tier: 512MB RAM, 1 web app
- Model AI akan lambat di-load pertama kali
- Setelah itu cepat

### Hugging Face
- Unlimited usage untuk public spaces
- Community support bagus
- Bisa upgrade ke private ($9/bulan) jika perlu

---

## 🆘 Troubleshooting

### PythonAnywhere: "Out of memory"
- Model AI terlalu besar untuk free tier
- Solusi: Pakai Hugging Face atau upgrade PythonAnywhere

### Hugging Face: Build failed
- Cek `requirements.txt` sudah benar
- Cek logs di Space dashboard

---

## 📞 Butuh Bantuan?

Pilih platform yang mau Anda pakai, lalu saya akan bantu setup detail!

**Rekomendasi: Mulai dengan Hugging Face Spaces (paling mudah!)** 🚀
