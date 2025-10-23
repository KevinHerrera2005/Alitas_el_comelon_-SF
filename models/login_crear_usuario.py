from flask import render_template, request, redirect, url_for, flash
from Main import app, db  # Importa la app y la conexión desde Main
import re
from models.validaciones import validar_datos_registro  # Importamos las validaciones externas

class MetodoPago(db.Model):
    __tablename__ = 'Metodo_de_pago'
    ID_Metodo_de_pago = db.Column(db.Integer, primary_key=True)
    Tipo = db.Column(db.SmallInteger, nullable=False)  # 1=tarjeta, 2=efectivo, 3=mixto
    Numero_Tarjeta = db.Column(db.String(16), nullable=False)
    Descripcion = db.Column(db.String(50))

class Usuario(db.Model):
    __tablename__ = 'Usuarios_cliente'
    ID_Usuario_ClienteF = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    telefono = db.Column(db.String(50), nullable=False)
    ID_sucursal = db.Column(db.Integer, nullable=False)
    ID_Metodo_de_pago = db.Column(db.Integer, db.ForeignKey('Metodo_de_pago.ID_Metodo_de_pago'))

class Direccion(db.Model):
    __tablename__ = 'Direcciones'
    ID_Direccion = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)

class DireccionCliente(db.Model):
    __tablename__ = 'Direccion_del_cliente'
    ID_US_CO = db.Column(db.Integer, primary_key=True)
    ID_Usuario_ClienteF = db.Column(db.Integer, nullable=False)
    Descripcion = db.Column(db.String(200), nullable=False)
    ID_Direccion = db.Column(db.Integer, db.ForeignKey('Direcciones.ID_Direccion'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(Username=username, password=password).first()
        if usuario:
            flash(f'Bienvenido {usuario.nombre}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        metodo_pago = request.form.get('metodo_pago')
        numero_tarjeta = request.form.get('numero_tarjeta')

        error = validar_datos_registro(username, password, nombre, apellido, telefono, direccion, metodo_pago, numero_tarjeta)
        if error:
            return error 

        if metodo_pago == "tarjeta":
            tipo = 1
            numero = numero_tarjeta if numero_tarjeta else "0000000000000000"
        elif metodo_pago == "efectivo":
            tipo = 2
            numero = "9999999999999999"
        elif metodo_pago == "mixto":
            tipo = 3
            numero = "0000000000000000"
        else:
            flash("Método de pago inválido.", "danger")
            return redirect(url_for('registro'))

        nuevo_metodo = MetodoPago(Tipo=tipo, Numero_Tarjeta=numero, Descripcion=metodo_pago)
        db.session.add(nuevo_metodo)
        db.session.commit()

        nuevo_usuario = Usuario(
            Username=username,
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            ID_sucursal=1,
            ID_Metodo_de_pago=nuevo_metodo.ID_Metodo_de_pago
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        direccion_base = Direccion(descripcion=direccion)
        db.session.add(direccion_base)
        db.session.commit()

        nueva_direccion = DireccionCliente(
            ID_Usuario_ClienteF=nuevo_usuario.ID_Usuario_ClienteF,
            Descripcion=direccion,
            ID_Direccion=direccion_base.ID_Direccion
        )
        db.session.add(nueva_direccion)
        db.session.commit()

        flash("Usuario registrado exitosamente.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/dashboard')
def dashboard():
    return "<h1 style='text-align:center;margin-top:20%;'>Bienvenido al panel de Alitas El Comelón</h1>"
