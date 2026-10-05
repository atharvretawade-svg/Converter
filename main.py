import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
import threading
import multiprocessing


# ============================================================
# TEXT TO SPEECH PROCESS
# ============================================================

def speech_process(text, voice_id, speed):

    try:

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            speed
        )

        engine.setProperty(
            "volume",
            1.0
        )

        if voice_id:

            engine.setProperty(
                "voice",
                voice_id
            )

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print("Speech Error:", e)


# ============================================================
# MAIN APPLICATION
# ============================================================

class SpeechTextApplication:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Speech & Text Application"
        )

        self.root.geometry(
            "800x600"
        )

        self.root.minsize(
            700,
            550
        )

        # Current page
        self.current_page = None

        # Speech-to-text
        self.recognizer = sr.Recognizer()

        self.is_listening = False

        # Text-to-speech
        self.speech_process = None

        # Main container
        self.main_frame = tk.Frame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # Start with home page
        self.show_home()

    # ========================================================
    # CLEAR CURRENT PAGE
    # ========================================================

    def clear_page(self):

        for widget in self.main_frame.winfo_children():

            widget.destroy()

    # ========================================================
    # HOME PAGE
    # ========================================================

    def show_home(self):

        self.stop_speech()

        self.clear_page()

        self.current_page = "home"

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = tk.Label(
            self.main_frame,
            text="Speech & Text Application",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=(70, 10)
        )

        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        subtitle = tk.Label(
            self.main_frame,
            text="Choose a conversion method",
            font=("Arial", 14)
        )

        subtitle.pack(
            pady=(0, 40)
        )

        # ----------------------------------------------------
        # SPEECH TO TEXT
        # ----------------------------------------------------

        speech_button = tk.Button(
            self.main_frame,
            text="🎤  Speech to Text",
            command=self.show_speech_to_text,
            width=30,
            height=2,
            font=("Arial", 15, "bold")
        )

        speech_button.pack(
            pady=12
        )

        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        text_button = tk.Button(
            self.main_frame,
            text="🔊  Text to Speech",
            command=self.show_text_to_speech,
            width=30,
            height=2,
            font=("Arial", 15, "bold")
        )

        text_button.pack(
            pady=12
        )

        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        info = tk.Label(
            self.main_frame,
            text="Convert speech into text or text into speech",
            font=("Arial", 11)
        )

        info.pack(
            pady=35
        )

    # ========================================================
    # SPEECH TO TEXT PAGE
    # ========================================================

    def show_speech_to_text(self):

        self.stop_speech()

        self.clear_page()

        self.current_page = "speech_to_text"

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top = tk.Frame(
            self.main_frame
        )

        top.pack(
            fill="x",
            padx=20,
            pady=15
        )

        back_button = tk.Button(
            top,
            text="← Home",
            command=self.show_home,
            font=("Arial", 11)
        )

        back_button.pack(
            side="left"
        )

        title = tk.Label(
            top,
            text="🎤 Speech to Text",
            font=("Arial", 22, "bold")
        )

        title.pack(
            side="left",
            padx=25
        )

        # ----------------------------------------------------
        # INSTRUCTION
        # ----------------------------------------------------

        tk.Label(
            self.main_frame,
            text="Click the button and speak into your microphone.",
            font=("Arial", 12)
        ).pack(
            pady=10
        )

        # ----------------------------------------------------
        # TEXT AREA
        # ----------------------------------------------------

        self.stt_text = tk.Text(
            self.main_frame,
            height=15,
            wrap="word",
            font=("Arial", 13)
        )

        self.stt_text.pack(
            padx=35,
            pady=15,
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = tk.Frame(
            self.main_frame
        )

        buttons.pack(
            pady=10
        )

        self.listen_button = tk.Button(
            buttons,
            text="🎤 Start Listening",
            command=self.start_listening,
            width=18,
            height=2,
            font=("Arial", 11, "bold")
        )

        self.listen_button.grid(
            row=0,
            column=0,
            padx=8
        )

        clear_button = tk.Button(
            buttons,
            text="Clear",
            command=self.clear_stt,
            width=15,
            height=2,
            font=("Arial", 11)
        )

        clear_button.grid(
            row=0,
            column=1,
            padx=8
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.stt_status = tk.Label(
            self.main_frame,
            text="Ready",
            font=("Arial", 10)
        )

        self.stt_status.pack(
            pady=10
        )

    # ========================================================
    # START LISTENING
    # ========================================================

    def start_listening(self):

        if self.is_listening:

            return

        self.is_listening = True

        self.listen_button.config(
            text="Listening..."
        )

        self.stt_status.config(
            text="Listening... Please speak."
        )

        thread = threading.Thread(
            target=self.recognize_speech,
            daemon=True
        )

        thread.start()

    # ========================================================
    # RECOGNIZE SPEECH
    # ========================================================

    def recognize_speech(self):

        try:

            with sr.Microphone() as source:

                self.root.after(
                    0,
                    lambda: self.stt_status.config(
                        text="Adjusting microphone..."
                    )
                )

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                self.root.after(
                    0,
                    lambda: self.stt_status.config(
                        text="Listening... Speak now."
                    )
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=30
                )

            self.root.after(
                0,
                lambda: self.stt_status.config(
                    text="Converting speech to text..."
                )
            )

            text = self.recognizer.recognize_google(
                audio
            )

            self.root.after(
                0,
                lambda: self.add_stt_text(text)
            )

        except sr.WaitTimeoutError:

            self.root.after(
                0,
                lambda: messagebox.showwarning(
                    "Timeout",
                    "No speech detected."
                )
            )

        except sr.UnknownValueError:

            self.root.after(
                0,
                lambda: messagebox.showwarning(
                    "Not Understood",
                    "Sorry, I could not understand the speech."
                )
            )

        except sr.RequestError:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Internet Error",
                    "Speech recognition service is unavailable."
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    str(e)
                )
            )

        finally:

            self.root.after(
                0,
                self.reset_listening
            )

    # ========================================================
    # ADD SPEECH TEXT
    # ========================================================

    def add_stt_text(self, text):

        self.stt_text.insert(
            tk.END,
            text + " "
        )

    # ========================================================
    # RESET LISTENING
    # ========================================================

    def reset_listening(self):

        self.is_listening = False

        self.listen_button.config(
            text="🎤 Start Listening"
        )

        self.stt_status.config(
            text="Ready"
        )

    # ========================================================
    # CLEAR STT
    # ========================================================

    def clear_stt(self):

        self.stt_text.delete(
            "1.0",
            tk.END
        )

    # ========================================================
    # TEXT TO SPEECH PAGE
    # ========================================================

    def show_text_to_speech(self):

        self.stop_speech()

        self.clear_page()

        self.current_page = "text_to_speech"

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top = tk.Frame(
            self.main_frame
        )

        top.pack(
            fill="x",
            padx=20,
            pady=15
        )

        back_button = tk.Button(
            top,
            text="← Home",
            command=self.show_home,
            font=("Arial", 11)
        )

        back_button.pack(
            side="left"
        )

        title = tk.Label(
            top,
            text="🔊 Text to Speech",
            font=("Arial", 22, "bold")
        )

        title.pack(
            side="left",
            padx=25
        )

        # ----------------------------------------------------
        # LABEL
        # ----------------------------------------------------

        tk.Label(
            self.main_frame,
            text="Enter text below:",
            font=("Arial", 12)
        ).pack(
            anchor="w",
            padx=35
        )

        # ----------------------------------------------------
        # TEXT AREA
        # ----------------------------------------------------

        self.tts_text = tk.Text(
            self.main_frame,
            height=12,
            wrap="word",
            font=("Arial", 13)
        )

        self.tts_text.pack(
            padx=35,
            pady=12,
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # VOICE OPTIONS
        # ----------------------------------------------------

        options = tk.Frame(
            self.main_frame
        )

        options.pack(
            pady=5
        )

        tk.Label(
            options,
            text="Voice:",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        # Get voices

        try:

            engine = pyttsx3.init()

            self.voices = engine.getProperty(
                "voices"
            )

            engine.stop()

        except:

            self.voices = []

        voice_names = []

        for i, voice in enumerate(self.voices):

            name = voice.name

            if not name:

                name = f"Voice {i + 1}"

            voice_names.append(
                name
            )

        self.voice_combo = ttk.Combobox(
            options,
            values=voice_names,
            state="readonly",
            width=35
        )

        self.voice_combo.grid(
            row=0,
            column=1,
            padx=5
        )

        if voice_names:

            self.voice_combo.current(
                0
            )

        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        tk.Label(
            options,
            text="Speed:",
            font=("Arial", 11)
        ).grid(
            row=1,
            column=0,
            pady=8
        )

        self.speed = tk.IntVar(
            value=150
        )

        tk.Scale(
            options,
            from_=80,
            to=250,
            orient="horizontal",
            variable=self.speed,
            length=250
        ).grid(
            row=1,
            column=1
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = tk.Frame(
            self.main_frame
        )

        buttons.pack(
            pady=10
        )

        tk.Button(
            buttons,
            text="🔊 Speak",
            command=self.speak_text,
            width=14,
            height=2,
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            buttons,
            text="⏹ Stop",
            command=self.stop_speech,
            width=14,
            height=2,
            font=("Arial", 11)
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear_tts,
            width=14,
            height=2,
            font=("Arial", 11)
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.tts_status = tk.Label(
            self.main_frame,
            text="Ready",
            font=("Arial", 10)
        )

        self.tts_status.pack(
            pady=8
        )

    # ========================================================
    # SPEAK TEXT
    # ========================================================

    def speak_text(self):

        text = self.tts_text.get(
            "1.0",
            tk.END
        ).strip()

        if not text:

            messagebox.showwarning(
                "Empty Text",
                "Please enter some text first."
            )

            return

        # Stop previous process

        self.stop_speech()

        selected = self.voice_combo.current()

        voice_id = None

        if (
            selected >= 0
            and selected < len(self.voices)
        ):

            voice_id = self.voices[
                selected
            ].id

        speed = self.speed.get()

        self.speech_process = multiprocessing.Process(
            target=speech_process,
            args=(
                text,
                voice_id,
                speed
            )
        )

        self.speech_process.start()

        self.tts_status.config(
            text="Speaking..."
        )

        self.check_speech()

    # ========================================================
    # CHECK SPEECH
    # ========================================================

    def check_speech(self):

        if self.speech_process is not None:

            if self.speech_process.is_alive():

                self.root.after(
                    200,
                    self.check_speech
                )

            else:

                self.speech_process = None

                if self.current_page == "text_to_speech":

                    self.tts_status.config(
                        text="Ready"
                    )

    # ========================================================
    # STOP SPEECH
    # ========================================================

    def stop_speech(self):

        if self.speech_process is not None:

            if self.speech_process.is_alive():

                self.speech_process.terminate()

                self.speech_process.join(
                    timeout=1
                )

            self.speech_process = None

        if (
            self.current_page == "text_to_speech"
            and hasattr(self, "tts_status")
        ):

            self.tts_status.config(
                text="Ready"
            )

    # ========================================================
    # CLEAR TTS
    # ========================================================

    def clear_tts(self):

        self.tts_text.delete(
            "1.0",
            tk.END
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    multiprocessing.freeze_support()

    root = tk.Tk()

    app = SpeechTextApplication(
        root
    )

    root.mainloop()