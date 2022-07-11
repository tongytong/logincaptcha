import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', '7968eda9a4962dbbf20446d061b79e06')

solver = TwoCaptcha(api_key)

try:
    result = solver('path/to/captcha.jpg')

except Exception as e:
    sys.exit(e)

else:
    sys.exit('solved: ' + str(result))