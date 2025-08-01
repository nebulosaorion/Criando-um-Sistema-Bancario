import textwrap

def menu():
    print(textwrap.dedent('''\
        1 - Adicionar um item
        2 - Remover um item
        3 - Listar itens
        4 - Sair
    '''))
    return input("Escolha uma opção: ")

def depositar(saldo, valor, extrato,/):
    if valor > 0:
        saldo += valor
        extrato.append(f'Depósito: R$ {valor:.2f}')
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso.')
    else:
        print('Valor de depósito inválido.')
    return saldo, extrato   

def sacar(saldo, valor, extrato,/):
    if 0 < valor <= saldo:
        saldo -= valor
        extrato.append(f'Saque: R$ {valor:.2f}')
        print(f'Saque de R$ {valor:.2f} realizado com sucesso.')
    else:
        print('Valor de saque inválido ou saldo insuficiente.')
    return saldo, extrato   

def listar_extrato(extrato, saldo, /):
    if extrato:
        print("Extrato:")
        for item in extrato:
            print(item)
        print(f'Saldo atual: R$ {saldo:.2f}')
    else:
        print('Nenhum item no extrato.')

def criar_conta():
    saldo = 0.0
    extrato = []
    
    while True:
        opcao = menu()
        
        if opcao == '1':
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == '2':
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato = sacar(saldo, valor, extrato)
        elif opcao == '3':
            listar_extrato(extrato, saldo)
        elif opcao == '4':
            print('Saindo...')
            break
        else:
            print('Opção inválida. Tente novamente.')       

def filtrar_contas(contas, nome):
    return [conta for conta in contas if nome.lower() in conta['nome'].lower()] 

def criar_usuario(nome, idade, contas):
    if not any(conta['nome'].lower() == nome.lower() for conta in contas):
        contas.append({'nome': nome, 'idade': idade, 'conta': criar_conta()})
        print(f'Usuário {nome} criado com sucesso.')
    else:
        print(f'Usuário {nome} já existe.') 

def filtrar_usuarios(contas, nome):
    return [conta for conta in contas if nome.lower() in conta['nome'].lower()]

def listar_contas(contas):
    if contas:
        print("Contas:")
        for conta in contas:
            print(f"Nome: {conta['nome']}, Idade: {conta['idade']}")
    else:
        print('Nenhuma conta cadastrada.')
def main():
    contas = []
    
    while True:
        print("\nMenu Principal:")
        print("1 - Criar usuário")
        print("2 - Filtrar usuários")
        print("3 - Listar contas")
        print("4 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            nome = input("Informe o nome do usuário: ")
            idade = int(input("Informe a idade do usuário: "))
            criar_usuario(nome, idade, contas)
        elif opcao == '2':
            nome = input("Informe o nome para filtrar usuários: ")
            usuarios_filtrados = filtrar_usuarios(contas, nome)
            if usuarios_filtrados:
                for usuario in usuarios_filtrados:
                    print(f"Nome: {usuario['nome']}, Idade: {usuario['idade']}")
            else:
                print('Nenhum usuário encontrado.')
        elif opcao == '3':
            listar_contas(contas)
        elif opcao == '4':
            print('Saindo do sistema...')
            break
        else:
            print('Opção inválida. Tente novamente.')   
if __name__ == "__main__":
    main()



