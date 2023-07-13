import unittest
from flask import Flask
from flask.testing import FlaskClient
from datetime import date

from app import app, contactos, mensajes_recibidos

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

         # Agregar contactos
        contactos['lmunoz'] = 'Luisa'
        contactos['mgrau'] = 'Miguel'

        # Enviar mensajes
        mensajes_recibidos.append('Christian te escribio "Hola" el {date}'.format(date=date.today().strftime("%d/%m/%Y")))

    def test_mostrar_contactos_exitoso(self):
        response = self.app.get('/mensajeria/contactos?mialias=cpaz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lmunoz: Luisa', response.data)
        self.assertIn(b'mgrau: Miguel', response.data)

    def test_enviar_mensaje_exitoso(self):
        response = self.app.get('/mensajeria/enviar?mialias=cpaz&aliasdestino=lmunoz&texto=hola')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Realizado en {date}.'.format(date=date.today().strftime("%d/%m/%Y")))

    def test_mostrar_mensajes_recibidos_exitoso(self):
        response = self.app.get('/mensajeria/recibidos?mialias=lmunoz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Christian te escribio', response.data)

    def test_mostrar_contactos_error(self):
        response = self.app.get('/mensajeria/contactos')
        self.assertEqual(response.status_code, 400)

    def test_enviar_mensaje_error(self):
        response = self.app.get('/mensajeria/enviar?mialias=cpaz&texto=hola')
        self.assertEqual(response.status_code, 400)

    def test_mostrar_mensajes_recibidos_error(self):
        response = self.app.get('/mensajeria/recibidos')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
