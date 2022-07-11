from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

from time import sleep

import base64
import requests
import time


#開啟博客來登入網頁
Browser = webdriver.Chrome()
LoginUrl= ('https://cart.books.com.tw/member/login')
Browser.get(LoginUrl)
#輸入帳密
UserName= ('haha17598@gmail.com')
UserPass= ('asd12345')
Ｕsername = Browser.find_element(by=By.XPATH, value='//*[@id="login_id"]').send_keys(UserName)
sleep(5)
UserPass = Browser.find_element(by=By.XPATH, value='//*[@id="login_pswd"]').send_keys(UserPass)
sleep(5)

#辨識驗證碼
img_base64 = Browser.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, Browser.find_element(by=By.XPATH, value='//*[@id="captcha_img"]/img'))

with open("captcha_login.png", 'wb') as image:
    image.write(base64.b64decode(img_base64))

file = {'file': open('captcha_login.png', 'rb')}  # 下載下來的一般驗證碼(Normal Captcha)圖片

api_key = '7968eda9a4962dbbf20446d061b79e06'
data = {
    'key': api_key,
    'method': 'post'
}

response = requests.post('http://2captcha.com/in.php', files=file, data=data)
print(f'response:{response.text}')

if response.ok and response.text.find('OK') > -1:

    captcha_id = response.text.split('|')[1]  # 擷取驗證碼ID

    for i in range(10):

        response = requests.get(
            f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
        print(f'response:{response.text}')

        if response.text.find('CAPCHA_NOT_READY') > -1:  # 尚未辨識完成
            time.sleep(3)

        elif response.text.find('OK') > -1:
            captcha_text = response.text.split('|')[1]  # 擷取辨識結果



            Browser.find_element(by=By.XPATH, value='//*[@id="captcha"]').send_keys(captcha_text)#輸入辨識結果的驗證碼

            sleep(3)
            Browser.find_element(by=By.XPATH, value='//*[@id="books_login"]').click()
            sleep(3)



            break

        else:
            print('取得驗證碼發生錯誤!')
else:
    print('提交驗證碼發生錯誤!')