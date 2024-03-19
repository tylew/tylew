from mnemonic import Mnemonic
import json
from itertools import combinations

def is_valid_mnemonic(words, language='english'):
    mnemo = Mnemonic(language)
    return mnemo.check(words)

def find_valid_mnemonics(wordlist, lengths):
    mnemo = Mnemonic('english')
    valid_mnemonics = []
    # Ensure the wordlist is a list of BIP39 words, this might require filtering your input list.
    bip39_words = [word for word in wordlist if word in mnemo.wordlist]
    
    for length in lengths:
        # Generate all possible combinations of the required length
        if len(bip39_words) >= length:
            for combo in combinations(bip39_words, length):
                phrase = ' '.join(combo)
                if is_valid_mnemonic(phrase):
                    valid_mnemonics.append(phrase)
    return valid_mnemonics

# Load your list of words from a file
with open('underlined_word_list.txt', 'r') as file:
    words = file.read().splitlines()

# Find valid mnemonics for both 12 and 24 word lengths
valid_mnemonics_12 = find_valid_mnemonics(words, [12])
valid_mnemonics_24 = find_valid_mnemonics(words, [24])

# Combine the results
valid_mnemonics = valid_mnemonics_12 + valid_mnemonics_24

# Write valid mnemonics to a JSON file
with open('valid_mnemonics.json', 'w') as json_file:
    json.dump(valid_mnemonics, json_file, indent=4)

print("Valid mnemonics found and saved to valid_mnemonics.json.")
