from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

#Criara classe base do ORM
Base = declarative_base()

class Usuario(Base):
    #Definir o nome da tabela
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    #Campo nome obrigatorio
    nome = Column(String(100), nullable=True)
    #unique=True > não é permitido e-mail repetido
    email = Column(String(100), nullable=True, unique=True)
    idade = Column(Integer)
    ativo = Column(Boolean, default=True)
    salario = Column(Float)

    def __init__(self, nome, email, idade, salario):
        self.nome = nome
        self.email = email
        self.idade = idade
        self.salario = salario

#Criar a conexão
engine = create_engine("sqlite:///empresa.db")

#Criar as tabelas
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    try: 
        #Buscando o usuario com o mesmo e-mail
        usuario_existente = session.query(Usuario).filter_by(email="cassioasrosa@gmail.com").first()
        if usuario_existente == None:
            #Criar um objeto
            usuario1 = Usuario("Cassio", "cassioasrosa@gmail.com",16,5000)
            session.add(usuario1)
            session.commit()
            print("Usuario cadastrado com sucesso")
        else:
            print("Ja existe um cadastro com esse e-mail")

    except Exception as erro:
        session.rollback()
        print(f"Ocorreu um erro : {erro}")

    