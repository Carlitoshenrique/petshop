import cliente
import animal
import funcionario
import servico
import pagamento 
import atendimento


while True:

    print("\n==========================================")
    print("             SISTEMA PETSHOP              ")
    print("==========================================")
    print("1 - Menu Cliente")
    print("2 - Menu Animal")
    print("3 - Menu Funcionário")
    print("4 - Menu Serviço")
    print("5 - Menu Atendimento")
    print("6 - Menu Pagamento")
    print("0 - Sair")
    print("==========================================")

    opcao = input("Escolha uma opção: ").strip()

  
    if opcao == "1":
        while True:
            print("\n--- CLIENTE ---")
            print("1 - Cadastrar Cliente")
            print("2 - Listar Clientes")
            print("3 - Atualizar Cliente")
            print("4 - Excluir Cliente")
            print("5 - Buscar Cliente por CPF")
            print("0 - Voltar ao Menu Principal")

            sub = input("Escolha uma ação: ").strip()

            if sub == "1":
                print("\n[Novo Cliente]")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                telefone = input("Telefone: ")
                cliente.cadastrar_cliente(nome, cpf, telefone)

            elif sub == "2":
                cliente.listar_cliente()

            elif sub == "3":  
                cliente.atualizar_cliente()

            elif sub == "4":
                print("\n[Remover Cliente]")
                cpf = input("CPF do cliente: ")
                cliente.excluir_cliente(cpf)

            elif sub == "5":
                print("\n[Buscar por CPF]")
                cpf = input("Digite o CPF: ")
                cliente.buscar_por_cpf(cpf)

            elif sub == "0":
                break

            else:
                 print("\n[Aviso] Opção inválida.")


    elif opcao == "2":
        while True:
            print("\n--- ANIMAL ---")
            print("1 - Cadastrar Animal")
            print("2 - Listar Animais")
            print("3 - Atualizar Animal")
            print("4 - Excluir Animal")
            print("0 - Voltar ao Menu Principal")
 
            sub = input("Escolha uma ação: ").strip()

            if sub == "1":
                print("\n[Novo Animal]")
                nome = input("Nome: ")
                especie = input("Espécie: ")
                raca = input("Raça: ")
                idade = input("Idade: ")
                cpf_cliente = input("CPF do Dono (Cliente): ")

                animal.cadastrar_animal(nome, especie, raca, idade, cpf_cliente)

            elif sub == "2":
                 animal.listar_animal()

            elif sub == "3":
                 animal.atualizar_animal()

            elif sub == "4":
                 print("\n[Remover Animal]")
                 cpf_cliente = input("CPF do Dono (Cliente): ")
                 nome_animal = input("Nome do animal: ")
                 animal.excluir_animal(cpf_cliente, nome_animal)

            elif sub == "0":
                break

            else:
                 print("\n[Aviso] Opção inválida.")


    elif opcao == "3":
        while True:
            print("\n--- FUNCIONÁRIO ---")
            print("1 - Cadastrar Funcionário")
            print("2 - Listar Funcionários")
            print("3 - Atualizar Funcionário")
            print("4 - Excluir Funcionário")
            print("5 - Busca por CPF")
            print("0 - Voltar ao Menu Principal")

            sub = input("Escolha uma ação: ").strip()
 
            if sub == "1":
                print("\n[Novo Funcionário]")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                cargo = input("Cargo: ")

                funcionario.cadastrar_funcionario(nome, cpf, cargo)
 
            elif sub == "2":
                funcionario.listar_funcionario()
 
            elif sub == "3":
                funcionario.atualizar_funcionario()

            elif sub == "4":
                print("\n[Remover Funcionário]")
                cpf = input("CPF do funcionário: ")
                funcionario.excluir_funcionario(cpf)

            elif sub == "5":
                print("\n[Buscar por CPF]")
                cpf = input("Digite o CPF: ")
                funcionario.buscar_por_cpf(cpf)

            elif sub == "0":
                break
                
            else:
                 print("\n[Aviso] Opção inválida.")

    elif opcao == "4":
        while True:
            print("\n--- SERVIÇO ---")
            print("1 - Cadastrar Serviço")
            print("2 - Listar Serviços")
            print("3 - Atualizar Serviço")
            print("4 - Excluir Serviço")
            print("0 - Voltar ao Menu Principal")

            sub = input("Escolha uma ação: ").strip()

            if sub == "1":
                print("\n[Novo Serviço]")
                nome = input("Nome do serviço: ")
                preco = input("Preço: ")

                servico.cadastrar_servico(nome, preco)

            elif sub == "2":
                servico.listar_servico()

            elif sub == "3":
                servico.atualizar_servico()
            
            elif sub == "4":
                print("\n[Remover Serviço]")
                nome_servico = input("Nome do serviço: ")

                servico.excluir_servico(nome_servico)

            elif sub == "0":
                break

            else:
                 print("\n[Aviso] Opção inválida.")

    elif opcao == "5":
        while True:
            print("\n--- ATENDIMENTO ---")
            print("1 - Agendar Atendimento")
            print("2 - Listar Atendimentos")
            print("3 - Finalizar Atendimento")
            print("4 - Cancelar Atendimento")
            print("5 - Buscar Atendimento por Código") 
            print("0 - Voltar ao Menu Principal")

            sub = input("Escolha uma ação: ").strip()

            if sub == "1":
                print("\n[Agendar Atendimento]")
                cpf_cliente = input("CPF do Cliente: ")
                nome_animal = input("Nome do Animal: ")
                nome_servico = input("Nome do Serviço: ")
                cpf_funcionario = input("CPF do Funcionário: ")
                data_hora = input("Data e hora (AAAA-MM-DD HH:MM:SS): ")
                
                atendimento.agendar_atendimento(cpf_cliente, nome_animal, nome_servico, cpf_funcionario, data_hora)

            elif sub == "2":
                 atendimento.listar_atendimento()

            elif sub == "3":
                print("\n[Finalizar Atendimento]")
                codigo_atendimento = input("Código do Atendimento: ")
                if not codigo_atendimento.strip():
                    print("\n[Erro] Código do atendimento inválido.")
                    continue
                
                print("\nFormas de pagamento suportadas:")
                print("1 - Pix (10% de desconto)")
                print("2 - Cartão")
                print("3 - Dinheiro (5% de desconto)")
                opcao_pagamento = input("Escolha a forma de pagamento: ").strip()

                forma = ""
                if opcao_pagamento == "1":
                    forma = "Pix"
                elif opcao_pagamento == "2":
                    forma = "Cartao"
                elif opcao_pagamento == "3":
                    forma = "Dinheiro"
                else:
                    forma = opcao_pagamento

                atendimento.finalizar_atendimento(codigo_atendimento, forma)
                
            elif sub == "4":
                print("\n[Cancelar Atendimento]")
                codigo_atendimento = input("Código do Atendimento: ")
                atendimento.cancelar_atendimento(codigo_atendimento)

            elif sub == "5":  
                print("\n[Buscar Atendimento]")
                codigo_atendimento = input("Código do Atendimento: ")
                atendimento.buscar_atendimento(codigo_atendimento)

            elif sub == "0":
                break

            else:
                 print("\n[Aviso] Opção inválida.")
 
    elif opcao == "6":
        while True:
            print("\n--- PAGAMENTO ---")
            print("1 - Listar Pagamentos")
            print("0 - Voltar ao Menu Principal")

            sub = input("Escolha uma ação: ").strip()

            if sub == "1":
                pagamento.listar_pagamento()

            elif sub == "0":
                break

            else:
                 print("\n[Aviso] Opção inválida.")


    elif opcao == "0":
        print("\nSaindo do sistema... Obrigado!")
        break

    else:
        print("\n[Aviso] Opção inválida! Escolha um número do menu.")
