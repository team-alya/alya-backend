from django.http import JsonResponse
from rest_framework.views import APIView
from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import GenerativeModel, Part, Image as VertexImage
import vertexai
import base64
from alyabackend.serializers import PictureSerializer
import io

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


    # Use the created Part in generate_content
    response_vertex = generative_multimodal_model.generate_content([image_part, "What is shown in this image?"])

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

    return result_combined