import requests
import json
import time

class Share:
    def __init__(self):
        self.config = {
            'cookies': '',
            'id': ''
        }
        self.a = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

    def input_config(self):
        self.config['cookies'] = input("Nhập cookie facebook: ")
        self.config['id'] = input("Nhập id bài viết: ")
        with open("config.json", "w") as f:
            json.dump(self.config, f)

    def load_config(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

    def get_token(self):
        self.headers['Cookie'] = self.config['cookies']
        response = requests.get("https://business.facebook.com/content_management", headers=self.headers)
        if "EAAG" in response.text:
            access_token = 'EAAG' + response.text.split('EAAG')[1].split('","')[0]
            return access_token
        else:
            raise Exception("Không lấy được access token.")

    def get_info(self, token):
        self.headers['Cookie'] = self.config['cookies']
        try:
            response = requests.get(f"https://graph.facebook.com/me?access_token={token}", headers=self.headers)
            data = response.json()
            return data.get('name', 'Bảo Thy')
        except:
            return 'Bảo Thy'

    def share(self, token):
        name = self.get_info(token)
        headers = {
            'User-Agent': self.headers['User-Agent'],
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'graph.facebook.com',
            'Cookie': self.config['cookies']
        }
        while True:
            try:
                url = f"https://graph.facebook.com/me/feed?link=https://m.facebook.com/{self.config['id']}&published=0&access_token={token}"
                response = requests.post(url, headers=headers)
                data = response.json()
                curr_time = time.strftime("%H:%M:%S")
                if 'id' in data:
                    self.a += 1
                    print(f"\033[1;37m| \033[1;33m{self.a} \033[1;37m| \033[1;32m{curr_time} \033[1;37m| \033[1;36m{name} \033[1;37m| \033[1;33mSHARE \033[1;37m| \033[1;32mSUCCESS \033[1;37m|")
                else:
                    print(f"\033[1;31m[ {curr_time} ] - Bị block tính năng!")
            except Exception as e:
                print(f"\033[1;31m[ ERROR ]: {str(e)}")
            time.sleep(1)


if __name__ == "__main__":
    share = Share()
    share.input_config()
    share.load_config()
    try:
        token = share.get_token()
        share.share(token)
    except Exception as e:
        print(f"Lỗi khi lấy token: {e}")
