#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyzbar import pyzbar
import cv2


# In[2]:


def readBarcodes(frame,list):    
    img = frame
    barcodes = pyzbar.decode(img)
    for barcode in barcodes: #iterate through all barcodes and QR codes in the frame
        if barcode is not None:            
            duplicate = False
            (x, y, w, h) = barcode.rect # get rectangle points
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # draw rectangle around detected barcodes
            barcodeText = barcode.data.decode("utf-8") # convert bytes type data to string
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeText, barcodeType)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
            # check if the detected barcode is duplicate
            for i in range(len(list)):                
                if list[i] == text:
                    duplicate = True
                    break
            if not duplicate:
                list.append(text)            
            
    return img


# In[3]:


cap = cv2.VideoCapture(0)   # read video file or stream. 0 means capturing from built in webcam.
barcodeNumbers = [] # list to store barcode numbers

while cap.isOpened(): # successful capture
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is not None:        
        detectedBarcodes = readBarcodes(frame,barcodeNumbers)        
        cv2.imshow('barcodes', detectedBarcodes)
        
        if cv2.waitKey(1) & 0xFF == 27: # exit when ESC is pressed
            break
    else:
        print('unable to read next frame')
        break

print(barcodeNumbers)
cap.release()
cv2.destroyAllWindows()

