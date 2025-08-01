from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Dict, Optional

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass
    
    @abstractmethod
    def registrar(self, conta) -> bool:
        pass

class Historico:
    def __init__(self):
        self._transacoes: List[Transacao] = []
    
    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes
    
    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

class Conta:
    def __init__(self, cliente, numero: int, agencia: str = "0001"):
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero: int) -> 'Conta':
        return cls(cliente, numero)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self) -> Historico:
        return self._historico
    
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        
        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente, numero: int, agencia: str = "0001", limite: float = 500.0, limite_saques: int = 3):
        super().__init__(cliente, numero, agencia)
        self._limite: float = limite
        self._limite_saques: int = limite_saques
        self._saques_realizados: int = 0
    
    def sacar(self, valor: float) -> bool:
        if self._saques_realizados >= self._limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        
        if valor > self._limite:
            print(f"Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
            return False
        
        if super().sacar(valor):
            self._saques_realizados += 1
            return True
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Cliente(ABC):
    def __init__(self, endereco: str):
        self._endereco: str = endereco
        self._contas: List[Conta] = []
    
    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)
    
    @property
    def contas(self) -> List[Conta]:
        return self._contas
    
    @property
    def endereco(self) -> str:
        return self._endereco

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self._cpf: str = cpf
        self._nome: str = nome
        self._data_nascimento: date = data_nascimento
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento
    
    def __str__(self):
        return f"Nome: {self.nome}\nCPF: {self.cpf}\nData de Nascimento: {self.data_nascimento.strftime('%d/%m/%Y')}"

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor: float = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> bool:
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor: float = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> bool:
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False
def main():
    clientes: List[PessoaFisica] = []
    contas: List[ContaCorrente] = []

    while True:
        print("\n========== MENU ==========")
        print("1. Novo cliente")
        print("2. Nova conta")
        print("3. Listar contas")
        print("4. Depositar")
        print("5. Sacar")
        print("6. Extrato")
        print("7. Sair")
        
        opcao = input("Selecione uma opção: ")
        
        if opcao == "1":
            criar_cliente(clientes)
        elif opcao == "2":
            criar_conta(clientes, contas)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            depositar(clientes)
        elif opcao == "5":
            sacar(clientes)
        elif opcao == "6":
            exibir_extrato(clientes)
        elif opcao == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def criar_cliente(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    try:
        dia, mes, ano = map(int, data_nascimento.split('-'))
        data_nascimento = date(ano, mes, dia)
    except ValueError:
        print("\nData de nascimento inválida! Use o formato dd-mm-aaaa.")
        return
    
    cliente = PessoaFisica(
        cpf=cpf,
        nome=nome,
        data_nascimento=data_nascimento,
        endereco=endereco
    )
    
    clientes.append(cliente)
    print("\nCliente criado com sucesso!")

def filtrar_cliente(cpf: str, clientes: List[PessoaFisica]) -> Optional[PessoaFisica]:
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_conta(clientes: List[PessoaFisica], contas: List[ContaCorrente]) -> None:
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado! Crie um cliente primeiro.")
        return
    
    numero_conta = len(contas) + 1
    conta = ContaCorrente(cliente, numero_conta)
    
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\nConta criada com sucesso!")
    print(conta)

def listar_contas(contas: List[ContaCorrente]) -> None:
    if not contas:
        print("\nNenhuma conta cadastrada!")
        return
    
    print("\n========== CONTAS ==========")
    for conta in contas:
        print(conta)
        print("=" * 30)

def depositar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    
    transacao = Deposito(valor)
    
    conta = cliente.contas[0]
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    
    transacao = Saque(valor)
    
    conta = cliente.contas[0]
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    
    conta = cliente.contas[0]
    
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not conta.historico.transacoes else "")
    
    for transacao in conta.historico.transacoes:
        print(f"{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n\tData: {transacao['data']}")
    
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=" * 30)

if __name__ == "__main__":
    main()