import json
import os
import time
import requests
import random
import subprocess
from datetime import datetime
from time import sleep

# --- KHAI BÁO MÀU SẮC VÀ FORMATING ---
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
xanh = "\033[1;36m"
v = "\033[38;2;220;200;255m"
thanh = f'\033[1;35m {trang}=> '

# --- BANNER ASCII ART CẦU VỒNG ---
RAINBOW_BANNER = r'''
,--,                                                        ,----,       ,----,           
,---.'|                                    ,--,              ,/   .`|     ,/   .`|           
|   | :       ,---,                      ,--.'|            ,`   .'  :   ,`   .'  : ,----..   
:   : |     .'  .' `\         ,---,   ,--,  | :          ;    ;     / ;    ;     //   /   \  
|   ' :   ,---.'     \       /_ ./|,---.'|  : '        .'___,/    ,'.'___,/    ,'|   :     : 
;   ; '   |   |  .`\  |,---, |  ' :|   | : _' |        |    :     | |    :     | .   |  ;. / 
'   | |__ :   : |  '  /___/ \.  : |:   : |.'  |        ;    |.';  ; ;    |.';  ; .   ; /--`  
|   | :.'||   ' '  ;  :.  \  \ ,' '|   ' '  ; :        `----'  |  | `----'  |  | ;   | ;     
'   :    ;'   | ;  .  | \  ;  `  ,''   |  .'. |            '   :  ;     '   :  ; |   : |     
|   |  ./ |   | :  |  '  \  \    ' |   | :  | '            |   |  '     |   |  ' .   | '___  
;   : ;   '   : | /  ;    '  \   | '   : |  : ;            '   :  |     '   :  | '   ; : .'| 
|   ,/    |   | '` ,/      \  ;  ; |   | '  ,/             ;   |.'      ;   |.'  '   | '/  : 
'---'     ;   :  .'         :  \  \;   : ;--'              '---'        '---'    |   :    /  
          |   ,.'            \  ' ;|   ,/                                         \   \ .'   
          '---'               `--` '---'                                           `---`     
                                                                                             
'''

def thanhngang(so):
    print(trang+'═'*so)

def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (length - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (length - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (length - 1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

def print_rainbow_banner():
    # Màu cầu vồng đơn giản cho độ rõ nét (Đỏ -> Xanh lục -> Xanh lam)
    rainbow_colors = [
        (255, 0, 0),    # Đỏ
        (255, 127, 0),  # Cam
        (255, 255, 0),  # Vàng
        (0, 255, 0),    # Xanh lục
        (0, 0, 255),    # Xanh lam
        (75, 0, 130),   # Chàm
        (148, 0, 211)   # Tím
    ]
    
    lines = RAINBOW_BANNER.split('\n')
    
    for i, line in enumerate(lines):
        if line.strip(): 
            start_color_index = i % len(rainbow_colors)
            end_color_index = (i + 1) % len(rainbow_colors)
            
            if len(lines) == 1:
                print(gradient(line, (255, 0, 0), (0, 0, 255)))
            else:
                print(gradient(line, rainbow_colors[start_color_index], rainbow_colors[end_color_index]))

def Delay(value):
    print(f'{v}[{xanh}TTC-TIKTOK{v}] Đang nghỉ {value} giây...', end='\r')
    sleep(value)
    print(" " * 50, end='\r') 

# --- CLASS TIKTOK DÙNG CHO DEEP-LINK ---
class TikTok:
    """Class mô phỏng tài khoản TikTok, dùng ID TTC để gọi deep-link."""
    def __init__(self, id_ttc):
        self.id = id_ttc
        self.name = f"User_{id_ttc}"
        
    def info(self):
        return {'success': 200, 'id': self.id, 'name': self.name}
    
    def open_tiktok_url(self, url):
        """Sử dụng lệnh shell để mở deep-link TikTok."""
        try:
            print(f"{luc}---> Đang mở TikTok deep-link...{trang}", end='\r')
            subprocess.run(["termux-open", url], check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"\n{do}!!! LỖI MỞ APP: Hãy đảm bảo bạn đã cài đặt {vang}termux-api{do} và lệnh {vang}termux-open{do} hoạt động. Lỗi: {e}{trang}")
            try:
                subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], check=True, capture_output=True)
                return True
            except:
                 return False

    def follow(self, target_id):
        url = f"https://www.tiktok.com/@{target_id}" 
        return self.open_tiktok_url(url)

    def like(self, target_id):
        url = f"https://www.tiktok.com/video/{target_id}" 
        return self.open_tiktok_url(url)

    def comment(self, target_id, message):
        pass 

# --- CLASS TƯƠNG TÁC CHÉO ---
class TuongTacCheoTikTok(object):
    """Class tương tác với API của nền tảng TuongTacCheo cho TikTok."""
    def __init__ (self, token):
        self.token = token
        self.ss = requests.Session()
        self.headers = {
            'Host': 'tuongtaccheo.com',
            'accept': '*/*',
            'origin': 'https://tuongtaccheo.com',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        self.cookie = None
        self.session_data = {'status': 'error'}
        self.login()

    def login(self):
        """Thực hiện đăng nhập và lấy cookie/session."""
        try:
            session_req = self.ss.post('https://tuongtaccheo.com/logintoken.php', 
                                       data={'access_token': self.token})
            
            self.cookie = session_req.headers.get('Set-cookie', '')
            self.session_data = session_req.json() if session_req.text else {}

            if self.session_data.get('status') == 'success':
                 self.headers['cookie'] = self.cookie
                 return True
            return False
        except Exception:
            return False

    def info(self):
        """Kiểm tra trạng thái đăng nhập và lấy thông tin User/Xu."""
        if self.session_data.get('status') == 'success':
            user = self.session_data.get('data',{}).get('user')
            xu = self.session_data.get('data',{}).get('sodu')
            if not user or not xu:
                 try:
                    home_req = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text
                    user = home_req.split('Xin chào, ')[1].split('<')[0]
                    xu = home_req.split('"soduchinh">')[1].split('<')[0]
                    return {'status': "success", 'user': user, 'xu': xu}
                 except:
                    return {'error': 'Lỗi lấy thông tin'}
            return {'status': "success", 'user': user, 'xu': xu}
        return {'error': 200}
        
    def cauhinh(self, id):
        """Cấu hình ID TikTok của bạn."""
        self.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        response = self.ss.post('https://tuongtaccheo.com/cauhinh/datnick.php', 
                                headers=self.headers, 
                                data={'iddat[]': id, 'loai': 'tt', }).text
        if response == '1':
            return {'status': "success", 'id': id}
        else:
            # Nếu phản hồi không phải '1' (lỗi cấu hình)
            return {'error': response} 

    def them_acc_tiktok(self, id):
        """Thêm ID TikTok vào tài khoản TTC."""
        self.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        add_url = 'https://tuongtaccheo.com/cauhinh/tiktok/themtiktok.php'
        add_data = {'uid': id, 'loai': 'tt', 'submit': 'submit'}
        
        try:
            add_req = self.ss.post(add_url, headers=self.headers, data=add_data)
            
            if 'Thành công' in add_req.text or 'Đã thêm' in add_req.text or add_req.status_code == 200:
                return self.cauhinh(id)
            else:
                return {'error': f"Lỗi thêm: {add_req.text[:50]}"}
        except Exception as e:
            return {'error': f"Lỗi kết nối khi thêm: {e}"}
        
    def getjob(self, nv):
        """Lấy Job TikTok."""
        return self.ss.get(f'https://tuongtaccheo.com/kiemtien/tiktok/{nv}/getpost.php', headers=self.headers)
    
    def nhanxu(self, id, nv):
        """Gửi yêu cầu nhận xu sau khi hoàn thành nhiệm vụ."""
        try:
            response = self.ss.post(f'https://tuongtaccheo.com/kiemtien/tiktok/{nv}/nhantien.php', 
                                    headers=self.headers, 
                                    data={'id': id}).json()
            
            xu_response = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text
            xu_sau = xu_response.split('"soduchinh">')[1].split('<')[0] if '"soduchinh">' in xu_response else '0'
            
            if response.get('mess') and xu_sau != '0':
                msg = response['mess'].split()[-2]
                return {'status': "success", 'msg': f'+{msg} Xu', 'xu': xu_sau} 
            return {'error': response}
        except:
             return {'error': {'mess': 'Lỗi nhận xu TTC'}}


# --- CHỨC NĂNG PHỤ TRỢ MỚI ---
def get_tiktok_id(force_new=False):
    """Lấy hoặc nhập ID TikTok. Nếu force_new=True, sẽ xóa file cũ và nhập mới."""
    file_ids = 'tiktok_id.json'
    
    if force_new and os.path.exists(file_ids):
        os.remove(file_ids)
        
    if os.path.exists(file_ids):
        try:
            return json.loads(open(file_ids, 'r').read())[0]
        except (json.JSONDecodeError, IndexError):
            # Nếu file lỗi, xóa file và yêu cầu nhập lại
            os.remove(file_ids)

    id_tt = input(f'{thanh}{luc}Nhập ID TikTok Cần Cấu Hình{trang}: {vang}')
    print(f'{thanh}{luc}ID Đã Nhập: {vang}{id_tt}')
    with open(file_ids,'w') as f:
        json.dump([id_tt], f)
    return id_tt

def load_or_get_token(force_new=False):
    """Load hoặc nhập Access Token. Nếu force_new=True, sẽ xóa file cũ và nhập mới."""
    file_token = 'ttc_tiktok_token.json'
    
    if force_new and os.path.exists(file_token):
        os.remove(file_token)
        
    if os.path.exists(file_token):
        try:
            token_json = json.loads(open(file_token,'r').read())
            token = token_json[0].split("|")[0]
            ttc = TuongTacCheoTikTok(token)
            checktoken = ttc.info()
            if checktoken.get('status') == 'success':
                 return ttc, checktoken['user'], checktoken['xu']
            else:
                 print(f'{do}Lỗi đăng nhập token cũ. Đang xóa {file_token} và yêu cầu nhập lại.')
                 os.remove(file_token)
        except (json.JSONDecodeError, IndexError):
            # Nếu file lỗi, xóa file và yêu cầu nhập lại
            os.remove(file_token)

    while True:
        token = input(f'{thanh}{luc} Nhập Access_Token TTC (TikTok){trang}: {vang}')
        print('\033[1;36mĐang Xử Lý....','     ',end='\r')
        ttc = TuongTacCheoTikTok(token)
        checktoken = ttc.info()
        if checktoken.get('status') == 'success':
            users, xu = checktoken['user'], checktoken['xu']
            print(f"{luc}Đăng Nhập Thành Công")
            with open(file_token,'w') as f:
                json.dump([token+'|'+users],f)
            return ttc, users, xu
        else:
            print(f'{do}Đăng Nhập Thất Bại')

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        print_rainbow_banner()
        thanhngang(70)
        
        # --- LỰA CHỌN CHỨC NĂNG KHỞI ĐỘNG ---
        print(f'{thanh}{luc}Nhập {do}[{vang}C{do}] {luc}Để Chạy Tool với cấu hình hiện tại.')
        print(f'{thanh}{luc}Nhập {do}[{vang}D{do}] {luc}Để Đổi Access Token TTC.')
        print(f'{thanh}{luc}Nhập {do}[{vang}I{do}] {luc}Để Đổi ID TikTok cấu hình.')
        
        choice = input(f'{thanh}{v}Chọn Chức Năng{trang}: {vang}').upper()
        
        if choice == 'D':
            # Đổi Token
            load_or_get_token(force_new=True)
            print(f'{luc}Token đã được cập nhật! Khởi động lại tool.{trang}')
            time.sleep(2)
            continue
        
        if choice == 'I':
            # Đổi ID TikTok
            get_tiktok_id(force_new=True)
            print(f'{luc}ID TikTok đã được cập nhật! Khởi động lại tool.{trang}')
            time.sleep(2)
            continue
        
        if choice == 'C' or choice == '':
            # Chạy Tool
            pass
        else:
            print(f'{do}Lựa chọn không hợp lệ. Vui lòng thử lại.{trang}')
            time.sleep(1)
            continue
        
        # --- QUY TRÌNH CHẠY TOOL ---
        ttc, users, xu = load_or_get_token()
        if not ttc:
            return

        id_ttc = get_tiktok_id()
        
        os.system("cls" if os.name == "nt" else "clear")
        
        # Hiển thị lại banner và thông tin sau khi đăng nhập thành công
        print_rainbow_banner()
        thanhngang(70) 

        print(f'{thanh}{luc}TTC User{trang}: {vang}{users}')
        print(f'{thanh}{luc}Total Coin{trang}: {vang}{xu}')
        print(f'{thanh}{luc}ID TikTok Cấu Hình{trang}: {vang}{id_ttc}')
        thanhngang(50)
        
        # Cấu hình ID
        cauhinh = ttc.cauhinh(id_ttc)
        if cauhinh.get('status') != 'success':
            print(f'{do}ID TikTok {id_ttc} chưa cấu hình trên TTC. Đang thử thêm tài khoản...{trang}')
            
            them_acc = ttc.them_acc_tiktok(id_ttc)
            if them_acc.get('status') == 'success':
                print(f'{luc}--> THÀNH CÔNG: Đã thêm và cấu hình ID {vang}{id_ttc}{luc} thành công!{trang}')
            else:
                print(f'{do}LỖI: Không thể thêm/cấu hình ID {id_ttc}. Lỗi: {them_acc.get("error")}{trang}')
                print(f'{do}Vui lòng kiểm tra lại ID TikTok và trạng thái trên trang web TTC.{trang}')
                return

        # CHỌN NHIỆM VỤ
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Để Chạy Nhiệm Vụ Follow (tt_sub)')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Để Chạy Nhiệm Vụ Like (tt_like)')
        
        nhiemvu = str(input(f'{thanh}{v}Nhập Số Để Chọn Nhiệm Vụ (VD: 12){trang}: {vang}'))
        list_nv = [x for x in nhiemvu if x in ['1','2']]
        
        if not list_nv:
            print(f'{do}Không có nhiệm vụ nào được chọn. Thoát tool.')
            return
            
        delay = int(input(f'{thanh}{v}Nhập Delay Job (sau khi hoàn thành){trang}: {vang}') or 5)
        
        tt_acc = TikTok(id_ttc) 
        JobSuccess, JobFail = 0, 0
        stt = 0
        xu_str = str(xu) 
        totalxu = int(xu_str.replace(',', '')) 

        print(gradient(f'\n*** BẮT ĐẦU CHẠY VỚI ID TIKTOK: {id_ttc} ***'))
        
        while True:
            list_nv_current = list_nv.copy()
            
            if not list_nv_current:
                 print(f'{do}Đã block tất cả nhiệm vụ. Vui lòng kiểm tra lại ID: {id_ttc} sau.{trang}')
                 break
                 
            random_nv = random.choice(list_nv_current)
            
            if random_nv == '1': fields = 'tt_sub'; task_func = tt_acc.follow
            elif random_nv == '2': fields = 'tt_like'; task_func = tt_acc.like
            else: continue

            try:
                getjob = ttc.getjob(fields)
                
                if getjob.status_code == 200 and ("idpost" in getjob.text or "uid" in getjob.text):
                    job_list = getjob.json()
                    print(f"{luc} Đã Tìm Thấy {len(job_list)} Nhiệm Vụ {fields.upper()}...{trang}", end = "\r")
                    
                    for x in job_list:
                        target_id = x.get('idpost') or x.get('UID')
                        
                        if not target_id: continue

                        # 1. THỰC HIỆN HÀNH ĐỘNG (Mở App)
                        task_func(target_id)
                        
                        # 2. XÁC NHẬN HOÀN THÀNH
                        print(f'\n{vang}BẮT BUỘC: Sau khi hoàn thành trên TikTok, nhấn {luc}ENTER {vang}để nhận xu và tiếp tục...{trang}')
                        input()

                        # 3. NHẬN XU
                        nhanxu = ttc.nhanxu(target_id, fields)

                        if nhanxu.get('status') == 'success':
                            msg, xu_current, timejob = nhanxu['msg'], nhanxu['xu'], datetime.now().strftime('%H:%M:%S')
                            
                            xu_current_str = str(xu_current)
                            totalxu = int(xu_current_str.replace(',', ''))

                            stt+=1
                            JobSuccess += 1
                            
                            print(f'{do}[ {xanh}{stt}{do} ] {do}[ {vang}TIKTOK-TOOL{do} ][ {xanh}{timejob}{do} ][ {vang}{fields.upper()}{do} ][ {trang}{target_id}{do} ][ {vang}{msg}{do} ][ {luc}{xu_current_str} {do}]')
                        else:
                            JobFail += 1
                            print(f'{trang}[{do}{JobFail}{trang}] {trang}[{do}ERROR NHẬN XU{trang}] {trang}{target_id} - {nhanxu.get("error",{}).get("mess", "Lỗi TTC")}')
                        
                        # 4. KIỂM TRA CHỐNG BLOCK
                        if JobFail >= 5:
                            print(do+f'\nID {id_ttc} gặp lỗi nhận xu liên tục ({fields.upper()}). Đang thử nhiệm vụ khác...{trang}')
                            list_nv.remove(random_nv)
                            JobFail = 0
                            break

                        # 5. DELAY
                        Delay(delay)
                
                else:
                    error_data = getjob.json() if getjob.status_code == 200 and getjob.text else {}
                    error_mess = error_data.get('error', 'Lỗi kết nối/Không có nhiệm vụ.')
                    countdown = error_data.get('countdown')
                    print(f'{vang}Không có Job {fields.upper()} hoặc lỗi: {error_mess}. Đang chuyển nhiệm vụ.{trang}', end='\r')
                    
                    if random_nv in list_nv:
                         list_nv.remove(random_nv)
                    
                    if not list_nv:
                        print(f'{do}Không còn nhiệm vụ nào khả dụng. Tạm dừng 60 giây.{trang}')
                        sleep(60)
                        list_nv = [x for x in nhiemvu if x in ['1','2']]
                    
                    if countdown: Delay(countdown)
                    sleep(1)

            except Exception as e:
                print(f'{do}Lỗi bất ngờ: {e}{trang}')
                if random_nv in list_nv:
                    list_nv.remove(random_nv)
                sleep(5)
            
if __name__ == "__main__":
    main()
