# Petshop.App
# Sistema Petshop

## 📊 Modelo Lógico do Sistema

[diagrama](ModeloLógicoPetshop.drawio.png)


Sistema Petshop

Este é um sistema de gerenciamento para petshop desenvolvido em Python com integração ao MySQL.  
O sistema permite o controle de clientes, animais, funcionários, serviços, atendimentos e pagamentos.

O Sistema Petshop foi criado para automatizar processos internos de um petshop, como:

- Cadastro de clientes e seus animais
- Gestão de funcionários
- Controle de serviços oferecidos
- Agendamento de atendimentos
- Registro de pagamentos
- Consultas e relatórios

 Funcionalidades

 Clientes
- Cadastrar cliente
- Listar clientes
- Atualizar cliente por CPF
- Excluir cliente (com validação de animais vinculados)
- Buscar cliente por CPF


Animais
- Cadastrar animal vinculado a um cliente
- Listar animais com dados do dono
- Atualizar animal por CPF do cliente
- Excluir animal (com validação de atendimentos)



Funcionários
- Cadastrar funcionário
- Listar funcionários
- Atualizar funcionário por CPF
- Excluir funcionário (com validação de atendimentos)



Serviços
- Cadastrar serviços
- Listar serviços
- Atualizar serviços
- Excluir serviços (validação de uso em atendimentos)



 Atendimentos
- Agendar atendimento (procedure)
- Listar atendimentos completos (view)
- Finalizar atendimento
- Cancelar atendimento
- Buscar atendimentos especificos.




 Pagamentos
- Listar pagamentos
- Finalizar pagamento via procedure

Tecnologias utilizadas
Python
MySQL
SQL (Views e Procedures)
Git/GitHub



Como Executar o Projeto

## 1. Clonar o repositório
```bash id="x7m2qa"
git clone https://github.com/seu-usuario/petshop.git

pip install mysql-connector-python

Criar o banco MySQL
Executar scripts de tabelas, inserts,views, procedures, funcções e trigger

No arquivo conexao.py, configure:
host="localhost"
user="root"
password="sua_senha"
database="petshop"

python main.py









