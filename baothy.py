#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
import time
from datetime import datetime
import base64
import re
import uuid
import random
from bs4 import BeautifulSoup
import sys

# ==============================================================================
# SECTION: UI & COLORS (v6.6 - Auto Clear Notification)
# ==============================================================================

class UI:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;39m'
    PURPLE = '\033[38;5;135m'
    CYAN = '\033[38;5;51m'
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[38;5;255m'
    GREY = '\033[38;5;240m'
    
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    
    RAINBOW_COLORS = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 51, 45, 39, 33, 27, 57, 93, 129, 165, 201]

    @staticmethod
    def banner():
        os.system('cls' if os.name == 'nt' else 'clear')
        logo = """
██╗  ██╗       ████████╗ ██████╗  ██████╗ ██╗     
██║  ██║       ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████║█████╗    ██║   ██║   ██║██║   ██║██║     
██╔══██║╚════╝    ██║   ██║   ██║██║   ██║██║     
██║  ██║          ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
        """
        colored_logo = ""
        c_idx = 0
        for char in logo:
            if char != " " and char != "\n":
                colored_logo += f"\033[38;5;{UI.RAINBOW_COLORS[c_idx % len(UI.RAINBOW_COLORS)]}m{char}"
                c_idx += 1
            else:
                colored_logo += char
        
        print(colored_logo + UI.RESET)
        print(f"{UI.BOLD}{UI.WHITE}──────────────────────────────────────────────────────────{UI.RESET}")
        print(f"{UI.YELLOW} Author   : {UI.WHITE}Trần Văn Quang Huy")
        print(f"{UI.YELLOW} Update   : {UI.GREEN}Version 4.1{UI.RESET}")
        print(f"{UI.BOLD}{UI.WHITE}──────────────────────────────────────────────────────────{UI.RESET}\n")

    @staticmethod
    def log(name, action, message, status="INFO"):
        now = datetime.now().strftime('%H:%M:%S')
        col_time = f"{UI.GREY}[{now}]{UI.RESET}"
        
        clean_name = name.strip()[:10]
        col_name = f"{UI.CYAN}{clean_name}{UI.RESET}" 
        col_action = f"{UI.YELLOW}{action}{UI.RESET}"

        if status == "SUCCESS":
            print(f"{col_time}|{col_name}|{col_action}|{UI.GREEN}SUCCESS{UI.RESET}| {UI.WHITE}{message}{UI.RESET}")
        elif status == "ERROR":
            print(f"{col_time}|{col_name}|{col_action}|{UI.RED}ERROR{UI.RESET}| {UI.RED}{message}{UI.RESET}")
        elif status == "WARNING":
            print(f"{col_time}|{col_name}|{col_action}|{UI.ORANGE}WARNING{UI.RESET}| {UI.ORANGE}{message}{UI.RESET}")
        elif status == "INFO":
            print(f"{col_time} {UI.BLUE}➤{UI.RESET} {message}")

    @staticmethod
    def searching_led(job_name):
        text = f"Đang tìm nhiệm vụ {job_name} ......"
        
        # Chạy hiệu ứng 1 lúc
        seconds = 1.0 
        fps = 10
        total_frames = int(seconds * fps)
        
        for frame in range(total_frames):
            led_text = ""
            offset = frame 
            for i, char in enumerate(text):
                color_idx = (i + offset) % len(UI.RAINBOW_COLORS)
                color = UI.RAINBOW_COLORS[color_idx]
                led_text += f"\033[38;5;{color}m{char}"
            
            sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   ")
            sys.stdout.flush()
            time.sleep(1.0 / fps)
        
        # Kết thúc hàm nhưng KHÔNG xóa dòng chữ vội, để yên đó cho user nhìn thấy trong lúc tải
        # Chỉ đưa con trỏ về đầu dòng (\r)
        sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   \r") 

    @staticmethod
    def progress_bar(seconds, message="Đợi"):
        fps = 5  
        total_frames = int(seconds * fps)
        
        for frame in range(total_frames):
            remaining = seconds - (frame // fps)
            display_str = f"{message} {remaining}s"
            
            led_text = ""
            offset = frame 
            for i, char in enumerate(display_str):
                color_idx = (i + offset) % len(UI.RAINBOW_COLORS)
                color = UI.RAINBOW_COLORS[color_idx]
                led_text += f"\033[38;5;{color}m{char}"
            
            sys.stdout.write(f"\r  {UI.BLUE}➤{UI.RESET} {led_text}{UI.RESET}   ")
            sys.stdout.flush()
            time.sleep(1.0 / fps)
            
        sys.stdout.write("\r" + " "*50 + "\r") 

# --- Constants ---
SETTINGS_FILE = "settings.json"
ACCOUNT_FILE = "account.txt"  
COOKIE_FILE = "cookie.txt"    
REACTION_TYPES = {
    "LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858",
    "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", "ANGRY": "444813342392137"
}

URLS = {
    "login_ttc": "https://tuongtaccheo.com/login.php",
    "get_ttc_token": "https://tuongtaccheo.com/api/",
    "get_account_info": "https://tuongtaccheo.com/logintoken.php",
    "config_ttc": "https://tuongtaccheo.com/caidat/",
    "set_main_account": "https://tuongtaccheo.com/cauhinh/datnick.php",
    "jobs": {
        "reaction": [
            {"fetch": "https://tuongtaccheo.com/kiemtien/camxucvipre/getpost.php", "claim": "https://tuongtaccheo.com/kiemtien/camxucvipre/nhantien.php", "source": "camxucvipre"},
            {"fetch": "https://tuongtaccheo.com/kiemtien/camxucvipcheo/getpost.php", "claim": "https://tuongtaccheo.com/kiemtien/camxucvipcheo/nhantien.php", "source": "camxucvipcheo"}
        ],
        "likevip": {"fetch": "https://tuongtaccheo.com/kiemtien/likepostvipcheo/getpost.php", "claim": "https://tuongtaccheo.com/kiemtien/likepostvipcheo/nhantien.php", "source": "likepostvipcheo"},
        "follow": {"fetch": "https://tuongtaccheo.com/kiemtien/subcheo/getpost.php", "claim": "https://tuongtaccheo.com/kiemtien/subcheo/nhantien.php", "source": "subcheo"},
        "share": {"fetch": "https://tuongtaccheo.com/kiemtien/sharecheo/getpost.php", "claim": "https://tuongtaccheo.com/kiemtien/sharecheo/nhantien.php", "source": "sharecheo"}
    },
    "facebook_api": "https://www.facebook.com/api/graphql/"
}

class StopToolException(Exception):
    pass

# ==============================================================================
# SECTION: CORE & FACEBOOK
# ==============================================================================

def login_ttc(username, password):
    login_data = {"username": username, "password": password, "submit": "ĐĂNG NHẬP"}
    session = requests.Session()
    try:
        response = session.post(URLS["login_ttc"], data=login_data, timeout=10)
        if "success" in response.text.lower():
            return session.cookies.get_dict(), username, password
    except: pass
    return None, None, None

def get_ttc_token(cookies):
    try:
        response = requests.get(URLS["get_ttc_token"], cookies=cookies, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'ttc_access_token'})
        return token_input.get('value') if token_input else None
    except: return None

def get_current_balance_api(cookies):
    try:
        response = requests.get("https://tuongtaccheo.com/home.php", cookies=cookies, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        sodu_el = soup.find('b', id='soduchinh')
        if sodu_el:
            return int(sodu_el.text.replace(',', '').replace('.', ''))
        text_xu = re.search(r'Số dư:.*?(\d+)', response.text)
        if text_xu:
            return int(text_xu.group(1))
    except:
        pass
    return 0

def set_main_account(cookies, fb_uid):
    headers = {
        "accept": "*/*", "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://tuongtaccheo.com", "referer": "https://tuongtaccheo.com/cauhinh/facebook.php",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    data = {"iddat[]": fb_uid, "loai": "fb"}
    try:
        response = requests.post(URLS["set_main_account"], headers=headers, cookies=cookies, data=data, timeout=10)
        return response.text.strip() == "1"
    except: return False

def _fetch_jobs_from_endpoint(url, cookies):
    headers = {"X-Requested-With": "XMLHttpRequest"}
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.text in ["0", "[]", ""]: return []
        jobs = response.json()
        return [job for job in jobs if isinstance(job, dict)]
    except: return []

def get_vip_reaction_jobs(cookies):
    jobs = []
    for endpoint in URLS["jobs"]["reaction"]:
        fetched_jobs = _fetch_jobs_from_endpoint(endpoint["fetch"], cookies)
        if fetched_jobs:
            jobs.extend([{"job": job, "source": endpoint["source"]} for job in fetched_jobs])
    return jobs

def get_likevip_jobs(cookies): return [{"job": job, "source": URLS["jobs"]["likevip"]["source"]} for job in _fetch_jobs_from_endpoint(URLS["jobs"]["likevip"]["fetch"], cookies)]
def get_follow_jobs(cookies): return [{"job": job, "source": URLS["jobs"]["follow"]["source"]} for job in _fetch_jobs_from_endpoint(URLS["jobs"]["follow"]["fetch"], cookies)]
def get_share_jobs(cookies): return [{"job": job, "source": URLS["jobs"]["share"]["source"]} for job in _fetch_jobs_from_endpoint(URLS["jobs"]["share"]["fetch"], cookies)]

def _claim_ttc_reward(claim_url, cookies, data):
    headers = {
        "accept": "*/*", "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "XMLHttpRequest", "origin": "https://tuongtaccheo.com",
        "referer": claim_url.replace("nhantien.php", ""),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    try:
        response = requests.post(claim_url, headers=headers, cookies=cookies, data=data, timeout=15)
        return response.json()
    except: return None

def claim_reaction_reward(cookies, post_id, reaction_type, source):
    if source == "likepostvipcheo": claim_url = URLS["jobs"]["likevip"]["claim"]
    else: claim_url = next(endpoint["claim"] for endpoint in URLS["jobs"]["reaction"] if endpoint["source"] == source)
    return _claim_ttc_reward(claim_url, cookies, {"id": post_id, "loaicx": reaction_type})

def claim_follow_reward(cookies, target_id): return _claim_ttc_reward(URLS["jobs"]["follow"]["claim"], cookies, {"id": target_id})
def claim_share_reward(cookies, post_id): return _claim_ttc_reward(URLS["jobs"]["share"]["claim"], cookies, {"id": post_id})

class FacebookAccount:
    def __init__(self, cookie_str):
        self.cookie = cookie_str
        self.name = "Unknown"
        self.uid = None
        self.fb_dtsg = None
        self.is_valid = self._validate_and_fetch_details()

    def _validate_and_fetch_details(self):
        try:
            uid_match = re.search(r"c_user=(\d+)", self.cookie)
            if uid_match: self.uid = uid_match.group(1)
            else: return False

            headers = {
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'cookie': self.cookie,
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
            homepage_response = requests.get('https://www.facebook.com/', headers=headers, timeout=20)
            homepage_text = homepage_response.text

            if 'login.php' in str(homepage_response.url) or "Đăng nhập Facebook" in homepage_text:
                return False

            fb_dtsg_match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', homepage_text) or \
                            re.search(r'name="fb_dtsg" value="(.*?)"', homepage_text) or \
                            re.search(r'"async_get_token":"(.*?)"', homepage_text)
            
            if fb_dtsg_match: self.fb_dtsg = fb_dtsg_match.group(1)

            name_match = re.search(r'"NAME":"(.*?)"', homepage_text)
            if name_match: 
                self.name = name_match.group(1).encode('latin1').decode('unicode-escape')
            else:
                soup = BeautifulSoup(homepage_text, 'html.parser')
                title_tag = soup.find('title')
                if title_tag: self.name = title_tag.string

            return True
        except: return False

class FacebookInteractor:
    def __init__(self, fb_account: FacebookAccount):
        self.account = fb_account
        self.base_headers = {
            "accept": "*/*", "accept-language": "en-US,en;q=0.9", "content-type": "application/x-www-form-urlencoded",
            "cookie": self.account.cookie, "origin": "https://www.facebook.com", "priority": "u=1, i",
            "sec-ch-ua": '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"', "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-fb-lsd": "SaEkSywP_uH8A3cpczP2RG"
        }

    def _handle_response(self, response, job_type):
        try:
            if response.text.startswith("for (;;);"):
                error_data = json.loads(response.text[9:])
                if error_data.get("error") == 1357001:
                    UI.log(self.account.name, "API", "LOGOUT", "ERROR")
                    self.account.is_valid = False
                    raise StopToolException("Account logged out")
            return True, None
        except: return False, None

    def react_to_post(self, post_id, reaction_name):
        reaction_id = REACTION_TYPES.get(reaction_name.upper(), REACTION_TYPES["LIKE"])
        variables = {
            "input": {
                "feedback_id": base64.b64encode(f"feedback:{post_id}".encode()).decode(),
                "feedback_reaction_id": reaction_id, "feedback_source": "NEWS_FEED", "actor_id": self.account.uid, "client_mutation_id": "1"
            }
        }
        data = {
            "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg,
            "fb_api_req_friendly_name": "CometUFIFeedbackReactMutation", "variables": json.dumps(variables), "doc_id": "9518016021660044"
        }
        try:
            response = requests.post(URLS["facebook_api"], headers=self.base_headers, data=data, timeout=15)
            is_ok, _ = self._handle_response(response, "reaction")
            return is_ok
        except StopToolException: raise
        except: return False

    def follow_user(self, target_id):
        try:
            timestamp = int(time.time())
            friend_headers = self.base_headers.copy()
            friend_headers.update({'x-fb-friendly-name': 'FriendingCometFriendRequestSendMutation'})
            friend_variables = {
                "input": {"attribution_id_v2": f"ProfileCometContextualProfileRoot.react,comet.profile.contextual_profile,unexpected,{timestamp}710,151967,,,", "friend_requestee_ids": [str(target_id)], "friending_channel": "PROFILE_BUTTON", "warn_ack_for_ids": [], "actor_id": self.account.uid, "client_mutation_id": "7"}, "scale": 1
            }
            friend_data = {
                "av": self.account.uid, "__user": self.account.uid, "__a": "1", "fb_dtsg": self.account.fb_dtsg, "variables": json.dumps(friend_variables), "doc_id": "9757269034400464"
            }
            requests.post(URLS["facebook_api"], headers=friend_headers, data=friend_data, timeout=15)

            follow_headers = self.base_headers.copy()
            follow_headers.update({'x-fb-friendly-name': 'CometUserFollowMutation'})
            follow_variables = {
                "input": {"attribution_id_v2": f"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,{timestamp}313,397001,250100865708545,,", "is_tracking_encrypted": False, "subscribe_location": "PROFILE", "subscribee_id": str(target_id), "tracking": None, "actor_id": self.account.uid, "client_mutation_id": "11", "session_id": str(uuid.uuid4())}, "scale": 1
            }
            follow_data = {
                "av": self.account.uid, "__user": self.account.uid, "__a": "1", "fb_dtsg": self.account.fb_dtsg, "variables": json.dumps(follow_variables), "doc_id": "9831187040342850"
            }
            res = requests.post(URLS["facebook_api"], headers=follow_headers, data=follow_data, timeout=15)
            is_ok, _ = self._handle_response(res, "follow")
            return is_ok
        except StopToolException: raise
        except: return False

    def share_post(self, post_id):
        headers = self.base_headers.copy()
        headers.update({'x-fb-friendly-name': 'ComposerStoryCreateMutation'})
        variables = {
            "input": {"composer_entry_point": "share_modal", "composer_source_surface": "feed_story", "composer_type": "share", "idempotence_token": f"{str(uuid.uuid4())}_FEED", "source": "WWW", "attachments": [{"link": {"share_scrape_data": json.dumps({"share_type": 22, "share_params": [str(post_id)]})}}], "audience": {"privacy": {"base_state": "EVERYONE"}}, "actor_id": self.account.uid, "client_mutation_id": "7"}
        }
        data = {
            "av": self.account.uid, "__user": self.account.uid, "fb_dtsg": self.account.fb_dtsg, "variables": json.dumps(variables), "doc_id": "9502543119760740"
        }
        try:
            res = requests.post(URLS["facebook_api"], headers=headers, data=data, timeout=15)
            is_ok, _ = self._handle_response(res, "share")
            return is_ok
        except StopToolException: raise
        except: return False

# ==============================================================================
# SECTION: MAIN LOGIC
# ==============================================================================

def extract_xu(msg):
    try: return int(re.search(r'cộng (\d+)', msg).group(1))
    except: return 0

def process_job_and_return_xu(job_type, job, ttc_cookies, interactor, ttc_username, ttc_token):
    if not isinstance(job, dict) or "job" not in job: return 'ACTION_FAILED', 0
    if not interactor.account.is_valid: return 'LOGGED_OUT', 0

    actual_job = job["job"]
    job_source = job.get("source", URLS["jobs"][job_type]["source"] if job_type != "reaction" else "camxucvipcheo")
    fb_name = interactor.account.name
    job_id_ttc = actual_job.get('idpost') or actual_job.get('id')

    success = False
    details = ""
    claim_func = None
    claim_args = []

    try:
        if job_type == "reaction":
            post_id = actual_job.get('idfb') or job_id_ttc
            rtype = actual_job.get('loaicx')
            details = f"{rtype}"
            success = interactor.react_to_post(post_id, rtype)
            claim_func = claim_reaction_reward
            claim_args = [ttc_cookies, job_id_ttc, rtype, job_source]
        
        elif job_type == "follow":
            target = actual_job.get('idpost') or actual_job.get('id')
            details = f"FOLLOW"
            success = interactor.follow_user(target)
            claim_func = claim_follow_reward
            claim_args = [ttc_cookies, target]

        elif job_type == "share":
            link = actual_job.get('link', '')
            post_id = link.split('/posts/')[1].split('?')[0].strip('/') if '/posts/' in link else job_id_ttc
            details = f"SHARE"
            success = interactor.share_post(post_id)
            claim_func = claim_share_reward
            claim_args = [ttc_cookies, job_id_ttc]

        elif job_type == "likevip":
            post_id = actual_job.get('idfb') or job_id_ttc
            details = f"LIKEVIP"
            success = interactor.react_to_post(post_id, 'LIKE')
            claim_func = claim_reaction_reward
            claim_args = [ttc_cookies, job_id_ttc, 'LIKE', job_source]

        if not interactor.account.is_valid: return 'LOGGED_OUT', 0

        if success:
            time.sleep(1)
            result = claim_func(*claim_args)

            if result and isinstance(result, dict):
                if result.get('mess'):
                    xu_earned = extract_xu(result.get('mess'))
                    current_balance_api = int(result.get('sodu', 0)) if result.get('sodu') else 0
                    return 'SUCCESS', xu_earned
                    
                elif "nick chính" in str(result):
                    UI.log(fb_name, "CONFIG", "Cấu hình lại...", "WARNING")
                    set_main_account(ttc_cookies, interactor.account.uid)
                    return 'RETRY', 0
                else:
                    UI.log(fb_name, details, f"Lỗi: {result}", "ERROR")
                    return 'ACTION_FAILED', 0
            return 'ACTION_FAILED', 0
        else:
            UI.log(fb_name, details, "FB Block/Lỗi", "ERROR")
            return 'ACTION_FAILED', 0

    except StopToolException as e:
        if str(e) == "Account logged out": return 'LOGGED_OUT', 0
        raise
    except: return 'ACTION_FAILED', 0

def main():
    UI.banner()

    # 1. LOGIN TTC & ACCOUNT SELECTION
    print(f"{UI.BG_GREEN}{UI.WHITE} CHỌN TÀI KHOẢN TUONGTACCHEO {UI.RESET}")
    
    saved_accounts = []
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, 'r') as f:
            for line in f:
                if '|' in line:
                    saved_accounts.append(line.strip().split('|'))

    valid_ttc_accounts = []
    
    if saved_accounts:
        print(f"Đang kiểm tra {len(saved_accounts)} tài khoản lưu trong máy...")
        for idx, (u, p) in enumerate(saved_accounts):
            ck, _, _ = login_ttc(u, p)
            if ck:
                bal = get_current_balance_api(ck)
                token = get_ttc_token(ck)
                valid_ttc_accounts.append({'u': u, 'p': p, 'ck': ck, 'tk': token, 'bal': bal})
    
    # Menu Selection
    chosen_account = None
    
    if valid_ttc_accounts:
        for i, acc in enumerate(valid_ttc_accounts):
            print(f"[{i+1}] {UI.CYAN}{acc['u']}{UI.RESET} | Xu: {UI.YELLOW}{acc['bal']}{UI.RESET}")
        
        print(f"[{len(valid_ttc_accounts)+1}] {UI.GREEN}Đăng nhập tài khoản mới{UI.RESET}")
        
        while True:
            try:
                choice = int(input(f"\n{UI.YELLOW}Nhập số thứ tự để chạy: {UI.RESET}"))
                if 1 <= choice <= len(valid_ttc_accounts):
                    chosen_account = valid_ttc_accounts[choice-1]
                    break
                elif choice == len(valid_ttc_accounts) + 1:
                    break
                else:
                    print("Lựa chọn không hợp lệ.")
            except: print("Vui lòng nhập số.")
            
    if not chosen_account:
        print("\nNhập thông tin tài khoản TTC mới:")
        u = input("Username: "); p = input("Password: ")
        ck, _, _ = login_ttc(u, p)
        if ck:
            bal = get_current_balance_api(ck)
            token = get_ttc_token(ck)
            chosen_account = {'u': u, 'p': p, 'ck': ck, 'tk': token, 'bal': bal}
            
            is_exist = False
            for acc in saved_accounts:
                if acc[0] == u: is_exist = True
            
            if not is_exist:
                with open(ACCOUNT_FILE, 'a') as f: f.write(f"\n{u}|{p}")
        else:
            print("Đăng nhập thất bại."); return

    ttc_u = chosen_account['u']
    ttc_ck = chosen_account['ck']
    ttc_tk = chosen_account['tk']
    total_balance = chosen_account['bal']

    print(f"\n{UI.GREEN}Đã chọn: {ttc_u} (Xu: {total_balance}){UI.RESET}")

    # 2. CONFIG
    global settings
    print(f"\n{UI.BG_GREEN}{UI.WHITE} CẤU HÌNH TOOL {UI.RESET}")
    
    try:
        delay_min = int(input(f"{UI.YELLOW}Delay Min (giây): {UI.RESET}"))
        delay_max = int(input(f"{UI.YELLOW}Delay Max (giây): {UI.RESET}"))
        
        jobs_break = int(input(f"{UI.YELLOW}Chạy xong bao nhiêu job thì nghỉ: {UI.RESET}"))
        time_break = int(input(f"{UI.YELLOW}Thời gian nghỉ (giây): {UI.RESET}"))
        
        job_switch = int(input(f"{UI.YELLOW}Bao nhiêu job đổi acc: {UI.RESET}"))
        max_job = int(input(f"{UI.YELLOW}Bao nhiêu job thì dừng acc (0=full): {UI.RESET}"))
        
        settings = {
            'DELAY_BETWEEN_JOBS': (delay_min, delay_max),
            'JOBS_BEFORE_BREAK': jobs_break,
            'BREAK_TIME': time_break,
            'JOBS_BEFORE_SWITCH': job_switch,
            'MAX_JOBS_PER_ACC': max_job
        }
    except ValueError:
        print(f"{UI.RED}Nhập sai! Dùng mặc định.{UI.RESET}")
        settings = {
            'DELAY_BETWEEN_JOBS': (5, 10),
            'JOBS_BEFORE_BREAK': 20,
            'BREAK_TIME': 60,
            'JOBS_BEFORE_SWITCH': 100,
            'MAX_JOBS_PER_ACC': 0
        }

    # 3. COOKIES
    print(f"\n{UI.BG_GREEN}{UI.WHITE} NHẬP COOKIE FACEBOOK {UI.RESET}")
    raw_cookies = []
    if input("1: Dán | 2: File cookie.txt : ") == '2':
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE) as f: raw_cookies = [l.strip() for l in f if l.strip()]
    else:
        print("Dán cookie (Enter dòng trống để chạy):")
        while True:
            c = input(); 
            if not c: break
            raw_cookies.append(c.strip())

    # 4. CHECK LIVE
    valid_accs = []
    print(f"\n{UI.BOLD}Đang kiểm tra cookie...{UI.RESET}")
    for i, c in enumerate(raw_cookies):
        acc = FacebookAccount(c)
        if acc.is_valid:
            valid_accs.append(acc)
            print(f"[{i+1}] {UI.GREEN}LIVE{UI.RESET} | {acc.name} | {acc.uid}")
        else:
            print(f"[{i+1}] {UI.RED}DIE {UI.RESET}")
    
    if not valid_accs: return

    # 5. SELECT JOBS
    print(f"\n{UI.BG_GREEN}{UI.WHITE} CHỌN JOB {UI.RESET}")
    print("1. Reaction  2. Follow  3. Share  4. LikeVIP")
    c = input("Chọn (vd 1+2): ")
    jmap = {"1": "reaction", "2": "follow", "3": "share", "4": "likevip"}
    selected_jobs = [jmap[x] for x in c.split('+') if x in jmap] or list(jmap.values())

    # 6. RUN
    UI.banner()
    print(f" {UI.BG_GREEN}{UI.WHITE} Chạy {len(valid_accs)} acc Facebook với TTC: {ttc_u} {UI.RESET}\n")
    print(f"{UI.YELLOW}Số dư ban đầu: {UI.GREEN}{total_balance} xu{UI.RESET}\n")

    acc_job_counters = {acc.uid: 0 for acc in valid_accs} 
    session_job_counter = 0
    acc_idx = 0
    blocked_jobs = {acc.uid: set() for acc in valid_accs}

    while True:
        try:
            curr_acc = valid_accs[acc_idx % len(valid_accs)]
            
            if not curr_acc.is_valid:
                valid_accs.remove(curr_acc)
                if not valid_accs: print("Hết acc."); break
                continue

            set_main_account(ttc_ck, curr_acc.uid)
            interactor = FacebookInteractor(curr_acc)
            
            avail_jobs = [j for j in selected_jobs if j not in blocked_jobs[curr_acc.uid]]
            if not avail_jobs:
                acc_idx += 1; continue

            jtype = random.choice(avail_jobs)
            fetcher = globals()[f"get_{'vip_' if jtype == 'reaction' else ''}{jtype}_jobs"]
            
            try:
                # 1. HIỆN TEXT TÌM JOB LED
                UI.searching_led(jtype.upper())
                
                # 2. TẢI JOB (TEXT VẪN CÒN ĐÓ)
                jobs = fetcher(ttc_ck)
                
                # 3. XÓA SẠCH DÒNG TEXT "ĐANG TÌM"
                sys.stdout.write("\r" + " "*80 + "\r")
                sys.stdout.flush()
                
                if jobs:
                    print(f"  {UI.GREEN}➤ Tìm thấy {len(jobs)} nhiệm vụ. Đang cày...{UI.RESET}")
                    
                    for job in jobs:
                        # Check limits
                        if settings['MAX_JOBS_PER_ACC'] > 0 and acc_job_counters[curr_acc.uid] >= settings['MAX_JOBS_PER_ACC']:
                            UI.log(curr_acc.name, "STOP", f"Đã xong {settings['MAX_JOBS_PER_ACC']} jobs.", "WARNING")
                            valid_accs.remove(curr_acc)
                            break 

                        if acc_job_counters[curr_acc.uid] > 0 and acc_job_counters[curr_acc.uid] % settings['JOBS_BEFORE_SWITCH'] == 0:
                            UI.log(curr_acc.name, "SWITCH", f"Đổi acc...", "INFO")
                            acc_idx += 1
                            break 

                        if session_job_counter > 0 and session_job_counter % settings['JOBS_BEFORE_BREAK'] == 0:
                            print(f"\n{UI.YELLOW}Đã làm {settings['JOBS_BEFORE_BREAK']} jobs. Nghỉ ngơi...{UI.RESET}")
                            UI.progress_bar(settings['BREAK_TIME'], "Nghỉ")
                            session_job_counter = 0 

                        status, earned = process_job_and_return_xu(jtype, job, ttc_ck, interactor, ttc_u, ttc_tk)
                        
                        if status == 'SUCCESS': 
                            total_balance += earned
                            acc_job_counters[curr_acc.uid] += 1
                            session_job_counter += 1
                            
                            details = f"{jtype.upper()}"
                            UI.log(curr_acc.name, details, f"+{earned} xu | {UI.YELLOW}{total_balance} xu{UI.RESET}", "SUCCESS")

                            delay = random.randint(settings['DELAY_BETWEEN_JOBS'][0], settings['DELAY_BETWEEN_JOBS'][1])
                            UI.progress_bar(delay, "Chờ")

                        elif status == 'LOGGED_OUT': 
                            curr_acc.is_valid = False
                            break 
                        elif status == 'ACTION_FAILED':
                             pass 
                    
                    if not valid_accs: print("Done."); break
                    
                else:
                    time.sleep(2) 

            except Exception as e:
                pass

        except KeyboardInterrupt: break
        except Exception: pass

if __name__ == "__main__":
    main()
