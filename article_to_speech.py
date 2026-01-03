import os
from gtts import gTTS
import pdfplumber
import io
from flask import Flask, request, send_file, jsonify
from pydub import AudioSegment

app = Flask(__name__)

def extract_text():
    pdf_File = pdfplumber.open("sample.pdf")
    article_content = []

    for page in pdf_File.pages:
        article_text = page.extract_text()
        if article_text:
            article_content.append(article_text)
    pdf_File.close()
    return " ".join(article_content)

def add_pauses_between_paras(text, language = 'en', slow = False, pause_ms = 500):
    # '\n\ indicates a new line (when i press enter)
    paragraphs = text.split('\n\n') 
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return AudioSegment.silent(duration = 0)
        
    # Create pause
    pause = AudioSegment.silent(duration=pause_ms)
    
    # Convert first paragraph to audio
    tts = gTTS(text=paragraphs[0], lang=language, slow=slow)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    final_audio = AudioSegment.from_file(mp3_fp, format='mp3')
    
    # Add remaining paragraphs with pauses
    for para in paragraphs[1:]:
        tts = gTTS(text=para, lang=language, slow=slow)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format='mp3')
        final_audio = final_audio + pause + audio
    
    return final_audio
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

 def text_to_speech():
    data = request.json
    language = data.get("language", "en")
    pace = data.get("pace", "normal")
    slow = data.get("slow", False)
    pause_duration = data.get("pause_duration", 800)
    
    text = extract_text()
    
    audio = add_pauses_between_paragraphs(text, language, slow, pause_duration)
    
    if pace == "slow":
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 0.75)
        }).set_frame_rate(audio.frame_rate)
    elif pace == "fast":
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 1.25)
        }).set_frame_rate(audio.frame_rate)
    
    audio.export("final_output.mp3", format="mp3")
    
    return send_file("final_output.mp3", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)



