import unittest

from pydantic import ValidationError

from schemas.usuario_schema import UsuarioSchemaCreate, UsuarioSchemaUpdate


class UsuarioSchemaTests(unittest.TestCase):
    def test_signup_rejects_extra_privilege_fields(self):
        with self.assertRaises(ValidationError):
            UsuarioSchemaCreate(
                nome="Ana",
                sobrenome="Silva",
                email="ana@example.com",
                senha="uma-senha-segura",
                eh_admin=True,
            )

    def test_update_accepts_omitted_fields(self):
        update = UsuarioSchemaUpdate(nome="Ana")
        self.assertEqual(update.model_dump(exclude_unset=True), {"nome": "Ana"})

    def test_update_preserves_explicit_false(self):
        update = UsuarioSchemaUpdate(eh_admin=False)
        self.assertEqual(
            update.model_dump(exclude_unset=True), {"eh_admin": False}
        )


if __name__ == "__main__":
    unittest.main()
