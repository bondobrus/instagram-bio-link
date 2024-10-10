import requests
import json
import re
import random
import time
import string
import uuid

class InstagramAuth:

    def __init__(self):
        self.phone_data = {
            'samsung': {
                'SM-G965F': {'resolution': '1440x2960', 'android_version': '26', 'model_code': 'SM-G965F', 'hardware_platform': 'star2lte', 'processor': 'samsungexynos9810'},
                'SM-G960F': {'resolution': '1440x2960', 'android_version': '26', 'model_code': 'SM-G960F', 'hardware_platform': 'starlte', 'processor': 'samsungexynos9810'},
                'SM-G973F': {'resolution': '1440x3040', 'android_version': '28', 'model_code': 'SM-G973F', 'hardware_platform': 'beyond1', 'processor': 'samsungexynos9820'},
                'SM-G980F': {'resolution': '1440x3200', 'android_version': '29', 'model_code': 'SM-G980F', 'hardware_platform': 'Wobble', 'processor': 'samsungexynos990'}
            }
        }
        self.ig_device_id = self.generate_ig_device_id()
        self.ig_android_id = self.generate_ig_android_id()
        self.user_agent = self.generate_user_agent()
        self.x_mid = self.generate_random_string(28)

    def generate_user_agent(self):
        phone_brand = random.choice(list(self.phone_data.keys()))
        phone_model, phone_specs = random.choice(list(self.phone_data[phone_brand].items()))

        resolution = phone_specs['resolution']
        android_version = phone_specs['android_version']
        model_code = phone_specs['model_code']
        hardware_platform = phone_specs['hardware_platform']
        processor = phone_specs['processor']

        static_part = 'Instagram 309.1.0.41.113 Android'
        user_agent = f"{static_part} ({android_version}/9; 480dpi; {resolution}; {phone_brand}; {model_code}; {hardware_platform}; {processor}; pl_PL; 541635897)"
        return user_agent

    def generate_ig_device_id(self):
        return str(uuid.uuid4())

    def generate_ig_android_id(self):
        return 'android-%x' % random.randrange(1 << 64)

    def generate_random_string(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def generate_phone_id(self):
        return str(uuid.uuid4())

    def generate_android_id(self):
        random_id = ''.join(random.choice(string.hexdigits) for _ in range(16))
        return 'android-' + random_id

    def get_login_data(self, proxy, username, encrypted_password):
        
        headers = {
            'x-ig-app-locale': 'en_US',
            'x-ig-device-locale': 'en_US',
            'x-ig-mapped-locale': 'en_US',
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': '0',
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.ig_device_id,
            'x-ig-android-id': self.ig_android_id,
            'x-ig-timezone-offset': '7200',
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427',
            'priority': 'u=3',
            'user-agent': self.user_agent,
            'accept-language': 'en-US',
            'x-mid': self.x_mid,
            'ig-intended-user-id': '0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        data = {
            'params': json.dumps({
                "client_input_params": {
                    "device_id": self.ig_device_id,
                    "sim_phones": [],
                    "login_attempt_count": 1,
                    "secure_family_device_id": "",
                    "machine_id": self.x_mid,
                    "accounts_list": [],
                    "auth_secure_device_id": "",
                    "has_whatsapp_installed": 0,
                    "password": encrypted_password,
                    "sso_token_map_json_string": "",
                    "fb_ig_device_id": [],
                    "device_emails": [],
                    "try_num": 1,
                    "lois_settings": {
                        "lois_token": "",
                        "lara_override": ""
                    },
                    "event_flow": "login_manual",
                    "event_step": "home_page",
                    "headers_infra_flow_id": "",
                    "openid_tokens": {},
                    "client_known_key_hash": "",
                    "contact_point": username,
                    "encrypted_msisdn": ""
                },
                "server_params": {
                    "should_trigger_override_login_2fa_action": 0,
                    "is_from_logged_out": 0,
                    "should_trigger_override_login_success_action": 0,
                    "login_credential_type": "none",
                    "server_login_source": "login",
                    "waterfall_id": None,
                    "login_source": "Login",
                    "is_platform_login": 0,
                    "offline_experiment_group": None,
                    "is_from_landing_page": 0,
                    "is_from_empty_password": 0,
                    "ar_event_source": "login_home_page",
                    "username_text_input_id": "bu5hmb:65",
                    "layered_homepage_experiment_group": None,
                    "should_show_nested_nta_from_aymh": 1,
                    "device_id": None,
                    "reg_flow_source": "login_home_native_integration_point",
                    "is_caa_perf_enabled": 1,
                    "credential_type": "password",
                    "is_from_password_entry_page": 0,
                    "caller": "gslr",
                    "family_device_id": None,
                    "INTERNAL_INFRA_THEME": "harm_f",
                    "is_from_assistive_id": 0,
                    "access_flow_version": "LEGACY_FLOW",
                    "is_from_logged_in_switcher": 0
                }
            }),
            'bk_client_context': json.dumps({
                "bloks_version": "9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a",
                "styles_id": "instagram"
            }),
            'bloks_versioning_id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
        }

        proxies = {"http": proxy, "https": proxy} if proxy != "no_proxy" else None
        response = requests.post(
            'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',
            headers=headers,
            data=data,
            proxies=proxies,
        )
        time.sleep(random.randint(5, 10))

        if 'Please wait a few minutes before you try again' in response.text:
            print('Instagram error: Please wait a few minutes before you try again.')
            exit(1)

        response_json = response.json()
        response_str = json.dumps(response_json)

        result = {}
        context_data = None

        # Find pk_id
        matches_pk = re.findall(r'(pk_id.{40})', response_str)
        for match in matches_pk:
            cleaned_match = match.replace('\\', '')
            result["pk_id"] = cleaned_match[8:-2]
            break  # Return after first match

        # Find IG-Set-Authorization
        matches_auth = re.findall(r'(IG-Set-Authorization.{0,350}?)",', response_str)
        for match in matches_auth:
            cleaned_match = match.replace('\\', '')
            result["IG-Set-Authorization"] = cleaned_match[24:]
            break  # Return after first match

        # Find x-ig-set-www-claim
        matches_auth = re.findall(r'(x-ig-set-www-claim.{0,350}?)",', response_str)
        for match in matches_auth:
            cleaned_match = match.replace('\\', '')
            result["x-ig-set-www-claim"] = cleaned_match[22:]
            break  # Return after first match

        # Find uuid
        matches_uuid = re.findall(r'(uuid.{0,250}?)",', response_str)
        for match in matches_uuid:
            cleaned_match = match.replace('\\', '')
            result["uuid"] = cleaned_match[8:]
            break  # Return after first match

        # Find x-mid
        matches_uuid = re.findall(r'(IG-Set-X-MID.{0,260}?)",', response_str)
        for match in matches_uuid:
            cleaned_match = match.replace('\\', '')
            result["IG-Set-X-MID"] = cleaned_match[16:]
            break  # Return after first match

        # Find X_IG_SALT_IDS
        matches_salt_ids = re.findall(r'(X_IG_SALT_IDS.{0,260}?)",', response_str)
        for match in matches_salt_ids:
            cleaned_match = match.replace('\\', '')
            result["X_IG_SALT_IDS"] = cleaned_match[15:]
            break  # Return after first match

        if "pk_id" not in result:
            pattern = re.compile(r'\(([^)]*aplc[^)]*)\)')
            matches = pattern.findall(response_str)

            if matches:
                for match in matches:
                    inner_pattern = re.compile(r'"([^"]*?)"')
                    inner_matches = inner_pattern.findall(match)
                    if inner_matches:
                        context_data = inner_matches[0]
                        context_data = context_data.replace("\\\\", "")
                        if context_data.endswith("\\"):
                            context_data = context_data[:-1]
                        break
            else:
                print("Could not find value with aplc (context_data).")
                print(response_str)

        return result, context_data

    def handle_two_step_verification_entrypoint_async_challenge(self, context_data):
        
        """
        Method for handling the two-step verification entrypoint async challenge.

        :param context_data: The context data returned from get_login_data.
        :return: The context data needed for the handle_two_step_verification_code_entry method.
        """
        headers = {
            'x-ig-app-locale': 'pl_PL',
            'x-ig-device-locale': 'pl_PL',
            'x-ig-mapped-locale': 'pl_PL',
            'x-pigeon-rawclienttime': '1727968334.640',
            'x-ig-bandwidth-speed-kbps': '-1.000',
            'x-ig-bandwidth-totalbytes-b': '0',
            'x-ig-bandwidth-totaltime-ms': '0',
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': '0',
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.ig_device_id,
            'x-ig-android-id': self.ig_android_id,
            'x-ig-timezone-offset': '7200',
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427',
            'priority': 'u=3',
            'user-agent': self.user_agent,
        }

        data = {
            'params': json.dumps({
                "client_input_params": {
                    "auth_secure_device_id": "",
                    "has_whatsapp_installed": 0,
                },
                "server_params": {
                    "context_data": (
                        context_data
                    ),
                    "device_id": self.ig_device_id,
                    "INTERNAL_INFRA_THEME": "harm_f,default,harm_f"
                }
            }),
            'bk_client_context': json.dumps({
                "bloks_version": "9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a",
                "styles_id": "instagram"
            }),
            'bloks_versioning_id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
        }

        response = requests.post(
            'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.ap.two_step_verification.entrypoint_async/',
            headers=headers,
            data=data,
        )

        time.sleep(random.randint(3, 6))

        response_json = response.json()

        print(f'Sent data: {data}')

        response_str = json.dumps(response_json)

        pattern = re.compile(r'\(([^)]*aplc[^)]*)\)')
        matches = pattern.findall(response_str)

        if matches:
            if len(matches) > 1:
                match = matches[1]
            else:
                match = matches[0]

            inner_pattern = re.compile(r'"([^"]*?)"')
            inner_matches = inner_pattern.findall(match)
            if inner_matches:
                context_data = inner_matches[0]
                print(f'Found value in handle_two_step_verification_entrypoint_async_challenge response: {context_data}')
                
                handle_two_step_verification_entrypoint_async_challenge_context_data = context_data
                
                handle_two_step_verification_entrypoint_async_challenge_context_data = handle_two_step_verification_entrypoint_async_challenge_context_data.replace("\\\\", "")
                if handle_two_step_verification_entrypoint_async_challenge_context_data.endswith("\\"):
                    handle_two_step_verification_entrypoint_async_challenge_context_data = handle_two_step_verification_entrypoint_async_challenge_context_data[:-1]
        else:
            print("No matches found.")
            #print(response_str)

        return handle_two_step_verification_entrypoint_async_challenge_context_data

    def handle_two_step_verification_code_entry(self, handle_two_step_verification_entrypoint_async_challenge_context_data):

        """
        Method for handling the two-step verification code entry.

        :param handle_two_step_verification_entrypoint_async_challenge_context_data: The context data returned from handle_two_step_verification_entrypoint_async_challenge.
        :return: The context data needed for the handle_two_step_verification_code_entry_async method.
        """
        headers = {
            'x-ig-app-locale': 'pl_PL',
            'x-ig-device-locale': 'pl_PL',
            'x-ig-mapped-locale': 'pl_PL',
            'x-pigeon-rawclienttime': '1727990979.776',
            'x-ig-bandwidth-speed-kbps': '-1.000',
            'x-ig-bandwidth-totalbytes-b': '0',
            'x-ig-bandwidth-totaltime-ms': '0',
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': '0',
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.ig_device_id,
            'x-ig-android-id': self.ig_android_id,
            'x-ig-timezone-offset': '7200',
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427',
            'priority': 'u=3',
            'user-agent': self.user_agent,
            'accept-language': 'en-US',
            'x-mid': self.x_mid,
            'ig-intended-user-id': '0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        data = {
            'params': json.dumps({
                "server_params": {
                    "context_data": handle_two_step_verification_entrypoint_async_challenge_context_data,
                    "INTERNAL_INFRA_THEME": "harm_f,default,default,harm_f",
                    "INTERNAL_INFRA_screen_id": "generic_code_entry"
                }
            }),
            'bk_client_context': json.dumps({
                "bloks_version": "9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a",
                "styles_id": "instagram"
            }),
            'bloks_versioning_id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
        }

        response = requests.post(
            'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.ap.two_step_verification.code_entry/',
            headers=headers,
            data=data,
        )

        time.sleep(random.randint(3, 6))

        response_json = response.json()

        print(f'Sent data: {data}')

        response_str = json.dumps(response_json)

        pattern = re.compile(r'\(([^)]*aplc[^)]*)\)')
        matches = pattern.findall(response_str)

        if matches:
            if len(matches) > 12:
                match = matches[6]
            else:
                match = matches[0]

            inner_pattern = re.compile(r'"([^"]*?)"')
            inner_matches = inner_pattern.findall(match)
            if inner_matches:
                context_data = inner_matches[0]
                print(f'Found value in handle_two_step_verification_code_entry response: {context_data}')
                
                handle_two_step_verification_code_entry = context_data
                
                handle_two_step_verification_code_entry = handle_two_step_verification_code_entry.replace("\\\\", "")
                if handle_two_step_verification_code_entry.endswith("\\"):
                    handle_two_step_verification_code_entry = handle_two_step_verification_code_entry[:-1]
        else:
            print("No value found in handle_two_step_verification_code_entry response.")
            #print(response_str)

        return handle_two_step_verification_code_entry

    def two_step_verification_code_entry_async(self, handle_two_step_verification_code_entry, verification_code):

        """
        Method for handling the two-step verification code entry asynchronously.

        :param handle_two_step_verification_code_entry: The context data returned from handle_two_step_verification_code_entry.
        :param verification_code: The verification code entered by the user.
        :return: The response object from the POST request. If the code is invalid, returns "invalid_code".
        """
        headers = {
            'x-ig-app-locale': 'pl_PL',
            'x-ig-device-locale': 'pl_PL',
            'x-ig-mapped-locale': 'pl_PL',
            'x-pigeon-rawclienttime': '1727990984.907',
            'x-ig-bandwidth-speed-kbps': '-1.000',
            'x-ig-bandwidth-totalbytes-b': '0',
            'x-ig-bandwidth-totaltime-ms': '0',
            'x-bloks-version-id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
            'x-ig-www-claim': '0',
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': self.ig_device_id,
            'x-ig-android-id': self.ig_android_id,
            'x-ig-timezone-offset': '7200',
            'x-fb-connection-type': 'WIFI',
            'x-ig-connection-type': 'WIFI',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': '567067343352427',
            'priority': 'u=3',
            'user-agent': self.user_agent,
            'accept-language': 'en-US',
            'x-mid': self.x_mid,
            'ig-intended-user-id': '0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True',
        }

        data = {
            'params': json.dumps({
                "client_input_params": {
                    "auth_secure_device_id": "",
                    "code": verification_code,
                },
                "server_params": {
                    "context_data": handle_two_step_verification_code_entry,
                    "INTERNAL__latency_qpl_marker_id": 36707139,
                    "INTERNAL__latency_qpl_instance_id": 1.76643131400167E14,
                    "INTERNAL_INFRA_THEME": "harm_f,default,default,harm_f"
                }
            }),
            'bk_client_context': json.dumps({
                "bloks_version": "9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a",
                "styles_id": "instagram"
            }),
            'bloks_versioning_id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
        }

        response = requests.post(
            'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.ap.two_step_verification.code_entry_async/',
            headers=headers,
            data=data,
        )

        print(f'Response from two_step_verification_code_entry_async: {response.text}')

        if "Error during code validation" in response.text:
            return "invalid_code"
        
        return response

    def check_proxy_ip(self, proxy):
        expected_ip = proxy.split('@')[1].split(':')[0]
        try:
            response = requests.get('https://api.ipify.org?format=json', proxies={"http": proxy, "https": proxy}, timeout=5)
            returned_ip = response.json()['ip']
            if returned_ip == expected_ip:
                print("IP matches the expected IP.")
                return True
            else:
                print("IP does not match the expected IP.")
                return False
        except Exception as e:
            print(f"Error checking proxy IP: {e}")
            return False