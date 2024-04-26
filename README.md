# Backend for Älyä-hanke project

## Technologies
- Python
- Google Vertex AI
- Google vision API
- CSC Allas
- Docker hub

## Framework
- We used Django and it's Rest framework as our web framework.

## Starting the app

After cloning the repository, execute these commands in the root folder. <br>
The terminal should notify you of a server running at http://127.0.0.1:8000/ 
```
cd arvolaskuri
pip install -r requirements.txt
python manage.py runserver
```
The terminal should inform you of a server at http://127.0.0.1:8000/

=======
While in the root folder arvolaskuri, type "python manage.py runserver" to your command line to start the development server at http://127.0.0.1:8000/


Use this command when you want to check the app in the Android Emulator.  <br>
In this case the emulator server is located at http://10.0.2.2:8000/
```
python manage.py runserver 0.0.0.0:8000
```

> [!NOTE]
> All required dependencies are in **requirements.txt**  file.

## Connect CSC allas

1. Go to the [CSC Pouta](https://pouta.csc.fi/dashboard/project/)
2. Log in 
3. Click your username in top right corner
4. Download Opestack RC File
5. Use the credentials in RC File in your environment variables


## Create Vertex AI 

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Set up Billing
3. Select or Create a Project
4. Add Vertex AI to your project: APIs & Services > Enable APIs and services > Vertex AI API
5. Go to Credentials: APIs & Services > Credentials
6. Create Service Account
7. Create Key for Service Account and save it. It should be JSON file. You will need it to enable Vertex AI in repository.
   
## Enable Vertex AI in repository

### **1. Install Vertex AI and Google Cloud Dependencies**  <br>
   Execute these commands in the root folder of your project

```
pip install google-cloud-aiplatform
pip install google-cloud-vision  
```

### **2. Configure Environment Variables** <br>
   In the environment file (env file), add a variable named "GOOGLE_APPLICATION_CREDENTIALS" and set its value to the path of the key file from the Service Account you have created.
### **3. Use Google Cloud CLI for Project Management (Optional)**  <br>
   If you prefer to manage your project easily using the command line interface, you can use the Google Cloud CLI. It provides a set of tools to create and manage Google Cloud resources. Refer to the installation guide for instructions on installing the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk).
  >Alternatively you can use Google Cloud CLI to enable Vertex AI in the repository. Execute this command in the root folder of your project:
   > ```
 >gcloud auth login  
 >```
## API endpoints
| API | Endpoint         | Description |
| --- | --- | --- |
| GET | `/instructions` | List all instructions and example pictures from database in JSON|
| POST | `/sendpic` | Send the picture to AI to determine the attributes of the furniture: type, brand, model, color, dimensions in centimeters, age, and condition. |
| POST | `/askprice` | Send the picture, its attributes, and the user's comments to AI for a price estimate. |


## Sending a picture

> [!IMPORTANT]
> You must convert your image file in to the base64 format first. You can use this website for converting: https://www.base64-image.de/

1. Open up Postman
2. Select the method to POST and enter http://127.0.0.1:8000/sendpic as the url
3. Click on the Body tab
4. Select the form-data radio button. A view with inputs for key and value is shown on the screen now.
5. Under the Key-input, write "picture"
7. Under the Value-input, paste your base64 image file. Example pic below. Then click the Send-button.
>![Screenshot_4](https://github.com/team-alya/alya-backend/assets/120372944/f52bf867-6eef-447a-8967-86dc120eaee0)

   
9. If the picture is succesfully sent to AI, the response body should show JSON info about furniture on the picture.
   

>![Screenshot_1](https://github.com/team-alya/alya-backend/assets/120372944/ef243ca4-ecee-4401-98aa-2f31d3d390c0)



## Sending a picture with attributes

1. Open up Postman
2. Select the method to POST and enter http://127.0.0.1:8000/askprice as the url
3. Click on the Body tab
4. Select the form-data radio button. A view with inputs for key and value is shown on the screen now.
5. Under the Key-input, write "picture, brand, condition, model, age, color"
6. Under the Value-input, paste your base64 image file and other information matching to the value on the left. Example pic below. Then click the Send-button.
7. If everything is succesfully sent to AI, the response body should show JSON info with price estimate for the furniture.
>![Screenshot_2](https://github.com/team-alya/alya-backend/assets/120372944/66b8354a-1679-4812-9435-12214a36eeb4)

> [!TIP]
>  If there is no information available for a specific field (e.g., "brand"), you can leave the corresponding value field empty. However, do not uncheck any key (e.g., "brand") in the left column.
