from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Image as VertexImage,
)
import vertexai
import json


def label_detection(uploaded_file):

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

    # Prompt text for the Vertex AI
    prompt = """ your task is to determine the following attributes of the furniture pieace in the photo: 
        type, brand, model, color, approximate dimensions (length, width and height) in cm 
        (don't include cm in dimensions), and condition (they values should start with a capital letter but they not). 
        Brand and model are very important, so please make sure to include them in your answer. 
        Provide this information in JSON string format which stays same format all requests.
        """

    response_vertex = generative_multimodal_model.generate_content(
        [
            "Based solely on this photo ",
            image_part,
            prompt,
        ]
    )

    # Process the response from Vertex AI
    result = (
        response_vertex.candidates[0]
        .content.parts[0]
        .text.strip(" ```\n")
        .replace("json\n", "", 1)
        .replace("JSON\n", "", 1)
    )
    return json.loads(result)
