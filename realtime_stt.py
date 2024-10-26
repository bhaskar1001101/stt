import sounddevice as sd
import numpy as np
import queue
import sys
import json
import threading
import argparse
import logging
from vosk import Model, KaldiRecognizer

class RealtimeSTT:
    def __init__(self, model_path="vosk-model-small-en-us-0.15", 
                 sample_rate=16000, callback=None):
        """
        Initialize the real-time STT system using Vosk
        
        Args:
            model_path (str): Path to Vosk model
            sample_rate (int): Audio sample rate
            callback (callable, optional): Function to call with transcribed text
        """
        self.sample_rate = sample_rate
        self.block_size = 8000
        self.running = False
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        try:
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            self.recognizer.SetWords(True)
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            print("Please ensure you have downloaded the Vosk model.")
            sys.exit(1)
            
        self.callback = callback if callback else self._default_callback
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Configure logging"""
        logger = logging.getLogger('RealtimeSTT')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _default_callback(self, text):
        """Default callback that prints the transcribed text"""
        if text.strip():
            print(f"Transcribed: {text}")

    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        if status:
            self.logger.warning(f"Audio stream status: {status}")
        if self.running:
            self.audio_queue.put(bytes(indata))

    def _process_audio(self):
        """Process audio data from queue and perform recognition"""
        while self.running:
            try:
                audio_data = self.audio_queue.get(timeout=2)
                if self.recognizer.AcceptWaveform(audio_data):
                    result = json.loads(self.recognizer.Result())
                    if result.get('text', '').strip():
                        self.result_queue.put(result['text'])
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error processing audio: {str(e)}")
                continue

    def _output_processor(self):
        """Process the converted text through the callback"""
        while self.running:
            try:
                text = self.result_queue.get(timeout=2)
                self.callback(text)
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in output processor: {str(e)}")
                continue

    def start(self):
        """Start the real-time STT system"""
        self.running = True
        
        # Start audio stream
        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            dtype=np.int16,
            channels=1,
            callback=self._audio_callback
        )
        
        self.stream.start()
        
        # Start processing threads
        threading.Thread(target=self._process_audio, daemon=True).start()
        threading.Thread(target=self._output_processor, daemon=True).start()
        
        self.logger.info("Real-time STT system started")

    def stop(self):
        """Stop the real-time STT system"""
        self.running = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        self.logger.info("Real-time STT system stopped")

def main():
    parser = argparse.ArgumentParser(description='Real-time Speech-to-Text System using Vosk')
    parser.add_argument('--model', type=str, default="vosk-model-small-en-us-0.15",
                      help='Path to Vosk model')
    parser.add_argument('--sample-rate', type=int, default=16000,
                      help='Audio sample rate')
    
    args = parser.parse_args()
    
    print("Starting Real-time Speech-to-Text System...")
    print("Make sure you have downloaded the Vosk model from https://alphacephei.com/vosk/models")
    print("Press Ctrl+C to exit")
    
    try:
        stt = RealtimeSTT(
            model_path=args.model,
            sample_rate=args.sample_rate
        )
        stt.start()
        
        while True:
            try:
                sys.stdin.readline()
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if 'stt' in locals():
            stt.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()