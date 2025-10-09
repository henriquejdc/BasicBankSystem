# Sistema bancário simples com clientes, contas e operações

from typing import List, Dict, Optional


def menu() -> str:
    return (
        """
\n[nu] Novo cliente
[nc] Nova conta
[lc] Listar contas
[d]  Depositar
[s]  Sacar
[e]  Extrato
[q]  Sair
\n=> """
    )


# ----------------------------- Clientes ----------------------------- #

def filtrar_cliente(cpf: str, clientes: List[Dict]) -> Optional[Dict]:
    return next((c for c in clientes if c["cpf"] == cpf), None)


def criar_cliente(clientes: List[Dict]) -> None:
    cpf = input("Informe o CPF (somente números): ").strip()
    if filtrar_cliente(cpf, clientes):
        print("\nJá existe cliente com esse CPF.")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/UF): "
    ).strip()

    clientes.append(
        {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
        }
    )
    print("\nCliente criado com sucesso.")


# ----------------------------- Contas ----------------------------- #

def listar_contas(contas: List[Dict], clientes: List[Dict]) -> None:
    if not contas:
        print("\nNão há contas cadastradas.")
        return

    print("\n=========== LISTA DE CONTAS ===========")
    for conta in contas:
        cliente = filtrar_cliente(conta["cliente_cpf"], clientes)
        nome = cliente["nome"] if cliente else "<desconhecido>"
        print(
            f"Agência: {conta['agencia']}  Conta: {conta['numero']}  Cliente: {nome} (CPF: {conta['cliente_cpf']})"
        )
    print("======================================")


essa_conta_inexistente = "\nOperação falhou! Conta inexistente para este CPF."


def criar_conta(
    agencia: str,
    numero_conta: int,
    clientes: List[Dict],
    contas: List[Dict],
) -> Optional[Dict]:
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, crie o cliente antes de criar a conta.")
        return None

    conta = {
        "agencia": agencia,
        "numero": numero_conta,
        "cliente_cpf": cpf,
        "saldo": 0.0,
        "extrato": "",
        "limite": 500.0,
        "numero_saques": 0,
        "limite_saques": 3,
    }
    contas.append(conta)
    print(
        f"\nConta criada com sucesso. Agência {agencia}, Conta {numero_conta} para {cliente['nome']}."
    )
    return conta


def contas_do_cliente(cpf: str, contas: List[Dict]) -> List[Dict]:
    return [c for c in contas if c["cliente_cpf"] == cpf]


def selecionar_conta_por_cliente(cpf: str, contas: List[Dict]) -> Optional[Dict]:
    contas_cliente = contas_do_cliente(cpf, contas)
    if not contas_cliente:
        print("\nCliente não possui contas.")
        return None

    if len(contas_cliente) == 1:
        return contas_cliente[0]

    print("\nContas do cliente:")
    for c in contas_cliente:
        print(f"- Conta: {c['numero']} (Agência: {c['agencia']})")

    try:
        numero = int(input("Informe o número da conta desejada: ").strip())
    except ValueError:
        print(essa_conta_inexistente)
        return None

    conta = next((c for c in contas_cliente if c["numero"] == numero), None)
    if not conta:
        print(essa_conta_inexistente)
    return conta


# ----------------------------- Operações ----------------------------- #

def depositar(conta: Dict, valor: float) -> None:
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso.")
    else:
        print("\nOperação falhou! O valor informado é inválido.")


def sacar(conta: Dict, valor: float) -> None:
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > conta["limite"]
    excedeu_saques = conta["numero_saques"] >= conta["limite_saques"]

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("\nSaque realizado com sucesso.")
    else:
        print("\nOperação falhou! O valor informado é inválido.")


def exibir_extrato(conta: Dict) -> None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("========================================")


# ----------------------------- Fluxo principal ----------------------------- #

def main() -> None:
    clientes: List[Dict] = []
    contas: List[Dict] = []
    AGENCIA = "0001"
    proximo_numero_conta = 1

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            conta = criar_conta(AGENCIA, proximo_numero_conta, clientes, contas)
            if conta:
                proximo_numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas, clientes)

        elif opcao == "d":
            cpf = input("Informe o CPF do titular da conta: ").strip()
            conta = selecionar_conta_por_cliente(cpf, contas)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do depósito: ").strip())
            except ValueError:
                print("\nOperação falhou! O valor informado é inválido.")
                continue
            depositar(conta, valor)

        elif opcao == "s":
            cpf = input("Informe o CPF do titular da conta: ").strip()
            conta = selecionar_conta_por_cliente(cpf, contas)
            if not conta:
                continue
            try:
                valor = float(input("Informe o valor do saque: ").strip())
            except ValueError:
                print("\nOperação falhou! O valor informado é inválido.")
                continue
            sacar(conta, valor)

        elif opcao == "e":
            cpf = input("Informe o CPF do titular da conta: ").strip()
            conta = selecionar_conta_por_cliente(cpf, contas)
            if not conta:
                continue
            exibir_extrato(conta)

        elif opcao == "q":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
