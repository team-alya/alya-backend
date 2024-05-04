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


def price_detection(saved_pic, filled_form):

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
    Provide me with a price estimate for my piece of furniture in the second-hand market, based on this description and the photo. 
    Pay close attention to the brand, material, age, condition, and defects. The second-hand market is based in Finland, 
    and the price should align with prices of similar items in Finnish web marketplaces.
    Return 3 prices and 1 description as a JSON object that has the fields highest_price, lowest_price, average_price, description and sell_probability. 
    In the description field, explain the criteria used to estimate the price and how accurate it is. 
    In the sell_probability field, give an estimation of how probable it will sell and which of the 3 prices for it would be most likely to sell.
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
