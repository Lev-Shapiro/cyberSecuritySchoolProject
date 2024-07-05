class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def _extend_key(self, length):
        key = self.key
        return (key * (length // len(key))) + key[:length % len(key)]

    def _shift_character(self, char, shift):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            return chr((ord(char) - base + shift) % 26 + base)
        return char

    def _unshift_character(self, char, shift):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            return chr((ord(char) - base - shift) % 26 + base)
        return char

    def encrypt(self, plaintext):
        extended_key = self._extend_key(len(plaintext))
        ciphertext = []
        for p, k in zip(plaintext, extended_key):
            shift = ord(k.lower()) - ord('a')
            ciphertext.append(self._shift_character(p, shift))
        return ''.join(ciphertext)

    def decrypt(self, ciphertext):
        extended_key = self._extend_key(len(ciphertext))
        plaintext = []
        for c, k in zip(ciphertext, extended_key):
            shift = ord(k.lower()) - ord('a')
            plaintext.append(self._unshift_character(c, shift))
        return ''.join(plaintext)