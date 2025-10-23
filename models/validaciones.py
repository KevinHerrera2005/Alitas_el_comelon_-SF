import re
from flask import flash, redirect, url_for

def validar_datos_registro(username, password, nombre, apellido, telefono, direccion, metodo_pago, numero_tarjeta):
    
    from models.login_crear_usuario import Usuario

    # Campos sin nada
    if not all([username, password, nombre, apellido, telefono, direccion, metodo_pago]):
        flash('Completa todos los campos obligatorios.', 'warning')
        return redirect(url_for('registro'))

    # nombre y apellido
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñ ]+$', nombre):
        flash('El nombre solo puede contener letras y espacios.', 'warning')
        return redirect(url_for('registro'))

    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñ ]+$', apellido):
        flash('El apellido solo puede contener letras y espacios.', 'warning')
        return redirect(url_for('registro'))

    #username
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        flash('El nombre de usuario solo puede contener letras, números y guiones bajos (sin espacios ni símbolos).', 'warning')
        return redirect(url_for('registro'))

    #duplicado 
    usuario_existente = Usuario.query.filter_by(Username=username).first()
    if usuario_existente:
        flash('Este usuario ya existe. Por favor elige otro.', 'danger')  # mensaje solicitado
        return redirect(url_for('registro'))

    #teléfono 
    if not telefono.isdigit():
        flash('El número de teléfono solo puede contener dígitos.', 'warning')
        return redirect(url_for('registro'))

    if len(telefono) < 8 or len(telefono) > 15:
        flash('El número de teléfono debe tener entre 8 y 15 dígitos.', 'warning')
        return redirect(url_for('registro'))

    #método de pago
    if metodo_pago not in ["tarjeta", "efectivo", "mixto"]:
        flash('Selecciona un método de pago válido.', 'danger')
        return redirect(url_for('registro'))

    #Si es tarjeta, validar número de tarjeta
    if metodo_pago == "tarjeta":
        if not numero_tarjeta or not numero_tarjeta.isdigit():
            flash('El número de tarjeta solo puede contener números.', 'warning')
            return redirect(url_for('registro'))
        if len(numero_tarjeta) != 16:
            flash('El número de tarjeta debe tener exactamente 16 dígitos.', 'warning')
            return redirect(url_for('registro'))

    #contraseña
    if len(password) < 10:
        flash('La contraseña debe tener al menos 10 caracteres.', 'warning')
        return redirect(url_for('registro'))

    if not re.search(r'[A-Z]', password):
        flash('La contraseña debe contener al menos una letra mayúscula.', 'warning')
        return redirect(url_for('registro'))

    if not re.search(r'[a-z]', password):
        flash('La contraseña debe contener al menos una letra minúscula.', 'warning')
        return redirect(url_for('registro'))

    if not re.search(r'\d', password):
        flash('La contraseña debe contener al menos un número.', 'warning')
        return redirect(url_for('registro'))

    if not re.search(r'[^A-Za-z0-9]', password):
        flash('La contraseña debe contener al menos un símbolo (por ejemplo: !@#$%).', 'warning')
        return redirect(url_for('registro'))

    
    if metodo_pago in ["efectivo", "mixto"]:
        numero_tarjeta = ""

    return None
