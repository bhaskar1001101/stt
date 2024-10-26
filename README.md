# Offline Real-time Speech-to-Text System

A cross-platform, real-time Speech-to-Text system built in Python using Vosk. This application provides continuous offline speech recognition capabilities similar to virtual assistants like JARVIS, focusing solely on high-quality speech-to-text conversion. Unlike cloud-based solutions, this system works entirely offline while maintaining high accuracy.

## Features

- Real-time speech recognition
- 100% offline operation - no internet required
- Cross-platform compatibility (Windows, macOS, Linux)
- Low latency response
- Multiple language model support
- Error handling and logging
- Thread-safe audio processing
- Clean shutdown mechanism
- Customizable output handling

## Requirements

- Python 3.7+
- Working microphone
- ~50MB disk space for the small model (larger models available)
- 2GB RAM minimum (4GB recommended)

## Installation

1. Clone the repository or download the script:
```bash
git clone <repository-url>
# or create a new directory and copy realtime_stt.py into it
```

2. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv stt_env

# Activate on Windows
stt_env\Scripts\activate

# Activate on macOS/Linux
source stt_env/bin/activate
```

3. Install required packages:
```bash
pip install vosk sounddevice numpy
```

4. Download Vosk model:
```bash
# Download small English model (150MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### Platform-Specific Dependencies

#### Windows
All dependencies should install automatically with pip.

#### macOS
Install PortAudio using Homebrew:
```bash
brew install portaudio
```

#### Linux (Ubuntu/Debian)
Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install libportaudio2
```

## Usage

### Basic Usage

Run the script with default settings:
```bash
python realtime_stt.py
```

### Advanced Usage

The script supports several command-line arguments for customization:

```bash
# Use a different Vosk model
python realtime_stt.py --model path/to/model

# Change audio sample rate
python realtime_stt.py --sample-rate 44100
```

### Command Line Arguments

- `--model`: Path to Vosk model directory (default: "vosk-model-small-en-us-0.15")
- `--sample-rate`: Audio sample rate in Hz (default: 16000)

### Using as a Module

You can import and use the STT system in your own Python code:

```python
from realtime_stt import RealtimeSTT

def custom_callback(text):
    print(f"Custom handler received: {text}")

# Initialize with custom settings
stt = RealtimeSTT(
    model_path="vosk-model-small-en-us-0.15",
    sample_rate=16000,
    callback=custom_callback
)

# Start the system
stt.start()

# ... your code ...

# Stop the system
stt.stop()
```

## Available Models

Vosk provides various models balancing size and accuracy:

1. Small Model (150MB)
   - Good for simple commands and dictation
   - Fast and memory efficient
   - `vosk-model-small-en-us-0.15`

2. Large Model (1.8GB)
   - Better accuracy
   - More resource intensive
   - `vosk-model-en-us-0.22`

3. Other Languages
   - Models available for 20+ languages
   - Visit [Vosk Models](https://alphacephei.com/vosk/models) for full list

## Troubleshooting

### Common Issues

1. **Model not found**
   - Ensure you've downloaded and unzipped the Vosk model
   - Check model path matches command line argument
   - Verify model directory structure is intact

2. **Audio device issues**
   - Check microphone connections
   - Verify system permissions for microphone access
   - Try different sample rates

3. **Performance issues**
   - Try smaller model if CPU usage is high
   - Adjust sample rate
   - Close CPU-intensive applications

### Error Messages

- "Error loading model": Check model path and installation
- "Audio stream status warning": Check microphone connection
- "Error processing audio": Verify audio settings and hardware

## Performance Tips

1. Choose the right model:
   - Small model for basic commands and limited resources
   - Large model for better accuracy when resources allow

2. Optimize sample rate:
   - Lower rates (16000Hz) for efficiency
   - Higher rates (44100Hz) for better quality

3. System considerations:
   - Close unnecessary applications
   - Ensure adequate RAM (4GB recommended)
   - SSD storage for faster model loading

## Limitations

- Accuracy depends on model size
- Resource usage varies with model size
- May have reduced accuracy in noisy environments
- Performance depends on CPU capabilities
- Some accents may not be recognized well with basic models

## Advanced Features

### Multiple Language Support

1. Download additional language models from Vosk
2. Initialize STT with different model path
3. Switch models during runtime (requires restart)

### Custom Vocabulary

1. Small model supports basic English vocabulary
2. Larger models include more domain-specific terms
3. Consider specialized models for technical terminology

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using Vosk Speech Recognition Engine
- Uses sounddevice for audio processing
- Inspired by virtual assistant systems like JARVIS

## Future Improvements

Planned features and improvements:

1. Dynamic model loading
2. Real-time model switching
3. Noise reduction capabilities
4. Speaker diarization
5. Confidence scores for recognition
6. Automatic language detection