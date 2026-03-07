from . import alumnos
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
import forms
from models import db, Alumnos

@alumnos.route('/perfil/nombres/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@alumnos.route("/alumnos", methods=['GET', 'POST'])
def index():
    create_form = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("alumnos/alumnos_lista.html", form=create_form, alumno=alumno)

@alumnos.route("/alumnosagregar", methods=['GET', 'POST'])
def agregar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.index'))       
    return render_template("alumnos/alumnos_agregar.html", form=create_form)

@alumnos.route("/alumnos/detalles", methods=['GET'])
def detalles():
    id_alumno = request.args.get('id')    
    alumno1 = db.session.query(Alumnos).filter(Alumnos.id == id_alumno).first()
    
    if not alumno1:
        return "Alumno no encontrado", 404
  
    return render_template('alumnos/alumnos_detalles.html', 
                           nombre=alumno1.nombre, 
                           apellidos=alumno1.apellidos, 
                           email=alumno1.email, 
                           telefono=alumno1.telefono,
                           cursos=alumno1.cursos)


@alumnos.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form) 
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        id = create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum:
            alum.nombre = create_form.nombre.data
            alum.apellidos = create_form.apellidos.data
            alum.email = create_form.email.data
            alum.telefono = create_form.telefono.data
            db.session.commit()
        return redirect(url_for('alumnos.index'))
        
    return render_template("alumnos/alumnos_modificar.html", form=create_form)

@alumnos.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        
    if request.method == 'POST':
        id = create_form.id.data
        alum = db.session.get(Alumnos, id)
        if alum:
            db.session.delete(alum)
            db.session.commit()
        return redirect(url_for('alumnos.index'))
        
    return render_template("alumnos/alumnos_eliminar.html", form=create_form)