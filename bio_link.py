import datetime
import logging
import os
import uuid
import json
from src import user
from colorama import Fore, Style

session_id = 'UFS-' + str(uuid.uuid4()) + '-0'

def setup_logger(config_file_name):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    account_log_dir = os.path.join(log_dir, config_file_name)
    if not os.path.exists(account_log_dir):
        os.makedirs(account_log_dir)

    log_file = os.path.join(account_log_dir, f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

    # Set up logger with filename to debug level to log_file
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s: %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console = logging.StreamHandler()
    # Set up console logger to info level
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def log_message(message, username, config_file_name, progress=None):
    if progress is not None:
        logging.info(f"{Fore.YELLOW}{config_file_name}{Style.RESET_ALL} - [{progress}] {message} {username}")
    else:
        logging.info(f"{Fore.YELLOW}{config_file_name}{Style.RESET_ALL} - {message} {username}")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_dir('accounts')

console_width = os.get_terminal_size().columns
print('-' * console_width)

def choose_account():
    config_files = [f for f in os.listdir('accounts') if f.endswith('.json')]
    if not config_files:
        print("There's no config file in 'accounts'.")
        return None, None

    for i, file in enumerate(config_files):
        print(f'{i + 1}. {file}')

    print('-' * console_width)

    file_num = int(input("Select account: ")) - 1
    config_file = config_files[file_num]

    with open(f'accounts/{config_file}', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config_file_name = config_file.split('.')[0]  # Get the file name without the extension
    setup_logger(config_file_name)  # Setup the logger with the config file name
    log_message(f"Selected account: {config_file_name}", "", config_file_name)
    log_message(f'Bio link: {config["bio_link"]}', "", config_file_name)

    return config, config_file_name

def main():
    account_data, config_file_name = choose_account()
    config_file_name = config_file_name.split('.')[0]  # Get the file name without the extension

    while True:
        proceed = input("Do you want to continue? (yes/no): ")
        if proceed.lower() == 'yes':
            break
        elif proceed.lower() == 'no':
            print("Exiting the program.")
            return
        else:
            print("Please enter either 'yes' or 'no'.")

    if account_data:
        bio_link = account_data['bio_link']

    # Create an instance of the InstagramUser class and test the proxy
    user_instagram = user.InstagramUser(account_data, [], logging)
    user_instagram.test_proxy()

    result = user_instagram.post_add_bio_link(bio_link)
            
    if result == 'added':
        log_message("Successfully added bio link.", "", config_file_name)
    elif result == 'failed':
        log_message("Failed to add bio link.", "", config_file_name)

if __name__ == '__main__':
    main()
