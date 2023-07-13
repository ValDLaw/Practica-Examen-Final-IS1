from flask import Flask, request, jsonify, abort
from datetime import date

app = Flask(__name__)

# Lista de contactos con su nombre
contactos = {
    'lmunoz': 'Luisa',
    'mgrau': 'Miguel',
    'cpaz': 'Christian'
}

# Lista de mensajes recibidos
mensajes_recibidos = []

@app.route('/')
def index():
    return '¡EXAMEN FINAL DE INGENIERIA DE SOFTWARE 1!'

@app.route('/mensajeria/contactos')
def mostrar_contactos():
    mi_alias = request.args.get('mialias')
    if mi_alias:
        response = ''
        for alias, nombre in contactos.items():
            response += f'{alias}: {nombre}\n'
        return response
    else:
        abort(400)
        return jsonify(error='Se requiere el parametro "mialias".'), 400

@app.route('/mensajeria/enviar')
def enviar_mensaje():
    mi_alias = request.args.get('mialias')
    alias_destino = request.args.get('aliasdestino')
    texto = request.args.get('texto')
    if mi_alias and alias_destino and texto:
        if mi_alias in contactos and alias_destino in contactos:
            mensaje = f'{contactos[mi_alias]} te escribió "{texto}" el {date.today().strftime("%d/%m/%Y")}.'
            mensajes_recibidos.append(mensaje)
            return f'Realizado en {date.today().strftime("%d/%m/%Y")}.'
        else:
            return 'Los alias no están en la lista de contactos.'
    else:
        abort(400)
        return 'Se requieren los parametros "mialias", "aliasdestino" y "texto".'

@app.route('/mensajeria/recibidos')
def mostrar_mensajes_recibidos():
    mi_alias = request.args.get('mialias')
    if mi_alias:
        response = ''
        for mensaje in mensajes_recibidos:
            response += f'{mensaje}\n'
        return response
    else:
        abort(400)
        return 'Se requiere el parametro "mialias".'

if __name__ == '__main__':
    app.run()
