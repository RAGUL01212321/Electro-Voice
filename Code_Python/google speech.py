import serial
import time
from google.cloud import speech
import pyaudio

# Morse code dictionary for encoding
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

# Initialize serial connection (replace 'COM6' with your Arduino's port)
try:
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
    print("Connected to Arduino on COM6")
except serial.SerialException as e:
    print(f"Error: Could not open serial port - {e}")
    exit()

# Function to convert text to Morse code
def text_to_morse(text):
    text = text.upper()
    morse_code = ""
    for char in text:
        if char == " ":
            morse_code += "//"  # Space between words
        elif char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + "/"
    return morse_code.strip("/")

# Function to listen to voice input using Google Cloud Speech-to-Text
def listen_for_speech():
    client = speech.SpeechClient()

    # Audio stream setup
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Listening for your command...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * 5)):  # Listen for 5 seconds
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    # Configure request
    audio = speech.RecognitionAudio(content=b''.join(frames))
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    # Recognize speech
    try:
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            text = result.alternatives[0].transcript
            print(f"Text Recognized: {text}")
            return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to send Morse code to Arduino
def send_morse_to_arduino(morse_code):
    for symbol in morse_code:
        if symbol == ".":
            arduino.write(b".")  # Send dot to Arduino
        elif symbol == "-":
            arduino.write(b"-")  # Send dash to Arduino
        elif symbol == "/":
            arduino.write(b"/")  # Send slash to indicate letter separation
        elif symbol == "//":
            arduino.write(b"//")  # Send double slash for word separation
        time.sleep(0.1)  # Delay between sending symbols

# Main program loop
while True:
    user_input = listen_for_speech()
    if user_input:
        morse_code = text_to_morse(user_input)
        print(f"Sending Morse Code: {morse_code}")
        send_morse_to_arduino(morse_code)
    time.sleep(1)  # Wait before listening again
