from constants import *
class check_and_merge_chain:
    def __init__(self, str_chain):
        # print(str_chain)
        exception = False
        try:
            chain = json.loads(str_chain)
        except Exception as e:
            print(f"[MINE] exception found while parsing the chain received REPORT -> {e}")
            exception = True
        if not exception:
            if self.checkChain(chain):
                print("[MINE] check chain passed")
                if (self.compareChain(chain)):
                    print(f"[MINE] changes made to the chain")
    
    def readChainFromFile(self):
        file = open(CHAIN_FILE)
        data = json.load(file)
        return data
    
    def calculate_merkle_root(self, transactions):
        if len(transactions) <= 0:
            return ""
        elif len(transactions) == 1:
            return hashlib.sha3_512(transactions[0].encode()).hexdigest()
        else:
            hashes = [hashlib.sha3_512(tx.encode()).hexdigest() for tx in transactions]
            while len(hashes) > 1:
                if len(hashes) % 2 != 0:
                    hashes.append(hashes[-1])
                new_hashes = []
                for i in range(0, len(hashes), 2):
                    combined_hash = hashlib.sha3_512(hashes[i].encode() + hashes[i + 1].encode()).hexdigest()
                    new_hashes.append(combined_hash)
                hashes = new_hashes
            return hashes[0]

    def checkChain(self, chain):
        check1 = True
        check2 = True
        check3 = True
        check4 = True

        breakpoint11 = 0
        breakpoint12 = 0

        chain_size = len(chain)-1

        while chain_size > 0:
            # print(f"{chain[str(chain_size)]}")
            if chain[str(chain_size)]["prev_block_hash"] != chain[str(chain_size - 1)]["block_hash"]:
                breakpoint11 = chain_size
                breakpoint12 = chain_size-1
                check1 = False
                break
            if chain[str(chain_size)]["merkle_hash"] != self.calculate_merkle_root( chain[str(chain_size)]["transactions"]):
                check2 = False
                break
            if chain[str(chain_size)]["time"] < chain[str(chain_size)]["time"]:
                check3 = False
                break
            header = chain[str(chain_size)]["prev_block_hash"] + chain[str(chain_size)]["merkle_hash"] + "0" * (20 - len(str(chain[str(chain_size)]["time"]))) + str(chain[str(chain_size)]["time"]) + "0" * (20 - len(str(chain[str(chain_size)]["nonce"]))) + str(chain[str(chain_size)]["nonce"])
            blc_hash =  hashlib.sha3_512(header.encode()).hexdigest()
            if blc_hash != chain[str(chain_size)]["block_hash"]:
                check4 = False
                break
            chain_size -= 1
        if not check1:
            print(f"check1 fked up between {breakpoint12} -:- {breakpoint11}")
        if not check2:
            print(f"check2 fked up")
        if not check3:
            print(f"check3 fked up")
        if not check4:
            print(f"check4 fked up")
        return check1 and check2 and check3 and check4

    def compareChain(self, chain):
        change = True
        data = self.readChainFromFile()
        breakpoint11 = -1
        if len(data) == 0:
            chain_no = len(data)
            while chain_no < len(chain):
                json_data = {str(chain_no) : {
                        "prev_block_hash": chain[str(chain_no)]["prev_block_hash"],
                        "merkle_hash": chain[str(chain_no)]["merkle_hash"],
                        "time": chain[str(chain_no)]["time"],
                        "nonce": chain[str(chain_no)]["nonce"],
                        "transactions": chain[str(chain_no)]["transactions"],
                        "block_hash" : chain[str(chain_no)]["block_hash"]
                    }
                }
                data.update(json_data)
        elif len(chain) == 1:
            if len(chain) > len(data):
                chain_no = len(chain)-1
                json_data = {str(chain_no) : {
                        "prev_block_hash": chain[str(chain_no)]["prev_block_hash"],
                        "merkle_hash": chain[str(chain_no)]["merkle_hash"],
                        "time": chain[str(chain_no)]["time"],
                        "nonce": chain[str(chain_no)]["nonce"],
                        "transactions": chain[str(chain_no)]["transactions"],
                        "block_hash" : chain[str(chain_no)]["block_hash"]
                    }
                }
                data.update(json_data)
            else:
                change = False
        else:
            if len(chain) > len(data):
                chain_no = len(data) - 1

                if chain[str(chain_no)]["block_hash"] == data[str(chain_no)]["block_hash"]:
                    chain_no += 1
                    while chain_no < len(chain):
                        json_data = {str(chain_no) : {
                                "prev_block_hash": chain[str(chain_no)]["prev_block_hash"],
                                "merkle_hash": chain[str(chain_no)]["merkle_hash"],
                                "time": chain[str(chain_no)]["time"],
                                "nonce": chain[str(chain_no)]["nonce"],
                                "transactions": chain[str(chain_no)]["transactions"],
                                "block_hash" : chain[str(chain_no)]["block_hash"]
                            }
                        }
                        data.update(json_data)
                        chain_no += 1
                else:
                    print(f"[CAMS] else ran due to last block hash not matching")
                    while chain_no > 0:
                        if chain[str(chain_no)]["block_hash"] == data[str(chain_no)]["block_hash"]:
                            breakpoint11 = chain_no + 1
                            break
                        chain_no -= 1

                    while breakpoint11 < len(chain):
                        json_data = {str(breakpoint11) : {
                                "prev_block_hash": chain[str(breakpoint11)]["prev_block_hash"],
                                "merkle_hash": chain[str(breakpoint11)]["merkle_hash"],
                                "time": chain[str(breakpoint11)]["time"],
                                "nonce": chain[str(breakpoint11)]["nonce"],
                                "transactions": chain[str(breakpoint11)]["transactions"],
                                "block_hash" : chain[str(breakpoint11)]["block_hash"]
                            }
                        }
                        data.update(json_data)
                        breakpoint11 += 1
            else:
                change = False

        if change:
            STOP_FLAG.set()
            time.sleep(1)
            with open(CHAIN_FILE, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"[MINE] wrote to file")
            time.sleep(1)
        
        return change    

class data:
    def chainData():
        return json.dumps(json.load(open(CHAIN_FILE)))