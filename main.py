from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import redirect, send_file
from flask import url_for
from flask import flash
from flask import g
from flask import json
from flask import copy_current_request_context
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
from flask_sqlalchemy import SQLAlchemy
import qrcode
from io import BytesIO
from base64 import b64encode
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
csrf.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()



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












@app.route('/superverificar', methods = ['GET', 'POST']) #Terminado
def superverificar():
    if 'username' in session:
        username = session['username']
        if username != "Dios":
            return redirect(url_for('index'))
    title = "Super Verificar"
    create_form = forms.todoesta(request.form)
    estacionamientos = Estacionamiento.query.all()
    esta = User.query.filter_by(username=username).first()
    tickets = Ticket.query.filter_by(estacionamiento=create_form.estacionamiento.data).all()
    tarifa = Tarifa.query.filter_by(estacionamiento=create_form.estacionamiento.data).first()
    return render_template('superverificar.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username,
                           tari=tarifa, estacio=estacionamientos, form=create_form)


@app.route('/superverificarTabla', methods = ['GET', 'POST']) #Terminado
def superverificarTabla():
    if 'username' in session:
        username = session['username']
        if username != "Dios":
            return redirect(url_for('index'))
    title = "Super Verificar"
    create_form = forms.todoesta(request.form)
    estacionamientos = Estacionamiento.query.all()
    esta = User.query.filter_by(username=username).first()
    tickets = Ticket.query.filter_by(estacionamiento=create_form.estacionamiento.data).all()
    tarifa = Tarifa.query.filter_by(estacionamiento=create_form.estacionamiento.data).first()
    return render_template('superverificarTabla.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username,
                           tari=tarifa, estacio=estacionamientos, form=create_form)






@app.route('/supermodificar', methods = ['GET', 'POST']) #Terminado
def supermodificar():
    if 'username' in session:
        username = session['username']
        if username != "Dios":
            return redirect(url_for('index'))
    title = "Super Modificar"
    create_form = forms.ModificarRol(request.form)
    estacionamientos =  Estacionamiento.query.all()
    esta = User.query.filter_by(username = username).first()
    us = User.query.all()

    if request.method == 'POST' and create_form.validate():
        User.query.filter_by(username=create_form.username.data).update(
            dict(rol = create_form.rol.data,
                    )
        )
        db.session.commit()
        success_message = 'Usuario actualzado exitosamente'
        flash(success_message)

        return redirect(url_for('supermodificar'))
    return render_template('supermodificar.html', title = title, estacionamiento = esta, usuario = username, estacio = estacionamientos, form = create_form, userall = us)





@app.route('/superpago', methods = ['GET', 'POST']) #Terminado
def superpago():
    if 'username' in session:
        username = session['username']
    title = "Super Pago"
    esta = User.query.filter_by(username = username).first()
    tickets = Ticket.query.filter_by(estacionamiento = esta.estacionamiento).all()
    return render_template('superpago.html', title = title, estacionamiento = esta, ticket = tickets, usuario = username)












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
    return redirect(url_for('index'))



@app.route('/modificar_usuario', methods =  ['GET', 'POST'])
def modificar_usuario():
    if request.method == 'POST':
        id = request.form['username']
        rol = request.form['rol']
        usuario = User.query.get(id)
        if usuario:
            if usuario.id == 1:
                flash('No puedes modificar a Dios, el lo es todo!')
            else:
                usuario_data = {
                'rol': rol,
                }

                User.query.filter_by(id=id).update(usuario_data)
                db.session.commit()
                flash('Usuario modificado correctamente!')
        else:
            flash('No se encontró el usuario a modificar!')
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
                 extra = create_form.extra.data,
                 pension_dia = create_form.pension_dia.data,
                 pension_semana = create_form.pension_semana.data,
                 pension_mes = create_form.pension_mes.data,)
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
    usu = User.query.filter_by(username = username).first()

    esta = Estacionamiento.query.filter_by(estacionamiento = usu.estacionamiento).first()
    if request.method == 'POST':
        if esta.lugares < esta.capacidad:

            lugares = esta.lugares + 1
            estacionamiento_data = {
                'lugares': lugares
            }

            Estacionamiento.query.filter_by(estacionamiento = usu.estacionamiento).update(estacionamiento_data)
            db.session.commit()

            ticket = Ticket( encargado=username, entrada = request.form['fecha'], salida=None, costo = None, estacionamiento=usu.estacionamiento)
            db.session.add(ticket)
            db.session.commit()

            qr_data = f"localhost:8000/codigo/{ticket.id}"
            qr = qrcode.make(qr_data)
            qr_io = BytesIO()
            qr.save(qr_io)
            qr_io.seek(0)

            ticket.qr_code = b64encode(qr_io.read())
            db.session.add(ticket)
            db.session.commit()





            return render_template('ticketEntrada.html', estacionamiento = esta, usuario = username, boleto = ticket)
        else:
            flash('El Cupo del estacionamiento esta lleno!')
            return redirect(url_for('entradas'))




























@app.route('/calSalida', methods=['GET', 'POST'])  # Terminado
def calSalida():
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username=username).first()
    boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
    title = "Salidas"
    tickets = Ticket.query.filter_by(estacionamiento=esta.estacionamiento).all()

    if boleto is None:  # Verificar si el boleto no existe
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

    if boleto.costo is None:
        if request.method == 'POST':
            if boleto.encargado == session['username']:
                Ticket.query.filter_by(id=request.form['codigo']).update(
                    dict(salida=request.form['salida']))

                boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
                fecha1_dt = datetime.strptime(str(boleto.entrada), '%Y-%m-%d %H:%M:%S')
                fecha2_dt = datetime.strptime(str(request.form['salida']), '%Y-%m-%dT%H:%M')
                tiempo = fecha2_dt - fecha1_dt
                tiempo = tiempo.total_seconds() / 60
                tarifa = Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).first()
                if tiempo <= tarifa.tolerancia:
                    total = 0
                elif tiempo <= 120:
                    total = tarifa.primerasDos
                elif tiempo >= 121:
                    tiempo = tiempo - 120
                    if tiempo <= 59:
                        total = tarifa.primerasDos + tarifa.extra
                    else:
                        total = (tiempo // 60) * tarifa.extra + tarifa.primerasDos
                Ticket.query.filter_by(id=request.form['codigo']).update(
                    dict(costo=total))
            else:
                success_message = 'No puedes pagar un boleto que no te corresponde'
                flash(success_message)
                return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

        return render_template('ticketSalida.html', est=esta, usuario=username, boleto=boleto, total=total,
                               salida=fecha2_dt)
    else:
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)



@app.route('/calSalidasuper', methods=['GET', 'POST'])  # Terminado
def calSalidasuper():
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username=username).first()
    boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
    title = "Salidas"
    tickets = Ticket.query.filter_by(estacionamiento=esta.estacionamiento).all()

    if boleto is None:  # Verificar si el boleto no existe
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('superpago.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

    if boleto.costo is None:
        if request.method == 'POST':

            fecha_hora_actual = datetime.now()

            Ticket.query.filter_by(id=request.form['codigo']).update(
                dict(salida=fecha_hora_actual)
            )
            db.session.commit()
            total = 0

            Ticket.query.filter_by(id=request.form['codigo']).update(
                dict(costo=total)
            )
            db.session.commit()


        success_message = 'Su pago ha sido registrado correctamente'
        flash(success_message)
        return render_template('superpago.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

    else:
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('superpago.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)
































@app.route('/codigo/<int:codigo>')
def codigo(codigo):
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username=username).first()
    total = 0
    boleto = Ticket.query.filter_by(id=codigo).first()
    title = "Salidas"
    tickets = Ticket.query.filter_by(estacionamiento=esta.estacionamiento).all()

    if boleto is None:  # Verificar si el boleto no existe
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

    if boleto.costo is None:
        if request.method == 'POST':
            if boleto.encargado == session['username']:
                Ticket.query.filter_by(id=request.form['codigo']).update(
                    dict(salida=request.form['salida']))

                boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
                fecha1_dt = datetime.strptime(str(boleto.entrada), '%Y-%m-%d %H:%M:%S')
                fecha2_dt = datetime.strptime(str(request.form['salida']), '%Y-%m-%dT%H:%M')
                tiempo = fecha2_dt - fecha1_dt
                tiempo = tiempo.total_seconds() / 60
                tarifa = Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).first()
                if tiempo <= 15:
                    total = 0
                elif tiempo <= 120:
                    total = tarifa.primerasDos
                elif tiempo >= 121:
                    tiempo = tiempo - 120
                    if tiempo <= 59:
                        total = tarifa.primerasDos + tarifa.extra
                    else:
                        total = (tiempo // 60) * tarifa.extra + tarifa.primerasDos
                Ticket.query.filter_by(id=request.form['codigo']).update(
                    dict(costo=total))

            else:
                success_message = 'No puedes pagar un boleto que no te corresponde'
                flash(success_message)
                return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

        return render_template('ticketSalida.html', est=esta, usuario=username, boleto=boleto, total=total,salida=boleto.salida)
    else:
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)


@app.route('/ticSalida', methods=['GET', 'POST'])  # Terminado
def ticSalida():
    if 'username' in session:
        username = session['username']
    esta = User.query.filter_by(username=username).first()
    boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
    title = "Salidas"
    tickets = Ticket.query.filter_by(estacionamiento=esta.estacionamiento).all()

    if boleto is None:  # Verificar si el boleto no existe
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)

    if boleto.costo is None:
        if request.method == 'POST':

            boleto = Ticket.query.filter_by(id=request.form['codigo']).first()
            Ticket.query.filter_by(id=boleto.id).update({'salida': request.form['salida']})
            db.session.commit()
            fecha1_dt = datetime.strptime(str(boleto.entrada), '%Y-%m-%d %H:%M:%S')
            fecha2_dt = datetime.strptime(str(request.form['salida']), '%Y-%m-%d %H:%M:%S')
            tiempo = fecha2_dt - fecha1_dt
            tiempo = tiempo.total_seconds() / 60
            tarifa = Tarifa.query.filter_by(estacionamiento=esta.estacionamiento).first()
            if tiempo <= tarifa.tolerancia:
                total = 0
            elif tiempo <= 120:
                total = tarifa.primerasDos
            elif tiempo >= 121:
                tiempo = tiempo - 120
                if tiempo <= 59:
                    total = tarifa.primerasDos + tarifa.extra
                else:
                    total = (tiempo // 60) * tarifa.extra + tarifa.primerasDos
            Ticket.query.filter_by(id=request.form['codigo']).update(
                dict(costo=total))
            db.session.commit()
        return render_template('ticketSalidaPago.html', est=esta, usuario=username, boleto=boleto, total=total,
                               salida=boleto.salida)
    else:
        total = 0
        success_message = 'Ticket invalido'
        flash(success_message)
        return render_template('salidas.html', title=title, estacionamiento=esta, ticket=tickets, usuario=username)


def gen_pdf(idBoleto):
    pdf_filename = f"Boleto_{idBoleto}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=(460, 445), title=f"Boleto {idBoleto}")
    boleto = Boletos.query.filter_by(idBoleto=idBoleto).first()
    qr_image = Image(BytesIO(base64.b64decode(boleto.qr_code)))
    qr_image.drawHeight = 1.5 * inch * qr_image.drawHeight / qr_image.drawWidth
    qr_image.drawWidth = 1.5 * inch

    # Datos para la tabla
    data_table = [
        ["Estatus", str(boleto.estatus)],
        ["El código de su ticket es:", str(boleto.idBoleto)],
        ["El estacionamiento es:", str(boleto.estacionamiento)],
        ["La hora de entrada es:", str(boleto.hora_entrada)],
    ]

    # Definir la tabla
    table = Table(data_table, colWidths=[2.5 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('SHADOW', (0, 0), (-1, -1), 5, 5, colors.gray)
    ]))

    data_qr = [[qr_image]]
    table_qr = Table(data_qr, colWidths=[1 * inch, 1 * inch])
    table_qr.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    texto1 = f"Información del boleto {idBoleto}."
    texto3 = f"© Estacionamientos SISCON"
    # Estilos para el párrafo
    styles = getSampleStyleSheet()
    paragraph_style = ParagraphStyle(
        "CustomParagraph",
        parent=styles["Normal"],
        fontSize=10,
        alignment=1,
    )
    paragraph_style3 = ParagraphStyle(
        "CustomParagraph",
        parent=styles["Normal"],
        fontSize=20,
        alignment=1,
    )
    paragraph_style2 = ParagraphStyle(
        "CustomParagraph",
        parent=styles["Normal"],
        fontSize=15,
        alignment=1,
    )

    texto2 = f"Para Pagar o Consultar el estatus del ticket escanee el Código QR:"
    spacer = Spacer(1, 0.2 * inch)
    content = [Paragraph(texto3, paragraph_style3), spacer, spacer, Paragraph(texto1, paragraph_style2), spacer,
                table, spacer, Paragraph(texto2, paragraph_style), table_qr]
    doc.build(content)
    return pdf_filename


@app.route('/boleto/<int:idBoleto>')
def boleto(idBoleto):
    pdf = gen_pdf(idBoleto)
    return send_file(pdf, as_attachment=True)


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
                    telefono = create_form.telefono.data,
                    lugares = 0)
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
                        pension_dia=200,
                        pension_semana=1000,
                        pension_mes=4000,
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

    app.run(port=8000)