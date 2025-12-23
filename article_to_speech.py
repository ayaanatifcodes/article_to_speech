import os
import pdfplumber
from gtts import gTTS
from flask import Flask, request, send_file

app = Flask(__name__)
def extracted_text():
    pdf_File = pdfplumber.open("sample.pdf")
    article_content = []

    for page in pdf_File.pages:
        article_text = page.extract_text()
        if article_text:
            article_content.append(article_text)
    pdf_File.close()
    return " ".join(article_content)

supported_languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru",
    "Urdu": "ur" ,
    "Hindi": "hi",
    "Korean": "ko",
    "Farsi": "fa"
}

@app.route("/tts", methods = ["POST"]) # This tells flask when /tts is requested and when to run function
def text_to_speech():
    data = request.json
    language = data.get("language", "English")
    text = extracted_text()

    lang_code = Supported_Languages.get(language, "en")
    tts = gTTS(text=text, lang=lang_code)
    audio_file = "output.mp3"
    tts.save(audio_file)

    return send_file(audio_file, as_attachment=True)
