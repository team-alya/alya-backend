Backend for Älyä hanke project
# Start
<<<<<<< HEAD
<<<<<<< HEAD
While in the root folder arvolaskuri, type "python manage.py runserver" to your command line to start the development server at http://127.0.0.1:8000/
=======
After cloning the repo, run these commands in the root folder
```
cd arvolaskuri
python manage.py runserver
```
The terminal should inform you of a server at http://127.0.0.1:8000/
>>>>>>> 37008e890ae0f89eb5d6c7448f3cb29b5bc4336b
=======
While in the root folder arvolaskuri, type "python manage.py runserver" to your command line to start the development server at http://127.0.0.1:8000/
>>>>>>> 37008e890ae0f89eb5d6c7448f3cb29b5bc4336b

# API endpoints
the frontpage.
GET http://127.0.0.1:8000/

url for sending a picture.
POST http://127.0.0.1:8000/sendpic

# Sending a picture

!You must convert your image file in to the base64 format first. You can use this website for converting: https://www.base64-image.de/!

1. Open up Postman
2. Select the method to POST and enter http://127.0.0.1:8000/sendpic as the url
3. Click on the Body tab
4. Select the form-data radio button. A view with inputs for key and value is shown on the screen now.
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 37008e890ae0f89eb5d6c7448f3cb29b5bc4336b
5. Under the Key-input, write "picture"
6. Under the Value-input, paste your base64 image file. Example pic below. Then click the Send-button.
   
![Näyttökuva (62)](https://github.com/team-alya/alya-backend/assets/95426094/5d14b8f6-e7ea-424f-b993-e6597a83b42c)


If the picture is succesfully sent, the response body should say: "message": "I have received your picture, thanks"
If theres an error with the photo the server will respond with: "message": "I have you know that this endpoint only accepts Base64 pictures"

<<<<<<< HEAD
=======
5. Under the Key-input, write "picture, brand, condition, model, material, priceWhenNew, age"
6. Under the Value-input, paste your base64 image file and other information matching to the value on the left. Example pic below. Then click the Send-button.
7. Example below pic below 👇👇

!!IMPORTANT!! You can leave the value fields empty if there is e.g. no "brand" information, but DONT uncheck the "brand" key in the left column.


![Näyttökuva (64)](https://github.com/team-alya/alya-backend/assets/95426094/d7ef1b34-aaba-426b-93f6-108a6ba844a2)



If the picture is succesfully sent, the response body should given an paragraph about the piece of furniture submitted including some information and a price estimate.
Remember to login with gcloud auth login, and set the credentials file $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\User\*\perceptive-arc-414309-8622811c3b44.json"
OR comment out the google vision services in alyabackend/prediction.py
If theres an error with the photo the server will respond with: "message": "I have you know that this endpoint only accepts Base64 pictures"



>>>>>>> 37008e890ae0f89eb5d6c7448f3cb29b5bc4336b
=======
>>>>>>> 37008e890ae0f89eb5d6c7448f3cb29b5bc4336b
# Technologies
- Python
- Google Vertex AI
- Google vision API

# Dependencies
- We used Django and it's Rest framework as our web framework.




