import cv2
import numpy as np
import easyocr
import requests

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
thickness = 2

# Load the image
img = cv2.imread("input_image2.jpg")
print('Image Read')
# Use EasyOCR to detect the text and its bounding box
reader = easyocr.Reader(['ja'])
texts = reader.readtext(img)
print('Text Read')
# Draw a solid white rectangle around each bounding box
for text in texts:
    text_to_translate = text[1]
    print(text_to_translate)
    bbox = np.array([text[0]], np.int32)
    cv2.fillPoly(img, [bbox], (255, 255, 255))
    print(bbox)
    
    print(bbox[0][0])
    
    # Send the Japanese text to localhost:14366
    url = "http://localhost:14366"
    headers = {'Content-type': 'application/json'}
    data = { "content": text_to_translate, "message": "translate sentences"}
    r = requests.post(url, json=data, headers=headers)
    print(str(r.status_code))
    print(r.json())

    # Get the response from the server
    response = r.json()
    english_text = r.json()
    x1,y1 = bbox[0][0]
    x2,y2 = bbox[0][1]
    x3,y3 = bbox[0][2]
    x4,y4 = bbox[0][3]
    
    #Get size of text before writing
    text_size = cv2.getTextSize(english_text, font, font_scale, thickness)[0]
    print(text_size)
    W, H = cv2.getTextSize(english_text, font, font_scale, thickness)[0]
    print(W, H)
    CenterX = int(((x1 + x2) / 2)-(W/2))
    CenterY = int((y1 + y3) / 2)
    
    Y2 =  int(y4-(H/1.5))
    X2 =  int(x4+(W/2))
    # Replace the Japanese text with the English text
    cv2.putText(img, english_text, (CenterX, Y2), font, font_scale, (0, 0, 0), thickness)

# Show the image with the solid white rectangles
cv2.imshow("Detected Text", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
