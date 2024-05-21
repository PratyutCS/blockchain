import socket
import subprocess
import sys

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
                    print(f"ipaddress is : {ipaddress}")
                    break
    return ipaddress

HOST = get_lan_ip()
PORT = 8000
try:
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.bind(("0.0.0.0",PORT))
    soc.listen(1)
except Exception as e:
    print(f"exception occured : REPORT -> {e}")

while True:
    try:
        conn,addr = soc.accept()
        print(conn)
        conn.close()
    except KeyboardInterrupt:
        sys.exit()