import cv2
import numpy as np
import pytesseract
import requests

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
thickness = 2


# Load the image
img = cv2.imread("input_image.jpg")
# Run OCR on the image using the Japanese language
text = pytesseract.image_to_string(img, lang='jpn')
txt = text.splitlines()
while("" in txt):
    txt.remove("")
print(text)
# Send the Japanese text to localhost:14366
url = "http://localhost:14366"
headers = {'Content-type': 'application/json'}
data = { "content": text, "message": "translate sentences"}
r = requests.post(url, json=data, headers=headers)
print(str(r.status_code))
print(r.json())

# Get the response from the server
response = r.json()
english_text = r.json()


# Get the bounding boxes for each character
d = pytesseract.image_to_data(img, lang='jpn', output_type=pytesseract.Output.DICT)
n_boxes = len(d['level'])
print(d)
# Find the top-left and bottom-right corners of the bounding box
x1, y1 = None, None
x2, y2 = None, None
for i in range(n_boxes):
    if d['text'][i] != '':
        x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
        if x1 is None or x < x1:
            x1 = x
        if y1 is None or y < y1:
            y1 = y
        if x2 is None or x + w > x2:
            x2 = x + w
        if y2 is None or y + h > y2:
            y2 = y + h

# Find the center point between x1, y1 and x2, y2
x3 = int((x1 + x2) / 2)
y3 = int((y1 + y2) / 2)
# Draw a red rectangle around all the characters
cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)

text_size = cv2.getTextSize(english_text, font, font_scale, thickness)[0]
print(text_size)
W2, H2 = cv2.getTextSize(english_text, font, font_scale, thickness)[0]
print(W2, H2)
C1= int((x3-(W2 / 2)))
C2= int(y2-(h / 4))

cv2.putText(img, english_text, (C1, C2), font, font_scale, (0, 0, 0), thickness)



# Display the result
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
