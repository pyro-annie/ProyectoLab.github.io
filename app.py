from flask import Flask, request, jsonify, render_template

import re
import secrets
import string

app = Flask(__name__)

# Almacenamiento en memoria para usuarios registrados
users = {}

# Requisitos de la contraseña
password_requirements = {
    'uppercase': 1,
    'digits': 1,
    'special': 1,
    'min_length': 8
}

from flask import Flask, jsonify, request, render_template
import re
import string
import secrets

app = Flask(__name__)

# Diccionario global para almacenar usuarios
users = {}

# Requisitos de la contraseña
password_requirements = {
    'uppercase': 1,
    'digits': 1,
    'special': 1,
    'min_length': 8
}

# Función para verificar si la contraseña cumple con los requisitos
def check_password_requirements(password):
    has_uppercase = len(re.findall(r'[A-Z]', password)) >= password_requirements['uppercase']
    has_digit = len(re.findall(r'\d', password)) >= password_requirements['digits']
    has_special = len(re.findall(r'\W', password)) >= password_requirements['special']
    is_long_enough = len(password) >= password_requirements['min_length']
    return has_uppercase and has_digit and has_special and is_long_enough

# Función para generar una contraseña segura
def generate_secure_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(password_requirements['min_length']))
        if check_password_requirements(password):
            break
    return password

@app.route('/generate-password', methods=['POST'])
def generate_password():
    return jsonify({'password': generate_secure_password()})

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    
    # Verificar si la contraseña cumple con los requisitos
    if not check_password_requirements(password):
        return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, caracter especiales y números.'}), 400
    
    
    # Verificar si el usuario ya existe
    if name in users:
        return jsonify({'error': 'El usuario ya existe'}), 400
    
    # Guardar el usuario
    users[name] = {'password': password}
    return jsonify({'message': 'Usuario registrado con éxito'})


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Verificar si el usuario existe
    if username not in users:
        return jsonify({'error': 'Usuario no registrado'}), 400
    
    # Verificar si la contraseña es correcta
    if users[username]['password'] != password:
        return jsonify({'error': 'Contraseña errónea, intente otra vez'}), 400
    
    # Si el usuario existe y la contraseña es correcta
    return jsonify({'message': 'Bienvenido, ' + username})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


