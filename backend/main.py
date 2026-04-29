from database import get_db, criar_tabelas
import user_crud as repo

# Garante que a tabela existe
criar_tabelas()

with get_db() as db:

    # ALTERAR SENHA
    print("Alterando senha do usuário 'ale'...")
    usuario_atualizado = repo.atualizar_senha(db, "ale", "nova123")

    if usuario_atualizado:
        print(f"Senha atualizada para: {usuario_atualizado.username}")
    else:
        print("Usuário não encontrado para atualização.")


    # EXCLUIR USUÁRIO
    print("\nExcluindo usuário 'teste'...")
    sucesso = repo.deletar_usuario(db, "teste")

    if sucesso:
        print("Usuário deletado com sucesso.")
    else:
        print("Usuário não encontrado para exclusão.")


    # LISTAR USUÁRIOS ATUAIS
    print("\nUsuários restantes:")
    usuarios = repo.listar_usuarios(db)
    
    for u in usuarios:
        print(f"- {u['username']}")