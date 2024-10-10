import requests
import time
import random
import datetime
import logging
import sys
from colorama import Fore, Style
import uuid
import json
from urllib.parse import quote
from requests.exceptions import ConnectTimeout


def log_message(message, username, config_file_name, progress=None):
    if progress is not None:
        logging.info(f"{Fore.YELLOW}{config_file_name}{Style.RESET_ALL} - [{progress}] {message} {username}")
    else:
        logging.info(f"{Fore.YELLOW}{config_file_name}{Style.RESET_ALL} - {message} {username}")


class InstagramUser:
    def __init__(self, account_data, users, logger):
        self.logger = logger
        self.account_data = account_data
        self.users = {user['id']: user for user in users}
        self.headers = {
            'user-agent': self.account_data['data']['user_agent'],
            'authorization': self.account_data['data']['IG-Set-Authorization'],
        }
        self.data = {
            'user-agent': self.account_data['data']['user_agent'],
            '_uuid': self.account_data['data']['uuid'],
            'ig_device_id': self.account_data['data']['ig_device_id'],
            'phone_id': self.account_data['data']['phone_id'],
            'ig_android_id': self.account_data['data']['ig_android_id'],
            'x-mid': self.account_data['data']['IG-Set-X-MID'],
            'id': self.account_data['data']['id'],
            'x-ig-set-www-claim': self.account_data['data']['x-ig-set-www-claim'],
            'X_IG_SALT_IDS': self.account_data['data']['X_IG_SALT_IDS'],
        }
        self.proxy = self.account_data['data']['proxy']
        self.previous_response_headers_get_check_frienship_status = None  # New attribute to store the previous response headers
        self.previous_response_headers_get_follow_user = None  # New attribute to store the previous response headers
        self.session_id = self.generate_uuid("UFS-", "-1")  # New attribute to store the session ID

    def generate_uuid(self, prefix: str = "", suffix: str = "") -> str:
            """
            Helper to generate uuids

            Returns
            -------
            str
                A stringified UUID
            """
            return f"{prefix}{uuid.uuid4()}{suffix}"

    def post_add_bio_link(self, bio_link):
        headers = {
            'x-ig-app-locale': 'en_US',
            'x-ig-device-locale': 'en_US',
            'x-ig-mapped-locale': 'en_US',
            'x-pigeon-session-id': self.session_id,
            "X-Pigeon-Rawclienttime": str(round(time.time(), 3)),
            "X-IG-Bandwidth-Speed-KBPS": str(
                random.randint(2500000, 3000000) / 1000
            ),  # "-1.000"
            "X-IG-Bandwidth-TotalBytes-B": str(
                random.randint(5000000, 90000000)
            ),  # "0"
            "X-IG-Bandwidth-TotalTime-MS": str(random.randint(2000, 9000)),  # "0"
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': self.account_data['data']['x-ig-set-www-claim'],
            'x-bloks-is-prism-enabled': 'true',
            'x-bloks-prism-button-version': '0',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.account_data['data']['ig_device_id'],
            'x-ig-family-device-id': self.account_data['data']['phone_id'],
            'x-ig-android-id': self.account_data['data']['ig_android_id'],
            'x-ig-timezone-offset': '7200',
            'x-ig-nav-chain': 'SelfFragment:self_profile:2:main_profile:1726069399.503::,ProfileMediaTabFragment:self_profile:3:button:1726069400.305::,EditProfileFragment:edit_profile:5:button:1726069405.124::,EditLinksListFragment:edit_links_list_fragment:6:button:1726069406.428::,MultipleLinksEditFragment:multiple_links_edit:7:button:1726069407.144::',
            'x-ig-salt-ids': self.account_data['data']['X_IG_SALT_IDS'],
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427', 
            'priority': 'u=3',
            'user-agent': self.account_data['data']['user_agent'],
            'accept-language': 'en-US',
            'authorization': self.account_data['data']['IG-Set-Authorization'],
            'x-mid': self.account_data['data']['IG-Set-X-MID'],
            'ig-u-ds-user-id': self.account_data['data']['id'],
            'ig-u-rur': self.previous_response_headers_get_follow_user.get('ig-set-ig-u-rur', '') if self.previous_response_headers_get_follow_user else '',
            'ig-intended-user-id': self.account_data['data']['id'],
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        signed_body = {
            "updated_links": json.dumps([{"url": bio_link, "title": "", "link_type": "external"}]),
            "_uid": self.account_data['data']['id'],
            "_uuid": self.account_data['data']['ig_device_id']
        }

        data = {
            "signed_body": f"SIGNATURE.{json.dumps(signed_body)}"
        }

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None

        max_attempts = 100
        for attempt in range(max_attempts):
            try:
                response = requests.post(f'https://i.instagram.com/api/v1/accounts/update_bio_links/', headers=headers, data=data, proxies=proxies)

                if response.status_code == 400 or response.status_code == 401 or response.status_code == 429 or response.status_code == 403:
                    print(f"Encountered error: {response.status_code}. Response: {response.text}")
                    self.logger.error(f"Encountered error: {response.status_code}. Response: {response.text}")
                    sys.exit(1)
                
                time.sleep(random.uniform(5, 10))

                response_json = response.json()
                self.logger.debug(f'Response: {response_json}')
                if response_json.get('status') == 'ok' and 'bio_links' in response_json['user']:
                    return 'added'
                else:
                    return 'failed'

            except (ConnectTimeout, requests.exceptions.ProxyError) as e:
                if attempt < max_attempts - 1:  # if this is not the last attempt
                    print(f"{type(e).__name__} occurred. Waiting 60 seconds before retrying. Attempt {attempt+1} of {max_attempts}")
                    time.sleep(60)
                    continue
                else:
                    print(f"{type(e).__name__} occurred. Reached maximum attempts ({max_attempts}). Exiting.")
                    sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                self.logger.debug(f"An error occurred: {e}")
                time.sleep(60)

    def post_get_links_data(self, user_id):
        """
        Post a request to get the links data of a user.

        :param user_id: The user ID.
        :return: A list of link IDs.
        """
        headers = {
            'x-ig-app-locale': 'en_US',
            'x-ig-device-locale': 'en_US',
            'x-ig-mapped-locale': 'en_US',
            'x-pigeon-session-id': self.session_id,
            "X-Pigeon-Rawclienttime": str(round(time.time(), 3)),
            "X-IG-Bandwidth-Speed-KBPS": str(
                random.randint(2500000, 3000000) / 1000
            ),  # "-1.000"
            "X-IG-Bandwidth-TotalBytes-B": str(
                random.randint(5000000, 90000000)
            ),  # "0"
            "X-IG-Bandwidth-TotalTime-MS": str(random.randint(2000, 9000)),  # "0"
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': self.account_data['data']['x-ig-set-www-claim'],
            'x-bloks-is-prism-enabled': 'true',
            'x-bloks-prism-button-version': '0',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.account_data['data']['ig_device_id'],
            'x-ig-family-device-id': self.account_data['data']['phone_id'],
            'x-ig-android-id': self.account_data['data']['ig_android_id'],
            'x-ig-timezone-offset': '7200',
            'x-ig-nav-chain': 'SelfFragment:self_profile:2:main_profile:1726069399.503::,ProfileMediaTabFragment:self_profile:3:button:1726069400.305::,EditProfileFragment:edit_profile:5:button:1726069405.124::,EditLinksListFragment:edit_links_list_fragment:6:button:1726069406.428::,MultipleLinksEditFragment:multiple_links_edit:7:button:1726069407.144::',
            'x-ig-salt-ids': self.account_data['data']['X_IG_SALT_IDS'],
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427', 
            'priority': 'u=3',
            'user-agent': self.account_data['data']['user_agent'],
            'accept-language': 'en-US',
            'authorization': self.account_data['data']['IG-Set-Authorization'],
            'x-mid': self.account_data['data']['IG-Set-X-MID'],
            'ig-u-ds-user-id': self.account_data['data']['id'],
            'ig-u-rur': self.previous_response_headers_get_follow_user.get('ig-set-ig-u-rur', '') if self.previous_response_headers_get_follow_user else '',
            'ig-intended-user-id': self.account_data['data']['id'],
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        params = {
            'is_prefetch': 'false',
            'entry_point': 'self_profile',
            'from_module': 'self_profile',
        }

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None

        response = requests.get(f'https://i.instagram.com/api/v1/users/{user_id}/info/', params=params, headers=headers, proxies=proxies)
        
        time.sleep(5)

        if response.status_code == 200:
            response_json = response.json()
            bio_links = response_json.get('user', {}).get('bio_links', [])
            link_ids = [link['link_id'] for link in bio_links]
            return link_ids
        else:
            self.logger.error(f"Failed to get links data: {response.status_code} - {response.text}")
            return []

    def remove_bio_links(self, link_ids):
        """Removes bio links from the user's profile.

        Args:
            link_ids (list): List of link IDs to remove.

        Returns:
            str: "all_links_removed" if all links were removed successfully, or "link_not_removed" if any links were not removed.
        """
        headers = {
            'x-ig-app-locale': 'en_US',
            'x-ig-device-locale': 'en_US',
            'x-ig-mapped-locale': 'en_US',
            'x-pigeon-session-id': self.session_id,
            "X-Pigeon-Rawclienttime": str(round(time.time(), 3)),
            "X-IG-Bandwidth-Speed-KBPS": str(
                random.randint(2500000, 3000000) / 1000
            ),  # "-1.000"
            "X-IG-Bandwidth-TotalBytes-B": str(
                random.randint(5000000, 90000000)
            ),  # "0"
            "X-IG-Bandwidth-TotalTime-MS": str(random.randint(2000, 9000)),  # "0"
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': self.account_data['data']['x-ig-set-www-claim'],
            'x-bloks-is-prism-enabled': 'true',
            'x-bloks-prism-button-version': '0',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.account_data['data']['ig_device_id'],
            'x-ig-family-device-id': self.account_data['data']['phone_id'],
            'x-ig-android-id': self.account_data['data']['ig_android_id'],
            'x-ig-timezone-offset': '7200',
            'x-ig-nav-chain': 'SelfFragment:self_profile:2:main_profile:1726069399.503::,ProfileMediaTabFragment:self_profile:3:button:1726069400.305::,EditProfileFragment:edit_profile:5:button:1726069405.124::,EditLinksListFragment:edit_links_list_fragment:6:button:1726069406.428::,MultipleLinksEditFragment:multiple_links_edit:7:button:1726069407.144::',
            'x-ig-salt-ids': self.account_data['data']['X_IG_SALT_IDS'],
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427', 
            'priority': 'u=3',
            'user-agent': self.account_data['data']['user_agent'],
            'accept-language': 'en-US',
            'authorization': self.account_data['data']['IG-Set-Authorization'],
            'x-mid': self.account_data['data']['IG-Set-X-MID'],
            'ig-u-ds-user-id': self.account_data['data']['id'],
            'ig-u-rur': self.previous_response_headers_get_follow_user.get('ig-set-ig-u-rur', '') if self.previous_response_headers_get_follow_user else '',
            'ig-intended-user-id': self.account_data['data']['id'],
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None

        for link_id in link_ids:
            data = {
                'signed_body': f'SIGNATURE.{{"_uid":"{self.account_data["data"]["id"]}","_uuid":"{self.account_data["data"]["ig_device_id"]}","link_ids":["{link_id}"]}}',
            }

            response = requests.post('https://i.instagram.com/api/v1/accounts/remove_bio_links/', headers=headers, data=data, proxies=proxies)

            time.sleep(5)

            if response.status_code == 200:
                self.logger.info(f"Link {link_id} removed successfully")
            else:
                self.logger.error(f"Failed to remove link {link_id}: {response.status_code} - {response.text}")
                return "link_not_removed"

        return "all_links_removed"

    def send_telegram_notification(self, message):
        bot_token = 'replace_with_your_bot_token' # REPLACE WITH YOUR BOT TOKEN
        chat_id = 'replace_with_your_chat_id' # REPLACE WITH YOUR CHAT ID
        full_message = f"Account: {self.account_data['account']}- {quote(message)}"
        full_message = full_message.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={full_message}'

        try:
            response = requests.get(send_text)
            response.raise_for_status()  # This will raise an exception if the status code is not 200
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred while sending Telegram notification: {http_err}')
            print(f'Response: {response.text}')
        except Exception as err:
            print(f'Other error occurred while sending Telegram notification: {err}')
            print(f'Response: {response.text}')
        else:
            return response.json()

    def test_proxy(self):
        if self.proxy == "no_proxy":
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: No proxy is being used.")
            return

        proxies = {"http": self.proxy, "https": self.proxy}
        response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
        proxy_ip = self.proxy.split('@')[1].split(':')[0]
        if response.json()['ip'] != proxy_ip:
            print(f"Expected Proxy IP: {proxy_ip}")
            print(f"Actual Proxy IP: {response.json()['ip']}")
            raise Exception(f'Proxy IP does not match: {response.text}')
        else:
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Proxy IP matches.")