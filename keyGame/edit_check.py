import json
from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic

def get_public_keys(file_path, step=500):
    public_keys = []

    # Load mnemonics from the JSON file
    with open(file_path, 'r') as json_file:
        mnemonics = json.load(json_file)
    
    for i in range(105000, len(mnemonics), step):
        mnemonic = mnemonics[i]
        seed = Mnemonic().to_seed(mnemonic)
        wallet_name = f"temp_walletr_{i}"  # Unique name based on index
        
        # Create a temporary wallet for this mnemonic
        wallet = Wallet.create(wallet_name, keys=seed, network='bitcoin', witness_type='segwit', db_uri=None)
        
        # Get the first public key of the wallet
        public_key = wallet.get_key()
        print(f'{i}: {public_key}')
        
        # Cleanup: remove the temporary wallet
        wallet_delete(wallet_name, force=True)
    
    return public_keys

# Example usage
file_path = 'valid_mnemonics.json'
public_keys = get_public_keys(file_path)
for public_key in public_keys:
    print(public_key)
