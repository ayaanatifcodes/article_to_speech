import os
import pdfplumber
from gtts import gTTS

article_File = pdf.plumber.open("article.pdf")
article_content = []

for page in article_File.pages:
    article_text = page.extract_text()
    if article_text:
        article_content = article_content.append(article_text)
article_File.close()

full_article = " ".join(article_content)
speech = gTTS(full_article, lang='en', slow = False)
speech.save("article_audio.mp3:)")