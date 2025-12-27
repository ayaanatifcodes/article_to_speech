# Article Text-To-Speech

## Overview
I created this project as an **interactive text-to-speech (TTS) system** to make reading on my personal website more engaging and obviously more accessible. The idea is to allow users to **listen to our articles** while they cannot physically sit down and read it as a whole. Yes, this is a pretty common thing to do but I wanted to challenge myself and build the feature from scratch and put a bit of my own twist in it.  

## Features
This feature is designed with user experience and accessibility in mind as I care about both of them more than anything when I am working on any of my projects. Key features include:

- **Multi-Language Support:** As it suggests, ssers can listen to content in different languages. This is perfect as Cosmoyage has users from 130+ countries and I woud love to accomodate them all.
- **Multiple Voices:** Options for different narration voices to suit preference (most of the voices will be taken from Google's TTS but I will try to add voices from larges LLMs as well).  
- **Adjustable Speed:** Control playback speed to match reading comfort and make it more accessible to users. 
- **Word Highlighting:** The current word being spoken is highlighted in real-time, helping users follow along easily and providing them with a autoscroll to make it easier from them to read without having to physically go down the page.

These features make the system suitable for readers who prefer audio, those with visual impairments, or anyone who wants to multitask while consuming content (a phenomenon grrowing pretty quick).

## Technology
This repository demonstrates how **Python, PDF processing, and TTS technologies** can be combined into a functional text-to-speech option for your platform/webistes. I will libraries such as `pdfplumber` (you can use `PyPDF2` but I am not using it due to it being present in every other project) to extract text from documents and `gTTS` to convert text into speech. I will keep on adding more technologies if I feel like it as the project goes on.

## Installation
To get started, ensure that Python is installed on your system by visiting `python.org` and, during installation, checking the option “Add Python to PATH.” Once installed, open the terminal in `VS Code (or your preferred code editor)` and type `python --version` to verify the installation. If Python is set up correctly, you can then install the required packages by running `python -m pip install pdfplumber gTTS` in the terminal.
