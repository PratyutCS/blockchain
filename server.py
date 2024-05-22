from constants import *
from peers import p2p
from cams import data

class server:
    def __init__(self):
        try:

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.server_socket.bind((HOST,PORT))

            self.server_socket.listen(1)

            print("[SERVER SCRIPT] " + "-" * 12+ f"Server Running {HOST}:{PORT}"+ "-" *21)
                
            self.run()
        except Exception as e:
            print(f"[SERVER SCRIPT] exception found in server script REPORT -> {e}")
            sys.exit()

    def handle_client(self,conn,addr):
        print(f"[SERVER SCRIPT] {addr} connected")
        try:
            connected = True
            while connected:
                msg_length = ""
                while len(msg_length) < HEADER:
                    msg_length += conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    acc_msg = conn.recv(msg_length).decode(FORMAT)
                    if acc_msg == DISCONNECT:
                        connected = False
                        self.disconnect(conn,addr)
                        sys.exit()
                    elif acc_msg == REQUEST:
                        self.send_chain(conn)
                    else:
                        print(f"[SERVER SCRIPT] {addr} : {acc_msg}")
        except Exception as e:
            print(f"[SERVER SCRIPT] system exited because an error occured REPORT --> {e} : {addr}")
            sys.exit()

    def send_peers(self, conn):
        peer_list = ""
        for peer in p2p.peers:
            peer_list = peer_list + str(peer) + ","
            
        message = PEER_BYTE_DIFFERENTIATOR + peer_list.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)
        print("[SERVER SCRIPT] " + "-"*21 + " peers sent " + "-"*21 )

    def send_chain(self, conn):
        print("[SERVER SCRIPT] " + "-" * 21 + " sending chain " + "-" * 21)

        block_chain = CHAIN_BYTE_DIFFERENTIATOR + data.chainData().encode(FORMAT)
        msg_length = len(block_chain)
        send_length = str(msg_length).encode(FORMAT)
        # print(f"[SERVER] message length {send_length}")
        send_length += b' ' * (HEADER - len(send_length))

        
        conn.send(send_length)
        conn.send(block_chain)

    def disconnect(self,conn,addr):
        conn.close()
        print("[SERVER SCRIPT] {}, disconnected".format(addr))

    def run(self):
        while True:
            conn , addr = self.server_socket.accept()

            found = False
            for pp in p2p.peers:
                if pp == addr[0]:
                    found = True
                    break
            if not found:
                p2p.peers.append(addr[0])
                print(f"[SERVER SCRIPT] updated peer list is : {p2p.peers}")

            try :
                self.send_peers(conn)
            except Exception as e:
                print(f"[SERVER SCRIPT] errors FOUND while sending peers {e}")

            thread = threading.Thread(target=self.handle_client, args=(conn , addr))
            thread.daemon = True
            thread.start()
            print(f"[SERVER SCRIPT] end line of run loop")