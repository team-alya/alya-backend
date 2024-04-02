import datetime
from alyabackend.allas_conf import conn
from swiftclient.service import SwiftError
from dotenv import load_dotenv
import os


load_dotenv()
bucket_name = os.getenv("ALLAS_BUCKET_NAME")
date = datetime.datetime.now()
date_time = date.strftime("%H:%M %d:%m:%Y")


#Adding image to object store
def store_image(image, brand, model):
    #Checking for empty fields
    if not brand:
        brand = "Unkonwn brand"
    if not model:
        model = "Unkonwn model"
    #Adding image to object store
    try:
        conn.put_object(bucket_name, f"{brand} {model} {date_time}.jpg", contents=image, content_type="image")
    except SwiftError as error:
        print(error)


