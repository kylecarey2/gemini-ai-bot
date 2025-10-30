import sys
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
import utils

MODEL = "gemini-2.5-flash"

client = genai.Client()

def img_gen(prompt: str):
    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=4,
        )
    )
    
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    for i, generated_image in enumerate(response.generated_images):
        file_path = os.path.join("generated_images", f"generated_image_{i}.png")
        
        generated_image.image.save(file_path)
        print(f"Image saved to {file_path}")
        

def img_describe(path: str):
    try:
        image = Image.open(path)
    except:
        print("Invalid path")
        sys.exit(0)
    
    print("Thinking...")
    
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=[image, "Explain or solve this image"]
    )

    for chunk in response:
        print(chunk.text, end="")


def chat(prompt: str):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            tools=[utils.get_wikipedia_summary, utils.get_current_datetime, utils.calculate_expression, utils.get_random_joke, utils.get_public_ip_address]
        ),
    )
    
    for chunk in response:
        print(chunk.text, end="")


if __name__ == "__main__":
    # argv list: main.py _ ...
    print(utils.get_wikipedia_summary("Adolf Hitler"))
    if len(sys.argv) < 2:
        prompt = input("What would you like to ask? ")
        chat(prompt)
    elif sys.argv[1] == "img":
        path = sys.argv[2]
        img_describe(path)
    elif sys.argv[1] == "imggen":
        prompt = input("What would you like to generate? ")
        img_gen(prompt)
    else: 
        prompt = input("What would you like to ask? ")
        chat(prompt)

    print()