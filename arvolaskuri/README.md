Backend for Älyä hanke project
# Start
While in the root folder arvolaskuri, type "python manage.py runserver" to your command line to start the development server at http://127.0.0.1:8000/

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
5. Under the Key-input, write "picture"
6. Under the Value-input, paste your base64 image file. Example pic below. Then click the Send-button.
   
![Näyttökuva (62)](https://github.com/team-alya/alya-backend/assets/95426094/5d14b8f6-e7ea-424f-b993-e6597a83b42c)


If the picture is succesfully sent, the response body should say: "message": "I have received your picture, thanks"
If theres an error with the photo the server will respond with: "message": "I have you know that this endpoint only accepts Base64 pictures"

# Technologies
- Python
- Google Vertex AI
- Google vision API

# Dependencies
- We used Django and it's Rest framework as our web framework.




