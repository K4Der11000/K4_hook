# Bootkit Web Panel by kader11000

This project simulates a web control panel for testing payload injection and encryption (XOR) using Flask.

## Features

- Upload external payload files
- Simulate hook injection (adds dummy bytes)
- XOR encryption
- Simulate payload execution (device count)
- Download final files
- Web interface using Tailwind CSS

## Setup

```bash
git clone https://github.com/kader11000/k4_hook.git
cd k4_hook
pip install flask
python app.py
open url : http://127.0.0.1:5000
