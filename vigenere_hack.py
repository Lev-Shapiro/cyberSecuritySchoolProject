import math
import string
from collections import Counter

class VigenereHack:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext.upper()
        self.alphabet = string.ascii_uppercase
        self.freq_eng = {
            'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 13.0, 'F': 2.2, 'G': 2.0,
            'H': 6.1, 'I': 7.0, 'J': 0.15, 'K': 0.77, 'L': 4.0, 'M': 2.4, 'N': 6.7,
            'O': 7.5, 'P': 1.9, 'Q': 0.095, 'R': 6.0, 'S': 6.3, 'T': 9.1, 'U': 2.8,
            'V': 0.98, 'W': 2.4, 'X': 0.15, 'Y': 2.0, 'Z': 0.074
        }

    def calculate_ioc(self, text):
        n = len(text)
        freq = Counter(text)
        ioc = sum(count * (count - 1) for count in freq.values()) / (n * (n - 1))
        return ioc

    def find_key_length(self, max_length=20):
        iocs = []
        for length in range(1, max_length + 1):
            substrings = [''.join(self.ciphertext[i::length]) for i in range(length)]
            avg_ioc = sum(self.calculate_ioc(s) for s in substrings) / length
            iocs.append((length, avg_ioc))
        
        iocs.sort(key=lambda x: x[1], reverse=True)
        return iocs[0][0]

    def shift_letter(self, letter, shift):
        if letter in self.alphabet:
            return self.alphabet[(self.alphabet.index(letter) - shift) % 26]
        return letter

    def calculate_chi_square(self, observed):
        expected = {char: self.freq_eng[char] * sum(observed.values()) / 100 for char in self.alphabet}
        return sum((observed.get(char, 0) - expected[char])**2 / expected[char] for char in self.alphabet)

    def find_key(self):
        key_length = self.find_key_length()
        key = ''

        for i in range(key_length):
            substring = self.ciphertext[i::key_length]
            chi_squares = []

            for shift in range(26):
                shifted = ''.join(self.shift_letter(c, shift) for c in substring)
                observed = Counter(c for c in shifted if c in self.alphabet)
                chi_square = self.calculate_chi_square(observed)
                chi_squares.append((shift, chi_square))

            best_shift = min(chi_squares, key=lambda x: x[1])[0]
            key += self.alphabet[best_shift]

        return key

    def calculate_probability(self, text):
        # Calculate the frequency distribution of the decrypted text
        freq = Counter(c for c in text if c in self.alphabet)
        total = sum(freq.values())
        
        # Calculate the log-likelihood of the text given English frequencies
        log_likelihood = sum(freq[c] * math.log(self.freq_eng[c] / 100) for c in self.alphabet if c in freq)
        
        # Normalize by text length to get a per-character log-likelihood
        normalized_log_likelihood = log_likelihood / total
        
        # Convert to a probability-like score between 0 and 1
        probability = 1 / (1 + math.exp(-normalized_log_likelihood))
        
        return probability