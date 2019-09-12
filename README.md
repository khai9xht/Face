# Front End For Face Recognition
## Set Up
- Create server.py 
- Create Router For Handling Request:
    - GET /webcam_face_detection => sendFile("webcanFaceDetection.html")
    - POST /face => Handle json data with format {data,landmarks} and return the id(name) of user
    - GET / => sendFile("index.html")

- Edit Url In Config.json In public/config.json   