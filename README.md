# Google GenAI personal assistant
Created for CS3560 - Software Engineering Tools and Best Practices. This could possibly be expanded on in the future
## Usage
Ensure that both python 3.10+ and pip are installed. To use, ensure that both google-genai and PIL is installed (I recommend using a virtual environment):
```bash
pip install -q -U google-genai
pip install pillow
```
Then, using your Gemini AI API Key, export it as:
```bash
export GEMINI_API_KEY="YOUR_KEY_HERE"
```
Note: You must have a paid API key to use image generation

Then, to prompt, run: 
```bash
python main.py
```
For image describing/solving,
```bash
python main.py img /path_to_image
```
And for image generation,
```bash
python main.py imggen
```
