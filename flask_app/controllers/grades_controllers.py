from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos modelo
from flask_app.models.users import User
from flask_app.models.grades import Grade


#Importación de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/grades')
def new_grades():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_grades.html',user=user )

@app.route('/create/grades', methods=['POST'])
def create_grade():

    if 'user_id' not in session:
        return redirect('/')


    #Validacion de calificacion
    if not Grade.valida_calificacion(request.form):
        return redirect('/new/grades')

    Grade.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/grade/<int:id>')
def edite_grade(id):
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Cual es la calificacion que se va a editar
    formulario_calificacion = {"id": id}
    grade = Grade.get_by_id(formulario_calificacion)

    return render_template('edit_grade.html', user=user, grade=grade)


@app.route('/update/grade', methods=['POST'])
def update_grade():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación de Calificación
    if not Grade.valida_calificacion(request.form):
        return redirect('/edit/grade/'+request.form['id']) #/edit/grade/1
    
    Grade.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/grade/<int:id>')
def delete_grade(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Grade.delete(formulario)

    return redirect('/dashboard')








