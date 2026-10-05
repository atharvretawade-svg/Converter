# Text-to-Speech Application in Python

## Description
A simple desktop Text-to-Speech application developed using Python and Tkinter. The application converts typed text into spoken audio using the `pyttsx3` library.

## Features
- Enter text in a text box
- Convert text to speech
- Select an installed system voice
- Adjust speech speed
- Stop speech
- Clear text

## Technologies
- Python 3
- Tkinter
- pyttsx3

## Installation

1. Make sure Python 3 is installed.
2. Open Command Prompt in this project folder.
3. Install the required package:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python text_to_speech.py
```

## Note for Windows
`pyttsx3` normally uses the Windows speech engine (SAPI5), so an internet connection is not required for basic speech synthesis.

## Project Objective
The objective of this project is to develop a simple and user-friendly application that converts written text into speech. It demonstrates Python GUI programming, functions, event handling, and text-to-speech technology.
