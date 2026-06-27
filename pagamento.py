from typing import Any
from conexao import conectar
from mysql.connector import Error


def listar_pagamento():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM vw_pagamento
        """)

        pagamentos: list[tuple[Any, ...]] | Any = cursor.fetchall()

        if len(pagamentos) == 0:
            print("\nNenhum pagamento cadastrado.")

        else:
            print("\n==================== LISTA DE PAGAMENTOS ====================")
            for p in pagamentos:
                print(
                    f"Código Pagamento: {p[0]} | Código Atendimento: {p[4]}\n"
                    f"Cliente: {p[7]} | Animal: {p[8]} | Funcionário: {p[9]}\n"
                    f"Serviço: {p[10]} (Status Atendimento: {p[6]})\n"
                    f"Valor: R$ {p[1]:.2f} | Forma: {p[2]} | Status Pagamento: {p[3]}\n"
                    f"{'-'*60}"
                )
            print("=============================================================")

    except Error as erro:
        print(f"\n[Erro] Erro ao listar pagamentos: {erro}")

    finally:
        cursor.close()
        conexao.close()


def finalizar_pagamento(codigo_atendimento, forma):
    forma = forma.strip()
    if not codigo_atendimento.strip() or not forma:
        print("\n[Erro] Código do atendimento e Forma de pagamento são obrigatórios.")
        return

    try:
        codigo_atendimento = int(codigo_atendimento)
    except ValueError:
        print("\n[Erro] O código do atendimento deve ser um número inteiro.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.callproc(
            "sp_finalizar_pagamento",
            [codigo_atendimento, forma]
        )

        conexao.commit()
        print("\n[Sucesso] Pagamento finalizado com sucesso!")

    except Error as erro:
        print(f"\n[Erro] Erro ao finalizar pagamento: {erro.msg if hasattr(erro, 'msg') else erro}")

    finally:
        cursor.close()
        conexao.close()
