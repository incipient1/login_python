
# coding: utf-8

# In[1]:


import requests
import hashlib
import fake_useragent
import re
import pprint


# In[2]:


s = requests.Session()
user_agent = fake_useragent.UserAgent().random
login_json = 'https://passport.lagou.com/login/login.json'


# login_json即为登陆时的链接，但是需要传入参数，尤其是password，一个字符串，能看出来是被加密了<br>
# ![传参数](C:/Users/incipient/Desktop/login_json_form_data.png)<br>
# 最后在网页的源码中找到这个密码串如何生成：
# ![生成密码串](C:\/Users/\incipient\/Desktop\/gen_password_md5.png)<br>
# 在request headers中还有'X-Anit-Forge-Code'、'X-Anit-Forge-Token'需要获取

# In[3]:


def gen_password_md5(password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    g = 'veenike'
    password = g + password + g
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password


# In[7]:


def code_token():
    login_page = 'https://passport.lagou.com/login/login.html'
    headers = {'User-Agent':user_agent,
               'Referer':'https://www.lagou.com/'
              }
    r1 = s.get(login_page, headers=headers)
    pattern1 = re.compile(r"window.X_Anti_Forge_Token = '(.+)'")
    pattern2 = re.compile(r"window.X_Anti_Forge_Code = '(\d+)'")
    forge_token = pattern1.search(r1.text).group(1)
    forge_code = pattern2.search(r1.text).group(1)
    return forge_code, forge_token


# In[5]:


def login(username,password):
    forge_code,forge_token = code_token()
    login_headers = {'X-Anit-Forge-Code':forge_code,
                     'X-Anit-Forge-Token':forge_token,
                     'X-Requested-With':'XMLHttpRequest',
                     'User-Agent':user_agent,
                     'Referer':'https://passport.lagou.com/login/login.html',
                    }
    form_data = {'isValidate':'true',
                 'username':username,
                 'password':gen_password_md5(password),
                 'request_form_verifyCode':'',
                 'submit':''
                }
    r2 = s.post(url = login_json,
                headers = login_headers,
                data = form_data)
    print(r2.text)


# In[8]:


if __name__ == "__main__":
    username = ''
    passwd = ''
    login(username, passwd)

