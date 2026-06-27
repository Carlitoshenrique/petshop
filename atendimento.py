from typing import Any
from conexao import conectar
from mysql.connector import Error
import validador


def agendar_atendimento(
    cpf_cliente,
    nome_animal,
    nome_servico,
    cpf_funcionario,
    data_hora
):
    cpf_cliente = cpf_cliente.strip()
    nome_animal = nome_animal.strip()
    nome_servico = nome_servico.strip()
    cpf_funcionario = cpf_funcionario.strip()
    data_hora = data_hora.strip()

    if not validador.validar_cpf(cpf_cliente):
        return
    if not validador.validar_nome(nome_animal, "Nome do Animal"):
        return
    if not validador.validar_nome(nome_servico, "Nome do Serviço"):
        return
    if not validador.validar_cpf(cpf_funcionario):
        return
    if not validador.validar_data_hora(data_hora):
        return

    cpf_cliente = validador.formatar_cpf(cpf_cliente)
    cpf_funcionario = validador.formatar_cpf(cpf_funcionario)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_cliente FROM Cliente WHERE cpf = %s", (cpf_cliente,))
        cliente_res = cursor.fetchone()
        if not cliente_res:
            print("\n[Erro] Cliente com o CPF informado não foi encontrado.")
            return
        id_cliente = cliente_res[0]

        cursor.execute(
            "SELECT id_animal FROM Animal WHERE nome_animal = %s AND id_cliente = %s",
            (nome_animal, id_cliente)
        )
        animal_res = cursor.fetchone()
        if not animal_res:
            print(f"\n[Erro] Animal '{nome_animal}' não cadastrado para o cliente do CPF informado.")
            return
        id_animal = animal_res[0]

        cursor.execute("SELECT id_servico FROM Servico WHERE nome_servico = %s", (nome_servico,))
        servico_res = cursor.fetchone()
        if not servico_res:
            print(f"\n[Erro] Serviço '{nome_servico}' não encontrado.")
            return
        id_servico = servico_res[0]

        cursor.execute("SELECT id_funcionario FROM Funcionario WHERE cpf = %s", (cpf_funcionario,))
        funcionario_res = cursor.fetchone()
        if not funcionario_res:
            print("\n[Erro] Funcionário com o CPF informado não foi encontrado.")
            return
        id_funcionario = funcionario_res[0]

        cursor.callproc(
            "sp_agendar_atendimento",
            [
                id_animal,
                id_servico,
                id_funcionario,
                data_hora
            ]
        )

        conexao.commit()
        print("\n[Sucesso] Atendimento agendado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Não foi possível agendar o atendimento: {erro.msg if hasattr(erro, 'msg') else erro}")

    finally:
        cursor.close()
        conexao.close()


def listar_atendimento():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""SELECT * FROM vw_atendimentos_completo""")
        atendimentos: list[tuple[Any, ...]] | Any = cursor.fetchall()

        if len(atendimentos) == 0:
            print("\nNenhum atendimento encontrado.")

        else: 
            print("\n========================= LISTA DE ATENDIMENTOS =========================")
            for a in atendimentos:
                cpf_cliente_fmt = validador.formatar_cpf(a[4])
                cpf_func_fmt = validador.formatar_cpf(a[8])
                print( 
                    f"Código Atendimento: {a[0]}\n"
                    f"Data/Hora: {a[1]} | Status: {a[2]}\n"
                    f"Cliente: {a[3]} (CPF: {cpf_cliente_fmt}) | Animal: {a[5]} ({a[6]})\n"
                    f"Funcionário: {a[7]} ({a[9]} - CPF: {cpf_func_fmt}) | Serviço: {a[10]} | Valor: R$ {a[11]:.2f}\n"
                    f"{'-'*75}"
                )
            print("=========================================================================")

    except Error as erro:
        print(f"\n[Erro] Erro ao listar atendimentos: {erro}")

    finally:
        cursor.close()
        conexao.close()


def finalizar_atendimento(codigo_atendimento, forma_pagamento):
    if not codigo_atendimento.strip():
        print("\n[Erro] Código do atendimento inválido.")
        return False

    try:
        codigo_atendimento = int(codigo_atendimento)
    except ValueError:
        print("\n[Erro] O código do atendimento deve ser um número inteiro.")
        return False

    forma_pagamento = forma_pagamento.strip()
    forma_pagamento_map = {
        "pix": "Pix",
        "cartao": "Cartao",
        "cartão": "Cartao",
        "dinheiro": "Dinheiro"
    }
    forma_normalizada = forma_pagamento_map.get(forma_pagamento.lower())
    if not forma_normalizada:
        print("\n[Erro] Forma de pagamento inválida. Use Pix, Cartão ou Dinheiro.")
        return False

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        conexao.autocommit = False

        cursor.callproc("sp_finalizar_atendimento", (codigo_atendimento,))

        cursor.callproc("sp_finalizar_pagamento", (codigo_atendimento, forma_normalizada))

        conexao.commit()
        print(f"\n[Sucesso] Atendimento finalizado e pagamento ({forma_normalizada}) registrado com sucesso!")
        return True

    except Error as erro:
        conexao.rollback()
        print(f"\n[Erro] Erro ao finalizar atendimento/pagamento: {erro.msg if hasattr(erro, 'msg') else erro}")
        return False

    finally:   
        cursor.close()
        conexao.close()


def cancelar_atendimento(codigo_atendimento):
    if not codigo_atendimento.strip():
        print("\n[Erro] Código do atendimento inválido.")
        return

    try:
        codigo_atendimento = int(codigo_atendimento)
    except ValueError:
        print("\n[Erro] O código do atendimento deve ser um número inteiro.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.callproc("sp_cancelar_atendimento", [codigo_atendimento])
        conexao.commit()
        print("\n[Sucesso] Atendimento cancelado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Erro ao cancelar atendimento: {erro.msg if hasattr(erro, 'msg') else erro}")

    finally:
        cursor.close()
        conexao.close()


def buscar_atendimento(codigo_atendimento):
    if not codigo_atendimento.strip():
        print("\n[Erro] Código do atendimento inválido.")
        return

    try:
        codigo_atendimento = int(codigo_atendimento)
    except ValueError:
        print("\n[Erro] O código do atendimento deve ser um número inteiro.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM vw_relatorio_atendimento
            WHERE id_atendimento = %s
        """, (codigo_atendimento,))

        resultado = cursor.fetchone()

        if resultado:
            cpf_cliente_fmt = validador.formatar_cpf(resultado[4])
            cpf_func_fmt = validador.formatar_cpf(resultado[9])

            print("\n================== RELATÓRIO DO ATENDIMENTO ==================")
            print(f"Código: {resultado[0]}")
            print(f"Data: {resultado[1]}")
            print(f"Status: {resultado[2]}")

            print("\n--- CLIENTE ---")
            print(f"Nome: {resultado[3]}")
            print(f"CPF: {cpf_cliente_fmt}")

            print("\n--- ANIMAL ---")
            print(f"Nome: {resultado[5]}")
            print(f"Espécie: {resultado[6]}")
            print(f"Raça: {resultado[7] if resultado[7] else 'N/A'}")

            print("\n--- FUNCIONÁRIO ---")
            print(f"Nome: {resultado[8]}")
            print(f"CPF: {cpf_func_fmt}")
            print(f"Cargo: {resultado[10]}")

            print("\n--- SERVIÇO ---")
            print(f"Serviço: {resultado[11]}")
            print(f"Valor: R$ {resultado[12]:.2f}")

            print("\n--- PAGAMENTO ---")
            print(f"Forma: {resultado[13] if resultado[13] else 'Não realizada'}")
            print(f"Status: {resultado[14] if resultado[14] else 'Pendente'}")
            print(f"Total Pago: R$ {resultado[15]:.2f}" if resultado[15] is not None else "Total Pago: N/A")
            print("==============================================================")

        else:
            print("\n[Erro] Atendimento não encontrado.")

    except Error as erro:
        print(f"\n[Erro] Erro ao buscar atendimento: {erro}")

    finally:
        cursor.close()
        conexao.close()


