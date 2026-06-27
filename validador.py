import re
from datetime import datetime


def validar_nome(nome, campo="Nome"):
    nome_limpo = nome.strip()
    if not nome_limpo:
        print(f"\n[Erro de Validação] O campo '{campo}' não pode estar vazio.")
        return False
    if len(nome_limpo) < 2:
        print(f"\n[Erro de Validação] O campo '{campo}' deve ter pelo menos 2 caracteres.")
        return False
    return True


def validar_cpf(cpf):
    cpf_limpo = "".join(c for c in cpf if c.isdigit())
    if len(cpf_limpo) != 11:
        print(f"\n[Erro de Validação] CPF '{cpf}' inválido. Deve conter 11 dígitos numéricos.")
        return False
    return True


def formatar_cpf(cpf):
    if not cpf:
        return ""
    cpf_limpo = "".join(c for c in cpf if c.isdigit())
    cpf_pad = cpf_limpo.zfill(11)
    if len(cpf_pad) > 11:
        cpf_pad = cpf_pad[-11:]
    return f"{cpf_pad[0:3]}.{cpf_pad[3:6]}.{cpf_pad[6:9]}-{cpf_pad[9:11]}"



def validar_telefone(telefone):
    telefone_limpo = telefone.strip()
    if not telefone_limpo:
        return True
    
    tel_digitos = "".join(c for c in telefone_limpo if c.isdigit())
    if len(tel_digitos) < 10 or len(tel_digitos) > 11:
        print(f"\n[Erro de Validação] Telefone '{telefone_limpo}' inválido. Deve conter entre 10 e 11 dígitos numéricos.")
        return False
        
    if not re.match(r"^[0-9\s()+-]*$", telefone_limpo):
        print(f"\n[Erro de Validação] Telefone '{telefone_limpo}' contém caracteres inválidos.")
        return False
    return True


def validar_idade(idade_val):
    if isinstance(idade_val, str):
        idade_val = idade_val.strip()
    
    try:
        idade = int(idade_val)
        if idade < 0:
            print(f"\n[Erro de Validação] Idade '{idade_val}' inválida. Deve ser um número maior ou igual a zero.")
            return None
        return idade
    except (ValueError, TypeError):
        print(f"\n[Erro de Validação] Idade '{idade_val}' inválida. Deve ser um número inteiro.")
        return None


def validar_preco(preco_val):
    if isinstance(preco_val, str):
        preco_val = preco_val.strip()
        
    try:
        preco = float(preco_val)
        if preco < 0.0:
            print(f"\n[Erro de Validação] Preço '{preco_val}' inválido. Deve ser maior ou igual a zero.")
            return None
        return preco
    except (ValueError, TypeError):
        print(f"\n[Erro de Validação] Preço '{preco_val}' inválido. Deve ser um valor numérico.")
        return None


def validar_data_hora(data_hora):
    data_hora_limpa = data_hora.strip()
    try:
        datetime.strptime(data_hora_limpa, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        print(f"\n[Erro de Validação] Data e hora '{data_hora}' inválida. Deve estar no formato AAAA-MM-DD HH:MM:SS.")
        return False
