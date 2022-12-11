import binascii

import win32crypt


class SecurityObject:
    """Secure Object Class"""

    def __init__(self, data_=None, encrypt=False):
        """ Constructor of SecurityObject

        Parameters:
            data_ (str): The encrypted or decrypted data to be saved.
            encrypt (bool): Should the data be encrypted?
        """
        if encrypt and data_ is not None:
            self._data = binascii.hexlify(
                win32crypt.CryptProtectData(str(data_).encode("utf-16-le"), None, None, None, None, 0)
            ).decode()
        else:
            self._data = data_

    def __str__(self):
        return self.data if self._data else "<Empty SecurityObject>"

    @property
    def data(self):
        """Getter Data

        :return: Data
        :rtype: str
        """
        try:
            _, decrypted_word_string = win32crypt.CryptUnprotectData(
                binascii.unhexlify(self._data), None, None, None, 0
            )

            decrypted_word = ''
            onoff = 0
            for letter in decrypted_word_string.decode():
                if onoff == 0:
                    decrypted_word += letter
                onoff = abs(onoff - 1)

            return decrypted_word
        except Exception as _:
            str(_)
            return self._data

    @data.setter
    def data(self, data):
        self._data = binascii.hexlify(
            win32crypt.CryptProtectData(data.encode("utf-16-le"), None, None, None, None, 0)
        ).decode()

    @property
    def encrypted_data(self):
        """Retourne les données encryptées"""
        return self._data

    @encrypted_data.setter
    def encrypted_data(self, data):
        self._data = data
