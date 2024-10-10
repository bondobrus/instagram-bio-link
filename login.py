import json
import os
import random
from src.password import PasswordMixin
from src.authentication import InstagramAuth
import logging

logging.basicConfig(level=logging.DEBUG)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_dir('accounts')

proxy = "no_proxy"

while True:
    use_proxy = input("Use proxy? (yes/no): ")
    if use_proxy.lower() == "yes":
        proxy_input = input("Proxy input in ip:port:username:password format: ")
        ip, port, username, password = proxy_input.split(":")
        proxy = f"http://{username}:{password}@{ip}:{port}"
        auth = InstagramAuth()
        if not auth.check_proxy_ip(proxy):
            print("Proxy IP check failed.")
            exit(1)
        proxies = {"http": proxy, "https": proxy}
        break
    elif use_proxy.lower() == "no":
        proxies = None
        break
    else:
        print("Incorrect input.")

username = input("Instagram username: ")
password_input = input("Instagram password: ")

# Initialize classes
auth = InstagramAuth()
password_mixin = PasswordMixin()

# Get public keys for password encryption
publickeyid, publickey = password_mixin.password_publickeys(proxy)

# Encrypt the password
encrypted_password = password_mixin.password_encrypt(password_input, publickeyid, publickey)

# Get login data
result, context_data = auth.get_login_data(proxy, username, encrypted_password)

# Generate X_IG_SALT_IDS if not present in result
if "X_IG_SALT_IDS" not in result:
    result["X_IG_SALT_IDS"] = str(random.randint(1061162222, 1061262222))

# Process response
if "pk_id" in result:
    print("Login successful!")
    
    # Save account data to JSON file
    account_data = {
        "account": username,
        "bio_link": None,
        "data": {
            "IG-Set-Authorization": result.get("IG-Set-Authorization"),
            "x-ig-set-www-claim": result.get("x-ig-set-www-claim"),
            "uuid": result.get("uuid"),
            "IG-Set-X-MID": result.get("IG-Set-X-MID"),
            "ig_device_id": auth.ig_device_id,
            "phone_id": auth.generate_phone_id(),
            "ig_android_id": auth.ig_android_id,
            "id": result.get("pk_id"),
            "proxy": proxy,
            "user_agent": auth.user_agent,
            "X_IG_SALT_IDS": result.get("X_IG_SALT_IDS")
        }
    }
    
    with open(f'accounts/{username}.json', 'w') as json_file:
        json.dump(account_data, json_file, indent=4)

    print(f"Account data saved to accounts/{username}.json")
else:
    print("Login failed. Checking for challenge.")
    if context_data:
        handle_two_step_verification_entrypoint_async_challenge_context_data = auth.handle_two_step_verification_entrypoint_async_challenge(context_data)
        handle_two_step_verification_code_entry_context_data = auth.handle_two_step_verification_code_entry(handle_two_step_verification_entrypoint_async_challenge_context_data)
        
        while True:
            verification_code = input("Please enter the verification code: ")
            response = auth.two_step_verification_code_entry_async(handle_two_step_verification_code_entry_context_data, verification_code)
            
            if response == "invalid_code":
                print("Invalid code. Please try again.")
            else:
                print("Verification successful!")
                
                # Save account data to JSON file after verification
                account_data = {
                    "account": username,
                    "bio_link": None,
                    "data": {
                        "IG-Set-Authorization": result.get("IG-Set-Authorization"),
                        "x-ig-set-www-claim": result.get("x-ig-set-www-claim"),
                        "uuid": result.get("uuid"),
                        "IG-Set-X-MID": result.get("IG-Set-X-MID"),
                        "ig_device_id": auth.ig_device_id,
                        "phone_id": auth.generate_phone_id(),
                        "ig_android_id": auth.ig_android_id,
                        "id": result.get("pk_id"),
                        "proxy": proxy,
                        "user_agent": auth.user_agent,
                        "X_IG_SALT_IDS": result.get("X_IG_SALT_IDS")
                    }
                }
                
                with open(f'accounts/{username}.json', 'w') as json_file:
                    json.dump(account_data, json_file, indent=4)
                
                print(f"Account data saved to accounts/{username}.json.")
                break

    else:
        print("No context data found for two-step verification.")