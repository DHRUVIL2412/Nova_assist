# Nova AI Project

## Description
Nova AI is a multi-functional project that includes:
1. A voice-controlled assistant that can launch macOS applications
2. A Solana DEX data dashboard built with Streamlit that tracks trading activities

## Features

### Voice Assistant
- Voice recognition and response capabilities
- Time-based greetings
- Application launcher for macOS
- Custom voice responses

## Requirements
```txt
numpy
pandas
openai
speechrecognition
wikipedia
pyaudio
streamlit
gql
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/DHRUVIL2412/Nova.git
cd Nova
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # For Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```



## Usage

### Voice Assistant
Run the voice assistant:
```bash
python nova.py
```

### Solana Dashboard
Run the Streamlit dashboard:
```bash
streamlit run nova.py
```

## Project Structure
```
Nova/
│
├── nova.py          # Main application file
├── common.py        # Common utilities and responses
├── requirements.txt # Project dependencies
│
└── www/            # Web interface files
    ├── index.html
    ├── style.css
    └── main.js
```

## License
[Add your license information here]

## Contributing
[Add contribution guidelines here]

## Authors
[DHRUVIL TANK - dhruvil24122003@gmail.com]
