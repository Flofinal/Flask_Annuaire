from flask_login import UserMixin


class User(UserMixin):
    def __init__(self,id,email,password,name,numero,role):
        self.name=name
        self.id=id
        self.email=email
        self.password=password
        self.numero=numero
        self.role=role
