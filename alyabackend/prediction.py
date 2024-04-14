from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Image as VertexImage,
)
import vertexai
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

    # Process Google Cloud Vision API response
    vision_labels = []
    for label in labels:
        vision_labels.append(
            {
                "description": label.description,
                "score": label.score,
            }
        )

    # Initialize Vertex AI
    PROJECT_ID = "perceptive-arc-414309"
    REGION = "us-central1"
    vertexai.init(project=PROJECT_ID, location=REGION)

    # Load the Gemini model and generate content
    generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

    # Convert the image content to base64-encoded string
    image_part = Part.from_image(VertexImage.from_bytes(image_content))

    # Generate content using the Gemini model
    response_vertex = generative_multimodal_model.generate_content(
        [
            "Based solely on this photo ",
            image_part,
            """ your task is to determine the following attributes of the furniture pieace in the photo: 
        type, brand, model, color, approximate dimensions (length, width and height) in cm 
        (don't include cm in dimensions), and condition (they values should start with a capital letter but they not). 
        Brand and model are very important, so please make sure to include them in your answer. 
        Provide this information in JSON string format which stays same format all requests.
        """,
        ]
    )

    # Process Vertex AI response and extract the JSON string from the response content
    # and store it in a list of dictionaries for further processing in the views.py
    vertex_labels = []
    if hasattr(response_vertex, "candidates"):
        for candidate in response_vertex.candidates:
            if hasattr(candidate.content, "parts"):
                for part in candidate.content.parts:
                    if hasattr(part, "text"):
                        json_string = part.text.strip(" ```\n")
                        json_string = json_string.replace("json\n", "", 1)
                        json_string = json_string.replace("JSON\n", "", 1)
                        print("JSON string:", json_string)
                        data = json.loads(json_string)
                        vertex_labels.append(
                            {
                                "text": data,
                            }
                        )

    # Combine the results from Google Cloud Vision API and Vertex AI
    result_combined = {
        "vision_labels": vision_labels,
        "vertex_answer": vertex_labels,
    }

    return result_combined
