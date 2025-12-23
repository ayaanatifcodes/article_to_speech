import os
import pdfplumber
from gtts import gTTS
from flask import Flask, request, send_file

app = Flask(__name__)
def extract_text():
    pdf_File = pdfplumber.open("sample.pdf")
    article_content = []
    for page in pdf_FIle.pages:
        article_text = page.extract_text()
        if article_text:
            article_content.append(article_text)
    pdf_File.close()
    return " ".join(article_content)

supported_languages = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean'
}

@app.route('/tts', methods = ['POST'])
def text_to_speech():
    data = request.json()
    language = data.get('language', 'English')
    text = extract_text()
    lang_code = supported_languages.get(language, 'en')
    tts = gTTS(text = text, lang = lang_code)
    tts.save("output.mp3")
    return send_file("output.mp3", as_attachment = True)

if __name__ == '__main__':
    app.run(debug = True)
