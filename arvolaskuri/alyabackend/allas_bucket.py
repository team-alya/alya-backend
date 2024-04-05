import datetime
from alyabackend.allas_conf import conn
from swiftclient.service import SwiftError
from dotenv import load_dotenv
import os
import uuid


load_dotenv()
bucket_name = os.getenv("ALLAS_BUCKET_NAME")


#Adding image to object store
def store_image(image):
    try:
        #Calling name_image function
        name = name_image()
        conn.put_object(bucket_name, f"{name}.jpg", contents=image, content_type="image")
        return name
    except SwiftError as error:
        print(error)


#Getting image from object store
def get_image(name):
    try:
        allas_name = f"{name}.jpg"
        allas_image = conn.get_object(bucket_name, allas_name)
        return allas_image
    except SwiftError as error:
        print(error)


#Naming image with UUID4
def name_image():
    image_name = uuid.uuid4()
    return image_name
