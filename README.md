# Turn Your Picture into an Audio Story

## Project Description

This is a Python-based storytelling application designed for children aged 3 to 10.  
Users can upload a picture, and the app will generate a short child-friendly story based on the image.  
The story is also converted into audio so children can read and listen at the same time.

This project was developed for the ISOM5240 Individual Assignment.

## Features

- Upload a JPG or PNG image
- Generate an image caption using a Hugging Face image captioning model
- Create a short story based on the image caption
- Convert the story into audio using a Hugging Face text-to-audio model
- Display the uploaded image, image description, generated story, and audio player
- Provide a child-friendly interface with large buttons, emojis, and simple instructions
- Allow users to generate another story with the same image
- Provide guidance for choosing a new image

## Target Users

This application is designed for children aged 3 to 10.  
The interface uses simple language, colorful design, large buttons, and friendly visual elements to improve usability for young users.

## Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- Salesforce/blip-image-captioning-base
- Matthijs/mms-tts-eng
- Pillow
- NumPy

## Models Used

### Image Captioning Model

```text
Salesforce/blip-image-captioning-base
```

This model is used to analyze the uploaded image and generate a short text description of what appears in the image.

Example output:

```text
a forest with trees and fog
```

### Text-to-Audio Model

```text
Matthijs/mms-tts-eng
```

This model is used to convert the generated story text into speech audio.

## Project Structure

```text
storytelling_app/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE

### File Description

| File | Description |
|---|---|
| `app.py` | Main source code of the Streamlit application |
| `requirements.txt` | List of Python packages required to run the app |
| `README.md` | Project description and usage instructions |

## How the App Works

```text
1. The user uploads a picture.
2. The app uses an image captioning model to describe the image.
3. The app creates a short child-friendly story based on the image description.
4. The story is converted into audio.
5. The app displays the image, description, story, and audio player.
6. The user can generate another story or choose a new image.
```

## How to Run Locally

First, install the required packages:

```bash
pip install -r requirements.txt
```

Then run the Streamlit app:

```bash
streamlit run app.py
```

After running the command, Streamlit will open the app in a web browser.

## Requirements

The `requirements.txt` file should include:

```txt
streamlit
transformers
torch
Pillow
sentencepiece
protobuf
accelerate
numpy
```

## Deployment

This application is designed to be deployed on Streamlit Cloud.

Deployment steps:

```text
1. Upload app.py, requirements.txt, and README.md to a GitHub repository.
2. Go to Streamlit Cloud.
3. Connect the GitHub repository.
4. Select app.py as the main application file.
5. Deploy the app.
6. Copy and submit the Streamlit Cloud URL.
```

## User Interface Design

The app is designed to be friendly and simple for young children. The user interface includes:

- Large buttons
- Emojis
- Simple instructions
- Colorful text boxes
- Loading spinners
- Friendly error messages
- Cartoon-style decorative elements

These design choices help improve usability and make the app more suitable for children aged 3 to 10.

## Error Handling

The app includes error handling for common problems, such as:

- Invalid image uploads
- Image processing errors
- Model loading errors
- Story generation errors
- Audio generation errors

If an error occurs, the app shows a friendly message to the user and provides debugging details for development purposes.

## License

This project is licensed under the GNU General Public License v3.0.

It was developed for educational purposes as part of the ISOM5240 Individual Assignment.


## Notes

The uploaded image does not need to contain a human face.

The app can work with different types of child-friendly images, such as:

- People
- Animals
- Toys
- Landscapes
- Food
- Cartoons
- Everyday objects

For better results, users should upload clear and appropriate images.

## Conclusion

This project demonstrates how Hugging Face pipelines can be used in a Streamlit web application to build an interactive storytelling app. It combines image captioning, story generation logic, and text-to-audio conversion to create a fun and accessible experience for young children.
