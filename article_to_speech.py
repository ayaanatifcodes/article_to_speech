import os  # Provides access to operating system utilities
import io  # Allows handling in-memory byte streams
import pdfplumber  # Library to extract text from PDF files
from gtts import gTTS  # Google Text-to-Speech for converting text to audio
from flask import Flask, request, send_file, jsonify  # Flask components for API handling
from pydub import AudioSegment  # Audio processing library for combining and modifying audio

app = Flask(__name__)  # Initialize Flask application

def extract_text():  # Function to extract text from a PDF
    pdf_File = pdfplumber.open("sample.pdf")  # Open the PDF file
    article_content = []  # List to store extracted text from all pages

    for page in pdf_File.pages:  # Loop through each page in the PDF
        article_text = page.extract_text()  # Extract text from the page
        if article_text:  # Check if text exists on the page
            article_content.append(article_text)  # Add text to the list

    pdf_File.close()  # Close the PDF file
    return " ".join(article_content)  # Combine all page text into a single string

def add_pauses_between_paras(text, language='en', slow=False, pause_ms=500):  # Convert text to speech with pauses
    paragraphs = text.split('\n\n')  # Split text into paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]  # Remove empty paragraphs

    if not paragraphs:  # If no valid paragraphs exist
        return AudioSegment.silent(duration=0)  # Return silent audio

    pause = AudioSegment.silent(duration=pause_ms)  # Create silent pause between paragraphs

    tts = gTTS(text=paragraphs[0], lang=language, slow=slow)  # Generate speech for first paragraph
    mp3_fp = io.BytesIO()  # Create in-memory byte buffer
    tts.write_to_fp(mp3_fp)  # Write audio data to buffer
    mp3_fp.seek(0)  # Reset buffer position
    final_audio = AudioSegment.from_file(mp3_fp, format='mp3')  # Load audio into AudioSegment

    for para in paragraphs[1:]:  # Loop through remaining paragraphs
        tts = gTTS(text=para, lang=language, slow=slow)  # Convert paragraph to speech
        mp3_fp = io.BytesIO()  # Create new in-memory buffer
        tts.write_to_fp(mp3_fp)  # Write audio data
        mp3_fp.seek(0)  # Reset buffer position
        audio = AudioSegment.from_file(mp3_fp, format='mp3')  # Load audio segment
        final_audio = final_audio + pause + audio  # Append pause and audio to final output

    return final_audio  # Return combined audio with pauses

supported_languages = {  # Dictionary of supported language codes
    'en': 'English',  # English language
    'es': 'Spanish',  # Spanish language
    'fr': 'French',  # French language
    'de': 'German',  # German language
    'it': 'Italian',  # Italian language
    'pt': 'Portuguese',  # Portuguese language
    'zh-cn': 'Chinese (Simplified)',  # Simplified Chinese
    'ja': 'Japanese',  # Japanese language
    'ko': 'Korean'  # Korean language
}

@app.route("/text-to-speech", methods=["POST"])  # Define POST API endpoint
def text_to_speech():  # API function for text-to-speech
    data = request.json if request.json else {}  # Get JSON payload from request

    language = data.get("language", "en")  # Get selected language
    pace = data.get("pace", "normal")  # Get speaking pace
    slow = data.get("slow", False)  # Get slow speech flag
    pause_duration = data.get("pause_duration", 800)  # Get pause duration in ms

    if language not in supported_languages:  # Validate language support
        return jsonify({"error": "Unsupported language"}), 400  # Return error response

    text = extract_text()  # Extract text from PDF

    audio = add_pauses_between_paras(  # Convert text to speech with pauses
        text=text,
        language=language,
        slow=slow,
        pause_ms=pause_duration
    )

    if pace == "slow":  # If slow pace is requested
        audio = audio._spawn(audio.raw_data, overrides={  # Modify playback speed
            "frame_rate": int(audio.frame_rate * 0.75)  # Reduce frame rate
        }).set_frame_rate(audio.frame_rate)  # Reset frame rate
    elif pace == "fast":  # If fast pace is requested
        audio = audio._spawn(audio.raw_data, overrides={  # Modify playback speed
            "frame_rate": int(audio.frame_rate * 1.25)  # Increase frame rate
        }).set_frame_rate(audio.frame_rate)  # Reset frame rate

    audio.export("final_output.mp3", format="mp3")  # Save final audio file
    return send_file("final_output.mp3", as_attachment=True)  # Send file to user

if __name__ == "__main__":  # Check if script is run directly
    app.run(debug=True)  # Start Flask server in debug mode
