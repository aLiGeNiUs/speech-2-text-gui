# speech-2-text-gui
Python script that records audio from a microphone, converts speech to text with multi-language support


 a Python script that records audio from a microphone, converts speech to text with multi-language support,
 and saves the text to a file. This will work across Linux, Windows, and macOS.

# Speech-to-Text GUI Application: A Python-Based Tool for Transcribing Speech

In this article, we will explore a Python-based **Speech-to-Text GUI Application** that allows users to convert spoken language into written text. This application is built using the `tkinter` library for the graphical user interface (GUI) and the `speech_recognition` library for handling speech-to-text conversion. The tool is designed to be user-friendly, customizable, and capable of handling multiple languages.

## Features of the Application

The Speech-to-Text GUI application offers the following features:

1. **Multi-language Support**: The application supports multiple languages, including English (US and UK), French, Spanish, German, Japanese, Russian, Chinese (Mandarin), Arabic, Portuguese (Brazil), Italian, Hindi, Korean, Dutch, and Swedish.

2. **Recording Duration Control**: Users can set the recording duration in seconds, allowing flexibility in how long the application listens to the audio input.

3. **Output File Saving**: The transcribed text can be saved to a file. Users can choose to append new transcriptions to an existing file or overwrite it.

4. **Continuous Recording Mode**: The application can operate in continuous recording mode, where it keeps listening and transcribing until the user stops it.

5. **Real-time Transcription**: The transcribed text is displayed in real-time in the GUI, along with a timestamp for each transcription.

6. **System Information**: The application displays system information, such as the operating system and microphone status.

7. **User-friendly Interface**: The GUI is designed to be intuitive, with buttons for starting/stopping recording, clearing the transcript, and saving the text.

## How to Install and Run the Code

### Prerequisites

Before running the code, ensure that you have the following installed on your system:

1. **Python 3.x**: The application is written in Python, so you need to have Python installed. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Required Libraries**: The application uses the `tkinter` library (which comes pre-installed with Python) and the `speech_recognition` library. You can install the `speech_recognition` library using pip:

   ```bash
   pip install SpeechRecognition
   ```

3. **Microphone**: Ensure that your system has a working microphone, as the application relies on it for audio input.

### Steps to Run the Application

1. **Download the Code**: Save the provided Python script as `speech-to-text-gui.py`.

2. **Run the Script**: Open a terminal or command prompt and navigate to the directory where the script is saved. Run the script using the following command:

   ```bash
   python speech-to-text-gui.py
   ```

3. **Using the Application**:
   - **Language Selection**: Choose the language you want to transcribe from the dropdown menu.
   - **Recording Duration**: Set the recording duration in seconds.
   - **Output File**: Specify the output file where the transcribed text will be saved. You can also choose to append to an existing file.
   - **Continuous Recording**: Enable continuous recording if you want the application to keep listening and transcribing until you stop it.
   - **Start Recording**: Click the "Start Recording" button to begin the transcription process. The transcribed text will appear in the transcript box in real-time.
   - **Save Text**: Once the transcription is complete, you can save the text to the specified output file.

### Code Overview

The application is structured as a Python class (`SpeechToTextGUI`) that handles the GUI and speech recognition logic. Here are some key components of the code:

- **GUI Setup**: The GUI is created using `tkinter`, with frames for settings, transcript display, and control buttons. The `ttk` module is used for themed widgets, ensuring a consistent look across different operating systems.

- **Speech Recognition**: The `speech_recognition` library is used to capture audio from the microphone and convert it to text using Google's speech recognition API.

- **Threading**: The recording process runs in a separate thread to ensure that the GUI remains responsive during long recordings.

- **File Handling**: The application allows users to save the transcribed text to a file, with options to append or overwrite the file.

### Customization and Extensions

The application can be easily extended or customized. For example:

- **Adding More Languages**: You can add more languages by extending the `languages` dictionary in the code.
- **Changing the API**: The application currently uses Google's speech recognition API. You can modify the code to use other APIs, such as Microsoft Azure or IBM Watson.
- **Enhancing the GUI**: You can customize the GUI by adding more features, such as a progress bar or additional controls.

## Conclusion

The Speech-to-Text GUI application is a powerful tool for converting spoken language into written text. It is easy to use, customizable, and supports multiple languages. Whether you need to transcribe interviews, lectures, or meetings, this application provides a simple and efficient solution. By following the steps outlined in this article, you can install and run the application on your system and start transcribing speech in no time.
