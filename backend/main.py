from database import criar_tabelas, get_db
import user_crud as repo

# Cria as tabelas automaticamente
criar_tabelas()

# Teste conexão com backend
with get_db() as db:
    print("Criando usuário...")
    repo.criar_usuario(db, "ale", "123456")

    print("Buscando usuário...")
    usuario = repo.buscar_usuario_por_username(db, "ale")
    print(usuario.username)

    print("Validando senha...")
    print(repo.verificar_senha(usuario, "123456"))

    print("Listando usuários...")
    print(repo.listar_usuarios(db))