import pathlib
from typing import Optional, Literal

from core.cipher import Cipher


class Secure:
    def __init__(
        self,
        base_path: Optional[pathlib.Path] = None,
        store_type: Literal["local", "vault"] = "local",
    ):
        self.base_path = (
            base_path or pathlib.Path(__file__).resolve().parent.parent / "config"
        )
        self.store_type = store_type
        self.cipher = Cipher(base_path=self.base_path, vault_type=store_type)

    def decrypt_password(self, password: bytes):
        return self.cipher.decrypt(password)
