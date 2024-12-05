#Convert speech to morse code then convert morse code to vibration

import serial
import time
import speech_recognition as sr

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

# Function to listen to voice input and convert to text
def listen_for_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Text Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the speech.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
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
