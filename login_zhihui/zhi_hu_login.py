
# coding: utf-8

# In[34]:


import requests
import re
import pprint
import json
import pyquery
import hmac
import time
import base64
import hmac
import hashlib


# In[35]:


s = requests.Session()


# In[36]:


sigup_url = 'https://www.zhihu.com/signup'
home_url = 'https://www.zhihu.com'
sigin_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'


# In[37]:


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'


# In[38]:


headers_sigup = {'User-Agent':user_agent,
                'Connection':'keep-alive',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Host':'www.zhihu.com'
                }


# In[39]:


client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
authorization = 'oauth ' + client_id


# In[40]:


headers_sigin = {
               'authorization':authorization,
               'Referer':sigup_url,
               'Origin':home_url,
               'User-Agent':user_agent,
              }


# In[41]:


headers_captcha = {
    'authorization':authorization,
    'Referer':sigup_url,
    'User-Agent':user_agent,
}


# In[42]:


payload = {
    'client_id':client_id,
    'grant_type':'password',
    'source' : 'com.zhihu.web',
    'lang':'en',
    'ref_source':'other',
    'utm_source':None,
    }


# In[43]:


def get_token():
    r1 = s.get(sigup_url,headers = headers_sigup,allow_redirects = False)
    xsrf_token = r1.cookies['_xsrf']
    return xsrf_token


# In[44]:


def get_captcha():
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha'
    query_string_parameters = {'lang':'en'}
    r2 = s.get(captcha_url,data = query_string_parameters,headers = headers_captcha)

    if json.loads(r2.text)['show_captcha'] :
        r3 = s.put(captcha_url,data = query_string_parameters,
                   headers = headers_captcha)
        pattern = re.compile(r'"img_base64":"(.+?)=\n"')
        img_base64 = pattern.findall(r3.text)[0]
        img_data = base64.b64decode(img_base64)
        with open('captcha_zhihu.png','wb') as f:
            f.write(img_data)

        capthca = str(input('请输入验证码：'))
        return captcha
    else:
        return None


# In[45]:


def get_signature(timestamp):
    h = hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod = hashlib.sha1)
    grant_type = payload['grant_type']
    source = payload['source']
    h.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
    return h.hexdigest()


# In[46]:


def login(username,password):
    xsrf_token = get_token()
    timestamp = str(int(time.time()*1000))
    signature = get_signature(timestamp)
    captcha = get_captcha()
    payload.update({
        'username' : username,
        'password' : password,
        'timestamp' : timestamp,
        'signature' : signature,
        'captcha' : captcha,
        })
    headers_sigin.update({'X-Xsrftoken':xsrf_token})
    r3 = s.post(sigin_url,data = payload,headers = headers_sigin,
               allow_redirects  =False)
    check = check_login()
    if 'error' in r3.text:
        print(r3.text)
    elif check:
        print('登陆成功！')


# In[47]:


def check_login():
    r4 = s.get(sigup_url,allow_redirects = True,
               headers = {'User-Agent':user_agent})
    if r4.url == home_url:
        return True


# In[48]:


password = 'ab61420160908'
username = 'anbangnihao@gmail.com'
login(username,password)

