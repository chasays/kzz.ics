#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting KZZ ICS generation..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found in current directory"
    exit 1
fi

# Run the Python script
echo "📅 Generating ICS file..."
python3 -u main.py

# Check if kzz.ics was created
if [ -f "kzz.ics" ]; then
    echo "✅ ICS file generated successfully: kzz.ics"
    echo "📊 File size: $(du -h kzz.ics | cut -f1)"
else
    echo "❌ Failed to generate kzz.ics file"
    exit 1
fi

echo "🎉 KZZ ICS generation completed!"