from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hola mundo'

@app.route('/name')
def name():
    param = request.args.get('param1', 'Debes ingresar el nombre')
    param_2 = request.args.get('param2', 'No contiene argumentos')
    return 'El parametro es: {}, {}'.format(param, param_2)

if __name__ == '__main__':
    app.run(debug = True, port=8000)

