import json
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pystyle import Write, Colors, Colorate
from datetime import datetime
import cloudscraper
import socket
import subprocess
from time import strftime
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from colorama import Fore, init
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
import psutil
import random
import re
import base64
import uuid

# --- KHAI BÁO MÀU SẮC ANSI (TỪ SCRIPT 1) ---
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
tim = '\033[1;39m'
hong = "\033[1;35m"
trang = "\033[1;37m"
whiteb = "\033[1;37m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'

# Thêm các màu tùy chỉnh từ Script 2
xanh = "\033[1;36m"
dep = "\033[38;2;160;231;229m"
v = "\033[38;2;220;200;255m"

# List of main colors for randomization (TỪ SCRIPT 1)
RANDOM_COLORS = [xnhac, do, luc, vang, xduong, hong]

def get_random_color():
    """Returns a random ANSI color code from the main color list."""
    return random.choice(RANDOM_COLORS)

def banner():
    """Hiển thị banner với hiệu ứng màu ngẫu nhiên và hiệu ứng gõ chữ."""
    # os.system("cls" if os.name == "nt" else "clear") # Giữ lại comment để tránh xóa màn hình trong một số môi trường
    
    # Tạo một danh sách màu ngẫu nhiên cho 6 dòng banner ASCII art
    COLORS_LIST = [luc, vang, do, hong, xnhac, xduong]
    random.shuffle(COLORS_LIST)
    
    c1, c2, c3, c4, c5, c6 = COLORS_LIST[0], COLORS_LIST[1], COLORS_LIST[2], COLORS_LIST[3], COLORS_LIST[4], COLORS_LIST[5]
    
    # Áp dụng chuỗi màu ngẫu nhiên theo mô hình tuần hoàn cho từng segment
    banner_ascii = f"""
{c1}██╗░░░░░{c2}██████╗░{c3}██╗░░░██╗{c4}██╗░░██╗{end}  {c5}████████╗░{c6}█████╗░░{c1}█████╗░{c2}██╗░░░░░
{c3}██║░░░░░{c4}██╔══██╗{c5}╚██╗░██╔╝{c6}██║░░██║{end}  {c1}╚══██╔══╝{c2}██╔══██╗{c3}██╔══██╗{c4}██║░░░░░
{c5}██║░░░░░{c6}██║░░██║{c1}░╚████╔╝░{c2}███████║{end}  {c3}░░░██║░░░{c4}██║░░██║{c5}██║░░██║{c6}██║░░░░░
{c1}██║░░░░░{c2}██║░░██║{c3}░░╚██╔╝░░{c4}██╔══██║{end}  {c5}░░░██║░░░{c6}██║░░██║{c1}██║░░██║{c2}██║░░░░░
{c3}███████╗{c4}██████╔╝{c5}░░░██║░░░{c6}██║░░██║{end}  {c1}░░░██║░░░{c2}╚█████╔╝{c3}╚█████╔╝{c4}███████╗
{c5}╚══════╝{c6}╚═════╝░{c1}░░░╚═╝░░░{c2}╚═╝░░╚═╝{end}  {c3}░░░╚═╝░░░{c4}░╚════╝░░{c5}╚════╝░{c6}╚══════╝\n
"""
    
    INFO_COLOR = get_random_color()
    
    # Information section using random colors
    banner_info = f"""{trang}Tool By: {INFO_COLOR}Let’s Do Your Hack 💻 {end}           {trang}Phiên Bản: {INFO_COLOR}DEMO{end}    
{trang}════════════════════════════════════════════════{end}  
{trang}[{do}<>{trang}]{hong} BOX ZALO{do} : {xnhac}https://zalo.me/g/ehnpay312{end}
{trang}[{do}<>{trang}]{vang} YOUTUBE{do} : {luc}Let’s Do Your Hack{end} 
{trang}[{do}<>{trang}]{luc} ADMIN{do} : {xduong}LŸ VÄN DÜY{end}

{trang}════════════════════════════════════════════════{end}  
"""
    full_banner = banner_ascii + banner_info
    
    # Typing effect
    for X in full_banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.00125)

# --- KẾT THÚC PHẦN BANNER ---


def gradient_3(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    start = (0, 255, 0)   # xanh lá
    end   = (0, 128, 255) # xanh biển

    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"
    
def gradient_tutu(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    start_color = (255, 192, 203)  # 🌸 Hồng phấn
    mid_color   = (152, 251, 152)  # 🌿 Mint nhạt
    end_color   = (255, 255, 102)  # 💛 Vàng chanh pastel

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def inp(text, colors=None):
    if not colors:
        # Default gradient màu tím - xanh biển - xanh lá
        colors = [129, 93, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123]
    result = ""
    for i, c in enumerate(text):
        color = colors[i % len(colors)]
        result += f"\033[38;5;{color}m{c}"
    return result + "\033[0m"
    
unicode_invisible = ("ㅤ")

def gradient_2(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    # 🎨 Màu gradient nổi bật hơn
    start_color = (255, 87, 34)     # 🧡 Cam đất
    mid_color   = (255, 20, 147)    # 💖 Hồng đậm neon
    end_color   = (255, 255, 0)     # 💛 Vàng sáng

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def gradient_1(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    # 🎨 Màu gradient nổi bật hơn
    start_color = (0, 128, 255)     # 💧 Xanh dương đậm
    mid_color   = (0, 255, 255)     # 🧊 Cyan sáng
    end_color   = (255, 255, 255)   # ⚪ Trắng sáng

    steps = len(text)
    result = ""

    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)

        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)

        result += rgb_to_ansi(r, g, b) + char

    return result + "\033[0m"
    
def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (length - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (length - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (length - 1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"  # Reset màu về mặc định
    return result

# Khởi tạo biến (từ Script 2)
thanh = f'\033[1;35m {trang}=> '
listCookie = []
list_nv = []

def thanhngang(so):
    for i in range(so):
        print(trang+'═',end ='')
    print('')
os.system("cls" if os.name == "nt" else "clear")
# Hàm banner() đã được định nghĩa ở trên

def Delay(value):
    while not(value <= 1):
        value -= 0.123
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [{vang}dqt-tool    {v}]''', '           ', end = '\r')
        sleep(0.02)
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [ {vang}dqt-tool   {v}]''', '           ', end = '\r')
        sleep(0.02)
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [  {vang}dqt-tool {v}]''', '            ', end = '\r')
        sleep(0.02)
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [   {vang}dqt-tool {v}]''', '           ', end = '\r')
        sleep(0.02)
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [    {vang}dqt-tool{v}]''', '           ', end = '\r')
        sleep(0.02)

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

class Facebook:
    def __init__(self, cookie: str):
        try:
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.session = requests.Session()
            self.id = self.cookie.split('c_user=')[1].split(';')[0]
            self.headers = {'authority': 'www.facebook.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'vi', 'sec-ch-prefers-color-scheme': 'light', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'viewport-width': '1366', 'Cookie': self.cookie}
            url = self.session.get(f'https://www.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            data_split = response.text.split('"CurrentUserInitialData",[],{')
            json_data = '{' + data_split[1].split('},')[0] + '}'
            parsed_data = json.loads(json_data)
            id = parsed_data.get('USER_ID', '0')
            name = parsed_data.get('NAME', '')
            if id == '0' and name == '': return 'cookieout'
            elif '828281030927956' in response.text: return '956'
            elif '1501092823525282' in response.text: return '282'
            elif '601051028565049' in response.text: return 'spam'
            else: id, name = parsed_data.get('USER_ID'), parsed_data.get('NAME')
            return {'success': 200, 'id': id, 'name': name}
        except:
            pass
        
    def likepage(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometProfilePlusLikeMutation','variables': '{"input":{"is_tracking_encrypted":false,"page_id":"'+str(id)+'","source":null,"tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"1"},"scale":1}','server_timestamps': 'true','doc_id': '6716077648448761',}
            response = self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers)
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return False
        except:
            pass

    def follow(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUserFollowMutation','variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1719765181042,489343,250100865708545,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,unexpected,1719765155735,648442,391724414624676,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1719765153341,865155,391724414624676,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"5"},"scale":1}','server_timestamps': 'true','doc_id': '25581663504782089',}
            response = self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers)
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return True
            else:
                return False
        except:
            pass

    def reaction(self, id: str, type: str):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            idreac = reac.get(type)
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': fr'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}
