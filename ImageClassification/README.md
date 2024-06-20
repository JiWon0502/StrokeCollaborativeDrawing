# Stroke-based Collaborative Drawing between AI and Human




## Installation
Implemented using python==3.9.*


Referenced source code : https://github.com/JiWon0502/StrokeCollaborativeDrawing/tree/Jimin/ImageClassification

Get the Source Code
 - Download Zip file from " https://github.com/JiWon0502/StrokeCollaborativeDrawing/ "

Set Environment
 - Must use Window OS
 - install numpy, pandas, PIL, png, os, opencv-python, tensorflow, scikeras
 - install cairocfifi : This cairocffi is supported only in Windows environment

## Download raw file
 - https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/simplified;tab=objects?prefix=&forceOnObjectsSortingFiltering=false
 - enter the site and download apple.ndjson, cat.ndjson, eye.ndjson, pig.ndjson
 - rename those file as full_simplified_apple.ndjson, full_simplified_cat.ndjson, full_simplified_eye.ndjson, full_simplified_pig.ndjson and put those file inside raw_data folder

## Caution
 - our project scaling and Lmser-pix2seq scaling is different so please check the image size
 - we set 256 * 256 in default but you should change this size to 32 - 128

## Run the program

- run with jupyter notebook


## Code Explanation


#### image-classification-quickdraw.ipynb
: Image Classification을 진행하는 코드이다.

CNN 모델을 기반으로 Image Classification을 진행하며, 그림의 scale에 따라 결과가 달라질 수 있다.
결과는 class 0 : apple, class 1 : cat, class 2 : eye, class 3 : pig이다.

실행 방법

1. main의 demoUI.py를 질행하고, save process 버튼을 누르면, results 폴더에 indexX라는 폴더가 생긴다.
2. 그 폴더에 들어가보면, 결과가 rdp_deltas_X.npy가 생기는데, 이를 npy/features_labels에 넣고 코드의 파일 명을 바꿔준다.
3. Classification 결과가 나온다.


## References

1. **Image Classification : https://github.com/amelie-vogel/image-classification-quickdraw
