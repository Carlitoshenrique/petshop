from typing import Any
from conexao import conectar
from mysql.connector import Error
import validador


def cadastrar_funcionario(nome, cpf, cargo):
    nome = nome.strip()
    cpf = cpf.strip()
    cargo = cargo.strip()

    if not validador.validar_nome(nome, "Nome"):
        return
    if not validador.validar_cpf(cpf):
        return
    if not validador.validar_nome(cargo, "Cargo"):
        return

    cpf = validador.formatar_cpf(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Funcionario (nome_funcionario, cpf, cargo)
            VALUES (%s, %s, %s)
            """,
            (nome, cpf, cargo)
        )

        conexao.commit()
        print("\n[Sucesso] Funcionário cadastrado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Não foi possível cadastrar o funcionário (CPF pode estar duplicado): {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_funcionario():
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM Funcionario ORDER BY nome_funcionario")
        funcionarios: list[tuple[Any, ...]] | Any = cursor.fetchall()

        if len(funcionarios) == 0:
            print("\nNenhum funcionário cadastrado.")
        else:
            print("\n==================== LISTA DE FUNCIONÁRIOS ====================")
            print(f"{'CPF':<18} | {'Nome':<25} | {'Cargo':<20}")
            print("-" * 68)
            for f in funcionarios:
                cpf_formatado = validador.formatar_cpf(f[2])
                print(f"{cpf_formatado:<18} | {f[1]:<25} | {f[3]:<20}")
            print("===============================================================")
    
    except Error as erro:
        print(f"\n[Erro] Erro ao listar funcionários: {erro}")
        
    finally:
        cursor.close()
        conexao.close()


def atualizar_funcionario():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT nome_funcionario, cpf
            FROM Funcionario
            ORDER BY nome_funcionario
        """)

        funcionarios = cursor.fetchall()

        if not funcionarios:
            print("\nNenhum funcionário cadastrado.")
            return

        print("\n==================== FUNCIONÁRIOS DISPONÍVEIS ====================")
        for f in funcionarios:
            cpf_formatado = validador.formatar_cpf(f[1])
            print(f"Nome: {f[0]:<25} | CPF: {cpf_formatado}")
        print("==================================================================")

        cpf = input("\nDigite o CPF do funcionário que deseja atualizar: ").strip()  
        if not cpf:
            print("\n[Aviso] CPF inválido.")
            return
        
        cpf = validador.formatar_cpf(cpf)

        cursor.execute("""
            SELECT id_funcionario,
                   nome_funcionario,
                   cpf,
                   cargo
            FROM Funcionario
            WHERE cpf = %s
        """, (cpf,))

        funcionario = cursor.fetchone()

        if not funcionario:
            print("\n[Erro] Funcionário não encontrado.")
            return

        print("\n=== FUNCIONÁRIO ENCONTRADO ===")
        print(f"Nome atual: {funcionario[1]}")
        print(f"CPF: {validador.formatar_cpf(funcionario[2])}")
        print(f"Cargo atual: {funcionario[3]}")

        nome = input("\nNovo nome (deixe vazio para manter o atual): ").strip()
        cargo = input("Novo cargo (deixe vazio para manter o atual): ").strip()

        if not nome:
            nome = funcionario[1]
        if not cargo:
            cargo = funcionario[3]

        if not validador.validar_nome(nome, "Nome"):
            return
        if not validador.validar_nome(cargo, "Cargo"):
            return

        cursor.execute("""
            UPDATE Funcionario
            SET nome_funcionario = %s,
                cargo = %s
            WHERE id_funcionario = %s
        """, (nome, cargo, funcionario[0]))

        conexao.commit()

        if cursor.rowcount > 0:
            print("\n[Sucesso] Funcionário atualizado com sucesso!")
        else:
            print("\n[Aviso] Nenhuma alteração foi realizada.")
       
    except Error as erro:
        print(f"\n[Erro] Erro ao atualizar funcionário: {erro}")

    finally:
        cursor.close()
        conexao.close()


def excluir_funcionario(cpf):
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
            SELECT id_funcionario, nome_funcionario
            FROM Funcionario
            WHERE cpf = %s
            """,
            (cpf,)
        )
        funcionario = cursor.fetchone()

        if not funcionario:
            print("\n[Erro] Funcionário não encontrado.")
            return

        id_funcionario = funcionario[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM Atendimento
            WHERE id_funcionario = %s
        """, (id_funcionario,))

        result = cursor.fetchone()
        qtd = result[0] if result else 0

        if qtd > 0:
            print(f"\n[Erro] Não é possível excluir o funcionário '{funcionario[1]}' porque ele possui {qtd} atendimento(s) registrado(s).")
            return

        cursor.execute("""
            DELETE FROM Funcionario
            WHERE id_funcionario = %s
        """, (id_funcionario,))

        conexao.commit()

        if cursor.rowcount > 0:
            print(f"\n[Sucesso] Funcionário '{funcionario[1]}' excluído com sucesso!")
        else:
            print("\n[Erro] Funcionário não encontrado.")

    except Error as erro:
        print(f"\n[Erro] Erro ao excluir funcionário: {erro}")

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
            SELECT id_funcionario, nome_funcionario, cpf, cargo
            FROM Funcionario
            WHERE cpf = %s
            """,
            (cpf,)
        )

        funcionario = cursor.fetchone()

        if funcionario:
            print("\n================ FUNCIONÁRIO ENCONTRADO ================")
            print(f"Nome: {funcionario[1]}")
            print(f"CPF: {validador.formatar_cpf(funcionario[2])}")
            print(f"Cargo: {funcionario[3]}")
            print("========================================================")
        else:
            print("\n[Erro] Funcionário não encontrado.")

        return funcionario

    except Error as erro:
        print(f"\n[Erro] Erro na busca por CPF: {erro}")
        return None

    finally:
        cursor.close()
        conexao.close()
