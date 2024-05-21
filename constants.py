import socket
import threading
import sys
import time
import hashlib
import json
import subprocess

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = "!DISCONNECT"
REQUEST = "!REQUEST"
PEER_BYTE_DIFFERENTIATOR = b'\x11'
CHAIN_BYTE_DIFFERENTIATOR = b'\x12'

def get_public_ip():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
    finally:
        temp_socket.close()
    return local_ip

def get_lan_ip():
    output = subprocess.check_output("ipconfig")
    # print(type(output))
    convert = output.decode("utf-8")
    # print(type(convert))
    # print(output)
    # print("\n \n \n")
    # print(convert)
    data = convert.split("\r\n\r\n")
    # print(data)
    ipaddress = ""
    flag = False
    for i in range(len(data)):
        if flag:
            break
        if data[i] == "Wireless LAN adapter Wi-Fi:":
            # print(data[i+1])
            datas = data[i+1].replace("\r\n","")
            subdata = datas.split("  ")
            # print("\n \n \n")
            # print(subdata)
            for i in subdata:
                if "IPv4" in i:
                    ipaddress = i.split(':')[1].strip()
                    # print(f"found {i}")
                    flag = True
                    # print(f"ipaddress is : {ipaddress}")
                    break
    return ipaddress

try:
    HOST = get_public_ip()
except:
    HOST = get_lan_ip()
    if HOST == "":
        print("[CONSTANTS] server cannot be started hostname not found")
        sys.exit()
INITIAL_COINS = float(50)
CHAIN_FILE = './data.json'
# wa = str(input("enter wallet address : "))
wa = "lmfoa1"
STOP_FLAG = threading.Event()
LOCK = threading.Lock()