import numpy as np
from PIL import Image
import simpleaudio as sa

def brightness_to_freq(brightness, min_freq=200, max_freq=2000):
    return (brightness / 255) * (max_freq - min_freq) + min_freq

def generate_tone(freq, duration_ms=100, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * (duration_ms / 1000)), False)
    wave = np.sin(freq * t * 2 * np.pi)
    audio = wave * (2**15 - 1) * volume
    return audio.astype(np.int16)

def image_to_sound(image_path):
    with Image.open(image_path) as img:
        print("Image loaded successfully.")  # Debug print
        grayscale = img.convert('L')
        grayscale = grayscale.resize((50, grayscale.height))
        pixels = list(grayscale.getdata())
        audio_signal = np.array([], dtype=np.int16)

        # Process a smaller portion of the image for testing
        for brightness in pixels[:100]:  # Adjust the range as needed
            freq = brightness_to_freq(brightness)
            tone = generate_tone(freq)
            audio_signal = np.concatenate((audio_signal, tone))

        # Print the shape of the audio signal array
        print(f"Audio signal shape: {audio_signal.shape}")  # Debug print

        # Play a short segment of the audio signal for testing
        play_obj = sa.play_buffer(audio_signal[:44100], 1, 2, 44100)  # Play first second
        play_obj.wait_done()

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    image_to_sound(image_path)