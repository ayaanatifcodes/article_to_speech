import os
import pdfplumber
from gtts import gTTS
from flask import Flask, request, send_file, jsonify
from pydub import AudioSegment

app = Flask(__name__)
def extract_text():
    pdf_File = pdfplumber.open("sample.pdf")
    article_content =[]
    for page in pdf_File.pages:
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

@app.route("/tts", methods=["POST"])
def text_to_speech():
    data = request.json
    language = data.get("language", "en")
    pace = data.get("pace", "normal")
    slow = data.get("slow", False)
    text = extract_text()
    
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save("temp_output.mp3")
    
    audio = AudioSegment.from_mp3("temp_output.mp3")

    if pace == "slow":
        audio = audio._spawn(audio.raw_data, overrides = {
            "frame_rate": int(audio.frame_rate * 0.75)
        }).set_frame_rate(audio.frame_rate)
    elif pace == "fast":
        audio = audio._spawn(audio.raw_data, overrides = {
            "frame_rate":int(audio.frame_rate * 1.25)
        }).set_frame_rate(audio.frame_rate)
    audio.export("final_output.mp3", format="mp3")

    if os.path.exists("temp_output.mp3"):
        os.remove("temp_output.mp3")
    
    return send_file("final_output.mp3", as_attachement = True)

if __name__ == "__main__":
    app.run(debug = True)
        

