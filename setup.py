import json
import os,sys

def get_user_input():
    config = []
    BOT_TOKEN = input("Enter your bot api token: ")
    CHAT_ID = input("Enter your desired chat id: ")
    init_info = {'BOT_TOKEN': BOT_TOKEN,
                 'CHAT_ID': CHAT_ID}
    config.append(init_info)
    while True:
        server = {}
        server["remote_server_ip"] = input("Enter the remote server IP (or 'done' to finish adding server): ")
        if server["remote_server_ip"].lower() == "done":
            break
        
        server["remote_username"] = input("Enter the remote username: ")
        server["remote_password"] = input("Enter the remote password: ")
        
        files = []
        num_paths = int(input("Enter the number of files/folders you want to backup from this server: "))
        for i in range(1, num_paths + 1):
            path_key = f"path{i}"
            path = input(f"Enter the file path for {path_key}: ")
            caption = input(f"Enter the file caption for {path_key}: ")
            file = {'path': path,
                    'caption': caption}
            files.append(file)
        
        server["files"] = files
        config.append(server)

    # Save the configuration to config.json
    config_location = str(os.path.dirname(os.path.abspath(__file__))) + "/config.json"
    with open(config_location, "w") as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__" and os.isatty(sys.stdout.fileno()):
    get_user_input()
