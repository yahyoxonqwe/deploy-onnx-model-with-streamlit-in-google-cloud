import streamlit as st
import tempfile
import cv2
import numpy as np
from PIL import Image
from numpy import ndarray
import time
from onnx_class import onnx_run



model = 'yolov8n.onnx'
detect = onnx_run(model)


def main():
# Create a video file uploader
    st.header("Upload a video")
    uploaded_file = None
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        # Load the video with cv2
        cap = cv2.VideoCapture(video_path)
        outputing2 = st.empty()
        outputing = st.empty()
        i = 0       
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            start = time.time()

            
            boxes , scores , class_ids = detect(frame)
            output = detect.draw_detections(frame)
            
            end = time.time()
            # Convert the output to an image that can be displayed
            outputing2.write(f"FPS : {round(1.0 / (end - start) , 2)}" , key = 0)
      
            output_image = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            
            # Display the image
            if i%5==0:
                time.sleep(1.5)
            i+=1
            outputing.image(output_image)

        cap.release() 
    else:
        st.write("Please upload a video file ")
      


if __name__=="__main__":
    main()
    

    
    
    
