from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import g
from flask import json
from flask import copy_current_request_context
from flask_mail import Mail
from flask_mail import Message
import threading
from config import DevelopmentConfig
from models import db
from models import User
from models import Estacionamiento
from models import Tarifa
from models import Ticket
# from models import Comment
from helper import date_format
from flask_wtf.csrf import CSRFProtect
import forms 
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
mail = Mail()

def send_email(user_email, username):
    msg = Message('Gracias por tu registro!', sender=app.config['MAIL_USERNAME'], recipients=[user_email])
    msg.html = render_template('email.html', username = username)
    mail.send(msg)

@app.errorhandler(404) #Terminado
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request(): #Terminado
    if 'username' not in session and request.endpoint in ['inicio', 'superinicio', 'entradas', 'salidas', 'tarifas', 'usuarios', 'superusuarios', 'ticEntrada', 'ticSalida']:
        return redirect(url_for('signin'))
    elif 'username' in session and request.endpoint in ['signin', 'create']:
        return redirect(url_for('index'))


@app.after_request #Terminado
def after_request(response):
    return response

@app.route('/reviews/', methods = ['GET'])
@app.route('/reviews/<int:page>', methods = ['GET']) #Ignorar
def reviews(page = 1):
    comments = Comment.query.join(User).add_columns(
                                            User.username,
                                            Comment.text,
                                            Comment.create_date).paginate(page=page,per_page=3,error_out=False)
    return render_template('reviews.html', comments = comments, current_page = page, date_format = date_format)
    #return render_template('reviews.html', comments = comments)**

@app.route('/', methods = ['GET', 'POST']) #Terminado
def index():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('superinicio'))
        else:
            return redirect(url_for('inicio'))
    else:
        return redirect(url_for('signin'))
    return render_template('index.html')


@app.route('/inicio', methods = ['GET', 'POST']) #Terminado
def inicio():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('index'))
    title = "Inicio"
    esta = User.query.filter_by(username = username).first()
    tickets = Ticket.query.filter_by(estacionamiento = esta.estacionamiento).all()
    return render_template('inicio.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username)

@app.route('/superinicio', methods = ['GET', 'POST']) #Terminado
def superinicio():
    if 'username' in session:
        username = session['username']
        if username != "Dios":
            return redirect(url_for('index'))
    title = "Super Inicio"
    create_form = forms.todoesta(request.form)
    estacionamientos =  Estacionamiento.query.all()
    esta = User.query.filter_by(username = username).first()
    tickets = Ticket.query.filter_by(estacionamiento = create_form.estacionamiento.data).all()
    tarifa = Tarifa.query.filter_by(estacionamiento = create_form.estacionamiento.data).first()
    return render_template('superini.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username, tari = tarifa, estacio = estacionamientos, form = create_form)

@app.route('/superusuarios', methods = ['GET', 'POST']) #Terminado
def superusuarios():
    if 'username' in session:
        username = session['username']
        if username != "Dios":
            return redirect(url_for('index'))
    title = "Super Usuarios"
    create_form = forms.CreateUserTodo(request.form)
    estacionamientos =  Estacionamiento.query.all()
    esta = User.query.filter_by(username = username).first()
    us = User.query.all()

    if request.method == 'POST' and create_form.validate():
        usuario = User(username = create_form.username.data, 
                    password = create_form.password.data,
                    rol = create_form.rol.data,
                    estacionamiento = create_form.estacionamiento.data)
        db.session.add(usuario)
        db.session.commit()

        success_message = 'Usuario registrado exitosamente'
        flash(success_message)
        return redirect(url_for('superusuarios'))
    return render_template('superusuarios.html', title = title, estacionamiento = esta, usuario = username, estacio = estacionamientos, form = create_form, userall = us)


@app.route('/eliminar', methods = ['GET', 'POST']) #Terminado
def eliminar():
    if request.method == 'POST':
        idd = request.form['username']
        if idd == "Dios":
            success_message = 'Dios no puede ser eliminado... al desafiarlo serás castigado...'
            flash(success_message)
            return redirect(url_for('superusuarios'))
        else:
            usuario = User.query.filter_by(username = idd).first()
            db.session.delete(usuario)
            db.session.commit()
            success_message = 'Usuario Eliminado'
            flash(success_message)
            return redirect(url_for('superusuarios'))


@app.route('/entradas', methods = ['GET', 'POST']) #Terminado
def entradas():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('index'))
    title = "Entradas"
    esta = User.query.filter_by(username = username).first()
    tickets = Ticket.query.filter_by(estacionamiento = esta.estacionamiento).all()
    return render_template('entradas.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username)

@app.route('/salidas', methods = ['GET', 'POST']) #Terminado
def salidas():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('index'))
    title = "Salidas"
    esta = User.query.filter_by(username = username).first()
    tickets = Ticket.query.filter_by(estacionamiento = esta.estacionamiento).all()
    return render_template('salidas.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username)

@app.route('/tarifas', methods = ['GET', 'POST']) #Terminado
def tarifas():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('index'))
    esta = User.query.filter_by(username = username).first()
    title = "Tarifa"
    tarifa = Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).first()
    create_form = forms.CreateTari(request.form)

    if request.method == 'POST' and create_form.validate():
        Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).update(
            dict(tolerancia = create_form.tolerancia.data,
                 primerasDos = create_form.primerasDos.data,
                 extra = create_form.extra.data,)
                 )
        db.session.commit()
        success_message = 'Tarifa actualzada exitosamente'
        flash(success_message)
    return render_template('tarifas.html', estacionamiento = esta, usuario = username, title = title, tari = tarifa, form = create_form)


@app.route('/usuarios', methods = ['GET', 'POST']) #Terminado
def usuarios():
    if 'username' in session:
        username = session['username']
        if username == "Dios":
            return redirect(url_for('index'))
    title = "Usuarios"
    esta = User.query.filter_by(username = username).first()
    user = User.query.filter_by(estacionamiento = esta.estacionamiento).all()
    create_form = forms.CreateUser(request.form)

    if request.method == 'POST' and create_form.validate():
        usuario = User(create_form.username.data, 
                    create_form.password.data,
                    create_form.rol.data,
                    estacionamiento = esta.estacionamiento)
        db.session.add(usuario)
        db.session.commit()

        success_message = 'Usuario registrado exitosamente'
        flash(success_message)
        return redirect(url_for('usuarios'))
    return render_template('usuarios.html', title = title, estacionamiento = esta, users = user, usuario = username,  form=create_form)

@app.route('/ticEntrada', methods = ['GET', 'POST']) #Terminado
def ticEntrada():
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username = username).first()
    if request.method == 'POST':
        ticket = Ticket( encargado=username, entrada = request.form['fecha'], salida=None, costo = None, estacionamiento=esta.estacionamiento)
        db.session.add(ticket)
        db.session.commit()
    return render_template('ticketEntrada.html', estacionamiento = esta, usuario = username, boleto = ticket)

@app.route('/ticSalida', methods = ['GET', 'POST']) #Terminado
def ticSalida():
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username = username).first()
    boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
    title = "Salidas"
    tickets = Ticket.query.filter_by(estacionamiento = esta.estacionamiento).all()

    if boleto is None:  # Verificar si el boleto no existe
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)
    
    if boleto.costo is None:
        if request.method == 'POST':
            Ticket.query.filter_by(id=request.form['codigo']).update(
                dict(salida = request.form['salida']))
            db.session.commit()
            boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
            fecha1_dt = datetime.strptime(str(boleto.entrada), '%Y-%m-%d %H:%M:%S')
            fecha2_dt = datetime.strptime(str(boleto.salida), '%Y-%m-%d %H:%M:%S')
            tiempo = fecha2_dt - fecha1_dt
            tiempo = tiempo.total_seconds() / 60
            tarifa = Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).first()
            if tiempo <= 15 :
                total = 0
            elif tiempo <=120 :
                total = tarifa.primerasDos
            elif tiempo >=121 :
                tiempo = tiempo -120
                if tiempo <=59:
                    total = tarifa.primerasDos+tarifa.extra
                else:
                    total = (tiempo//60)*tarifa.extra+tarifa.primerasDos
            Ticket.query.filter_by(id=request.form['codigo']).update(
                dict(costo = total))
            db.session.commit()
        return render_template('ticketSalida.html', est = esta, usuario = username, boleto = boleto, total = total, salida = boleto.salida)
    else:
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username)

@app.route('/cookie') #Ignorar
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('galleta', 'Kevin Angeles')
    return response

@app.route('/logout') #Terminado
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('signin')) 

@app.route('/signin', methods = ['GET', 'POST']) #Terminado
def signin():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():

        username = login_form.username.data
        password = login_form.password.data
    
        user = User.query.filter_by(username = username).first()

        if user is not None and user.verify_password(password):  
            
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = username
            session['user_id']=user.id
            return redirect(url_for('index'))
        else: 
            # print(username)
            # print(password)
            error_message = 'Usuario o Password invalidos!'
            flash(error_message)
            if 'username' in session:
                session.pop('username') 
            return redirect(url_for('signin'))        
        session['username'] = login_form.username.data
    title= "Login"
    return render_template('signin.html', title = title ,form = login_form)

@app.route('/ajax-login', methods=['POST']) #Terminado
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = {'status':200, 'username':username, 'id':1}
    return json.dumps(response)

@app.route('/signup', methods = ['GET', 'POST']) #Terminado
def signup():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        # registra el estacionamiento primero
        estacionamiento = Estacionamiento(estacionamiento = create_form.estacionamiento.data,
                    capacidad = create_form.capacidad.data,
                    cp = create_form.cp.data,
                    telefono = create_form.telefono.data)
        db.session.add(estacionamiento)
        db.session.commit()
        # registra al usuario vinculado al estacionamiento
        user = User(create_form.username.data, 
                    create_form.password.data,
                    rol = "Administrador",
                    estacionamiento = create_form.estacionamiento.data)
        db.session.add(user)
        db.session.commit()
        # registra la tarifa por default de la tabla
        tarifa = Tarifa(tolerancia = 15,
                        primerasDos = 20,
                        extra = 20,
                        estacionamiento = create_form.estacionamiento.data)
        db.session.add(tarifa)
        db.session.commit()

        # @copy_current_request_context
        # def send_message(email, username):
        #     send_email(email, username)
        # sender = threading.Thread(name='mail_sender', target = send_message, args = (user.email, user.username))
        # sender.start()

        success_message = 'Usuario registrado exitosamente'
        flash(success_message)
    title = "Registro"
    return render_template('signup.html',  title = title, form=create_form)



if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    

    with app.app_context():
        db.create_all()

    app.run(port=8000)