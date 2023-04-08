from tkinter import filedialog
import os
import string

def install_library():
    os.system('py -m pip install pytesseract')
    os.system('py -m pip install pandas')
    os.system('py -m pip install open-cv')
    os.system('py -m pip install numpy')
    os.system('py -m pip install tqdm')
    os.system('cls')
    import pandas as pd
    import cv2
    import pytesseract
    import numpy as np
    import tqdm
    from tqdm import tqdm
    import string

try:
    import pandas as pd
    import cv2
    import pytesseract
    from pytesseract import *
    import numpy as np
    import tqdm
    from tqdm import tqdm
    import string
except ModuleNotFoundError:
    install_library()

from pytesseract import *

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def getText(filename):
    
    global txt
    #read img
    img = cv2.imread(filename)

    # threshold for red pixel
    lower = np.array([0, 0, 0])
    upper = np.array([40, 40, 255])
    thresh = cv2.inRange(img, lower, upper)

    #change all other color pixel to white
    result = img.copy()
    result[thresh != 255] = (255,255,255)

    #tesseract OCR to scan text 
    txt = image_to_string(result, config="--psm 6 digits") #config to get number

    #write img
    cv2.imwrite('red_numerals_thresh.jpg', thresh)
    cv2.imwrite('red_numerals_result.jpg', result)
    txt.strip()

    #text processing
    for i in txt:
        if i.isdigit() == True:
            continue
        if i == '-':
           txt = txt.replace(i,'') 
               
        if i in string.punctuation:
            continue
        else:
            txt = txt.replace(i,'') 
    txt = txt[0:7]
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return txt

    
  
#get to file
img_path = filedialog.askdirectory()  
result = []
directory = []
dir = []
for root, dirs, files in os.walk(img_path):
    for file in files:
        if(file.endswith(".jpg")):
            directory.append(file)
            dir.append(os.path.join(root,file))
print('Happy that fit you though, Sasha NPI.')            
for i,img in zip(tqdm(range(len(dir)),desc= 'Loading'),dir):
    getText(img)
    result.append(txt)


     
data = {'Name':directory,'Eboxy Thickness':result,}
df = pd.DataFrame(data) 
out_put = img_path + r'\result.csv'
df.to_csv(out_put,index = False) 
os.startfile(out_put)     
     