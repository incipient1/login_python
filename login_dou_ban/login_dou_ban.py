import requests
import re
from pyquery import PyQuery

session = requests.session()

def login(url,username,password):
    data = {
    'source':None,
    'redir':'https://www.douban.com/',
    'form_email':username,
    'form_password':password,
    'login':'登陆'

    }
    captcha_image_url,captcha_id = get_vcode(url)
    print('captcha_id',captcha_id)
    if captcha_id:
        data['captcha-id'] = captcha_id
        data['captcha-solution'] = input('请输入验证码：')

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/63.0.3239.132 Safari/537.36'
    referer = 'https://www.douban.com/'
    headers = {'User-Agent':user_agent,
                'Referer':referer,
            }
    session.get(url)

    response = session.post(url,data,headers = headers)
    jpy = PyQuery(response.text)
    username = jpy('#db-global-nav > div > div.top-nav-info > ul > li.nav-user-account > a > span:nth-child(1)').text()
    print(username)

def get_vcode(url):
    response = requests.get(url)
    try:
        captcha_image_url = re.findall(r'id="captcha_image" src="(.*?)" alt',response.text)[0]
        print(captcha_image_url,type(captcha_image_url))

        captcha_id = re.findall(r'id=(.*?)&amp',captcha_image_url)[0]

        response = requests.get(captcha_image_url)
        with open('vcode_douban.png','wb') as f:
            f.write(response.content)
        return captcha_image_url,captcha_id
    except:
        print('没有验证码')
        return None

if __name__ == '__main__':
    username = input('请输入你的邮箱：')
    password = input('请输入你的密码：')
    url = 'https://accounts.douban.com/login'
    login(url,username,password)