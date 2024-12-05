# Convert input from Arduino UNO to Voice 

import serial
import time
import pyttsx3  # Import the pyttsx3 library for TTS

# Morse code dictionary for decoding
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
    '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
    '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...'
    : '7', '---..': '8', '----.': '9','@':'.--.-.'
}

# Initialize serial connection (replace 'COM6' with your Arduino's port)
try:
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
    print("Connected to Arduino on COM6")
except serial.SerialException as e:
    print(f"Error: Could not open serial port - {e}")
    exit()

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Function to decode Morse code into text
def decode_morse(morse_message):
    words = morse_message.split('//')  # Split message into words
    decoded_message = ""
    
    for word in words:
        letters = word.split('/')  # Split word into letters
        decoded_word = "".join([MORSE_CODE_DICT.get(letter, '') for letter in letters])  # Decode each letter
        decoded_message += decoded_word + " "  # Add decoded word with a space
    
    return decoded_message.strip()  # Return decoded message without trailing space

# Function to read text aloud
def speak_text(text):
    engine.say(text)
    engine.runAndWait()  # Wait until the speech is finished

# Continuously read from Arduino and display all outputs, converting Morse to text when Arduino resets
def read_arduino_live():
    live_output = ""  # String to hold incoming characters for the current line

    while True:
        if arduino.in_waiting > 0:  # Check if there's incoming data from Arduino
            data = arduino.read().decode()  # Read one characte  mr at a time
            if data == "\n":  # Newline indicates end of a message
                print("Morse Code:", live_output)  # Print the Morse code
                decoded_text = decode_morse(live_output)  # Decode Morse to text
                print("Decoded Text:", decoded_text)  # Print the translated text
                speak_text(decoded_text)  # Read aloud the decoded text
                live_output = ""  # Clear for new line data
            else:
                live_output += data  # Append incoming character to live output

try:
    read_arduino_live()
except KeyboardInterrupt:
    print("\nProgram interrupted. Closing serial connection.")
finally:
    arduino.close()
    engine.stop()  # Stop the TTS engine when the program ends
