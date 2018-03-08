
# coding: utf-8

# In[25]:


import requests
import re
import fake_useragent
import base64


# In[26]:


user_agent = fake_useragent.UserAgent().random
s = requests.Session()

def get_captcha_img():
    r1 = s.get(url = 'https://sso.toutiao.com/',
               headers = {'Referer':'https://www.toutiao.com/',
                        'User-Agent':user_agent
                         }
               )
    pattern = re.compile(r"captcha: '(.+)'")
    captcha_base64 = pattern.search(r1.text).group(1)
    img_data = base64.b64decode(captcha_base64)
    with open('tou_tiao_captcha.png','wb') as f:
        f.write(img_data)


# 加载的验证码是Data Url，需要先用base64解码，然后保存验证码图片。验证码上的文字识别，只能靠肉眼了。

# In[48]:


def login():
    get_captcha_img()
    captcha = input('请输入验证码：')
    login_url = 'https://sso.toutiao.com/account_login/'
    login_headers = {'Referer':'https://sso.toutiao.com/',
                     'User-Agnent':user_agent,
                     'X-CSRFToken':'undefined',
                     'X-Requested-With':'XMLHttpRequest'}
    form_data = {'mobile':None,
                 'code':None,
                 'account':account,
                 'password':password,
                 'captcha':captcha,
                 'is_30_days_no_login':'false',
                 'service':'https://www.toutiao.com/'}
    r2 = s.post(login_url,headers = login_headers,data = form_data)
    return r2


# In[31]:


account = '18938021227'
password = 'Ab6142008'


# In[49]:


login()

