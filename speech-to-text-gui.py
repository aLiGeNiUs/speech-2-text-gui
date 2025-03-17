import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import speech_recognition as sr
import os
import platform
import threading
import time
from datetime import datetime

class SpeechToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Set theme based on system
        self.system = platform.system()
        if self.system == "Darwin":  # macOS
            self.root.configure(bg="#f0f0f0")
        elif self.system == "Windows":
            self.root.configure(bg="#f0f0f0")
        else:  # Linux
            self.root.configure(bg="#e0e0e0")
            
        # Variables
        self.language_var = tk.StringVar(value="en-US")
        self.timeout_var = tk.IntVar(value=5)
        self.output_file_var = tk.StringVar()
        self.append_var = tk.BooleanVar(value=False)
        self.continuous_var = tk.BooleanVar(value=False)
        self.is_recording = False
        self.transcribed_text = ""
        
        # Initialize status variable before creating widgets
        self.status_var = tk.StringVar(value="Ready")
        
        # Language options
        self.languages = {
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "French": "fr-FR",
            "Spanish": "es-ES",
            "German": "de-DE",
            "Japanese": "ja-JP",
            "Russian": "ru-RU",
            "Chinese (Mandarin)": "zh-CN",
            "Arabic": "ar-AE",
            "Portuguese (Brazil)": "pt-BR",
            "Italian": "it-IT",
            "Hindi": "hi-IN",
            "Korean": "ko-KR",
            "Dutch": "nl-NL",
            "Swedish": "sv-SE"
        }
        
        # Create the GUI
        self.create_widgets()
        
        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for controls
        left_panel = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Language selection
        ttk.Label(left_panel, text="Language:").grid(row=0, column=0, sticky=tk.W, pady=5)
        language_combo = ttk.Combobox(left_panel, textvariable=self.language_var, state="readonly")
        language_combo['values'] = list(self.languages.keys())
        language_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        language_combo.bind("<<ComboboxSelected>>", self.on_language_select)
        
        # Recording timeout
        ttk.Label(left_panel, text="Recording Duration (sec):").grid(row=1, column=0, sticky=tk.W, pady=5)
        timeout_spin = ttk.Spinbox(left_panel, from_=1, to=60, textvariable=self.timeout_var, width=5)
        timeout_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Output file
        ttk.Label(left_panel, text="Output File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(left_panel)
        file_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_file_var, width=15).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.LEFT, padx=5)
        
        # Append checkbox
        ttk.Checkbutton(left_panel, text="Append to File", variable=self.append_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Continuous mode checkbox
        ttk.Checkbutton(left_panel, text="Continuous Recording", variable=self.continuous_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(left_panel)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.record_button = ttk.Button(button_frame, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Text", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Text", command=self.save_text).pack(side=tk.LEFT, padx=5)
        
        # Device info
        device_frame = ttk.LabelFrame(left_panel, text="System Info")
        device_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        ttk.Label(device_frame, text=f"OS: {self.system}").pack(anchor=tk.W)
        
        # Get default microphone info
        mic_info = "Checking microphone..."
        try:
            with sr.Microphone() as source:
                mic_info = "Microphone detected"
        except Exception as e:
            mic_info = f"Microphone error: {str(e)}"
        
        ttk.Label(device_frame, text=mic_info).pack(anchor=tk.W)
        
        # Right panel for transcript display
        right_panel = ttk.LabelFrame(main_frame, text="Transcript", padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Transcription display
        self.transcript_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, width=40, height=20)
        self.transcript_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def on_language_select(self, event):
        selected_language = event.widget.get()
        self.language_var.set(self.languages[selected_language])
        
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
            
    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.record_button.config(text="Start Recording")
            self.status_var.set("Recording stopped")
        else:
            self.is_recording = True
            self.record_button.config(text="Stop Recording")
            # Start recording in a separate thread
            threading.Thread(target=self.record_audio, daemon=True).start()
            
    def record_audio(self):
        try:
            # If continuous mode is enabled
            if self.continuous_var.get():
                self.status_var.set("Continuous recording started")
                while self.is_recording:
                    self.perform_single_recording()
                    time.sleep(1)  # Small pause between recordings
            else:
                self.perform_single_recording()
                self.is_recording = False
                self.root.after(0, lambda: self.record_button.config(text="Start Recording"))
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.is_recording = False
            self.root.after(0, lambda: self.record_button.config(text="Start Recording"))
            
    def perform_single_recording(self):
        try:
            with sr.Microphone() as source:
                self.root.after(0, lambda: self.status_var.set("Adjusting for ambient noise..."))
                # Increase ambient noise adjustment time for better results
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                timeout = self.timeout_var.get()
                self.root.after(0, lambda: self.status_var.set(f"Listening for {timeout} seconds..."))
                
                # Add parameters to better handle fast speech
                self.recognizer.pause_threshold = 0.5  # Reduce pause detection time
                self.recognizer.phrase_threshold = 0.3  # Lower threshold for detecting speech
                
                # Use phrase_time_limit to handle fast speech better
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
                self.root.after(0, lambda: self.status_var.set("Processing speech..."))
                
                # Use Google's speech recognition
                text = self.recognizer.recognize_google(audio, language=self.language_var.get())
                
                # Format with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_text = f"[{timestamp}] ({self.language_var.get()}): {text}\n\n"
                
                # Update transcript
                self.root.after(0, lambda: self.append_to_transcript(formatted_text))
                
                # Save to file if specified
                output_file = self.output_file_var.get()
                if output_file:
                    write_mode = 'a' if self.append_var.get() else 'w'
                    with open(output_file, write_mode, encoding='utf-8') as f:
                        f.write(formatted_text)
                    self.root.after(0, lambda: self.status_var.set(f"Text saved to {output_file}"))
                else:
                    self.root.after(0, lambda: self.status_var.set("Speech recognized"))
                    
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status_var.set("Could not understand audio"))
        except sr.RequestError as e:
            self.root.after(0, lambda: self.status_var.set(f"API error: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            
    def append_to_transcript(self, text):
        self.transcript_text.insert(tk.END, text)
        self.transcript_text.see(tk.END)
        
    # Adding the missing clear_text method
    def clear_text(self):
        self.transcript_text.delete(1.0, tk.END)
        self.status_var.set("Transcript cleared")
        
    def save_text(self):
        if not self.output_file_var.get():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                self.output_file_var.set(filename)
            else:
                return
                
        try:
            with open(self.output_file_var.get(), 'w', encoding='utf-8') as f:
                f.write(self.transcript_text.get(1.0, tk.END))
            self.status_var.set(f"Text saved to {self.output_file_var.get()}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
            self.status_var.set("Error saving file")

def main():
    root = tk.Tk()
    app = SpeechToTextGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
