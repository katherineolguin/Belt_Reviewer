from flask_app.config.mysqlconnection import connectToMySQL #IMPORTACION CON BASE DATOS
from flask import flash #Encargado de mostrar mensajes o errores

from datetime import datetime  #Manipular fechas


import re #Importando las expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class Grade:

    def __init__(self, data):

        self.id = data['id']
        self.alunmo = data['alunmo']
        self.stack = data['stack']
        self.fecha = data['fecha']
        self.calificacion = data['calificacion']
        self.cinturon = data['cinturon']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.user_id = data['user_id']

    @staticmethod
    def valida_calificacion(formulario):

        es_valido = True

        if formulario['alunmo'] == '':
            flash ('Alumno no puede ser vacio', 'grades')
            es_valido = False

        if formulario['calificacion'] == '':
            flash('Ingrese una calificacion','grades')
            es_valido = False
        
        else:

            if int(formulario['calificacion']) < 1 or int(formulario['calificacion']) > 10:
                flash ('Calificación debe ser entre 1 y 10', 'grades')
                es_valido = False

        if formulario ['fecha'] =='':
            flash('Debe ingresar una fecha', 'grades')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['fecha'], '%Y-%m-%d') #Estamos transformando un tecto a formato de fecha

            hoy = datetime.now() #me da la fecha de hoy
            if hoy < fecha_obj:
                flash('La fecha debe ser en pasado', 'grades')
                es_valido = False
        
        return es_valido
        
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO grades(alunmo, stack, fecha, calificacion, cinturon, user_id)VALUES( %(alunmo)s,  %(stack)s,  %(fecha)s,  %(calificacion)s,  %(cinturon)s,  %(user_id)s )"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM grades"
        results = connectToMySQL('belt_reviewer').query_db(query) #Lista de Diccionarios
        grades = []

        for grade in results:
            grades.append(cls(grade)) #1.- cls(grade) crea una instancia en base al diccionario. 2.- grades.append() me agrega esa instancia a mi lista
        
        return grades

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM grades WHERE id = %(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        grade = cls(result[0])
        return grade

    @classmethod
    def update(cls, formulario):
        query = "UPDATE grades SET alunmo=%(alunmo)s, stack=%(stack)s, fecha=%(fecha)s, calificacion=%(calificacion)s, cinturon=%(cinturon)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM grades WHERE id = %(id)s"
        result = connectToMySQL('belt_reviewer').query_db(query, formulario)
        return result

                


                
            


