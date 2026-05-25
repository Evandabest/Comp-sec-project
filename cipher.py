class PolyalphabeticCesearShift:
    def __init__(self):
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, message, shift):
        encrypted = ""
        for index, char in enumerate(message):
            if char.isalpha():
                charPosition = ord(char.upper()) - ord("A")
                s = shift[index % len(shift)]
                encrypted += self.ALPHABET[(charPosition + s) % 26]
            else:
                encrypted += char

        return encrypted

    def decrypt(self, message, shift):
        decrypted = ""
        for index, char in enumerate(message):
            if char.isalpha():
                charPosition = ord(char.upper()) - ord("A")
                s = shift[index % len(shift)]
                decrypted += self.ALPHABET[(charPosition - s) % 26]
            else:
                decrypted += char

        return decrypted
