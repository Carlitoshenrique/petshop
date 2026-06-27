from typing import Any
from conexao import conectar
from mysql.connector import Error
import validador


def cadastrar_animal(nome, especie, raca, idade, cpf_cliente):
    nome = nome.strip()
    especie = especie.strip()
    raca = raca.strip()
    cpf_cliente = cpf_cliente.strip()

    if not validador.validar_nome(nome, "Nome do Animal"):
        return
    if not validador.validar_nome(especie, "Espécie"):
        return
    if not validador.validar_cpf(cpf_cliente):
        return
    
    idade_validada = validador.validar_idade(idade)
    if idade_validada is None:
        return

    cpf_cliente = validador.formatar_cpf(cpf_cliente)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_cliente FROM Cliente WHERE cpf = %s", (cpf_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("\n[Erro] Cliente com o CPF informado não foi encontrado.")
            return

        id_cliente = cliente[0]

        cursor.execute("""
            INSERT INTO Animal (nome_animal, especie, raca, idade, id_cliente)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, especie, raca, idade_validada, id_cliente))

        conexao.commit()
        print("\n[Sucesso] Animal cadastrado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Erro ao cadastrar animal: {erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_animal():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
        SELECT 
            a.nome_animal,
            a.especie,
            a.raca,
            a.idade,
            c.nome AS cliente,
            c.cpf AS cliente_cpf
        FROM Animal a
        JOIN Cliente c ON a.id_cliente = c.id_cliente
        ORDER BY c.nome, a.nome_animal
        """)

        animais: list[tuple[Any, ...]] | Any = cursor.fetchall()

        if len(animais) == 0:
            print("\nNenhum animal cadastrado.")
        else:
            print("\n========================= LISTA DE ANIMAIS =========================")
            print(f"{'Dono (CPF)':<18} | {'Dono (Nome)':<20} | {'Animal':<15} | {'Espécie':<12} | {'Raça':<12} | {'Idade':<5}")
            print("-" * 92)
            for a in animais:
                cpf_formatado = validador.formatar_cpf(a[5])
                print(f"{cpf_formatado:<18} | {a[4]:<20} | {a[0]:<15} | {a[1]:<12} | {a[2] if a[2] else 'N/A':<12} | {a[3]:<5}")
            print("====================================================================")

    except Error as erro:
        print(f"\n[Erro] Erro ao listar animais: {erro}")

    finally:
        cursor.close()
        conexao.close()


def atualizar_animal():
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

        cpf = input("\nDigite o CPF do cliente: ").strip()
        if not cpf:
            print("\n[Aviso] CPF inválido.")
            return

        cpf = validador.formatar_cpf(cpf)

        cursor.execute("""
            SELECT id_cliente, nome
            FROM Cliente
            WHERE cpf = %s
        """, (cpf,))

        cliente = cursor.fetchone()

        if not cliente:
            print("\n[Erro] Cliente não encontrado.")
            return
 
        print(f"\nCliente selecionado: {cliente[1]}")

        cursor.execute("""
            SELECT id_animal, nome_animal, especie, raca, idade
            FROM Animal
            WHERE id_cliente = %s
        """, (cliente[0],))

        animais = cursor.fetchall()

        if not animais:
            print("\nEste cliente não possui animais cadastrados.")
            return
        
        print("\n=== ANIMAIS DO CLIENTE ===")
        for a in animais:
            print(f"Nome: {a[1]:<15} | Espécie: {a[2]:<12} | Raça: {a[3] if a[3] else 'N/A':<12} | Idade: {a[4]}")
        
        nome_animal = input("\nDigite o nome do animal que deseja atualizar: ").strip()
        
        animal_selecionado = None
        for a in animais:
            if a[1].lower() == nome_animal.lower():
                animal_selecionado = a
                break

        if not animal_selecionado:
            print("\n[Erro] Animal não encontrado para este cliente.")
            return

        id_animal = animal_selecionado[0]
        
        print(f"\n=== EDITANDO ANIMAL: {animal_selecionado[1]} ===")
        nome = input(f"Novo nome (deixe vazio para manter '{animal_selecionado[1]}'): ").strip()
        raca = input(f"Nova raça (deixe vazio para manter '{animal_selecionado[3]}'): ").strip()
        idade_str = input(f"Nova idade (deixe vazio para manter '{animal_selecionado[4]}'): ").strip()
        
        if not nome:
            nome = animal_selecionado[1]
        if not raca:
            raca = animal_selecionado[3]
        if not idade_str:
            idade = animal_selecionado[4]
        else:
            try:
                idade = int(idade_str)
            except ValueError:
                print("\n[Erro] Idade inválida. Mantendo a idade atual.")
                idade = animal_selecionado[4]

        if not validador.validar_nome(nome, "Nome do Animal"):
            return
        
        idade_validada = validador.validar_idade(idade)
        if idade_validada is None:
            return

        cursor.execute("""
           UPDATE Animal 
           SET nome_animal = %s, raca = %s, idade = %s 
           WHERE id_animal = %s 
           """, (nome, raca, idade_validada, id_animal))

        conexao.commit()

        if cursor.rowcount > 0:
            print("\n[Sucesso] Animal atualizado com sucesso!")
        else:
            print("\n[Aviso] Nenhuma alteração foi realizada.")
    
    except Error as erro:
        print(f"\n[Erro] Erro ao atualizar animal: {erro}")

    finally:
        cursor.close()
        conexao.close()


def excluir_animal(cpf_cliente, nome_animal):
    cpf_cliente = cpf_cliente.strip()
    nome_animal = nome_animal.strip()

    if not cpf_cliente or not nome_animal:
        print("\n[Erro] CPF do Dono e Nome do Animal são obrigatórios.")
        return

    cpf_cliente = validador.formatar_cpf(cpf_cliente)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_cliente FROM Cliente WHERE cpf = %s", (cpf_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("\n[Erro] Cliente não encontrado.")
            return

        id_cliente = cliente[0]

        cursor.execute(
            "SELECT id_animal, nome_animal FROM Animal WHERE nome_animal = %s AND id_cliente = %s",
            (nome_animal, id_cliente)
        )
        animal = cursor.fetchone()

        if not animal:
            print("\n[Erro] Animal não encontrado para este cliente.")
            return

        id_animal = animal[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM Atendimento
            WHERE id_animal = %s
              AND status_atendimento <> 'Cancelado'
        """, (id_animal,))

        result = cursor.fetchone()
        qtd = result[0] if result else 0

        if qtd > 0:
            print("\n[Erro] Não é possível excluir: o animal possui atendimentos ativos ou realizados.")
            return

        cursor.execute("DELETE FROM Animal WHERE id_animal = %s", (id_animal,))
        conexao.commit()

        if cursor.rowcount > 0:
            print(f"\n[Sucesso] Animal '{animal[1]}' removido com sucesso!")
        else:
            print("\n[Erro] Animal não encontrado.")

    except Error as erro:
        print(f"\n[Erro] Erro ao excluir animal: {erro}")

    finally:  
        cursor.close()
        conexao.close()
