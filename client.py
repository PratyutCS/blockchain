from constants import *
from peers import p2p
from cams import check_and_merge_chain

class client:
    def __init__(self, addr):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = addr
        # self.client_socket.settimeout(5)
        try:
            self.client_socket.connect((addr, PORT))
        except Exception as e:
            print(f"[CLIENT SCRIPT] removing peer due to exception {e} : {addr}")
            p2p.peers.remove(addr)
            sys.exit()

        # i_thread = threading.Thread(target=self.send_message, args=[REQUEST])
        # i_thread.daemon = True
        # i_thread.start()

        while True:

            data = self.recieve_message()

            if not data:
               # means the server has failed
               print("[CLIENT SCRIPT] " + "-" * 21 + " Server failed " + "-" * 21)
               sys.exit()

            elif data[0:1] == PEER_BYTE_DIFFERENTIATOR.decode(FORMAT):
               print("[CLIENT SCRIPT] Got peers")
               # first byte is the byte '\x11 we added to make sure that we have peers
               self.update_peers(data[1:])
               self.send_message(REQUEST)

            elif data[0:1] == CHAIN_BYTE_DIFFERENTIATOR.decode(FORMAT):
               print("[CLIENT SCRIPT] Got block_chain")
               # first byte is the byte '\x12 we added to make sure that we have chain
               check_and_merge_chain(data[1:])
               self.disconnect()
            else:
               print(f"[CLIENT SCRIPT] {data}")

    def disconnect(self):
        self.send_message(DISCONNECT)
        print(f"[CLIENT SCRIPT] disconnnected from peer network")
        sys.exit()

    def update_peers(self, peers):
        peers_list = peers.split(',')[:-1]
        for pp in peers_list:
            if pp != HOST:
                found = False
                for po in p2p.peers:
                    if po == pp:
                        found = True
                        break
                if not found:
                    p2p.peers.append(pp)
        print("[CLIENT SCRIPT] " + "-"*21 + f"updated peers {p2p.peers}" + "-"*21)

    def send_message(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        self.client_socket.send(send_length)
        self.client_socket.send(message)

    def recieve_message(self):
        try:
            print(f"[CLIENT SCRIPT] Recieving ------- {self.addr}")
            msg_length = ""
            while len(msg_length) < HEADER:
                msg_length += self.client_socket.recv(HEADER).decode(FORMAT)
            # print(f"[CLIENT SCRIPT] msg length is : {msg_length}")
            acc_msg = ""
            if msg_length:
                msg_length = int(msg_length)
                while len(acc_msg) < msg_length:
                    acc_msg += self.client_socket.recv(msg_length).decode(FORMAT)
                print(f"[CLIENT SCRIPT] acc_msg - {len(acc_msg)} : msg_pength - {msg_length}")
                # print(f"[CLIENT SCRIPT] acc_msg recieved")
            return acc_msg
        except KeyboardInterrupt:
            self.disconnect()