from sqlalchemy.orm import Session
from database import UsuarioChatbot
import bcrypt


def criar_usuario(db: Session, username: str, senha: str):
    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    usuario = UsuarioChatbot(
        username=username,
        senha_hash=senha_hash
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def buscar_usuario_por_username(db: Session, username: str):
    return db.query(UsuarioChatbot).filter(
        UsuarioChatbot.username == username
    ).first()


def listar_usuarios(db: Session):
    usuarios = db.query(UsuarioChatbot).all()
    return [{"id": u.id, "username": u.username} for u in usuarios]

def atualizar_senha(db: Session, username: str, nova_senha: str):
    usuario = buscar_usuario_por_username(db, username)

    if not usuario:
        return None

    usuario.senha_hash = bcrypt.hashpw(
        nova_senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    db.commit()
    db.refresh(usuario)

    return usuario


def deletar_usuario(db: Session, username: str):
    usuario = buscar_usuario_por_username(db, username)

    if not usuario:
        return False

    db.delete(usuario)
    db.commit()

    return True


def verificar_senha(usuario, senha: str) -> bool:
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        usuario.senha_hash.encode("utf-8")
    )