from google.cloud import vision_v1p3beta1 as vision
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Image as VertexImage,
)
import vertexai
import logging
import json

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


def repairing_instructions(saved_pic, filled_form):

    # Read the content of the image file
    image_content = saved_pic.read()

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

    if filled_form.get("defects"):
        # 'defects' key exists and it's not empty
        defects = filled_form["defects"]
    else:
        # 'defects' key does not exist or it's empty
        defects = "None"

    # Prompt text for the Vertex AI
    prompt = f"""Description of the piece of furniture in the photo:\n\n
    The type of the furniture is {filled_form['type']}. The maker of the furniture is {filled_form['brand']} and its model is {filled_form['model']}.
    The color of the furniture is {filled_form['color']}. The approximate dimensions are {filled_form['dimensions']} in cm. 
    The condition is {filled_form['condition']}. The age is {filled_form['age']}. The material is {filled_form['material']} There are defects: {defects}. \n\n 
    Give me instructions on how to restore/repair or recycle my piece of furniture, based on the description and photo provided to you. 
    If the furniture is in bad condition, give me instructions on how to restore/repair it, or if it's beyond repair, provide instructions on how to recycle it. 
    Pay close attention to the brand, material, age, condition, and defects. 
    Return instructions as a JSON object that has the fields repair_instructions, recycle_instructions, and suggestion. 
    In the repair_instructions field, provide instructions on how to repair this furniture piece if it is necessary. 
    In the recycle_instructions field, provide information on how to recycle this furniture in Finland. 
    In both repair_instructions and recycle_instructions field provide extensive step by step instructions with explanation.
    In the suggestion field, you need to suggest to the user what he/she should do with this furniture based on the information and picture given to you above. 
    Should the user repair/restore or recycle it? In the suggestion field, provide only your suggestion and not instructions like in the repair_instructions and recycle_instructions fields.
    Text in those fields should be without new lines. The format of you outputs should stay consistent.
    Provide this information in JSON string format, which remains consistent across all requests."""

    try:
        # Generate content using the Gemini model
        response_vertex = generative_multimodal_model.generate_content(
            [
                "Heres a photo of my piece of furniture:",
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

        try:
            response = json.loads(result)
            return response
        except:
            response = response_vertex.candidates[0].content.parts[0].text
            return {"error": response}

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {"error": "An unexpected error occurred."}
