# Front End For Face Recognition
## Set Up
    - Create server.py 
    - Create Router For Handling Request:
        - GET /webcam_face_detection => sendFile("webcanFaceDetection.html")
        - POST /face => Handle json data with format {data,landmarks} and return the id(name) of user
     - Edit Url In Config.json In public/config.json   

# Backend setup
* Step 0: download `backend.zip` from this [link](https://drive.google.com/open?id=1-7Sb7hII-dM4yo43qaNLtgl6FmCD8FP5)
* Step 1: unzip `backend.zip` to the same folder as `app.py`
* Step 2: run `python app.py`
