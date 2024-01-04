# Robo-Filter ⚡️

Robot-Face-Filter using computer vision in aid of socket programming via TCP.
The Video feed moves from the client to the server via TCP: Transmission Control Protocol. At the server, the video frames are formatted a to desired size  with openCV. Finally With use of the OpenCV Haar Cascades models involving, Smile, Eyes and Face detection. in the end, you can see a robot face on your face, hence the filter ;))


##Points to Note:
1. The client and server must be connected to the same IP address.
2. Remember to place the server IP at the client-side code.



To Run the client, navigate to client.py and run 
```
python client.py
```


To Run the Server, navigate to server.py and run 
```
python server.py
```
