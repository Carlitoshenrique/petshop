from conexao import conectar
from mysql.connector import Error
from typing import Any
import validador


def cadastrar_cliente(nome, cpf, telefone):
    nome = nome.strip()
    cpf = cpf.strip()
    telefone = telefone.strip()

    if not validador.validar_nome(nome, "Nome"):
        return
    if not validador.validar_cpf(cpf):
        return
    if not validador.validar_telefone(telefone):
        return

    cpf = validador.formatar_cpf(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Cliente (nome, cpf, telefone)
            VALUES (%s, %s, %s)
            """,
            (nome, cpf, telefone)
        )

        conexao.commit()
        print("\n[Sucesso] Cliente cadastrado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Não foi possível cadastrar o cliente (CPF pode estar duplicado): {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM Cliente ORDER BY nome")
        clientes: list[tuple[Any, ...]] | Any = cursor.fetchall()

        if len(clientes) == 0:
            print("\nNenhum cliente cadastrado.")
        else:
            print("\n==================== LISTA DE CLIENTES ====================")
            print(f"{'CPF':<18} | {'Nome':<25} | {'Telefone':<15}")
            print("-" * 65)
            for c in clientes:
                # Mascarar CPF vindo do banco
                cpf_formatado = validador.formatar_cpf(c[2])
                print(f"{cpf_formatado:<18} | {c[1]:<25} | {c[3] if c[3] else 'N/A':<15}")
            print("===========================================================")
    except Error as erro:
        print(f"\n[Erro] Erro ao listar clientes: {erro}")
        
    finally:
        cursor.close()
        conexao.close()


def atualizar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT nome, cpf
            FROM Cliente
            ORDER BY nome
        """)

        clientes = cursor.fetchall()

        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        print("\n==================== CLIENTES DISPONÍVEIS ====================")
        for c in clientes:
            cpf_formatado = validador.formatar_cpf(c[1])
            print(f"Nome: {c[0]:<25} | CPF: {cpf_formatado}")
        print("==============================================================")

        cpf = input("\nDigite o CPF do cliente que deseja atualizar: ").strip()
        if not cpf:
            print("\n[Aviso] CPF inválido.")
            return

        cpf = validador.formatar_cpf(cpf)

        cursor.execute("""
            SELECT id_cliente,
                   nome,
                   cpf,
                   telefone
            FROM Cliente
            WHERE cpf = %s
        """, (cpf,))
        
        cliente = cursor.fetchone()

        if not cliente:
            print("\n[Erro] Cliente não encontrado.")
            return
        
        print("\n=== CLIENTE ENCONTRADO ===")
        print(f"Nome atual: {cliente[1]}")
        print(f"CPF: {validador.formatar_cpf(cliente[2])}")
        print(f"Telefone atual: {cliente[3] if cliente[3] else 'N/A'}")

        nome = input("\nNovo nome (deixe vazio para manter o atual): ").strip()
        telefone = input("Novo telefone (deixe vazio para manter o atual): ").strip()

        if not nome:
            nome = cliente[1]
        if not telefone:
            telefone = cliente[3]

        if not validador.validar_nome(nome, "Nome"):
            return
        if not validador.validar_telefone(telefone):
            return

        cursor.execute(
            """
            UPDATE Cliente
            SET nome = %s, telefone = %s
            WHERE id_cliente = %s
            """,
            (nome, telefone, cliente[0])
        )

        conexao.commit()

        if cursor.rowcount > 0:
            print("\n[Sucesso] Cliente atualizado com sucesso!")
        else:
            print("\n[Aviso] Nenhuma alteração foi realizada.")

    except Error as erro:
        print(f"\n[Erro] Erro ao atualizar cliente: {erro}")

    finally:
        cursor.close()
        conexao.close()


def excluir_cliente(cpf):
    cpf = cpf.strip()
    if not cpf:
        print("\n[Erro] CPF inválido.")
        return

    cpf = validador.formatar_cpf(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_cliente, nome
            FROM Cliente
            WHERE cpf = %s
            """,
            (cpf,)
        )
        cliente = cursor.fetchone()

        if not cliente:
            print("\n[Erro] Cliente não encontrado.")
            return

        id_cliente = cliente[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Animal
            WHERE id_cliente = %s
            """,
            (id_cliente,)
        )

        result = cursor.fetchone()
        qtd_animais = result[0] if result else 0

        if qtd_animais > 0:
            print(f"\n[Erro] Não é possível excluir o cliente '{cliente[1]}' porque ele possui {qtd_animais} animal(ais) cadastrado(s).")
            return

        cursor.execute(
            """
            DELETE FROM Cliente
            WHERE id_cliente = %s
            """,
            (id_cliente,)
        )

        conexao.commit()

        if cursor.rowcount > 0:
            print(f"\n[Sucesso] Cliente '{cliente[1]}' removido com sucesso!")
        else:
            print("\n[Erro] Cliente não encontrado.")

    except Error as erro:
        print(f"\n[Erro] Erro ao excluir cliente: {erro}")

    finally:
        cursor.close()
        conexao.close()


def buscar_por_cpf(cpf):
    cpf = cpf.strip()
    if not cpf:
        print("\n[Erro] CPF inválido.")
        return None

    cpf = validador.formatar_cpf(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT id_cliente, nome, cpf, telefone
            FROM Cliente
            WHERE cpf = %s
            """,
            (cpf,)
        )

        cliente = cursor.fetchone()

        if cliente:
            print("\n================ CLIENTE ENCONTRADO ================")
            print(f"Nome: {cliente[1]}")
            print(f"CPF: {validador.formatar_cpf(cliente[2])}")
            print(f"Telefone: {cliente[3] if cliente[3] else 'N/A'}")
            print("====================================================")
        else:
            print("\n[Erro] Cliente não encontrado.")

        return cliente  

    except Error as erro:
        print(f"\n[Erro] Erro na busca por CPF: {erro}")
        return None

    finally:
        cursor.close()
        conexao.close()
