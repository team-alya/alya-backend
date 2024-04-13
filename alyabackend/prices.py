from django.http import JsonResponse
from rest_framework.views import APIView
from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import GenerativeModel, Part, Image as VertexImage
import vertexai
import base64
from alyabackend.serializers import PictureSerializer
import io
import json

def price_detection(saved_pic, filled_form):


    # Read the content of the image file
    image_content = saved_pic.read()

    # Initialize Google Cloud Vision API client
    image_vision = vision.Image(content=image_content)
     
    # Perform label detection using Google Cloud Vision API
    client = vision.ImageAnnotatorClient()
    response_vision = client.label_detection(image=image_vision)
    labels = response_vision.label_annotations
    # print(f"Furniture dict: {filled_form}")
    # Process Google Cloud Vision API response
    vision_labels = []
    for label in labels:
        vision_labels.append({
            'description': label.description,
            'score': label.score,
        })
    
    # Initialize Vertex AI
    PROJECT_ID = "perceptive-arc-414309"
    REGION = "us-central1"
    vertexai.init(project=PROJECT_ID, location=REGION)

    # Load the Gemini model and generate content
    generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision")


    # Convert the image content to base64-encoded string
    image_part = Part.from_image(VertexImage.from_bytes(image_content))

    def vertex_prompt_formatter(prompt):
        summary = "Description of the piece of furniture in the photo:\n\n"
        if "brand" in filled_form and filled_form["brand"]:
            summary += f"The maker of the furniture is {filled_form['brand']}"
        if "model" in filled_form and filled_form["model"]:
            summary += f" and its model is {filled_form['model']}. "
        else:
            summary += ". "
    
        if "material" in filled_form and filled_form["material"]:
            summary += f"It's made of {filled_form['material']}. "
        
        if "condition" in filled_form and filled_form["condition"]:
            summary += f"The condition is {filled_form['condition']}. "
        
        if "priceWhenNew" in filled_form and filled_form["priceWhenNew"]:
            summary += f"If purchased new, it would have cost ${filled_form['priceWhenNew']}. "
        
        if "age" in filled_form and filled_form["age"]:
            summary += f"It's {filled_form['age']} years old. "
        
        vertex_query = summary + """\n\nGive me only a price estimate for my piece of furniture, in the second-hand market based on this description and the photo. 
        Pay close attention to the brand and model. The second-hand market is based in Finland and the price should match prices of similar items in finnish web-marketplaces.
        Return 3 prices and 1 descriprion as a JSON object that has the fields highest_price, lowest_price, average_price and description. 
        In description field explain on which criteria you gave estimated price. Example: {"highest_price": 200,
    "lowest_price": 100,
    "average_price": 150,
    "description": "desc"}"""
    
        return vertex_query


    # Use the created Part in generate_content
    response_vertex = generative_multimodal_model.generate_content(["Heres a photo of my piece of furniture:",image_part, vertex_prompt_formatter(filled_form)])

    # Vertex AI response
    
    if hasattr(response_vertex, 'candidates'):
        for candidate in response_vertex.candidates:
            if hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        # print(f"Part text: {part.text}")
                        try:
                            return json.loads(part.text)
                        except:
                            return {"highest_price": 0,
                                    "lowest_price": 0,
                                    "average_price": 0,
                                    "description": part.text}

    raise RuntimeError(f"Vertex AI response does not contain candidates or parts {response_vertex}")