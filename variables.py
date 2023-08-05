from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/user/<name>')
def user(name='Kevin'):
    age = 20
    lista = ['UTEZ','9°A','Ing. RIyC']
    return render_template('user.html', nombre=name, edad=age, mi_lista=lista)

if __name__ == '__main__':
    app.run(debug = True, port=8000)