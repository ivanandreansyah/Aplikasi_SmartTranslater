"""
SmartTranslate - Gradio App for Hugging Face Spaces
Indonesian ↔ English AI Translator using MarianMT
"""

import gradio as gr
from transformers import MarianMTModel, MarianTokenizer
import torch

# Load models
print("Loading models...")
tokenizer_id_en = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-id-en")
model_id_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-id-en")

tokenizer_en_id = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-id")
model_en_id = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-id")
print("Models loaded successfully!")

def translate(text, source_lang, target_lang):
    """
    Translate text between Indonesian and English
    """
    if not text or not text.strip():
        return "⚠️ Please enter some text to translate"
    
    if source_lang == target_lang:
        return "⚠️ Source and target languages must be different"
    
    # Determine direction
    direction = f"{source_lang}-{target_lang}"
    
    # Select appropriate model
    if direction == "id-en":
        tokenizer, model = tokenizer_id_en, model_id_en
    elif direction == "en-id":
        tokenizer, model = tokenizer_en_id, model_en_id
    else:
        return f"❌ Unsupported translation direction: {direction}"
    
    try:
        # Tokenize and translate
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            translated = model.generate(**tokens)
        
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        return result
    
    except Exception as e:
        return f"❌ Translation error: {str(e)}"

# Example translations
examples = [
    ["Halo, apa kabar? Semoga harimu menyenangkan!", "id", "en"],
    ["Hello, how are you? Have a great day!", "en", "id"],
    ["Saya suka belajar bahasa Indonesia", "id", "en"],
    ["I love learning new languages", "en", "id"],
    ["Terima kasih banyak atas bantuannya", "id", "en"],
]

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🌐 SmartTranslate
        ### AI-Powered Indonesian ↔ English Translator
        
        Powered by **MarianMT** (Helsinki-NLP) - State-of-the-art neural machine translation
        """
    )
    
    with gr.Row():
        with gr.Column():
            source_lang = gr.Radio(
                choices=["id", "en"],
                value="id",
                label="Source Language",
                info="Language of the input text"
            )
            
            input_text = gr.Textbox(
                label="Text to Translate",
                placeholder="Enter text here...",
                lines=5,
                max_lines=10
            )
        
        with gr.Column():
            target_lang = gr.Radio(
                choices=["en", "id"],
                value="en",
                label="Target Language",
                info="Language to translate to"
            )
            
            output_text = gr.Textbox(
                label="Translation Result",
                lines=5,
                max_lines=10,
                interactive=False
            )
    
    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear", variant="secondary")
        translate_btn = gr.Button("🔄 Translate", variant="primary", scale=2)
    
    gr.Markdown("### 📝 Example Translations")
    gr.Examples(
        examples=examples,
        inputs=[input_text, source_lang, target_lang],
        outputs=output_text,
        fn=translate,
        cache_examples=False
    )
    
    gr.Markdown(
        """
        ---
        ### ℹ️ About
        - **Models**: Helsinki-NLP/opus-mt-id-en & opus-mt-en-id
        - **Framework**: Hugging Face Transformers
        - **Interface**: Gradio
        
        Made with ❤️ using open-source AI
        """
    )
    
    # Event handlers
    translate_btn.click(
        fn=translate,
        inputs=[input_text, source_lang, target_lang],
        outputs=output_text
    )
    
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=[],
        outputs=[input_text, output_text]
    )
    
    # Auto-translate on Enter
    input_text.submit(
        fn=translate,
        inputs=[input_text, source_lang, target_lang],
        outputs=output_text
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
