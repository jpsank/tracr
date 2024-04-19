import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os

SAMPLE_RATE = 44100  # Hz

def make_pink_noise(duration, sample_rate, decibels):
    # Generate pink noise
    num_samples = int(duration * sample_rate)
    pink_noise = np.random.normal(0, 1, num_samples)
    pink_noise = np.cumsum(pink_noise)
    pink_noise -= np.mean(pink_noise)
    pink_noise /= np.max(np.abs(pink_noise))

    # Normalize the pink noise to the desired decibel level
    pink_noise *= 10 ** (decibels / 20)

    return pink_noise

def make_silence(duration, sample_rate):
    return np.zeros(int(duration * sample_rate))

def generate_dataset():
    # Constants
    sample_rate = SAMPLE_RATE  # Hz
    num_trials = 20
    decibel_low, decibel_high = 6, 9.2  # scaled down from 60-92 dB
    delays = [2, 4, 6]  # seconds

    # Call the function
    for t in range(num_trials):
        delay = np.random.choice(delays)
        decibel_a = np.random.uniform(decibel_low, decibel_high)
        decibel_b = np.random.uniform(decibel_low, decibel_high)
        tone_a = make_pink_noise(0.4, sample_rate, decibel_a)
        tone_b = make_pink_noise(0.4, sample_rate, decibel_b)
        # go tone is a 6-kHz pure tone for 200 ms
        go_tone = np.sin(2 * np.pi * 6000 * np.linspace(0, 0.2, int(0.2 * sample_rate)))
        sample = np.concatenate([
            make_silence(0.25, sample_rate), tone_a, make_silence(delay, sample_rate), tone_b, make_silence(0.25, sample_rate), go_tone])
        
        # Save the sample
        correct = decibel_a > decibel_b  # if a is louder than b
        wavfile.write(f"wavs/ratsp_trial_{t}_correct_{int(correct)}.wav", sample_rate, sample)

def play_dataset():
    # Load the dataset
    for file in os.listdir("wavs"):
        if file.endswith(".wav"):
            sample_rate, sample = wavfile.read(f"wavs/{file}")
            print(len(sample))
            assert sample_rate == SAMPLE_RATE

            # Play the sound
            sd.play(sample, sample_rate)
            sd.wait()

