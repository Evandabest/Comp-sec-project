class PolyalphabeticCesearShift:
    def __init__(self):
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, message, shift):
        encrypted = ""
        for i, char in enumerate(message):
            charPosition = ord(char) - ord("A")
            s = int(shift[i % len(shift)])
            encrypted += self.ALPHABET[(charPosition + s) % 26]

        return encrypted

    def decrypt(self, message, shift):
        decrypted = ""
        for i, char in enumerate(message):
            charPosition = ord(char) - ord("A")
            s = int(shift[i % len(shift)])
            decrypted += self.ALPHABET[(charPosition - s) % 26]

        return decrypted
