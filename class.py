# module python
import requests
import os
import sys
import time
import json
import re
import base64
import random
from urllib.parse import urlparse
from typing import Dict, Union, List, Optional, Tuple
from bs4 import BeautifulSoup

class Colors:
    DASAR = '\x1b[0m'
    TEBAL = '\x1b[1m'
    GARIS = '\x1b[4m'
    GERAK = '\x1b[5m'
    # Warna Teks
    MERAH = '\x1b[31;1m'
    HIJAU = '\x1b[32;1m'
    KUNING = '\x1b[33;1m'
    BIRU = '\x1b[34;1m'
    UNGU = '\x1b[35;1m'
    CYAN = '\x1b[36;1m'
    PUTIH = '\x1b[37;1m'
    # Warna Background
    BG_M = '\x1b[41;1m'
    BG_H = '\x1b[42;1m'
    BG_K = '\x1b[43;1m'
    BG_B = '\x1b[44;1m'
    BG_U = '\x1b[45;1m'
    BG_C = '\x1b[46;1m'
    BG_P = '\x1b[47;1m'

DATA_FILE = 'data.json'

class Requests:
  @staticmethod
  def curl(url, method='GET', data=None, headers=None, cookies_file='cookie.txt'):
    while True:
      session = requests.Session()
      try:
        with open(cookies_file, 'r') as f:
          cookies = {}
          for line in f.readlines():
            name, value = line.strip().split('=')
            cookies[name] = value
            session.cookies.update(cookies)
      except FileNotFoundError:
        pass
      try:
        if method.upper() == 'GET':
          response = session.get(url, headers=headers)
        elif method.upper() == 'POST':
          response = session.post(url, data=data, headers=headers)
        else:
          raise ValueError('Metode tidak didukung')
          response.raise_for_status()
      except requests.exceptions.RequestException as e:
        print(f"Koneksi terputus Mencoba lagi...")
        time.sleep(5)
        continue
      with open(cookies_file, 'w') as f:
        for cookie in session.cookies.items():
          f.write(f"{cookie[0]}={cookie[1]}\n")
      return response.text
class Display:
    @staticmethod
    def menu(no: Union[int, str], name: str) -> None:
        print(f'{Colors.PUTIH}[{Colors.KUNING}{no}{Colors.PUTIH}] {Colors.PUTIH}{name}')
    @staticmethod
    def succes(msg: str) -> None:
        print(f'{Colors.PUTIH}[{Colors.HIJAU}✓{Colors.PUTIH}] {Colors.HIJAU}{msg}{Colors.DASAR}')
    @staticmethod
    def error(msg: str) -> None:
        print(f'{Colors.PUTIH}[{Colors.MERAH}!{Colors.PUTIH}] {Colors.MERAH}{msg}{Colors.DASAR}')
    @staticmethod
    def title(name: str, length: int = 44, pad_char: str = " ") -> None:
        padded_name = name.center(length, pad_char)
        print(f'{Colors.BG_B}{Colors.PUTIH}{padded_name}{Colors.DASAR}')
    @staticmethod
    def line(length: int = 44) -> None:
        print(f'{Colors.CYAN}-'*length)
class Functions:
    @staticmethod
    def setConfig(key: str, value: Optional[str] = None) -> str:
        config = {}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                config = {}
        if value is None:
            if key in config:
                return config[key]
            value = input(f'--[>] Input {key}: ')
        config[key] = value
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            Display.error(f"Gagal menyimpan konfigurasi: {e}")
        return value
    @staticmethod
    def menu_api() -> Tuple[str, str]:
        Display.menu(1, 'Multibot')
        Display.menu(2, 'Xevil')
        Display.line()
        options = {
            1: {"host": "api.multibot.in", "apikey": "apikey-multibot"},
            2: {"host": "api.sctg.xyz", "apikey": "apikey-xevil"}
        }
        while True:
            try:
                cap = int(input(f'{Colors.HIJAU}--Input Number: {Colors.PUTIH}'))
                if cap in options:
                    break
                Display.error('Pilihan tidak valid. Silakan coba lagi.')
            except ValueError:
                Display.error('Input harus angka. Silakan coba lagi.')
        host = options[cap]["host"]
        api_key = Functions.setConfig(options[cap]["apikey"])
        return host, api_key
    @staticmethod
    def Tmr(tmr: int) -> None:
        while tmr > 0:
            mins, secs = divmod(tmr, 60)
            timeformat = f'\033[1;97m\033[1;93m•\033[1;97m Wait \033[1;92m{mins:02d}:{secs:02d}'
            print(f"{timeformat}", end='\r')
            time.sleep(1)
            tmr -= 1
        print(" " * 30, end='\r')  # Clear line
    @staticmethod
    def prosesBypasIcon(icontoken,host,h):
      if icontoken:
        while True:
          amjad = IconBypass(host,h)
          icon = amjad.icon_bypass(icontoken)
          if not icon:
            print(f'\r{Colors.PUTIH}--[{Colors.MERAH}!{Colors.PUTIH}] Bypas Gagal !\r',end='')
            time.sleep(2)
            continue
          print(f'\r{Colors.PUTIH}--[{Colors.HIJAU}✓{Colors.PUTIH}] Bypas Succes\r',end='')
          time.sleep(2)
          return icon
class Captcha:
    @staticmethod
    def get_in(data: Dict) -> str:
        url = f'http://{HOST_CAP}/in.php?'
        params = {'key': API_CAP}
        params.update(data)
        try:
            res = requests.get(url, params=params, timeout=30).json()
            return res.get('request', '')
        except (requests.RequestException, json.JSONDecodeError) as e:
            Display.error(f"Gagal mendapatkan captcha ID: {e}")
            raise

    @staticmethod
    def get_res(api_id: str) -> Dict:
        url = f'http://{HOST_CAP}/res.php?key={API_CAP}&json=1&id={api_id}'
        try:
            res = requests.get(url, timeout=30)
            return res.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            Display.error(f"Gagal mendapatkan hasil captcha: {e}")
            return {'request': 'ERROR', 'error': str(e)}

    @staticmethod
    def Filter(method: str) -> str:
        method_map = {
            'userrecaptcha': 'RecaptchaV2',
            'hcaptcha': 'Hcaptcha',
            'turnstile': 'Turnstile'
        }
        return method_map.get(method, method)

    @staticmethod
    def getResult(data: Dict) -> str:
        method_value = data.get('method', '')
        cap_type = Captcha.Filter(method_value)
        max_attempts = 60
        try:
            captcha_id = Captcha.get_in(data)
            for _ in range(max_attempts):
                res = Captcha.get_res(captcha_id)
                if res.get('request') == 'CAPCHA_NOT_READY':
                    print(f"\rBaypas {cap_type}", end='')
                    time.sleep(1)
                    continue
                if res.get('request') == 'ERROR':
                    raise Exception(res.get('error', 'Unknown error'))
                Display.succes(f'Baypas {cap_type} sukses')
                time.sleep(2)
                print(" " * 30, end='\r')  # Clear line
                return res.get('request', '')
            raise Exception("Captcha tidak selesai dalam waktu yang ditentukan")
        except Exception as e:
            Display.error(f"Gagal bypass captcha: {e}")
            raise

    @staticmethod
    def Recaptchav2(sitekey: str, pageurl: str) -> str:
        data = {
            'method': 'userrecaptcha',
            'sitekey': sitekey,
            'pageurl': pageurl,
            'json': 1
        }
        return Captcha.getResult(data)

    @staticmethod
    def Hcaptcha(sitekey: str, pageurl: str) -> str:
        data = {
            'method': 'hcaptcha',
            'sitekey': sitekey,
            'pageurl': pageurl,
            'json': 1
        }
        return Captcha.getResult(data)

    @staticmethod
    def Turnstile(sitekey: str, pageurl: str) -> str:
        data = {
            'method': 'turnstile',
            'sitekey': sitekey,
            'pageurl': pageurl,
            'json': 1
        }
        return Captcha.getResult(data)
class HtmlScrap:
    def __init__(self):
        self._captcha_pattern = re.compile(r'class=["\']([^"\']+)["\'][^>]*data-sitekey=["\']([^"\']+)["\'][^>]*>')
        self._input_pattern = re.compile(r'<input[^>]*name=["\'](.*?)["\'][^>]*value=["\'](.*?)["\'][^>]*>')
        self._limit_pattern = re.compile(r'(\d{1,})\/(\d{1,})')
        self._security_patterns = {
            'cloudflare': re.compile(r'Just a moment...'),
            'firewall': re.compile(r'Firewall'),
            'locked': re.compile(r'Locked')
        }

    def _scrap(self, pattern: re.Pattern, html: str) -> List[Tuple[str, ...]]:
        return pattern.findall(html)

    def get_captcha(self, html: str) -> Dict[str, str]:
        matches = self._scrap(self._captcha_pattern, html)
        return {match[0]: match[1] for match in matches}

    def get_inputs(self, html: str, form_index: int = 1) -> Dict[str, str]:
        forms = html.split('<form')
        if len(forms) <= form_index:
            return {}
        form_content = forms[form_index]
        matches = self._scrap(self._input_pattern, form_content)
        return {name: value for name, value in matches}

    def get_limits(self, html: str) -> List[Tuple[str, str]]:
        return self._scrap(self._limit_pattern, html)

    def check_security(self, html: str) -> Dict[str, bool]:
        return {name: bool(pattern.search(html)) for name, pattern in self._security_patterns.items()}

    def parse_responses(self, html: str) -> Dict[str, Union[str, bool, None]]:
        result = {
            'success': None,
            'warning': None,
            'unset': False,
            'exit': False
        }
        if 'icon: \'success\',' in html:
            success_part = html.split("icon: 'success',")[1]
            if "html: '" in success_part:
                success_msg = success_part.split("html: '")[1].split("'")[0]
                result['success'] = re.sub('<[^<]+?>', '', success_msg)
            return result
        warning_msg = None
        if 'html: \'' in html:
            warning_msg = html.split("html: '")[1].split("'")[0]
        error_conditions = [
            ('<div class="alert text-center alert-danger"><i class="fas fa-exclamation-circle"></i> Your account', 
             lambda: html.split('Your account')[1].split('</div>')[0], True),
            ('invalid amount', "You are sending an invalid amount", True),
            ('Shortlink in order to claim from the faucet!', warning_msg, True),
            ('sufficient funds', "Sufficient funds", True)
        ]
        for condition, message, exit_flag in error_conditions:
            if condition in html:
                result['warning'] = message() if callable(message) else message
                result['exit'] = exit_flag
                return result
        result['warning'] = warning_msg or "Not Found"
        return result

    def get_title(self, html: str) -> str:
        title_parts = html.split('<title>')
        if len(title_parts) > 1:
            return title_parts[1].split('</title>')[0]
        return ""

    def scrape_all(self, html: str, form_index: int = 1) -> Dict[str, Union[str, bool, Dict, List]]:
        return {
            'title': self.get_title(html),
            **self.check_security(html),
            'captcha': self.get_captcha(html),
            'input': self.get_inputs(html, form_index) or self.get_inputs(html, 2),
            'faucet': self.get_limits(html),
            'response': self.parse_responses(html)
        }

    @staticmethod
    def bs_get_forms(html: str) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        soup = BeautifulSoup(html, 'html.parser')
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get').upper(),
                'inputs': {}
            }
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                if name:
                    form_data['inputs'][name] = input_tag.get('value', '')
            forms.append(form_data)
        return forms

    @staticmethod
    def bs_get_links(html: str, base_url: str = '') -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url and not href.startswith(('http://', 'https://')):
                href = base_url + href
            links.append({
                'text': a.get_text(strip=True),
                'href': href
            })
        return links
class IconBypass:
  def __init__(self, host, headers):
    self.host = host
    self.headers = headers
  def widget_id(self):
    import uuid
    return str(uuid.uuid4())
  def msg(self, text, j=10):
    symbols = ['-', '/', '|', '\\']
    for i in range(j, 0, -1):
      for n, s in enumerate(symbols):
        print(f" [{s}] {text} {'➤' * n}", end='\r')
        time.sleep(0.1)
    print(" " * 30, end='\r')
  def icon_bypass(self, token):
    try:
        # Persiapan header
        icon_header = self.headers.copy()
        icon_header.update({
            'origin': self.host,
            'x-iconcaptcha-token': token,
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded'
        })

        # --- STEP 1: LOAD CAPTCHA ---
        self.msg("Loading captcha", 3)
        timestamp = int(time.time() * 1000)
        widget_id = self.widget_id()
        payload = {
            "widgetId": widget_id,
            "action": "LOAD",
            "theme": "light",
            "token": token,
            "timestamp": timestamp,
            "initTimestamp": timestamp - 2000
        }
        
        # Encode payload
        data = {
            "payload": base64.b64encode(
                json.dumps(payload).encode('utf-8')
            ).decode('utf-8')
        }
        
        # Kirim request
        response = Requests.curl(
            self.host + "icaptcha/req",
            method='POST',
            headers=icon_header,
            data=data
        )
        
        # Handle response
        try:
            decoded = base64.b64decode(response).decode('utf-8')
            response_data = json.loads(decoded)
        except:
            print("Invalid response format:", response.text[:200])
            return None

        if 'identifier' not in response_data:
            print("No identifier in response")
            return None

        challenge_id = response_data['identifier']
        
        # --- STEP 2: SEND SELECTION ---
        self.msg("Solving captcha", 3)
        timestamp = int(time.time() * 1000)
        payload = {
            "widgetId": widget_id,
            "challengeId": challenge_id,
            "action": "SELECTION",
            "x": random.randint(150, 170),  # Koordinat acak di area tengah
            "y": random.randint(20, 30),
            "width": 320,
            "token": token,
            "timestamp": timestamp,
            "initTimestamp": timestamp - 2000
        }
        
        data = {
            "payload": base64.b64encode(
                json.dumps(payload).encode('utf-8')
            ).decode('utf-8')
        }
        
        response = Requests.curl(
            self.host + "icaptcha/req",
            method='POST',
            headers=icon_header,
            data=data
        )
        
        try:
            decoded = base64.b64decode(response).decode('utf-8')
            response_data = json.loads(decoded)
        except:
            print("Invalid response format:", response.text[:200])
            return None

        if not response_data.get('completed', False):
            return None

        # --- STEP 3: RETURN RESULT ---
        return {
            "captcha": "icaptcha",
            "_iconcaptcha-token": token,
            "ic-rq": 1,
            "ic-wid": payload["widgetId"],
            "ic-cid": challenge_id,
            "ic-hp": '',
            "human_move": 1
        }

    except Exception as e:
        print(f"Error in bypass: {str(e)}")
        return None