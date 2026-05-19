class PolyalphabeticCesearShift:
    def __init__(self):
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, message, shift):
        encrypted = ""
        shift_index = 0
        for char in message:
            if char.isalpha():
                charPosition = ord(char.upper()) - ord("A")
                s = int(shift[shift_index % len(shift)])
                encrypted += self.ALPHABET[(charPosition + s) % 26]
                shift_index += 1
            else:
                encrypted += char

        return encrypted

    def decrypt(self, message, shift):
        decrypted = ""
        shift_index = 0
        for char in message:
            if char.isalpha():
                charPosition = ord(char.upper()) - ord("A")
                s = int(shift[shift_index % len(shift)])
                decrypted += self.ALPHABET[(charPosition - s) % 26]
                shift_index += 1
            else:
                decrypted += char

        return decrypted
