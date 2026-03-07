from . import maestros
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
import forms
from models import db, Maestros

@maestros.route('/perfil/nombres/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros", methods=['GET', 'POST'])
def listamaestros():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
    return render_template("maestros/maestros_lista.html", form=create_form, maestros=maestros)

@maestros.route("/maestros/agregar", methods=['GET', 'POST'])
def maestrosagregar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        create_form.descripcion.data = "Sin descripción" 
        create_form.idmaestro.data = 0 
        
        if create_form.validate():
            maestro_new = Maestros(
                nombre=create_form.nombre.data,
                apellidos=create_form.apellidos.data,
                especialidad=create_form.especialidad.data,
                email=create_form.email.data
            )
            db.session.add(maestro_new)
            db.session.commit()
            return redirect(url_for('maestros.listamaestros'))        
    return render_template("maestros/maestros_agregar.html", form=create_form)

@maestros.route("/maestros/detalles", methods=['GET', 'POST'])
def maestrosdetalles():
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        # select * from maestros where matricula=matricula
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        nombre = maestro1.nombre
        apellidos = maestro1.apellidos
        especialidad = maestro1.especialidad
        email = maestro1.email
    return render_template('maestros/maestros_detalles.html', id=id, nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email)

@maestros.route("/maestros/modificar", methods=['GET', 'POST'])
def maestrosmodificar():
    create_form = forms.UserForm(request.form) 
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maestro1:
            create_form.matricula.data = maestro1.matricula
            create_form.nombre.data = maestro1.nombre
            create_form.apellidos.data = maestro1.apellidos
            create_form.especialidad.data = maestro1.especialidad
            create_form.email.data = maestro1.email
            
    if request.method == 'POST':
        create_form.descripcion.data = "Sin descripción"
        create_form.idmaestro.data = 0

        if create_form.validate():
            matricula = create_form.matricula.data
            maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
            
            if maes:
                maes.nombre = create_form.nombre.data
                maes.apellidos = create_form.apellidos.data
                maes.especialidad = create_form.especialidad.data
                maes.email = create_form.email.data
                db.session.commit()
                return redirect(url_for('maestros.listamaestros'))
    return render_template("maestros/maestros_modificar.html", form=create_form)

@maestros.route("/maestros/eliminar", methods=['GET', 'POST'])
def maestroseliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maestro1:
            create_form.matricula.data = maestro1.matricula
            create_form.nombre.data = maestro1.nombre
            create_form.apellidos.data = maestro1.apellidos
            create_form.especialidad.data = maestro1.especialidad
            create_form.email.data = maestro1.email
        
    if request.method == 'POST':
        matricula = create_form.matricula.data
        maes = db.session.get(Maestros, matricula)
        if maes:
            db.session.delete(maes)
            db.session.commit()
        return redirect(url_for('maestros.listamaestros'))
        
    return render_template("maestros/maestros_eliminar.html", form=create_form)