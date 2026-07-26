from pwdlib import PasswordHash


class PasswordService:
    """
    Handles password hashing and verification.
    """

    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(
        self,
        password: str,
    ) -> str:
        return self.password_hash.hash(password)

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify a password against its hash.
        """

        return self.password_hash.verify(
            password,
            password_hash,
        )