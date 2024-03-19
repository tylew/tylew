import json
from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic
from multiprocessing import Process, Value, Lock
import time

target_public_key = '1K4ezpLybootYF23TM4a8Y4NyP7auysnRo'

def append_to_file(file_path, text):
    """
    Appends the given text to the file specified by file_path.

    Parameters:
    file_path (str): The path to the file.
    text (str): The text to append to the file.
    """
    with open(file_path, 'a') as file:
        file.write(text + '\n')

def process_mnemonic(mnemonics, start, end, counter, lock):
    for i in range(start, end):
        mnemonic = mnemonics[i]
        seed = Mnemonic().to_seed(mnemonic)
        wallet_name = "temp_wallet_" + mnemonic[:8]  # Ensure unique wallet name
        wallet = Wallet.create(wallet_name, keys=seed, network='bitcoin', witness_type='segwit', db_uri=None)
        
        address = wallet.get_key().address
        
        if address == target_public_key:
            append_to_file('success.txt', mnemonic)
            print(f'found {address} using mnemonic: {mnemonic}')
        
        wallet_delete(wallet_name, force=True)
        
        with lock:
            counter.value += 1

def monitor(counter):
    while True:
        with counter.get_lock():
            print(f"Processed {counter.value} mnemonics")
        time.sleep(10)

if __name__ == "__main__":
    with open('valid_mnemonics.json', 'r') as json_file:
        mnemonics = json.load(json_file)
    
    counter = Value('i', 0)  # Shared memory integer
    lock = Lock()
    num_processes = 3
    chunk_size = len(mnemonics) // num_processes
    
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(mnemonics)
        p = Process(target=process_mnemonic, args=(mnemonics, start, end, counter, lock))
        processes.append(p)
        p.start()
    
    monitor_process = Process(target=monitor, args=(counter,))
    monitor_process.start()
    
    for p in processes:
        p.join()
    
    monitor_process.terminate()  # Stop the monitoring process
    print("Finished processing all mnemonics.")

# # Make sure to clean up any pre-existing temporary wallets
# wallet_delete("temp_wallet", force=True)
# # Replace 'path/to/your/json_file.json' with the actual file path
# process_mnemonics('valid_mnemonics.json')
# # print(mnemonics_with_funds)
