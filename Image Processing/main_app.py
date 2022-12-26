#Import libraries
import streamlit as st
import numpy as np
import cv2
from  PIL import Image, ImageEnhance
import streamlit.components.v1 as stc 

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Photo Converter</h1>
		<h4 style="color:white;text-align:center;">Image Processing and Streamlit </h4>
		</div>
		"""
stc.html(html_temp)

#upload File
uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])

#Add 'before' and 'after' columns
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
        st.image(image,width=300)  

    with col2:
        st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
        
        #Add the filter in the sidebar
        filter = st.sidebar.radio('Covert your photo to:', ['Original','Add Tone','Gray Image', 'Black and White', 'Blur Effect','Warm Tone','Cool Tone']) 
        if filter == 'Gray Image':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                st.image(gray_scale, width=300)
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('GrayScaleImage.png',gray_scale)
                    st.text("File Saved")
     
        elif filter == 'Black and White':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                st.image(blackAndWhiteImage, width=300)
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('BlackandWhiteImage.png',blackAndWhiteImage)
                    st.text("File Saved")
     
        elif filter == 'Blur Effect':
                converted_img = np.array(image.convert('RGB'))
                slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                st.image(blur_image, channels='BGR', width=300) 
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('BlurImage.png',blur_image)
                    st.text("File Saved")
     
     
        elif filter == 'Add Tone':
                converted_img = np.array(image.convert('RGB'))
                #getting Red green blue colour values
                slider1 =  st.sidebar.slider('Adjust the intensity of Red Colour', 0, 255,80 ,step=1)
                slider2 = st.sidebar.slider('Adjust the intensity of Green Colour', 0, 255,20, step=1)
                slider3 = st.sidebar.slider('Adjust the intensity of Blue Colour', 5, 255,100, step=1)
                ##Getting alpha beta values
                a = st.sidebar.slider("Adjust the Alpha value",0.0,1.0,0.5,step=0.1)
                b = st.sidebar.slider("Adjust the Beta value",0.0,1.0,0.5,step=0.1)
                

                #code for imposing colours on our image
                background = []
                cols = converted_img.shape[1]
                rows = converted_img.shape[0]

                #imposing the background with the image
                for i in range(rows):
                    temp = []
                    for j in range(cols):
                        temp.append([slider1,slider2,slider3])
                    background.append(temp)
                background = np.array(background).astype(np.uint8)
                final = cv2.addWeighted(converted_img, a , background, b , 0)
                st.image(final, channels='BGR', width=300) 
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('TonedImage.png',final)
                    st.text("File Saved")
                
                
        elif filter == 'Warm Tone':
                converted_img = np.array(image.convert('RGB'))
                st.sidebar.caption("Warm Tone basically means merging the image with a tint of yellow colour.")
                yellow = [108,222,249]
                ##Getting alpha beta values
                a = st.sidebar.slider("Adjust the Alpha value",0.0,1.0,0.8,step=0.1)
                b = st.sidebar.slider("Adjust the Beta value",0.0,1.0,0.2,step=0.1)
                
                #Background Creation
                background = []
                rows = converted_img.shape[0]
                cols = converted_img.shape[1]
                for i in range(rows):
                    temp = []
                    for j in range(cols):
                        temp.append(yellow)
                    background.append(temp)    
                background = np.array(background).astype(np.uint8)
                
                merged = cv2.addWeighted(converted_img, a, background, b, 0)

                st.image(merged, channels='BGR', width=300)
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('WarmTonedImage.png',merged)
                    st.text("File Saved")
            
        elif filter == 'Cool Tone':
                converted_img = np.array(image.convert('RGB'))
                st.sidebar.caption("Cool Tone basically means merging the image with a tint of Blue colour.")
                blue = [247,206,139]
                ##Getting alpha beta values
                a = st.sidebar.slider("Adjust the Alpha value",0.0,1.0,0.8,step=0.1)
                b = st.sidebar.slider("Adjust the Beta value",0.0,1.0,0.2,step=0.1)
                
                #Background Creation
                background = []
                rows = converted_img.shape[0]
                cols = converted_img.shape[1]
                for i in range(rows):
                    temp = []
                    for j in range(cols):
                        temp.append(blue)
                    background.append(temp)    
                background = np.array(background).astype(np.uint8)
                
                merged = cv2.addWeighted(converted_img, a, background, b, 0)

                st.image(merged, channels='BGR', width=300)
                save = st.radio("Do you want to save this Image?",("False","True"))
                if save =='True':
                    cv2.imwrite('CoolTonedImage.png',merged)
                    st.text("File Saved")
            
            
        
        else: 
                st.image(image, width=300)
                
   


