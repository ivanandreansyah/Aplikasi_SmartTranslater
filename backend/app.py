import os
from typing import Any, Dict, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import MarianMTModel, MarianTokenizer


app = Flask(__name__)
CORS(app, resources={r"/translate": {"origins": "*"}})

# Supported translation directions
SUPPORTED_MODELS = {
    "id-en": os.getenv("SMARTTRANSLATE_MODEL_ID_EN", "Helsinki-NLP/opus-mt-id-en"),
    "en-id": os.getenv("SMARTTRANSLATE_MODEL_EN_ID", "Helsinki-NLP/opus-mt-en-id"),
}

# Cache loaded models and tokenizers so they only download once
MODEL_CACHE: Dict[str, Tuple[MarianTokenizer, MarianMTModel]] = {}


def get_model(direction: str) -> Tuple[MarianTokenizer, MarianMTModel]:
    if direction not in MODEL_CACHE:
        model_name = SUPPORTED_MODELS[direction]
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        MODEL_CACHE[direction] = (tokenizer, model)
    return MODEL_CACHE[direction]


@app.post("/translate")
def translate() -> Any:
    """
    Translate text between Indonesian <-> English using MarianMT.
    """
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    text: str = (payload.get("text") or "").strip()
    source = (payload.get("source") or "").strip().lower()
    target = (payload.get("target") or "").strip().lower()

    if not text:
        return jsonify({"error": "Text field must not be empty."}), 400

    if not source or not target:
        return jsonify({"error": "Source and target languages are required."}), 400

    if source == target:
        return jsonify({"error": "Source and target languages must be different."}), 400

    direction = f"{source}-{target}"
    if direction not in SUPPORTED_MODELS:
        return jsonify({"error": f"Unsupported direction: {direction}."}), 400

    try:
        tokenizer, model = get_model(direction)
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**tokens)
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        return jsonify({"result": result})
    except Exception as exc:  # pragma: no cover - defensive path
        return jsonify({"error": f"Translation failed: {exc}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)


