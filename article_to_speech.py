import io
import pdfplumber
from flask import Flask, request, send_file
from gtts import gTTS
from pydub import AudioSegment

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                content.append(text)
    return "\n\n".join(content)

def add_pauses_between_paragraphs(text, lang="en", slow=False, pause_ms=800):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    pause = AudioSegment.silent(duration=pause_ms)

    final_audio = AudioSegment.empty()

    for para in paragraphs:
        tts = gTTS(text=para, lang=lang, slow=slow)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        final_audio += audio + pause

    return final_audio

@app.route("/generate-audio", methods=["POST"])
def text_to_speech():
    data = request.json
    language = data.get("language", "en")
    pause_duration = data.get("pause_duration", 800)

    text = extract_text_from_pdf("sample.pdf")
    audio = add_pauses_between_paragraphs(text, language, pause_duration)

    audio.export("cosmoyage_article.mp3", format="mp3")
    return send_file("cosmoyage_article.mp3", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
