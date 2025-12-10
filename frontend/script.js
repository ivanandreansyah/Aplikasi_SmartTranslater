const API_URL = "http://127.0.0.1:5000/translate";
const FORM_ID = "smarttranslate-history";

const textInput = document.getElementById("textInput");
const translateBtn = document.getElementById("translateBtn");
const statusText = document.getElementById("status");
const resultText = document.getElementById("resultText");
const historyList = document.getElementById("historyList");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");
const sourceLangSelect = document.getElementById("sourceLang");
const targetLangSelect = document.getElementById("targetLang");
const swapBtn = document.getElementById("swapBtn");
const speakBtn = document.getElementById("speakBtn");
const copyBtn = document.getElementById("copyBtn");
const speakInputBtn = document.getElementById("speakInputBtn");
const micBtn = document.getElementById("micBtn");

const MAX_HISTORY = 10;

// Speech Recognition setup
let recognition = null;
let isRecording = false;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  
  recognition.onstart = () => {
    isRecording = true;
    micBtn.classList.add("recording");
    micBtn.textContent = "⏹️";
    setStatus("Listening... Speak now.");
  };
  
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    textInput.value = transcript;
    textInput.dispatchEvent(new Event("input"));
    setStatus("Voice captured. Click Translate to proceed.");
  };
  
  recognition.onerror = (event) => {
    setStatus(`Speech recognition error: ${event.error}`, true);
    isRecording = false;
    micBtn.classList.remove("recording");
    micBtn.textContent = "🎤";
  };
  
  recognition.onend = () => {
    isRecording = false;
    micBtn.classList.remove("recording");
    micBtn.textContent = "🎤";
    if (!textInput.value.trim()) {
      setStatus("No speech detected. Try again.");
    }
  };
} else {
  micBtn.disabled = true;
  micBtn.title = "Speech recognition not supported in this browser";
}

const animateResult = () => {
  resultText.classList.remove("result-show");
  void resultText.offsetWidth;
  resultText.classList.add("result-show");
};

const LANGUAGE_VOICE_HINT = {
  en: "en",
  id: "id",
};

let availableVoices = [];

const refreshVoices = () => {
  availableVoices = window.speechSynthesis
    ? window.speechSynthesis.getVoices()
    : [];
};

if ("speechSynthesis" in window) {
  refreshVoices();
  window.speechSynthesis.onvoiceschanged = refreshVoices;
}

const speakText = (text, langCode) => {
  if (!("speechSynthesis" in window)) {
    setStatus("Text-to-speech not supported in this browser.", true);
    return;
  }

  if (!text.trim()) return;

  const utterance = new SpeechSynthesisUtterance(text);
  const hint = LANGUAGE_VOICE_HINT[langCode] || "en";
  utterance.lang = langCode === "id" ? "id-ID" : "en-US";
  const voice =
    availableVoices.find((v) => v.lang.toLowerCase().startsWith(hint)) || null;
  if (voice) {
    utterance.voice = voice;
  }

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
};

const speakResult = () => {
  const text = resultText.textContent.trim();
  if (!text) return;
  const target = targetLangSelect.value;
  speakText(text, target);
};

const speakInput = () => {
  const text = textInput.value.trim();
  if (!text) return;
  const source = sourceLangSelect.value;
  speakText(text, source);
};

const loadHistory = () => {
  const stored = localStorage.getItem(FORM_ID);
  return stored ? JSON.parse(stored) : [];
};

const saveHistory = (entries) => {
  localStorage.setItem(FORM_ID, JSON.stringify(entries.slice(0, MAX_HISTORY)));
};

const renderHistory = () => {
  const history = loadHistory();
  historyList.innerHTML = "";

  if (history.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No translations yet.";
    empty.classList.add("history-entry");
    historyList.appendChild(empty);
    return;
  }

  history.forEach((item) => {
    const li = document.createElement("li");
    li.className = "history-entry";

    const meta = document.createElement("span");
    meta.textContent = `${item.source} → ${item.target} • ${item.timestamp}`;

    const original = document.createElement("p");
    original.textContent = item.text;

    const translated = document.createElement("p");
    translated.textContent = item.result;
    translated.style.fontWeight = "600";

    li.append(meta, original, translated);
    historyList.appendChild(li);
  });
};

const addToHistory = (entry) => {
  const history = loadHistory();
  history.unshift(entry);
  saveHistory(history);
  renderHistory();
};

const setStatus = (message, isError = false) => {
  statusText.textContent = message;
  statusText.style.color = isError ? "#dc2626" : "#6b7280";
};

const translateText = async () => {
  const text = textInput.value.trim();
  if (!text) {
    setStatus("Please provide text to translate.", true);
    resultText.textContent = "";
    return;
  }

  const source = sourceLangSelect.value;
  const target = targetLangSelect.value;

  if (source === target) {
    setStatus("Source and target languages must differ.", true);
    resultText.textContent = "";
    return;
  }

  translateBtn.disabled = true;
  setStatus("Translating...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, source, target }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unexpected server error.");
    }

    resultText.textContent = data.result;
    animateResult();
    const entry = {
      text,
      result: data.result,
      source: sourceLangSelect.selectedOptions[0].text,
      target: targetLangSelect.selectedOptions[0].text,
      timestamp: new Date().toLocaleString(),
    };
    addToHistory(entry);
    setStatus("Done.");
    speakBtn.disabled = false;
    copyBtn.disabled = false;
  } catch (error) {
    setStatus(error.message, true);
    resultText.textContent = "";
    speakBtn.disabled = true;
    copyBtn.disabled = true;
    resultText.classList.remove("result-show");
  } finally {
    translateBtn.disabled = false;
  }
};

translateBtn.addEventListener("click", translateText);

textInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
    translateText();
  }
});

textInput.addEventListener("input", () => {
  const hasText = textInput.value.trim().length > 0;
  speakInputBtn.disabled = !hasText;
});

micBtn.addEventListener("click", () => {
  if (!recognition) {
    setStatus("Speech recognition not supported in this browser.", true);
    return;
  }
  
  if (isRecording) {
    recognition.stop();
    return;
  }
  
  const source = sourceLangSelect.value;
  recognition.lang = source === "id" ? "id-ID" : "en-US";
  recognition.start();
});

speakInputBtn.addEventListener("click", speakInput);

clearHistoryBtn.addEventListener("click", () => {
  localStorage.removeItem(FORM_ID);
  renderHistory();
});

swapBtn.addEventListener("click", () => {
  const sourceValue = sourceLangSelect.value;
  sourceLangSelect.value = targetLangSelect.value;
  targetLangSelect.value = sourceValue;
  setStatus("Language selection updated.");
});

speakBtn.addEventListener("click", speakResult);

const copyResult = async () => {
  const text = resultText.textContent.trim();
  if (!text) return;

  try {
    await navigator.clipboard.writeText(text);
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "✓";
    copyBtn.style.background = "rgba(34, 197, 94, 0.9)";
    setStatus("Copied to clipboard!");
    
    setTimeout(() => {
      copyBtn.textContent = originalText;
      copyBtn.style.background = "";
    }, 2000);
  } catch (error) {
    // Fallback untuk browser yang tidak support clipboard API
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand("copy");
      const originalText = copyBtn.textContent;
      copyBtn.textContent = "✓";
      copyBtn.style.background = "rgba(34, 197, 94, 0.9)";
      setStatus("Copied to clipboard!");
      
      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = "";
      }, 2000);
    } catch (err) {
      setStatus("Failed to copy. Please select and copy manually.", true);
    }
    document.body.removeChild(textArea);
  }
};

copyBtn.addEventListener("click", copyResult);

renderHistory();


