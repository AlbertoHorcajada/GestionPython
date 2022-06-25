'''
@Author Alberto Horcajada Perez
@Version 1.0   on 15 feb 2022
'''

'''
Como he planteado las tablas de la BBDD?? decidí hacer 2 tablas, una que se encarga de 
almacenar el usuario y la contraseña para la hora de iniciar sesion con las credenciales siendo
el usuario la clave principal, y la clave foranea de la tabla de vacaciones, la tabla de vacaciones
tiene como PK el usuario y el mes, y luego cuenta con 3 TyniInt, que serán los dias que ha disfrutado
de un mes, los dias disponibles de vacaciones y los dias que tiene reservados
'''


import re
import mysql.connector

class bbdd():
    '''
    La funcion contructor la uso para crear los atributos de la clase dejandolos a None
    para no crear una conexion solo por instanciar la clase ya que seria un fallo de seguridad
    tambien creo a configuracion que se va a usar para conectarme
    '''
    def __init__(self) -> None:
        self.config = {"user":"root", "password":"rootroot","host":"localhost"}
        self.conn = None
        self.cursor = None

    def __usarBBDD(self):
        sql = "USE practicaFinal"
        self.cursor.execute(sql)

    #En esta funcion creo la conexion con mysql
    def abrirConexion(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
    
    
    #Esta funcion la usare al principio para ccrera las tablas e ingresar algun dato predefinido para probar todoo un poco
    def crearTablas(self):
        self.abrirConexion()
        #Crear de nuevo la BBDD eliminando primero por si existiese
        sql = "DROP SCHEMA IF EXISTS practicaFinal"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "CREATE SCHEMA practicaFinal"
        self.cursor.execute(sql)
        self.__usarBBDD()

        #Crear tabla usuario
        sql = "CREATE TABLE usuario(\n"
        sql +="nombre VARCHAR(30) PRIMARY KEY,\n"
        sql +="psswd VARCHAR(30),\n"
        sql +="adm TINYINT)Engine=InnoDB"
        self.cursor.execute(sql)
        self.conn.commit()
        #crear tabla de las horas disfrutadas
        sql = "CREATE TABLE vacaciones(\n"
        sql +="nombre VARCHAR(30),\n"
        sql +="mes VARCHAR(12),\n"
        sql +="disponibles TINYINT,\n"
        sql +="disfrutados TINYINT,\n"
        sql +="reservados TINYINT,\n"
        sql += "foreign key(nombre) references usuario(nombre),\n"
        sql +="primary key(nombre,mes))Engine=InnoDB"
        self.cursor.execute(sql)
        self.conn.commit()

        #Inseserto un par de datos para hacer mas pruebas

        self.__insertarDatos()

        self.cerrarConexion()

    def __insertarDatos(self):
        #Insertar datos en la tabla de usuarios
        sql = "INSERT INTO usuario(nombre,psswd,adm) VALUES ('admin','admin',1)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO usuario(nombre,psswd,adm) VALUES ('user1','user1',0)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO usuario(nombre,psswd,adm) VALUES ('user2','user2',0)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO usuario(nombre,psswd,adm) VALUES ('user3','user3',0)"
        self.cursor.execute(sql)
        self.conn.commit()
        #Insertar datos en la tabla de horas disfrutadas
        #Usuario 1
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user1','ene',2,2,2)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user1','abr',2,1,3)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user1','jul',3,4,3)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user1','oct',4,2,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user1','may',5,1,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        #Usuario 2
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user2','feb',0,2,4)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user2','may',0,0,0)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user2','ago',3,1,5)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user2','nov',4,1,0)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user2','sep',2,1,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        #Usuario 3
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user3','mar',3,2,2)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user3','jun',4,2,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user3','sep',2,3,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user3','dic',1,2,4)"
        self.cursor.execute(sql)
        self.conn.commit()
        sql = "INSERT INTO vacaciones(nombre, mes, disponibles, disfrutados, reservados) VALUES ('user3','ene',2,2,1)"
        self.cursor.execute(sql)
        self.conn.commit()
        #Insertar datos en la tabla de disponibles

    #Con esta funcion cierro la conexion y la usare cada vez que llamo a cualquier funcion para no dejar la conexion abierta
    def cerrarConexion(self):
        self.conn.close()
    '''
    Funcion que me comprueba si el usuario que me pasa coincide con su contrasenia
    No la paso por la otra funcion de comprobar si existe el usuario porque ya me ocupo
    de ello con el try except
    '''
    def iniciarSesion(self, usuario, psswd)-> bool:
        exito = False
        self.abrirConexion()
        self.__usarBBDD()
        sql = "SELECT psswd FROM usuario WHERE nombre = '" + usuario + "'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        try:
            passTabla = resultado[0][0]
            if(psswd == passTabla):
                exito = True
        except:
            exito = False
            
        self.cerrarConexion()
        return exito
    '''
    Funcion que me comprueba si existe un usuario, compruebo si me da algun resultado
    al seleccionar por nombre de usuario, si me da alguno existe si no no
    '''
    def existeUsuario(self,usu):
        existe = False
        self.abrirConexion()
        self.__usarBBDD()
        sql = "SELECT * FROM usuario WHERE nombre = '" + usu + "'"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if(len(res)>0):
            existe = True
        self.cerrarConexion()
        return existe
    '''
    Funcion que se ocupa de cambiar la contraseña de un usuario, primero comprueba que existe, si no 
    no hace nada, si existe lanza la consulta de actualizacion
    '''
    def cambioContrasenia(self,usu,passwd):
        if(self.existeUsuario(usu=usu)):
            self.abrirConexion()
            self.__usarBBDD()
            try:
                sql = "UPDATE usuario SET psswd = '" + passwd + "' WHERE nombre = '" + usu + "'"
                self.cursor.execute(sql)
                self.conn.commit()
                exito = True
            except:
                exito = False
            self.cerrarConexion()
        else:
            exito = False
        return exito

    '''
    Funcion que comprueba si un usuario es admiistrador o no partiendo de la siguiente logica:
    0: Usuario normal
    1: Usuario administrador
    '''
    def isAdmin(self, usu):
        admin = False
        if(self.existeUsuario(usu=usu)):
            self.abrirConexion()
            self.__usarBBDD()
            sql = "SELECT adm FROM usuario WHERE nombre ='" + usu + "'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if(result[0][0]==1):
                admin = True
            self.cerrarConexion()
        return admin
    
    def buscarInfoUsuario(self, usu):
        resultado = ""
        
        if self.existeUsuario(usu):
            if not(self.isAdmin(usu)):
                self.abrirConexion()
                self.__usarBBDD()
                sql = "SELECT * FROM vacaciones WHERE nombre = '" + usu + "'"
                self.cursor.execute(sql)
                resultado = self.cursor.fetchall()
            else:
                resultado="admin"
        self.cerrarConexion()
        return resultado
    
    def diasdisponiblesPorMes(self, usu, mes):
        if(self.existeUsuario(usu)):
            self.abrirConexion()
            self.__usarBBDD()
            sql = "SELECT disponibles FROM vacaciones WHERE nombre = '" + usu + "' AND mes = '" + mes + "'"
            try:
                self.cursor.execute(sql)
                resultado = self.cursor.fetchall()
                self.cerrarConexion()
                return resultado[0][0]
            except:
                self.cerrarConexion()
                return 0
    

    def diasReservadosPorMes(self, usu, mes):
        if(self.existeUsuario(usu)):
            self.abrirConexion()
            self.__usarBBDD()
            sql = "SELECT reservados FROM vacaciones WHERE nombre = '" + usu + "' AND mes = '" + mes + "'"
            try:
                self.cursor.execute(sql)
                resultado = self.cursor.fetchall()
                self.cerrarConexion()
                return resultado[0][0]
            except:
                self.cerrarConexion()
                return 0
            

    def quitarDiasReservados(self,usu,mes,dias):
        exito = False
        if(self.existeUsuario(usu)):
            reservados = self.diasReservadosPorMes(usu=usu,mes=mes)
            if(not(dias>reservados)):
                self.abrirConexion()
                self.__usarBBDD()
                reservados = reservados-dias
                sql = "UPDATE vacaciones SET reservados =" + str(reservados) + " WHERE nombre= '" + usu + "' AND mes = '" + mes + "'"
                
                try:
                    self.cursor.execute(sql)
                    self.conn.commit()
                    exito = True
                except:
                    pass
        
                self.cerrarConexion()
        return exito

    def devolverVacacionesYMeses(self):
        sql = "SELECT nombre, mes, disfrutados FROM vacaciones ORDER BY nombre, mes"
        self.abrirConexion()
        self.__usarBBDD()
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.cerrarConexion()
        return resultado

    def vacacionesPorMes(self):
        sql = "select sum(disfrutados) from vacaciones group by mes order by mes"
        self.abrirConexion()
        self.__usarBBDD()
        try:
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
        except:
            resultado = 0
        
        self.cerrarConexion()
        return resultado

    def hacerReserva(self,usu,mes,dias):
        reservados = self.diasReservadosPorMes(mes=mes, usu=usu)
        disponibles = self.diasdisponiblesPorMes(usu=usu,mes=mes)
        
        if(disponibles<reservados):
            exito = False
        else:
            restantes = disponibles-reservados
            self.abrirConexion()
            self.__usarBBDD()
            #Sumo a los dias que quiere reservar los que ya tenia reservados
            dias +=reservados
            sql1 = "UPDATE vacaciones SET reservados =" + str(dias) + " WHERE nombre= '" + usu + "' AND mes = '" + mes + "'"
            sql2= "UPDATE vacaciones SET disponibles = " + str(restantes) + " WHERE nombre= '" + usu + "' AND mes = '" + mes + "'"
            try:
                self.cursor.execute(sql1)
                self.conn.commit()
                self.cursor.execute(sql2)
                self.conn.commit()
                exito = True
            except:
                exito=False
            self.cerrarConexion()

        return exito
    
    
                        