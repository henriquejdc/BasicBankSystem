import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def criar_cliente(self, nome, data_nascimento, cpf, endereco):
        if self.filtrar_cliente(cpf):
            return False, "Já existe cliente com esse CPF!"
        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        self.clientes.append(cliente)
        return True, "Cliente criado com sucesso!"

    def criar_conta(self, cpf):
        cliente = self.filtrar_cliente(cpf)
        if not cliente:
            return False, "Cliente não encontrado, fluxo de criação de conta encerrado!"
        numero_conta = len(self.contas) + 1
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        self.contas.append(conta)
        cliente.adicionar_conta(conta)
        return True, "Conta criada com sucesso!"

    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def recuperar_conta_cliente(self, cliente, indice=0):
        if not cliente.contas:
            return None, "Cliente não possui conta!"
        if len(cliente.contas) == 1 or indice == 0:
            return cliente.contas[0], None
        if 0 <= indice < len(cliente.contas):
            return cliente.contas[indice], None
        return None, "Índice de conta inválido!"

    def depositar(self, cpf, valor, conta_indice=0):
        cliente = self.filtrar_cliente(cpf)
        if not cliente:
            return False, "Cliente não encontrado!"
        conta, erro = self.recuperar_conta_cliente(cliente, conta_indice)
        if not conta:
            return False, erro
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)
        return True, "Depósito realizado!"

    def sacar(self, cpf, valor, conta_indice=0):
        cliente = self.filtrar_cliente(cpf)
        if not cliente:
            return False, "Cliente não encontrado!"
        conta, erro = self.recuperar_conta_cliente(cliente, conta_indice)
        if not conta:
            return False, erro
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)
        return True, "Saque realizado!"

    def exibir_extrato(self, cpf, conta_indice=0):
        cliente = self.filtrar_cliente(cpf)
        if not cliente:
            return False, "Cliente não encontrado!"
        conta, erro = self.recuperar_conta_cliente(cliente, conta_indice)
        if not conta:
            return False, erro
        transacoes = conta.historico.transacoes
        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
        saldo = f"\nSaldo:\n\tR$ {conta.saldo:.2f}"
        return True, f"{extrato}{saldo}"

    def listar_contas(self):
        return [str(conta) for conta in self.contas]


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = banco.filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            if len(cliente.contas) > 1:
                for idx, conta in enumerate(cliente.contas):
                    print(f"[{idx}] {conta}")
                conta_indice = int(input("Escolha o número da conta: "))
            else:
                conta_indice = 0
            valor = float(input("Informe o valor do depósito: "))
            sucesso, msg = banco.depositar(cpf, valor, conta_indice)
            print(f"\n{'===' if sucesso else '@@@'} {msg} {'===' if sucesso else '@@@'}")

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = banco.filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            if len(cliente.contas) > 1:
                for idx, conta in enumerate(cliente.contas):
                    print(f"[{idx}] {conta}")
                conta_indice = int(input("Escolha o número da conta: "))
            else:
                conta_indice = 0
            valor = float(input("Informe o valor do saque: "))
            sucesso, msg = banco.sacar(cpf, valor, conta_indice)
            print(f"\n{'===' if sucesso else '@@@'} {msg} {'===' if sucesso else '@@@'}")

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = banco.filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            if len(cliente.contas) > 1:
                for idx, conta in enumerate(cliente.contas):
                    print(f"[{idx}] {conta}")
                conta_indice = int(input("Escolha o número da conta: "))
            else:
                conta_indice = 0
            sucesso, msg = banco.exibir_extrato(cpf, conta_indice)
            print("\n================ EXTRATO ================")
            print(msg)
            print("=========================================")

        elif opcao == "nu":
            cpf = input("Informe o CPF (somente número): ")
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            sucesso, msg = banco.criar_cliente(nome, data_nascimento, cpf, endereco)
            print(f"\n{'===' if sucesso else '@@@'} {msg} {'===' if sucesso else '@@@'}")

        elif opcao == "nc":
            cpf = input("Informe o CPF do cliente: ")
            sucesso, msg = banco.criar_conta(cpf)
            print(f"\n{'===' if sucesso else '@@@'} {msg} {'===' if sucesso else '@@@'}")

        elif opcao == "lc":
            contas = banco.listar_contas()
            for conta in contas:
                print("=" * 100)
                print(textwrap.dedent(conta))

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()

