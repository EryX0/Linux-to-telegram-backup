import paramiko
import os
import zipfile
import json
from telegram.ext import Application
import asyncio
import shutil

async def sendFiles(chat_id,local_file_path ,local_file_name, caption) -> None:
    # send document to chat
    app = Application.builder().token(file_json[0]['BOT_TOKEN']).build()
    file = open(local_file_path, 'rb')
    try : await app.bot.send_document(chat_id=chat_id,document=file, filename=local_file_name, caption=caption)
    except Exception as error: 
        print(error)
        await app.bot.send_message(chat_id=chat_id, text=f"Couldn't send the file with caption : {caption}")

def download_remote_file(sftp_client, remote_path, local_path):
    try:
        remote_path = remote_path.replace("\\", "/")  # Convert backslashes to forward slashes

        if sftp_client.stat(remote_path).st_mode & 0o040000:  # Check if it's a directory
            # Download the entire directory
            os.makedirs(local_path, exist_ok=True)  # Create the local folder if it doesn't exist

            for item in sftp_client.listdir(remote_path):
                item_remote_path = os.path.join(remote_path, item)
                item_local_path = os.path.join(local_path, item)
                download_remote_file(sftp_client, item_remote_path, item_local_path)
        else:
            # Download individual file
            sftp_client.get(remote_path, local_path)  # local_path is now a full file path, including the filename
    except FileNotFoundError as e:
        print(f"Error: Remote file/folder not found - {remote_path}")
        print(f"Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")


def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, relative_path)

def get_file_from_remote_server(chat_id,remote_server_ip, remote_username, remote_password, remote_file_path, local_file_name, caption):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(remote_server_ip, username=remote_username, password=remote_password)

        sftp_client = ssh_client.open_sftp()

        # Get the directory where the code file is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the local folder name
        local_folder_name = "temp"

        # Create the local folder if it doesn't exist
        local_folder_path = os.path.join(current_directory, local_folder_name)
        os.makedirs(local_folder_path, exist_ok=True)

        local_file_path = os.path.join(local_folder_path, local_file_name)

        # Download the remote file or folder
        download_remote_file(sftp_client, remote_file_path, local_file_path)

        # Zip the directory if it was a folder
        if sftp_client.stat(remote_file_path).st_mode & 0o040000:  # Check if it's a directory
            zip_file_name = local_file_name + '.zip'
            zip_file_path = os.path.join(local_folder_path, zip_file_name)
            zip_directory(local_file_path, zip_file_path)
            asyncio.run(sendFiles(chat_id,zip_file_path ,zip_file_name, caption))
        
        else: 
            asyncio.run(sendFiles(chat_id,local_file_path ,local_file_name, caption))

        sftp_client.close()
        ssh_client.close()

        print(f"File(s) downloaded successfully to {local_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
config_location = str(os.path.dirname(os.path.abspath(__file__))) + "/config.json"
file = open(config_location, "r")
file_json = json.load(file)
chat_id = file_json[0]['CHAT_ID']
for i in file_json:
    try:
        remote_server_ip = i['remote_server_ip']
        remote_username = i['remote_username']
        remote_password = i['remote_password']
        
        for j in i['files']:
            remote_file_path = j['path']  # Use forward slashes for the remote path
            local_file_name = os.path.basename(remote_file_path)
            file_caption = j['caption']
            get_file_from_remote_server(chat_id,remote_server_ip, remote_username, remote_password, remote_file_path, local_file_name, file_caption)
    except Exception as error: 
        print(error)
        continue

#Cleanup the TEMP FOLDER

tmpfolder = str(os.path.dirname(os.path.abspath(__file__))) + "/temp"
for filename in os.listdir(tmpfolder):
    file_path = os.path.join(tmpfolder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        print(f"Successfully deleted {filename} from temp folder")
    except Exception as e:
        print('Failed to delete %s. Reason: %s, please delete the file manually from ./temp folder' % (file_path, e))

print("all operations done succesfully")
