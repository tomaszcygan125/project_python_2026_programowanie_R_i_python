import hashlib
import hmac
import os


class PasswordHasher:

    #Return hashed password using given salt
    @staticmethod
    def compute_hash(password: str, salt: bytes) -> bytes:
        hmac_obj = hmac.new(
            key=salt,                         # satl as a key
            msg=password.encode('utf-8'),
            digestmod=hashlib.sha512          # HMAC-SHA512
        )
        return hmac_obj.digest()
    @staticmethod
    def hashPassword(password):

        salt = os.urandom(128)  # 128 bytes

        #generate hash password based on salt
        hash_bytes = hmac.new(salt, password.encode('utf-8'), hashlib.sha512).digest()

        return [hash_bytes, salt]