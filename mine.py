from constants import *

class Block:
    def __init__(self, prev_block_hash, transactions):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 1")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        self.transactions = transactions
        self.prev_block_hash = prev_block_hash
        # print(f"inside block : {transactions}")
        self.header = self.prev_block_hash
        # print(f"header after adding prev_block_hash : {self.header}")
        self.merkleHash = self.calculate_merkle_root()
        self.header += self.merkleHash
        # print(f"header after adding merkleHash : {self.header}")
        self.nonce = self.block_mining()
        self.header += ("0" * (20 - len(str(self.time))) + str(self.time)) + ("0" * (20 - len(str(self.nonce))) + str(self.nonce))
        # print(f"final header : {self.header}")
        self.blc_hash =  hashlib.sha3_512(self.header.encode()).hexdigest()

    def calculate_merkle_root(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 2")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        if len(self.transactions) <= 0:
            return ""
        elif len(self.transactions) == 1:
            return hashlib.sha3_512(self.transactions[0].encode()).hexdigest()
        else:
            hashes = [hashlib.sha3_512(tx.encode()).hexdigest() for tx in self.transactions]
            while len(hashes) > 1:
                if STOP_FLAG.is_set():
                    print(f"[MINE] aye aye amigos exiting mining 3")
                    STOP_FLAG.clear()
                    thread2 = threading.Thread(target = Mine)
                    thread2.daemon = True
                    thread2.start()
                    sys.exit()
                if len(hashes) % 2 != 0:
                    hashes.append(hashes[-1])
                new_hashes = []
                for i in range(0, len(hashes), 2):
                    if STOP_FLAG.is_set():
                        print(f"[MINE] aye aye amigos exiting mining 4")
                        STOP_FLAG.clear()
                        thread2 = threading.Thread(target = Mine)
                        thread2.daemon = True
                        thread2.start()
                        sys.exit()
                    combined_hash = hashlib.sha3_512(hashes[i].encode() + hashes[i + 1].encode()).hexdigest()
                    new_hashes.append(combined_hash)
                hashes = new_hashes
            return hashes[0]
        
    def block_mining(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 5")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        self.time = int(time.time())
        nonce = 0
        print("[MINE] mining....")
        while True:
            if STOP_FLAG.is_set():
                print(f"[MINE] aye aye amigos exiting mining 6")
                STOP_FLAG.clear()
                thread2 = threading.Thread(target = Mine)
                thread2.daemon = True
                thread2.start()
                sys.exit()
            if(nonce > 18446744073709551615):
                nonce = 0
                self.time = int(time.time())
                continue
            else:
                stringToHash = self.header + ("0" * (20 - len(str(self.time))) + str(self.time)) + ("0" * (20 - len(str(nonce))) + str(nonce))
                blockHash = hashlib.sha3_512(stringToHash.encode()).hexdigest()
                # todo adjust difficulty level automatically
                # if blockHash.startswith("0000000000"):
                if blockHash.startswith("000000"):
                    print("[MINE] nonce found ---- {}".format(nonce))
                    # print("encrypted value ::: {}".format(stringToHash))
                    return nonce
            # print("{} :-: {}".format(nonce,blockHash))
            nonce +=1

class Mine:
    def __init__(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 7 {STOP_FLAG}")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        self.data = self.readChainFromFile()
        self.main()

    def mineGenesisBlock(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 8")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        genesis_block = Block("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", ["The first text to start the blockchain"])
        json_data = {"0" : {
                "prev_block_hash": genesis_block.prev_block_hash,
                "merkle_hash": genesis_block.merkleHash,
                "time": genesis_block.time,
                "nonce": genesis_block.nonce,
                "transactions": genesis_block.transactions,
                "block_hash" : genesis_block.blc_hash
            }
        }
        # print(json_data)
        # print("\n dumps \n")
        # print(json.dumps(json_data))
        return json_data

    def mineBlock(self):
        global INITIAL_COINS
        file = open(CHAIN_FILE)
        data = json.load(file)
        if len(data) > 1:
            INITIAL_COINS = float(data[str(len(data)-1)]["transactions"][0].split(" ")[0])
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 9")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        if(len(self.data) % 10 == 0):
            INITIAL_COINS = INITIAL_COINS / 2
        # to take transactions from the memory pool
        coinbase_transaction = f"{INITIAL_COINS} coins credited to {wa} from blockRewards"
        transactions = [coinbase_transaction]
        block = Block(self.data[str(len(self.data)-1)]["block_hash"], transactions)
        json_data = {str(len(self.data)) : {
                "prev_block_hash": block.prev_block_hash,
                "merkle_hash": block.merkleHash,
                "time": block.time,
                "nonce": block.nonce,
                "transactions": block.transactions,
                "block_hash" : block.blc_hash
            }
        }
        # print(json_data)
        # print("\n dumps \n")
        # print(json.dumps(json_data))
        return json_data

    def readChainFromFile(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 10")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        file = open(CHAIN_FILE)
        data = json.load(file)
        return data

    def writeChainToFile(self):
        if STOP_FLAG.is_set():
            print(f"[MINE] aye aye amigos exiting mining 11")
            STOP_FLAG.clear()
            thread2 = threading.Thread(target = Mine)
            thread2.daemon = True
            thread2.start()
            sys.exit()
        with open(CHAIN_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    def main(self):
        while True:
            if(len(self.data) != 0):
                blc_details = self.mineBlock()
                if STOP_FLAG.is_set():
                    print(f"[MINE] aye aye amigos exiting mining 12")
                    STOP_FLAG.clear()
                    thread2 = threading.Thread(target = Mine)
                    thread2.daemon = True
                    thread2.start()
                    sys.exit()
                key = list(blc_details.keys())[0]
                if STOP_FLAG.is_set():
                    print(f"[MINE] aye aye amigos exiting mining 13")
                    STOP_FLAG.clear()
                    thread2 = threading.Thread(target = Mine)
                    thread2.daemon = True
                    thread2.start()
                    sys.exit()
                self.data = self.readChainFromFile()
                flag = True
                for i in self.data.keys():
                    if STOP_FLAG.is_set():
                        print(f"[MINE] aye aye amigos exiting mining 14")
                        STOP_FLAG.clear()
                        thread2 = threading.Thread(target = Mine)
                        thread2.daemon = True
                        thread2.start()
                        sys.exit()
                    if key == i:
                        flag = False
                if flag:
                    self.data.update(blc_details)
                    if STOP_FLAG.is_set():
                        print(f"[MINE] aye aye amigos exiting mining 15")
                        STOP_FLAG.clear()
                        thread2 = threading.Thread(target = Mine)
                        thread2.daemon = True
                        thread2.start()
                        sys.exit()
                    self.writeChainToFile()
                    print(f"[MINE] written to the file")
            else:
                self.data.update(self.mineGenesisBlock())
                if STOP_FLAG.is_set():
                    print(f"[MINE] aye aye amigos exiting mining 16")
                    STOP_FLAG.clear()
                    thread2 = threading.Thread(target = Mine)
                    thread2.daemon = True
                    thread2.start()
                    sys.exit()
                self.writeChainToFile()
                print(f"[MINE] written to the file")