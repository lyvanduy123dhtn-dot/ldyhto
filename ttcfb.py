import json
import os
import sys
import time
import requests
import re
import base64
import uuid
import random
from time import sleep, strftime
from datetime import datetime
# Import thư viện giao diện và màu sắc
from pystyle import Write, Colors, Colorate # Giữ lại các import bạn dùng
from colorama import Fore, init
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Khởi tạo colorama
init(autoreset=True)

# --- KHU VỰC CÁC HÀM XỬ LÝ MÀU VÀ HIỂN THỊ ---

def rgb_to_ansi(r, g, b):
    """Chuyển đổi màu RGB sang mã ANSI 24-bit."""
    return f"\033[38;2;{r};{g};{b}m"

def gradient_3(text):
    """Gradient xanh lá -> xanh biển."""
    start = (0, 255, 0)
    end   = (0, 128, 255)
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

# Sửa lỗi IndentationError tại dòng 498 (hoặc gần đó)
def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    """Gradient tím -> cyan."""
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        if length <= 1: t = 0
        else: t = i / (length - 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t) # Đảm bảo thụt lề đúng
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m"
    return result

# Khôi phục các biến màu bạn đã định nghĩa
do = "\033[1;31m"      # Đỏ
luc = "\033[1;32m"     # Lục
vang = "\033[1;33m"    # Vàng
trang = "\033[1;37m"   # Trắng
tim = "\033[1;35m"     # Tím
xanh = "\033[1;36m"    # Cyan
dep = "\033[38;2;160;231;229m" # Xanh mint nhạt
v = "\033[38;2;220;200;255m"   # Tím sữa
thanh = f'\033[1;35m {trang}=> '

# Định nghĩa các hàm hiển thị bạn đã dùng
def thanhngang(so):
    print(trang + '═' * so)

def Delay(value):
    while value > 0:
        value -= 0.123
        if value < 0: value = 0
        
        # Chỉ hiển thị một kiểu delay để code gọn gàng hơn
        print(f'''{v}[{xanh}ttc-tool{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [{vang}dqt-tool{v}]''', '           ', end = '\r')
        sleep(0.06)
        
    print(" " * 80, end='\r') # Xóa dòng delay sau khi xong

# --- KHU VỰC HÀM TIỆN ÍCH ---

def decode_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except:
        return ""

def encode_to_base64(_data):
    try:
        byte_representation = _data.encode('utf-8')
        base64_bytes = base64.b64encode(byte_representation)
        return base64_bytes.decode('utf-8')
    except:
        return ""

# --- CLASS FACEBOOK ---

class Facebook:
    def __init__(self, cookie: str):
        self.fb_dtsg = ''
        self.jazoest = ''
        self.cookie = cookie
        self.session = requests.Session()
        self.id = cookie.split('c_user=')[1].split(';')[0] if 'c_user=' in cookie else None
        self.headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/53736',
            'viewport-width': '1366',
            'Cookie': self.cookie
        }
        self.get_tokens()

    def get_tokens(self):
        """Lấy fb_dtsg và jazoest."""
        if not self.id: return
        try:
            # Truy cập trang cá nhân hoặc trang home để lấy token
            response = self.session.get(f'https://www.facebook.com/profile.php', headers=self.headers)
            
            # Lấy fb_dtsg
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response.text)
            if matches:
                self.fb_dtsg = matches[0]
            
            # Lấy jazoest
            jazoest_match = re.search(r'jazoest=(\d+)', response.text)
            if jazoest_match:
                self.jazoest = jazoest_match.group(1)
            
        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass

    def info(self):
        """Lấy thông tin tài khoản và check checkpoint."""
        if not self.id: return 'cookieout' # Đảm bảo check id trước
        try:
            # Sửa: Dùng URL đơn giản hơn để lấy info
            response = self.session.get('https://www.facebook.com/me', headers=self.headers, params={"locale": "vi_VN"})
            text = response.text
            
            # Checkpoint/Khóa
            if '828281030927956' in text: return '956'
            if '1501092823525282' in text: return '282'
            if '601051028565049' in text: return 'spam'
            if 'title="Log in to Facebook">' in text or 'c_user=' not in self.cookie: return 'cookieout'

            # Lấy info
            data_match = re.search(r'"CurrentUserInitialData",\[\],({.*?})', text)
            if data_match:
                json_data = data_match.group(1)
                parsed_data = json.loads(json_data)
                id = parsed_data.get('USER_ID')
                name = parsed_data.get('NAME')
                if id and name:
                    return {'success': 200, 'id': id, 'name': name}
            
            return 'cookieout' # Trường hợp không lấy được info
        except Exception:
            return 'error'

    def _graphql_request(self, doc_id, variables, friendly_name):
        """Hàm chung để gửi request GraphQL."""
        if not self.fb_dtsg or not self.jazoest:
            self.get_tokens() # Thử lấy lại token nếu bị mất
            if not self.fb_dtsg or not self.jazoest:
                # print("Lỗi: Không lấy được token Facebook")
                return None
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': friendly_name,
                'variables': variables,
                'server_timestamps': 'true',
                'doc_id': doc_id,
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', data=data, headers=self.headers)
            return response
        except Exception:
            return None

    def likepage(self, id: str):
        variables = f'{{"input":{{"is_tracking_encrypted":false,"page_id":"{id}","source":null,"tracking":null,"actor_id":"{self.id}","client_mutation_id":"1"}},"scale":1}}'
        response = self._graphql_request('6716077648448761', variables, 'CometProfilePlusLikeMutation')
        return response and '"subscribe_status":"IS_SUBSCRIBED"' in response.text

    def follow(self, id: str):
        variables = f'{{"input":{{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1719765181042,489343,250100865708545,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,unexpected,1719765155735,648442,391724414624676,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1719765153341,865155,391724414624676,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"{id}","tracking":null,"actor_id":"{self.id}","client_mutation_id":"5"}},"scale":1}}'
        response = self._graphql_request('25581663504782089', variables, 'CometUserFollowMutation')
        return response and '"subscribe_status":"IS_SUBSCRIBED"' in response.text

    def reaction(self, id: str, type: str):
        reac = {"LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858", "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", "ANGRY": "444813342392137"}
        idreac = reac.get(type, "1635855486666999") # Default to LIKE
        variables = f'{{"input":{{"attribution_id_v2":"CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"tracking":[],"session_id":"{uuid.uuid4()}","actor_id":"{self.id}","client_mutation_id":"3"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}'
        self._graphql_request('7047198228715224', variables, 'CometUFIFeedbackReactMutation')

    def reactioncmt(self, id: str, type: str):
        reac = {"LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858", "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", "ANGRY": "444813342392137"}
        id_reac = reac.get(type, "1635855486666999")
        d = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        datetime_object = datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f")
        starttime = str(datetime_object.timestamp()).replace('.', '')
        
        variables = f'{{"input":{{"attribution_id_v2":"CometVideoHomeNewPermalinkRoot.react,comet.watch.injection,via_cold_start,1719930662698,975645,2392950137,,","feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{id_reac}","feedback_source":"TAHOE","is_tracking_encrypted":true,"tracking":[],"session_id":"{uuid.uuid4()}","downstream_share_session_id":"{uuid.uuid4()}","downstream_share_session_origin_uri":"https://fb.watch/t3OatrTuqv/?mibextid=Nif5oz","downstream_share_session_start_time":"{starttime}","actor_id":"{self.id}","client_mutation_id":"1"}},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}}'
        self._graphql_request('7616998081714004', variables, 'CometUFIFeedbackReactMutation')

    def share(self, id: str):
        variables = f'{{"input":{{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"{uuid.uuid4()}_FEED","source":"WWW","attachments":[{{"link":{{"share_scrape_data":"{{\\"share_type\\":22,\\"share_params\\":[{id}]}}"}}}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{{"privacy":{{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}}}},"is_tracking_encrypted":true,"tracking":["AZWWGipYJ1gf83pZebtJYQQ-iWKc5VZxS4JuOcGWLeB-goMh2k74R1JxqgvUTbDVNs-xTyTpCI4vQw_Y9mFCaX-tIEMg2TfN_GKk-PnqI4xMhaignTkV5113HU-3PLFG27m-EEseUfuGXrNitybNZF1fKNtPcboF6IvxizZa5CUGXNVqLISUtAWXNS9Lq-G2ECnfWPtmKGebm2-YKyfMUH1p8xKNDxOcnMmMJcBBZkUEpjVzqvUTSt52Xyp0NETTPTVW4zHpkByOboAqZj12UuYSsG3GEhafpt91ThFhs7UTtqN7F29UsSW2ikIjTgFPy8cOddclinOtUwaoMaFk2OspLF3J9cwr7wPsZ9CpQxU21mcFHxqpz7vZuGrjWqepKQhWX_ZzmHv0LR8K07ZJLu8yl51iv-Ram7er9lKfWDtQsuNeLqbzEOQo0UlRNexaV0V2m8fYke8ubw3kNeR5XsRYiyr958OFwNgZ3RNfy-mNnO9P-4TFEF12NmNNEm4N6h0_DRZ-g74n-X2nGwx9emPv4wuy9kvQGeoCqc636BfKRE-51w2GFSrHAsOUJJ1dDryxZsxQOEGep3HGrVp_rTsVv7Vk3JxKxlzqt3hnBGDgi6suTZnJw69poVOIz6TPCTthRhj7XUu4heyKBSIeHsjBRC2_s3NwuZ4kKNCQ2JkVuBXz_hsRhDmbAnBi6WUFIJhLHO_bGgKbEASuU4vtj4FNKo_G8p-J1kYmCo0Pi72Csi3EikuocfjHFwfSD3cCbetr3V8Yp6OmSGkqX63FkSqzBoAcHFeD-iyCAkn0UJGqU-0o670ZoR-twkUDcSJPXDN2NYQfqiyb9ZknZ7j04w1ZfAyaE7NCiCc-lDt1ic79XyHunjOyLStgXIW30J4OEw_hAn86LlRHbYVhi-zBBTZWWnEl9piuUz0qtnN-qEd002DjNYaMy0aDAbL9oOYDdN8mHvnXq1aKove9I4Jy0WtlxeN8279ayz7NdDZZ9LrajY_YxIJJqdZtJIuRYTunEeDsFrORpu3RYRbFwpGnQbHeSLH1YvwOyOJRXhYYmVLJEGD2N9r5wkPbgbx2HoWsGjWj_DpkEAyg59eBJy4RYPJHvOsetBQABEWmGI7nhUDYTPdhrzVxqB_g4fQ9JkPzIbEhcoEZjmspGZcR4z4JxUDJCNdAz2aK4lR4P5WTkLtj2uXMDD_nzbl8r_DMcj23bjPiSe0Fubu-VIzjwr7JgPNyQ1FYhp5u4lpqkkBkGtfyAaUjCgFhg4FW-H3d3vPVMO--GxbhK9kN0QAcOE3ZqQR2dRz6NbhcvTyNfDxy0dFTRw-f_vxn04gjJB5ZEG3WfSzQv0VbqDYm6-NFYAzIxbDLoiCu34WAa2lckx5qxncXBhQj6Fro2gXGPXo4d32DvyQg7_RHQ-SF_WLqdxRCXF91NIqxYmFZsOJAuQ5m6TafzuNnQoJB3OQFoknv8Uy5O4FKuwazh1rvLrsj-1QEMi3sTrr9KxJkZy9EKXs92ndlb3edgfycLOffTil-gW2BvxeNiMQzqF1xJqFBKHDyatgwpXDX81HDwxkuMEaGPREIeQLuOlBJrL_20RD1e4Gu4tjQD8vRsb29UNG60DqpDvc-H4Z2oxeppm0KIwQNaCTtGUxxmvT807fXMnuVEf5QI5qTx9YRJh56GiWLoHC_zPMhoikMbAybIVWh9HtVgZGgImDmz0l9P4LgtpKNnKbQj_2ZKn2ZhOYKZLdt1P2Jq2Z2z76MtbRQTrpZpFb14zWVnh1LFCSFPAB7sqC1-u-KQOf2_SjEecztPccso8xZB2nkhLetyPn9aFuO-J_LCZydQeiroXx4Z8NxhDpbLoOpw2MbRCVB_TxfnLGNn1QD0To9TTChxK5AHNRRLDaj3xK1e0jd37uSmHTkT6QJVHFHEYMVLBcuV1MQcoy0wsvc1sRb",null],"logging":{{"composer_session_id":"{uuid.uuid4()}"}},"navigation_data":{{"attribution_id_v2":"FeedsCometRoot.react,comet.most_recent_feed,tap_bookmark,1719641912186,189404,608920319153834,,"}},"event_share_metadata":{{"surface":"newsfeed"}},"actor_id":"{self.id}","client_mutation_id":"3"}},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometIsAdaptiveUFIEnabledrelayprovider":true,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__IncludeCommentWithAttachmentrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__StoriesRingrelayprovider":false,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}}'
        self._graphql_request('8167261726632010', variables, 'ComposerStoryCreateMutation')

    def group(self, id: str):
        variables = f'{{"feedType":"DISCUSSION","groupID":"{id}","imageMediaType":"image/x-auto","input":{{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1673041528761,114928,2361831622,","group_id":"{id}","group_share_tracking_params":{{"app_id":"2220391788200892","exp_id":"null","is_from_share":false}},"actor_id":"{self.id}","client_mutation_id":"1"}},"inviteShortLinkKey":null,"isChainingRecommendationUnit":false,"isEntityMenu":true,"scale":2,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometEntityMenuEmbeddedrelayprovider":true,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":false}}'
        self._graphql_request('5853134681430324', variables, 'GroupCometJoinForumMutation')

    def comment(self, id, msg: str):
        # Escape double quotes in message for JSON string
        msg = msg.replace('"', '\\"')
        variables = f'{{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"groupID":null,"input":{{"client_mutation_id":"4","actor_id":"{self.id}","attachments":null,"feedback_id":"{encode_to_base64(f"feedback:{id}")}","formatting_style":null,"message":{{"ranges":[],"text":"{msg}"}},"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,1718688700413,194880,4748854339,,","vod_video_timestamp":null,"feedback_referrer":"/","is_tracking_encrypted":true,"tracking":["AZX1ZR3ETYfGknoE2E83CrSh9sg_1G8pbUK70jA-zjEIcfgLxA-C9xuQsGJ1l2Annds9fRCrLlpGUn0MG7aEbkcJS2ci6DaBTSLMtA78T9zR5Ys8RFc5kMcx42G_ikh8Fn-HLo3Qd-HI9oqVmVaqVzSasZBTgBDojRh-0Xs_FulJRLcrI_TQcp1nSSKzSdTqJjMN8GXcT8h0gTnYnUcDs7bsMAGbyuDJdelgAlQw33iNoeyqlsnBq7hDb7Xev6cASboFzU63nUxSs2gPkibXc5a9kXmjqZQuyqDYLfjG9eMcjwPo6U9i9LhNKoZwlyuQA7-8ej9sRmbiXBfLYXtoHp6IqQktunSF92SdR53K-3wQJ7PoBGLThsd_qqTlCYnRWEoVJeYZ9fyznzz4mT6uD2Mbyc8Vp_v_jbbPWk0liI0EIm3dZSk4g3ik_SVzKuOE3dS64yJegVOQXlX7dKMDDJc7P5Be6abulUVqLoSZ-cUCcb7UKGRa5MAvF65gz-XTkwXW5XuhaqwK5ILPhzwKwcj3h-Ndyc0URU_FJMzzxaJ9SDaOa9vL9dKUviP7S0nnig0sPLa5KQgx81BnxbiQsAbmAQMr2cxYoNOXFMmjB_v-amsNBV6KkES74gA7LI0bo56DPEA9smlngWdtnvOgaqlsaSLPcRsS0FKO3qHAYNRBwWvMJpJX8SppIR1KiqmVKgeQavEMM6XMElJc9PDxHNZDfJkKZaYTJT8_qFIuFJVqX6J9DFnqXXVaFH4Wclq8IKZ01mayFbAFbfJarH28k_9LIxS8hOgq9VKNW5LW7XuIaMZ1Z17XlqZ96HT9TtCAcze9kBS9kMJewNCl-WYFvPCTCnwzQZ-HRVOM04vrQOgSPud7vlA3OqD4YY2PSz_ioWSbk98vbJ4c7WVHiFYwQsgQFvMzwES20hKPDrREYks5fAPVrHLuDK1doffY1hPTWF2KkSt0uERAcZIibeD5058uKSonW1fPurOnsTpAg8TfALFu1QlkcNt1X4dOoGpYmBR7HGIONwQwv5-peC8F758ujTTWWowBqXzJlA2boriCvdZkvS15rEnUN57lyO8gINQ5heiMCQN8NbHMmrY_ihJD3bdM4s2TGnWH4HBC2hi0jaIOJ8AoCXHQMaMdrGE1st7Y3R_T6Obg6VnabLn8Q-zZfToKdkiyaR9zqsVB8VsMrAtEz0yiGpaOF3KdI2sxvii3Q5XWIYN6gyDXsXVykFS25PsjPmXCF8V1mS7x6e9N9PtNTWwT8IGBZp9frOTQN2O52dOhPdsuCHAf0srrBVHbyYfCMYbOqYEEXQG0pNAmG_wqbTxNew9kTsXDRzYKW-NmEJcvy_xh1dDwg8xJc58Cl71e-rau3iP7o8mWhVSaxi4Bi6LAuj4UKVCt3IYCfm9AR1d5LqBFWU9LrLbRZSMlmUYwZf7PlrKmpnCnZvuismiL7DH3cnUjP0lWAvhy3gxZm1MK8KyRzWmHnTNqaVlL37c2xoE4YSyponeOu5D-lRl_Dp_C2PyR1kG0TCWS66UbU89Fu1qmwWjeQwYhzj2Jly9LRyClAbe86VJhIZE18YLPB-n1ng78qz7hHtQ8qT4ejY4csEjSRjjnHdz8U-06qErY-CXNNsVtzpYGuzZ1ZaXqzAQkUcREm98KR8c1vaXaQXumtDklMVgs76gLqZyiG1eCRbOQ6_EcQv7GeFnq5UIqoMH_Xzc78otBTvC5j3aCs5Pvf6k3gQ5ZU7E4uFVhZA7xoyD8sPX6rhdGL8JmLKJSGZQM5ccWpfpDJ5RWJp0bIJdnAJQ8gsYMRAI2OBxx2m2c76lNiUnB750dMe2H3pFzFQVkWQLkmGVY37cgmRNHyXboDMQ1U2nlbNH017dmklJCk4jVU8aA9Gpo8oHw","{{\\"assistant_caller\\":\\"comet_above_composer\\",\\"conversation_guide_session_id\\":\\"{uuid.uuid4()}\\",\\"conversation_guide_shown\\":null}}"]}}'
        self._graphql_request('7994085080671282', variables, 'useCometUFICreateCommentMutation')

    def page_review(self, id, msg: str):
        msg = msg.replace('"', '\\"')
        variables = f'{{"input":{{"composer_entry_point":"inline_composer","composer_source_surface":"page_recommendation_tab","source":"WWW","audience":{{"privacy":{{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}}}},"message":{{"ranges":[],"text":"{msg}"}},"with_tags_ids":[],"text_format_preset_id":"0","page_recommendation":{{"page_id":"{id}","rec_type":"POSITIVE"}},"actor_id":"{self.id}","client_mutation_id":"1"}},"feedLocation":"PAGE_SURFACE_RECOMMENDATIONS","feedbackSource":0,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","UFI2CommentsProvider_commentsKey":"ProfileCometReviewsTabRoute","hashtag":null,"canUserManageOffers":false}}'
        self._graphql_request('5737011653023776', variables, 'PageReviewMutation') # Tên friendly_name không có trong code gốc, tự thêm.

    def sharend(self, id, msg: str):
        msg = msg.replace('"', '\\"')
        variables = f'{{"input":{{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"{uuid.uuid4()}_FEED","source":"WWW","attachments":[{{"link":{{"share_scrape_data":"{{\\"share_type\\":22,\\"share_params\\":[{id}]}}"}}}},{{"link":{{"share_scrape_data":"{{\\"share_type\\":22,\\"share_params\\":[{id}]}}"}}}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{{"privacy":{{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}}}},"is_tracking_encrypted":true,"tracking":["AZXEWGOa5BgU9Y4vr1ZzQbWSdaLzfI3EMNtpYwO1FzzHdeHKOCyc4dd677vkeHFmNfgBKbJ7vHSB96dnQh4fQ0-dZB3zHFN1qxxhg5F_1K8RShMHcVDNADUhhRzdkG2C6nujeGpnPkw0d1krhlgwq2xFc1lM0OLqo_qr2lW9Oci9BzC3ZkT3Jqt1m8-2vpAKwqUvoSfSrma8Y5zA1x9ZF0HLeHojOeodv_w5-S9hcdgy3gvF5o4lTdzfp3leby36PkwOyJqCOI51h6jp-cH0WUubXMbH2bVM-v9Mv7kHw9_yC8dP5b_tjerx7ggHtnhr1KtOEiolPmCkQiapP5dX9phUaW908T9Kh1aDk4sK7cd7QfVaGj6LSOiHS599VsgvvbHopOVxH80a96LkuhH4t0DLc8QjljGwAmublnMVuvUbVaiChuyjzAIQe-xj2C7yMGzxmOacqR7yaepDUI-fpRZAzkcfVUdumVzbjWtCYGZLJgw4lAKVv6Y37tBedtAGHF7P7EEdQSXOX6ADg0cEYUeusp9Oho1SAbz_rVGiJc-oSkWY6S2XwD5vBXwV9lfdg6vuH3DKDcIDDoua3xXN7sYbVOw3ClcTbxMAmQqE8ClYrlbIXNp-QCW2Rr_3ro3VgYqNo1UkRyDXhCHs8rWUNY6N-bhMWCHI9CPOEebbqXnSRayKmgxYrDOIuHIzyHujUBYLnEikCYIfVwaeEB4X-Et3ZZvgoHdaZAhSO3YNFLYjyimb1tR8A-Pm2KoKwIF6equnjWWLHKoovFhbhQLRmjYYBJUhP4n0yLunWLnPwn8e7ev9h4fsGMREmonEbizxwrsr1bqpDBjHWliiPTPHDdlJNVko7anmeT1txjmTaOrA8oejbs1hDeNEZoEuL2vkN7HdjiJFhLu2yTNw2Rc3WHHOb8FcFlwTOzCDUHGDbv_bV8iAlybhEZFE-3kmoMrw7kXPjwC8D_x4VRW1BQ1wVEsYFjBrLOjk05nsuuU0X5aD5DJi3zrL3bET2eGIIlbXdXvn57Q2JtCnnS0uRyaB2pHghXTkrT2l_1fPqTJIhJOi6YQDymf2paNIUd1Fe3fDZBp1D4VMsNphQr4mSIANKGHZP29cmWJox94ztH7mrLIhSRiSzs_DrTb5o5YH6AwBkg9XzNdlM7uMxAPB9lbqVAPWXEBANhoAHvYjQI1-61myVarQBrk36dbz15PASG1c5Fina9vATWju6Bfj7PjoqJ4rARcZBJOO011e2eLy4yekMuG8bD5TvEwuiRn_M23iuC-k_w77abKvcW4MJX1f4Gfv9S4C_8N4pSiWOPNRgHPJWEQ6vhhu3euzWVSKYJ5jmfeqA9jFd_U6qVkEXenI0ofFBXw-fzjoWoRHy5y8xBG9qg",null],"message":{{"ranges":[],"text":"{msg}"}},"logging":{{"composer_session_id":"{uuid.uuid4()}"}},"navigation_data":{{"attribution_id_v2":"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,1743945123087,176702,,,"}},"event_share_metadata":{{"surface":"newsfeed"}},"actor_id":"{self.id}","client_mutation_id":"1"}},"feedLocation":"NEWSFEED","feedbackSource":1,"focusCommentID":null,"gridMediaWidth":null,"groupID":null,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":false,"renderLocation":"homepage_stream","useDefaultActor":false,"inviteShortLinkKey":null,"isFeed":true,"isFundraiser":false,"isFunFactPost":false,"isGroup":false,"isEvent":false,"isTimeline":false,"isSocialLearning":false,"isPageNewsFeed":false,"isProfileReviews":false,"isWorkSharedDraft":false,"hashtag":null,"canUserManageOffers":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":false,"__relay_internal__pv__CometIsReplyPagerDisabledrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__CometFeedPYMKHScrollInitialPaginationCountrelayprovider":10,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":true}}'
        self._graphql_request('29449903277934341', variables, 'ComposerStoryCreateMutation') # Doc_ID không khớp với tên friendly_name trong code gốc, giữ nguyên doc_id của bạn.
    
    def clickDissMiss(self):
        """Tắt thông báo spam 601...049 (Dismiss)."""
        variables = "{}"
        self._graphql_request('6339492849481770', variables, 'FBScrapingWarningMutation')

# --- CLASS TUONGTACCHEO ---

class TuongTacCheo(object):
    def __init__(self, token):
        self.ss = requests.Session()
        self.cookie = None
        self.session_data = None
        self.headers = {}
        try:
            # Sửa: Thêm timeout cho request
            session = self.ss.post('https://tuongtaccheo.com/logintoken.php', data={'access_token': token}, timeout=10)
            self.cookie = session.headers.get('Set-cookie')
            self.session_data = session.json()
            if self.cookie:
                self.headers = {
                    'Host': 'tuongtaccheo.com',
                    'accept': '*/*',
                    'origin': 'https://tuongtaccheo.com',
                    'x-requested-with': 'XMLHttpRequest',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    "cookie": self.cookie
                }
        except Exception as e:
            # print(f"Lỗi khởi tạo TTC: {e}")
            pass

    def info(self):
        # Sửa: Kiểm tra data có tồn tại và hợp lệ
        if self.session_data and self.session_data.get('status') == 'success' and 'data' in self.session_data:
            return {'status': "success", 'user': self.session_data['data'].get('user', 'N/A'), 'xu': self.session_data['data'].get('sodu', '0')}
        else:
            return {'error': 200}
        
    def cauhinh(self, id):
        if not self.headers: return {'error': 200}
        try:
            response = self.ss.post('https://tuongtaccheo.com/cauhinh/datnick.php', headers=self.headers, data={'iddat[]': id, 'loai': 'fb', }).text
            if response == '1':
                return {'status': "success", 'id': id}
            else:
                return {'error': 200}
        except Exception:
            return {'error': 500}
        
    def getjob(self, nv):
        if not self.headers: return None
        try:
            response = self.ss.get(f'https://tuongtaccheo.com/kiemtien/{nv}/getpost.php', headers=self.headers, timeout=10)
            return response
        except Exception:
            return None
    
    def nhanxu(self, id, nv):
        if not self.headers: return {'error': 'Lỗi kết nối TTC'}
        try:
            # Thử lấy xu trước (không cần thiết nhưng giữ lại logic kiểm tra)
            
            response = self.ss.post(f'https://tuongtaccheo.com/kiemtien/{nv}/nhantien.php', headers=self.headers, data={'id': id}).json()
            
            if 'mess' in response and '+' in response['mess']:
                # Lấy xu sau
                xu_sau_text = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text
                xu_match = re.search(r'"soduchinh">(\d+)<', xu_sau_text)
                xu_sau = xu_match.group(1) if xu_match else '0'

                parts = response['mess'].split()
                msg = parts[-2]
                return {'status': "success", 'msg': '+'+msg+' Xu', 'xu': xu_sau} 
            else:
                return {'error': response}
        except Exception:
            return {'error': 'Lỗi nhận xu'}

# Định nghĩa ngoại lệ tùy chỉnh để thoát khỏi vòng lặp nhiệm vụ và chuyển acc
class SwitchAccount(Exception):
    """Ngoại lệ tùy chỉnh để chuyển sang tài khoản kế tiếp."""
    pass

# --- KHU VỰC HÀM CHÍNH VÀ LUỒNG CHẠY ---

listCookie = []
list_nv = []
unicode_invisible = ("ㅤ")

def banner():
    """Hàm hiển thị banner (đã giữ lại cấu trúc nhưng nội dung gốc của bạn trống)."""
    console = Console()
    welcome_text = gradient("         *** TTC AUTO TOOL *** ")
    console.print(Panel(welcome_text, border_style="cyan", title=gradient("  DQT-TOOL  ")))
    thanhngang(50)

def addcookie():
    global listCookie
    i = 0
    print(trang + 'Bắt đầu nhập Cookie Facebook. Nhập trống để dừng.')
    while True:
        i += 1
        cookie = input(f'{thanh}{luc}Nhập Cookie Facebook Số{vang} {i}{trang}: {vang}')
        if not cookie and i != 1:
            break 
        if not cookie and i == 1:
            i -= 1
            continue

        fb = Facebook(cookie)
        info = fb.info()
        
        if isinstance(info, dict) and 'success' in info:
            name = info['name']
            print(f'{thanh}{luc}Username: {vang}{name}')
            thanhngang(50)
            listCookie.append(cookie)
        else:
            print(f'{do}Cookie Facebook Die hoặc Lỗi! Vui Lòng Nhập Lại !!!')
            i -= 1
        if i >= 1 and not cookie:
            break


def main_flow():
    """Hàm chứa luồng xử lý chính của tool."""
    global listCookie, list_nv, stt, totalxu

    os.system("cls" if os.name == "nt" else "clear")
    banner()

    # --- BƯỚC 1: XỬ LÝ TOKEN TƯƠNG TÁC CHÉO ---
    ttc = None
    checktoken = None
    token_json = []
    users = 'N/A'
    xu = '0'

    if os.path.exists(f'tokenttcfb.json'):
        try:
            with open('tokenttcfb.json','r') as f:
                token_json = json.load(f)
        except:
            token_json = []

    if not token_json:
        # Nhập token mới nếu không có
        while True:
            token = input(f'{thanh}\033[38;2;0;255;0m Nhập Access_Token TTC{trang}:{vang} ')
            print('\033[1;36mĐang Xử Lý....','     ',end='\r')
            ttc = TuongTacCheo(token)
            checktoken = ttc.info()
            if checktoken.get('status') == 'success':
                users, xu = checktoken['user'], checktoken['xu']
                print(f"{luc}Đăng Nhập Thành Công")
                token_json.append(token+'|'+users)
                with open('tokenttcfb.json','w') as f:
                    json.dump(token_json,f)
                break
            else:
                print(f'{do}Đăng Nhập Thất Bại')
    else:
        # Chọn hoặc nhập token mới
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        stt_token = 0
        valid_tokens = []
        for tokens in token_json:
            if len(tokens.split('|')) == 2:
                stt_token += 1
                print(f'{thanh}{luc}Nhập {do}[{vang}{stt_token}{do}] {luc}Để Chạy Tài Khoản: {vang}{tokens.split("|")[1]}')
                valid_tokens.append(tokens)
        token_json = valid_tokens

        print(gradient("-"*50))
        print(f'{thanh}{luc}Nhập {do}[{vang}C{do}] {luc}Chọn Acc Tương Tác Chéo Để Chạy Tool')
        print(f'{thanh}{luc}Nhập {do}[{vang}N{do}] {luc}Nhập Access_Token Tương Tác Chéo Mới')
        print(gradient("-"*50))
        
        while True:
            chon = input(f'{thanh}{luc}Nhập: {vang}').upper()
            thanhngang(50)
            if chon == 'C':
                while True:
                    try:
                        tokenttcfb = int(input(f'{thanh}{luc}Nhập Số Acc: {vang}'))
                        thanhngang(50)
                        selected_token_data = token_json[tokenttcfb - 1]
                        ttc = TuongTacCheo(selected_token_data.split("|")[0])
                        checktoken = ttc.info()
                        if checktoken.get('status') == 'success':
                            users, xu = checktoken['user'], checktoken['xu']
                            print(f"{luc}Đăng Nhập Thành Công")
                            break
                        else:
                            print(f'{do}Đăng Nhập Thất Bại')
                    except IndexError:
                        print(f'{do}Số Acc Không Tồn Tại')
                    except Exception:
                        print(f'{do}Lỗi khi chọn tài khoản.')
                break
            elif chon == 'N':
                while True:
                    token = input(f'{thanh}{luc}Nhập Access_Token TTC{trang}: {vang}')
                    print('\033[1;32mĐang Xử Lý....','     ',end='\r')
                    ttc = TuongTacCheo(token)
                    checktoken = ttc.info()
                    if checktoken.get('status') == 'success':
                        users, xu = checktoken['user'], checktoken['xu']
                        print(f"{luc}Đăng Nhập Thành Công")
                        token_json.append(token+'|'+users)
                        with open('tokenttcfb.json','w') as f:
                            json.dump(token_json,f)
                        break
                    else:
                        print(f'{do}Đăng Nhập Thất Bại')
                break
            else:
                print(f'{do}Vui Long Nhập Chính Xác (C/N)')

    # Kiểm tra lại TTC
    if not ttc or checktoken.get('status') != 'success':
        print(f'{do}Lỗi nghiêm trọng: Không thể đăng nhập vào Tương Tác Chéo.')
        sys.exit()

    # --- BƯỚC 2: XỬ LÝ COOKIE FACEBOOK ---
    os.system("cls" if os.name == "nt" else "clear")            
    banner()

    if os.path.exists(f'cookiefb-ttc.json') == False:
        addcookie()
        if listCookie:
            with open('cookiefb-ttc.json','w') as f:
                json.dump(listCookie, f)
    else:
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Sử Dụng Cookie Facebook Đã Lưu')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Cookie Facebook Mới')
        thanhngang(50)
        chon = input(f'{thanh}{luc}Nhập{trang}: {vang}')
        thanhngang(50)
        while True:
            if chon == '1':
                print(f'{luc}Đang Lấy Dữ Liệu Đã Lưu ','          ',end='\r')
                sleep(1)
                try:
                    with open('cookiefb-ttc.json', 'r') as f:
                        listCookie = json.load(f)
                except:
                    print(f'{do}Lỗi đọc file cookie, vui lòng nhập mới.')
                    addcookie()
                break
            elif chon == '2':
                addcookie()
                with open('cookiefb-ttc.json','w') as f:
                    json.dump(listCookie, f)
                break
            else:
                print(f'{do}Vui Lòng Nhập Đúng !!!')
                chon = input(f'{thanh}{luc}Nhập{trang}: {vang}')

    if not listCookie:
        print(f'{do}Không có cookie Facebook nào được nhập hoặc lưu. Thoát chương trình.')
        sys.exit()

    # --- BƯỚC 3: CẤU HÌNH NHIỆM VỤ VÀ THÔNG SỐ KHÁC ---
    os.system("cls" if os.name == "nt" else "clear")            
    banner()

    # Sửa: Đảm bảo xu là số nguyên để format
    xu_formatted = str(format(int(xu),",")) if xu.isdigit() else xu
    
    print(f'{thanh}{luc}Facebook Name{trang}: {vang}{users}')
    print(f'{thanh}{luc}Total Coin{trang}: {vang}{xu_formatted}')
    print(f'{thanh}{luc}Total Cookie Facebook{trang}: {vang}{len(listCookie)}')
    thanhngang(50)
    print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}1{do}]\033[38;2;160;231;229m Để Chạy Nhiệm Vụ Like Vip')
    print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}2{do}]\033[38;2;160;231;229m Để Chạy Nhiệm Vụ Like Thường')
    print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}3{do}]\033[38;2;160;231;229m Để Chạy Nhiệm Vụ Cảm Xúc Vip')
    print(f'{thanh}{dep}Nhập {do}[{vang}4{do}]{dep} Để Chạy Nhiệm Vụ Cảm Xúc Thường')
    print(f'{thanh}{dep}Nhập {do}[{vang}5{do}]{dep} Để Chạy Nhiệm Vụ Cảm Xúc Comment')
    print(f'{thanh}{dep}Nhập {do}[{vang}6{do}]{dep} Để Chạy Nhiệm Vụ Comment')
    print(f'{thanh}{dep}Nhập {do}[{vang}7{do}]{dep} Để Chạy Nhiệm Vụ Share')
    print(f'{thanh}{dep}Nhập {do}[{vang}8{do}]{dep} Để Chạy Nhiệm Vụ Like Page')
    print(f'{thanh}{dep}Nhập {do}[{vang}9{do}]{dep} Để Chạy Nhiệm Vụ Follow')
    print(f'{thanh}{dep}Nhập {do}[{vang}0{do}]{dep} Để Chạy Nhiệm Vụ Group')
    print(f'{thanh}{dep}Nhập {do}[{vang}q{do}]{dep} Để Chạy Nhiệm Vụ Review')
    print(f'{thanh}{dep}Nhập {do}[{vang}s{do}]{dep} Để Chạy Nhiệm Vụ Share Nội Dung')
    print(f'{thanh}{dep}Có Thể Chọn Nhiều Nhiệm Vụ {do}({vang}VD: 123...{do})')
    thanhngang(50)

    nhiemvu_raw = str(input(f'{thanh}\033[38;2;220;200;255mNhập Số Để Chọn Nhiệm Vụ{trang}: {vang}'))
    valid_options = ['1','2','3','4','5','6','7','8','9','0', 'q', 's']
    list_nv = [x for x in nhiemvu_raw if x in valid_options]
    
    if not list_nv:
        print(f'{do}Không có nhiệm vụ hợp lệ nào được chọn. Thoát chương trình.')
        sys.exit()

    while True:
        try:
            delay = int(input(f'{thanh}{v}Nhập Delay Job (giây){trang}: {vang}'))
            if delay < 0: raise ValueError
            break
        except:
            print(f'{do}Vui Lòng Nhập Số Nguyên Lớn Hơn hoặc Bằng 0')
    
    while True:
        try:
            JobbBlock = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chống Block{trang}: {vang}'))
            if JobbBlock <= 1:
                print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
                continue
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')
            
    while True:
        try:
            DelayBlock = int(input(f'{thanh}{v}Sau {vang}{JobbBlock} {v}Nhiệm Vụ Nghỉ Bao Nhiêu Giây{trang}: {vang}'))
            if DelayBlock < 0: raise ValueError
            break
        except:
            print(f'{do}Vui Lòng Nhập Số Nguyên Lớn Hơn hoặc Bằng 0')
            
    while True:
        try:
            JobBreak = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chuyển Acc{trang}: {vang}'))
            if JobBreak <= 1:
                print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
                continue
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')

    runidfb = input(f'{thanh}{v}Bạn Có Muốn Ẩn Id Facebook Không? {do}({vang}y/n{do}){v}: {vang}')
    thanhngang(50)

    # --- BƯỚC 4: VÒNG LẶP CHẠY NHIỆM VỤ ---

    stt = 0
    totalxu = 0
    list_cookie_working = listCookie.copy()
    
    while True:
        if not list_cookie_working:
            print(f'{do}Tất cả Cookie đã bị loại khỏi danh sách. Vui lòng nhập Cookie mới.')
            # Logic nhập lại cookie
            listCookie.clear()
            addcookie()
            with open('cookiefb-ttc.json','w') as f:
                json.dump(listCookie, f)
            list_cookie_working = listCookie.copy()
            if not list_cookie_working:
                print(f'{do}Không có cookie mới. Thoát chương trình.')
                break
                
        # Lặp qua từng cookie
        for cookie in list_cookie_working[:]: 
            JobSuccess, JobFail = 0, 0
            fb = Facebook(cookie)
            info = fb.info()
            
            namefb = '' 
            idfb = ''
            
            try:
                if isinstance(info, dict) and 'success' in info:
                    namefb = info['name']
                    idfb = str(info['id'])
                    idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if runidfb.upper() =='Y' else idfb
                else:
                    status = info
                    print(f'{do}Cookie {status} ({namefb if namefb else "N/A"})! Đã Xóa Ra Khỏi List !!!')
                    if cookie in list_cookie_working:
                        list_cookie_working.remove(cookie)
                    raise SwitchAccount # Dùng ngoại lệ tùy chỉnh để chuyển acc ngay lập tức

                cauhinh = ttc.cauhinh(idfb)
                if cauhinh.get('status') == 'success':
                    print(f'\n{gradient("-"*50)}\n{luc}Đang Chạy Tài Khoản: {vang}{namefb} {do}| {luc}ID: {vang}{idrun}')
                    thanhngang(50)
                else:
                    print(f'{luc}Chưa Cấu Hình Id Facebook{trang}: {vang}{idfb}{do} | {luc}Tên Tài Khoản{trang}: {vang}{namefb}')
                    if cookie in list_cookie_working:
                        list_cookie_working.remove(cookie)
                    raise SwitchAccount
                
                # --- VÒNG LẶP NHIỆM VỤ CHO TỪNG ACC ---
                
                current_nv_list = list_nv.copy()
                while current_nv_list:
                    random_nv = random.choice(current_nv_list)
                    
                    # Ánh xạ nhiệm vụ
                    mapping = {
                        '1': ('likepostvipcheo', 'LIKE'), '2': ('likepostvipre', 'LIKE'), '3': ('camxucvipcheo', 'CX'), 
                        '4': ('camxuccheo', 'CX'), '5': ('camxuccheobinhluan', 'CXCMT'), '6': ('cmtcheo', 'COMMENT'), 
                        '7': ('sharecheo', 'SHARE'), '8': ('likepagecheo', 'LIKEPAGE'), '9': ('subcheo', 'FOLLOW'), 
                        '0': ('thamgianhomcheo', 'GROUP'), 'q': ('danhgiapage', 'REVIEW'), 's': ('sharecheokemnoidung', 'SHAREND')
                    }
                    
                    fields, type_label = mapping.get(random_nv, ('', 'N/A'))
                    
                    try:
                        getjob = ttc.getjob(fields)
                        
                        # SỬA LOGIC GET JOB (an toàn hơn)
                        if getjob and getjob.status_code == 200:
                            try:
                                job_list = getjob.json()
                                if not isinstance(job_list, list) or not job_list:
                                    raise ValueError("Dữ liệu job không phải là list hợp lệ.")
                            except Exception:
                                # Nếu không phải JSON hợp lệ (ví dụ: là thông báo lỗi/countdown)
                                raise ValueError("Lỗi parse JSON hoặc không có job.")

                            print(luc+f" Đã Tìm Thấy {len(job_list)} Nhiệm Vụ {fields.upper()}                             ",end = "\r")
                            
                            for x in job_list:
                                job_data = {}
                                # Lấy ID job
                                if 'idpost' in x:
                                    job_data['id_post'] = x['idpost'].split('_')[-1]
                                    job_data['id_job_ttc'] = x['idpost']
                                elif 'UID' in x:
                                    job_data['id_post'] = x['UID'].split('_')[-1]
                                    job_data['id_job_ttc'] = x['UID']
                                elif 'idfb' in x:
                                    job_data['id_post'] = x['idfb'].split('_')[-1]
                                    job_data['id_job_ttc'] = x['idfb']
                                
                                id_post = job_data.get('id_post', 'N/A')
                                id_job_ttc = job_data.get('id_job_ttc', '')

                                # Thực hiện nhiệm vụ FB
                                if random_nv in ["1", "2"]:
                                    fb.reaction(id_post, "LIKE")
                                elif random_nv == "3":
                                    fb.reaction(id_post, x.get('loaicx', 'LOVE')) 
                                elif random_nv == "4":
                                    fb.reaction(id_post, x.get('loaicx', 'LOVE')) 
                                elif random_nv == "5":
                                    fb.reactioncmt(id_post, x.get('loaicx', 'LOVE')) 
                                elif random_nv == "6":
                                    msg = random.choice(json.loads(x.get("nd", '["Nice post!"]'))) 
                                    fb.comment(id_post, msg)
                                elif random_nv == "7":
                                    fb.share(id_post)
                                elif random_nv == "8":
                                    fb.likepage(id_post)
                                elif random_nv == "9":
                                    fb.follow(id_post)
                                elif random_nv == "0":
                                    fb.group(id_post)
                                elif random_nv == 'q':
                                    msg = random.choice(json.loads(x.get("nd", '["Good service!"]'))) 
                                    fb.page_review(id_post, msg)
                                elif random_nv == "s":
                                    msg = random.choice(json.loads(x.get("nd", '["Shared content!"]'))) 
                                    fb.sharend(id_post, msg)
                                
                                # Nhận xu
                                nhanxu = ttc.nhanxu(id_job_ttc, fields)

                                if nhanxu.get('status') == 'success':
                                    msg_xu, xu_hien_tai = nhanxu['msg'], nhanxu['xu']
                                    xutotal = msg_xu.replace(' Xu','')
                                    totalxu += int(xutotal)
                                    stt+=1
                                    JobSuccess += 1
                                    timejob = datetime.now().strftime('%H:%M:%S')
                                    
                                    print(f'{do}[ \033[1;36m{stt}{do} ] {do}[ {vang}QT-Tool{do} ][ {xanh}{timejob}{do} ][ {vang}{type_label.upper()}{do} ][ {trang}{id_post}{do} ][ {vang}{msg_xu}{do} ][ {luc}{str(format(int(xu_hien_tai),","))} {do}]')
                                    
                                    if stt % 10 == 0:
                                        xu_wrk_fmt = str(format(int(xu_hien_tai),",")) if xu_hien_tai.isdigit() else xu_hien_tai
                                        totalxu_fmt = str(format(int(totalxu),","))
                                        print(f'{trang}[{luc}Total Cookie Facebook: {vang}{len(list_cookie_working)}{trang}] [{luc}Total Coin: {vang}{totalxu_fmt}{trang}] [{luc}Tổng Xu: {vang}{xu_wrk_fmt}{trang}]')
                                    
                                    JobFail = 0 # Reset JobFail khi thành công

                                else:
                                    JobFail += 1
                                    error_msg_nhanxu = nhanxu.get("error") if isinstance(nhanxu.get("error"), str) else str(nhanxu.get("error"))
                                    print(f'{trang}[{do}{JobFail}{trang}] {trang}[{do}ERROR{trang}] {trang}{id_post} - {error_msg_nhanxu}','            ',end="\r")
                                
                                
                                # --- LOGIC CHỐNG BLOCK & CHUYỂN ACC ---
                                
                                if JobSuccess != 0 and JobSuccess % int(JobBreak) == 0:
                                    print(f'\n{vang}Đã hoàn thành {JobSuccess} nhiệm vụ. Chuyển sang tài khoản tiếp theo...')
                                    raise SwitchAccount 

                                if nhanxu.get('status') == 'success':
                                    if stt % int(JobbBlock)==0:
                                        Delay(DelayBlock)
                                    else:
                                        Delay(delay)
                                
                                if JobFail >= 20:
                                    check = fb.info()
                                    if check == 'spam':
                                        print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Spam (601...), Đang thử Dismiss.')
                                        fb.clickDissMiss()
                                    elif check in ['282', '956']:
                                        print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Checkpoint ({check}), Đã Xoá Khỏi List.')
                                        if cookie in list_cookie_working: list_cookie_working.remove(cookie)
                                        raise SwitchAccount 
                                    elif check == 'cookieout':
                                        print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Out Cookie, Đã Xoá Khỏi List.')
                                        if cookie in list_cookie_working: list_cookie_working.remove(cookie)
                                        raise SwitchAccount
                                    else:
                                        # Bị block nhiệm vụ
                                        print(do+f'Tài Khoản {vang}{namefb} {do}Đã Bị Block Nhiệm Vụ {fields.upper()}. Chuyển Nhiệm Vụ...')
                                        JobFail = 0 # Reset fail count
                                        current_nv_list.remove(random_nv) # Loại nhiệm vụ bị block ra khỏi list hiện tại
                                        if not current_nv_list:
                                            print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Block Tất Cả Tương Tác. Chuyển Acc.')
                                            if cookie in list_cookie_working: list_cookie_working.remove(cookie)
                                            raise SwitchAccount 
                                        break # Thoát vòng lặp jobs, chọn nhiệm vụ mới
                                
                        else:
                            # Trường hợp không có job hoặc lỗi từ TTC
                            error_data = getjob.json() if getjob and getjob.status_code == 200 else {}
                            error_msg = error_data.get('error', 'Lỗi kết nối/Không có phản hồi')
                            countdown = error_data.get('countdown', 0)
                            
                            if countdown > 0:
                                print(f'{do}Tiến Hành Get Job {fields.upper()}, COUNTDOWN: {str(round(countdown, 3))}         ',end="\r")
                                Delay(countdown)
                            elif "Không tìm thấy nhiệm vụ" in error_msg:
                                print(do+f'Không còn nhiệm vụ {fields.upper()} trên hệ thống. Chuyển nhiệm vụ...                             ',end="\r")
                                current_nv_list.remove(random_nv)
                                sleep(1)
                            else:
                                print(do+f'Lỗi TTC ({fields.upper()}): {error_msg}                                                 ',end="\r")
                                current_nv_list.remove(random_nv)
                                sleep(1)
                                
                            if not current_nv_list:
                                print(f'{vang}\nĐã thử hết tất cả nhiệm vụ. Chuyển sang tài khoản Facebook tiếp theo...')
                                raise SwitchAccount 
                                
                    except ValueError:
                        # Bắt lỗi parse JSON hoặc lỗi job không hợp lệ
                        print(do+f'Lỗi dữ liệu job {fields.upper()}. Chuyển nhiệm vụ...                             ',end="\r")
                        current_nv_list.remove(random_nv)
                        sleep(1)
                        if not current_nv_list:
                            print(f'{vang}\nĐã thử hết tất cả nhiệm vụ. Chuyển sang tài khoản Facebook tiếp theo...')
                            raise SwitchAccount 
                            
                    except requests.exceptions.RequestException as e:
                        # Lỗi mạng/kết nối FB
                        print(f'{do}Lỗi kết nối Facebook: {e}. Thử lại nhiệm vụ khác...')
                        current_nv_list.remove(random_nv)
                        sleep(2)
                        if not current_nv_list:
                            print(f'{vang}\nĐã thử hết tất cả nhiệm vụ. Chuyển sang tài khoản Facebook tiếp theo...')
                            raise SwitchAccount 
                    except Exception as e:
                        # Lỗi không xác định
                        # print(f'{do}Lỗi không xác định trong vòng lặp job: {e}')
                        current_nv_list.remove(random_nv)
                        sleep(1)
                        if not current_nv_list:
                            print(f'{vang}\nĐã thử hết tất cả nhiệm vụ. Chuyển sang tài khoản Facebook tiếp theo...')
                            raise SwitchAccount
                            
            except SwitchAccount:
                # Bắt ngoại lệ để chuyển sang cookie kế tiếp
                continue
            except Exception as e:
                # Bắt lỗi phát sinh khi xử lý cookie, đảm bảo không dừng chương trình
                # print(f'{do}Lỗi xử lý tài khoản: {e}. Chuyển acc...')
                if cookie in list_cookie_working: list_cookie_working.remove(cookie)
                continue

if __name__ == '__main__':
    # Sửa: Đặt stt và totalxu ở global scope trước khi gọi main_flow
    stt = 0
    totalxu = 0
    main_flow()
