# Audio-Enhanced Reading Platform

## Overview
I created this project as an **interactive text-to-speech (TTS) system** to make reading on my personal website more engaging, immersive, and accessible. The idea is to allow users to **listen to articles, documents, and other text content** while following along with highlighted words. This creates a seamless audio-visual experience that improves focus, comprehension, and overall engagement with the content.

## Features
The platform is designed with user experience and accessibility in mind. Key features include:

- **Multi-language support:** Users can listen to content in different languages.  
- **Multiple voices:** Options for different narration voices to suit preference.  
- **Adjustable speed:** Control playback speed to match reading comfort.  
- **Word highlighting:** The current word being spoken is highlighted in real-time, helping users follow along easily.  

These features make the system suitable for readers who prefer audio, those with visual impairments, or anyone who wants to multitask while consuming content.

## Technology
This repository demonstrates how **Python, PDF processing, and TTS technologies** can be combined into a functional web-ready platform. It uses libraries such as `pdfplumber` to extract text from documents and `gTTS` to convert text into speech. The project is designed to be extensible, so more voices, languages, and user-customizable options can be added in future iterations.

## Installation and Usage
To get started, ensure Python is installed on your system. Then, install the required packages:

```bash
python -m pip install pdfplumber gTTS
