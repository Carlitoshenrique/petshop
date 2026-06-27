from conexao import conectar
from mysql.connector import Error
import validador


def cadastrar_servico(nome, preco):
    nome = nome.strip()

    if not validador.validar_nome(nome, "Nome do Serviço"):
        return
    
    preco_validado = validador.validar_preco(preco)
    if preco_validado is None:
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO Servico (nome_servico, preco)
            VALUES (%s, %s)
        """, (nome, preco_validado))

        conexao.commit()
        print("\n[Sucesso] Serviço cadastrado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Erro ao cadastrar serviço: {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_servico():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM Servico ORDER BY nome_servico")
        servicos = cursor.fetchall()

        if len(servicos) == 0:
            print("\nNenhum serviço cadastrado.")
        else:
            print("\n==================== SERVIÇOS DISPONÍVEIS ====================")
            print(f"{'Serviço':<30} | {'Preço':<15}")
            print("-" * 48)
            for s in servicos:
                print(f"{s[1]:<30} | R$ {s[2]:.2f}")
            print("==============================================================")

    except Error as erro:
        print(f"\n[Erro] Erro ao listar serviços: {erro}")

    finally:
        cursor.close()
        conexao.close()


def atualizar_servico():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT nome_servico, preco
            FROM Servico
            ORDER BY nome_servico
        """)
    
        servicos = cursor.fetchall()

        if not servicos:
            print("\nNenhum serviço cadastrado.")
            return

        print("\n==================== SERVIÇOS DISPONÍVEIS ====================")
        for s in servicos:
            print(f"Serviço: {s[0]:<30} | Preço: R$ {s[1]:.2f}")
        print("==============================================================")

        nome_busca = input("\nDigite o nome do serviço que deseja atualizar: ").strip()
        if not nome_busca:
            print("\n[Aviso] Nome inválido.")
            return

        cursor.execute("""
            SELECT id_servico, nome_servico, preco
            FROM Servico
            WHERE nome_servico = %s
        """, (nome_busca,))

        servico = cursor.fetchone()

        if not servico:
            print("\n[Erro] Serviço não encontrado.")
            return

        print("\n=== SERVIÇO ENCONTRADO ===")
        print(f"Nome atual: {servico[1]}")
        print(f"Preço atual: R$ {servico[2]:.2f}")

        nome = input("\nNovo nome (deixe vazio para manter o atual): ").strip()
        preco_str = input("Novo preço (deixe vazio para manter o atual): ").strip()

        if not nome:
            nome = servico[1]
        if not preco_str:
            preco = servico[2]
        else:
            try:
                preco = float(preco_str)
            except ValueError:
                print("\n[Erro] Preço inválido. Mantendo o preço atual.")
                preco = servico[2]

        if not validador.validar_nome(nome, "Nome do Serviço"):
            return
        
        preco_validado = validador.validar_preco(preco)
        if preco_validado is None:
            return

        cursor.execute("""
            UPDATE Servico
            SET nome_servico = %s,
                preco = %s
            WHERE id_servico = %s
        """, (nome, preco_validado, servico[0]))

        conexao.commit()
    
        if cursor.rowcount > 0:
            print("\n[Sucesso] Serviço atualizado com sucesso!")
        else:
            print("\n[Aviso] Nenhuma alteração foi realizada.")

    except Error as erro:
        print(f"\n[Erro] Erro ao atualizar serviço: {erro}")

    finally:
        cursor.close()
        conexao.close()


def excluir_servico(nome_servico):
    nome_servico = nome_servico.strip()
    if not nome_servico:
        print("\n[Erro] Nome inválido.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_servico FROM Servico WHERE nome_servico = %s", (nome_servico,))
        servico = cursor.fetchone()

        if not servico:
            print("\n[Erro] Serviço não encontrado.")
            return

        id_servico = servico[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM Atendimento
            WHERE id_servico = %s
        """, (id_servico,))

        result = cursor.fetchone()
        qtd = result[0] if result else 0

        if qtd > 0:
            print(f"\n[Erro] Não é possível excluir o serviço '{nome_servico}' porque ele está associado a {qtd} atendimento(s).")
            return

        cursor.execute("""
            DELETE FROM Servico
            WHERE id_servico = %s
        """, (id_servico,))

        conexao.commit()

        if cursor.rowcount > 0:
            print(f"\n[Sucesso] Serviço '{nome_servico}' excluído com sucesso!")
        else:
            print("\n[Erro] Serviço não encontrado.")

    except Error as erro:
        print(f"\n[Erro] Erro ao excluir serviço: {erro}")

    finally:
        cursor.close()
        conexao.close()
