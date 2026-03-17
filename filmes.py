from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=True)
    genero = Column(String(100), nullable=True)
    ano_lancamento = Column(Integer)
    nota = Column(Float)
    disponivel = Column(Boolean, default=True)

    def __init__(self, nome_filme, genero_filme, ano_filme, nota_filme, disponivel=True):
        self.titulo = nome_filme
        self.genero = genero_filme
        self.ano_lancamento = ano_filme
        self.nota = nota_filme
        self.disponivel = disponivel

    def __repr__(self):
        print(f"Titulo: {self.titulo} | Genero:{self.genero} | Ano de Lançamento:{self.ano_lancamento} | Nota:{self.nota} | Disponibilidade:{self.disponivel}")


engine = create_engine("sqlite:///catalogo_filmes.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def cadastrar_filme():
    print("\n--- CADASTRAR FILMES ---")

    nome_filme = input("Digite o titulo do filme: ")
    genero = input("Digite o genero do filme: ")
    ano = int(input("Digite o ano de lançamento do filme: "))
    nota = float(input("Digite a nota do filme: "))

    with Session() as session:
        try:
            buscar_filme = session.query(Filme).filter_by(
                titulo=nome_filme,
                ano_lancamento=ano
            ).first()

            if buscar_filme is None:
                novo_filme = Filme(nome_filme, genero, ano, nota)
                session.add(novo_filme)
                session.commit()
                print("Filme cadastrado com sucesso")

            else:
                print("Já existe um filme com esse título e ano")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

def listar_filmes():
    print(f"--- FILMES CADASTRADOS ---")
    with Session() as session:
        try:
            conferir_tabela = session.query(Filme).all()

            if conferir_tabela is None:
                print(F"Sua tabela esta vazia")
            else:
                for f in conferir_tabela:
                    print(f)
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

def atualizar_filmes():
    print(F"--- ATUALIZE UM FILME ---")
    id_atualizar = int(input("Digite o ID do filme que você quer atualizar: "))
    with Session() as session:
        try:
            validar = session.query(Filme).filter_by(id=id_atualizar).first()
            if validar is None:
                print(F"Filme com ID{id_atualizar}, não encontrado na tabela")
            else:
                nome_filme = input("Digite o titulo do filme: ")
                genero = input("Digite o genero do filme: ")
                ano = int(input("Digite o ano de lançamento do filme: "))
                nota = float(input("Digite a nota do filme: "))
                validar.titulo, validar.genero, validar.ano_lancamento, validar.nota = nome_filme, genero, ano, nota
                session.commit()
                print("Filme atualizado com sucesso com sucesso")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

    
atualizar_filmes()