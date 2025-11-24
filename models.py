class Usuario:
    def __init__(self, id, nombre, apellido, edad, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.fecha_creacion = fecha_creacion
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'fecha_creacion': self.fecha_creacion
        }

class Correo:
    def __init__(self, id, usuario_id, tipo, correo, fecha_creacion=None, nombre=None, apellido=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.correo = correo
        self.fecha_creacion = fecha_creacion
        self.nombre = nombre
        self.apellido = apellido
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'correo': self.correo,
            'fecha_creacion': self.fecha_creacion,
            'nombre': self.nombre,
            'apellido': self.apellido
        }