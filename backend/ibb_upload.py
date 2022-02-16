"""
Upload Image to ibb.co through API.

@author: EJacobsen
@date: 12/12/2021

"""

import requests
import base64
from config import IBB_API_KEY

PATH = f'C:\\Users\\ejacobsen\\Downloads\\EJacobsen\\crypto_tools\\Convex Labs\\honestnft-shenanigans\\fair_drop\\scatterplots\\0N1_Force_scatterplot.png'
with open(PATH, "rb") as img_file:
    myString = base64.b64encode(img_file.read())

ibbUrl = f"https://api.imgbb.com/1/upload?expiration=600&key={IBB_API_KEY}"

myObj = {'image':myString}
x = requests.post(ibbUrl, data = myObj)
print(x._content)
