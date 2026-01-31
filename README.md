# iPhoenix - Ethical OSINT Investigation Tool

![iPhoenix Banner](https://via.placeholder.com/800x200/333/FFFFFF?text=iPhoenix+OSINT+Tool)

## Overview

iPhoenix is a CLI-based Open Source Intelligence (OSINT) tool designed for ethical investigation of online scams, fraud patterns, and digital footprints. It analyzes **publicly available information only** and is built for cybersecurity professionals, journalists, and researchers.

## Features

### 🔍 Image Analysis (`--image`)
- Generate perceptual hashes (pHash/dHash) for image matching
- Extract EXIF metadata (when available)
- Detect possible image reuse patterns
- **No facial recognition, no identity claims**

### 👤 Username Analysis (`--username`)
- Check username presence across 20+ public platforms
- HTTP-based existence checks only
- **No private data access, no scraping**

### 📧 Email Analysis (`--email`)
- Validate email format and domain
- Check Gravatar presence
- Domain reputation indicators
- **No password checks, no private data**

### 📞 Phone Analysis (`--phone`)
- Validate and normalize phone numbers
- Carrier and geographic information (country level)
- Check for public mentions
- **No owner lookup, no tracking**

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone or download the tool
git clone https://github.com/yourusername/iphoenix.git
cd iphoenix

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x iphoenix.py