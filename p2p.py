from constants import *
from client import client
from server import server
from peers import p2p
from mine import Mine

def execute_server_thread():
    try:
        server_thread = threading.Thread(target = server)
        server_thread.daemon = True
        server_thread.start()
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"[P2P SCRIPT] problem faced in server -> {e} Restarting...")
        time.sleep(3)
        execute_server_thread()

def main():

    thread1 = threading.Thread(target = execute_server_thread)
    thread1.daemon = True
    thread1.start()

    for peer in p2p.peers:
        print(f"[P2P SCRIPT] clients peers execution in progress {peer}")
        try:
            client_thread = threading.Thread(target = client, args = (peer,))
            client_thread.daemon = True
            client_thread.start()
            client_thread.join()
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(f"[P2P SCRIPT] problem faced in client -> {e}")

    STOP_FLAG.set()

    while True:
        if STOP_FLAG.is_set():
            STOP_FLAG.clear()
            print(f"[MINE] starting the mining again after stopping ... ")
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
        time.sleep(2)
        print("[P2P SCRIPT] connecting clients to peer servers")
        if len(p2p.peers) == 0:
            print("[P2P SCRIPT] no peers left")
        else:
            for peer in p2p.peers:
                print(f"[P2P SCRIPT] clients peers execution in progress {peer}")
                try:
                    client_thread = threading.Thread(target = client, args = (peer,))
                    client_thread.daemon = True
                    client_thread.start()
                    client_thread.join()
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    print(f"[P2P SCRIPT] problem faced in client -> {e}")

if __name__ == "__main__":
    main()