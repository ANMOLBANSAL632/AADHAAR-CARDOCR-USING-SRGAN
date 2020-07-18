# AADHAAR-CARDOCR-USING-SRGAN
Extracted Aadhar Card Number using Pytesseract-OCR from bad quality aadhar images using SRGAN and then validate it using Regex.
Project:- https://drive.google.com/drive/folders/1HEwF2cj0jZwQ0MuKVMi-jMCTEV4tg28Q?usp=sharing
Colab Notebook Link:- https://colab.research.google.com/drive/1N3owZRFLrSLNVSFy6Eh37zDNTChwKqn2?usp=sharing 
Reference:- https://github.com/idealo/image-super-resolution

Process Used:- Described in the given file using comments (OCR.ipynb)
Pretrained Model:- Using ISR module in Python which is trained on DIV2K dataset Run the code in Google Colab with GPU runtime

General Process:-

Taken the low quality aadhar image use ISR module to get high quality aadhar image.
Put the image into tessereact to extract aadhar no.
If aadhar no. not found sharpen the image and then again send it into tesseract.
if not found again then rotate the image by 90 degree and repeat the process.
After find aadhar no. validate it using Verhoeff Algorithm
Note:- Before converting the image into high quality do the OCR with low qualty images.

Other Technique:- EAST pretrained model: https://drive.google.com/drive/folders/1BS6tCzCitiAKX2VHhRzREFI-i6d17lYW?usp=sharing east.py will take image put it into EAST model and extract parts of the images than use tesseract to detect aadhar card number. Note:- EAST model can be combined with GANs to get better accuracy.
