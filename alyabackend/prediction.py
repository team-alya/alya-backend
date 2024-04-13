from django.http import JsonResponse
from rest_framework.views import APIView
from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import GenerativeModel, Part, Image as VertexImage
import vertexai
import base64
from alyabackend.serializers import PictureSerializer
import io
import json


def label_detection(uploaded_file, furnitureDict):

    

    # Read the content of the image file
    image_content = uploaded_file.read()
     
    # Initialize Google Cloud Vision API client
    image_vision = vision.Image(content=image_content)

    # Perform label detection using Google Cloud Vision API
    client = vision.ImageAnnotatorClient()
    response_vision = client.label_detection(image=image_vision)
    labels = response_vision.label_annotations
    # print(f"Furniture dict: {furnitureDict}")
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
        summary = ""
        """"
        summary = "Description of the piece of furniture in the photo:\n\n"
        if "brand" in furnitureDict and furnitureDict["brand"]:
            summary += f"The maker of the furniture is {furnitureDict['brand']}"
        if "model" in furnitureDict and furnitureDict["model"]:
            summary += f" and its model is {furnitureDict['model']}. "
        else:
            summary += ". "
    
        if "material" in furnitureDict and furnitureDict["material"]:
            summary += f"It's made of {furnitureDict['material']}. "
        
        if "condition" in furnitureDict and furnitureDict["condition"]:
            summary += f"The condition is {furnitureDict['condition']}. "
        
        if "priceWhenNew" in furnitureDict and furnitureDict["priceWhenNew"]:
            summary += f"If purchased new, it would have cost ${furnitureDict['priceWhenNew']}. "
        
        if "age" in furnitureDict and furnitureDict["age"]:
            summary += f"It's {furnitureDict['age']} years old. "
        """
        summary += """Based on this photo alone you need to determine which type of furniture it is, its model, its brand
        its colour, its approximate dimensions and its condition all as a string. ALSO give me an price estimate for the furniture.
        the furniture is to be sold in finland. The response needs to be in application/json format, as it will be sent over a server."""
        #converted_json = convert_to_json(json_string)
        #print(converted_json)
        return summary


    # Use the created Part in generate_content
    response_vertex = generative_multimodal_model.generate_content(["Heres a photo of my piece of furniture:",image_part, vertex_prompt_formatter(furnitureDict)])
    print(response_vertex)
        # Vertex AI response
    vertex_labels = []
    if hasattr(response_vertex, 'candidates'):
        for candidate in response_vertex.candidates:
            if hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        vertex_labels.append({
                            'text': part.text,
                        })

    # Combine all results in a dictionary
    result_combined = {
       'vision_labels': vision_labels,
        'vertex_answer': vertex_labels,
    }

    def convert_to_json(json_string):
        # Parse the JSON string into a Python dictionary
        data = json.loads(json_string)
        # Return the dictionary as JSON string
        return json.dumps(data)

    print(vertex_prompt_formatter(furnitureDict))
    print(result_combined.get('vertex_answer'))
    return result_combined