from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
import csv
import json
from pathlib import Path

# ========= Configurações =========
ARQUIVO_DADOS = Path("conta.json")      # Persistência local (pode trocar / remover)
MOEDA = "R$"
LIMITE_SAQUE_VALOR = Decimal("500.00")  # Valor máximo por saque
LIMITE_SAQUES_DIA = 3                   # Nº máx de saques por dia

# Precisão e arredondamento para dinheiro
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP

MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[f] Extrato por período
[x] Exportar extrato (CSV)
[r] Resetar dados
[q] Sair
=> """

# ========= Modelo de dados =========
def dinheiro(x: Decimal | str | float | int) -> Decimal:
    """Normaliza para Decimal com 2 casas."""
    if not isinstance(x, Decimal):
        x = Decimal(str(x))
    return x.quantize(Decimal("0.01"))

def hoje_str() -> str:
    return date.today().isoformat()

def agora_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def carregar_estado() -> dict:
    if ARQUIVO_DADOS.exists():
        try:
            dados = json.loads(ARQUIVO_DADOS.read_text(encoding="utf-8"))
            # Converte saldo e valores de volta para Decimal
            dados["saldo"] = dinheiro(dados.get("saldo", "0"))
            for t in dados.get("transacoes", []):
                t["valor"] = dinheiro(t["valor"])
            return dados
        except Exception:
            pass
    return {"saldo": dinheiro("0"), "transacoes": []}

def salvar_estado(estado: dict) -> None:
    dados = {
        "saldo": str(estado["saldo"]),
        "transacoes": [{**t, "valor": str(t["valor"])} for t in estado["transacoes"]],
    }
    ARQUIVO_DADOS.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def ler_valor_positivo(prompt: str) -> Decimal | None:
    bruto = input(prompt).strip().replace(",", ".")
    try:
        valor = dinheiro(bruto)
        if valor <= 0:
            print("Valor precisa ser maior que zero.")
            return None
        return valor
    except (InvalidOperation, ValueError):
        print("Valor inválido.")
        return None

def registrar_transacao(estado: dict, tipo: str, valor: Decimal) -> None:
    estado["transacoes"].append(
        {
            "momento": agora_str(),
            "tipo": tipo,  # "DEPÓSITO" ou "SAQUE"
            "valor": dinheiro(valor),
        }
    )

def depositar(estado: dict) -> None:
    valor = ler_valor_positivo("Informe o valor do depósito: ")
    if valor is None:
        return
    estado["saldo"] = dinheiro(estado["saldo"] + valor)
    registrar_transacao(estado, "DEPÓSITO", valor)
    print(f"Depósito efetuado: {MOEDA} {valor:.2f} | Saldo: {MOEDA} {estado['saldo']:.2f}")

def saques_hoje(estado: dict) -> int:
    hoje = hoje_str()
    return sum(1 for t in estado["transacoes"] if t["tipo"] == "SAQUE" and t["momento"][:10] == hoje)

def sacar(estado: dict) -> None:
    valor = ler_valor_positivo("Informe o valor do saque: ")
    if valor is None:
        return

    if valor > estado["saldo"]:
        print("Operação falhou! Saldo insuficiente.")
        return
    if valor > LIMITE_SAQUE_VALOR:
        print(f"Operação falhou! O valor excede o limite por saque ({MOEDA} {LIMITE_SAQUE_VALOR:.2f}).")
        return
    if saques_hoje(estado) >= LIMITE_SAQUES_DIA:
        print(f"Operação falhou! Limite diário de {LIMITE_SAQUES_DIA} saques atingido.")
        return

    estado["saldo"] = dinheiro(estado["saldo"] - valor)
    registrar_transacao(estado, "SAQUE", valor)
    print(f"Saque efetuado: {MOEDA} {valor:.2f} | Saldo: {MOEDA} {estado['saldo']:.2f}")

def formatar_transacao(t: dict) -> str:
    sinal = "+" if t["tipo"] == "DEPÓSITO" else "-"
    return f"{t['momento']}  {t['tipo']:<9} {sinal}{MOEDA} {t['valor']:.2f}"

def extrato(estado: dict, ini: str | None = None, fim: str | None = None) -> None:
    print("\n================ EXTRATO ================")
    transacoes = estado["transacoes"]
    if ini or fim:
        if ini:
            transacoes = [t for t in transacoes if t["momento"][:10] >= ini]
        if fim:
            transacoes = [t for t in transacoes if t["momento"][:10] <= fim]
        print(f"Período: {ini or 'início'} até {fim or 'hoje'}")

    if not transacoes:
        print("Não foram realizadas movimentações no período.")
    else:
        for t in transacoes:
            print(formatar_transacao(t))

    print(f"\nSaldo atual: {MOEDA} {estado['saldo']:.2f}")
    print("=========================================\n")

def extrato_por_periodo(estado: dict) -> None:
    ini = input("Data inicial (YYYY-MM-DD) ou Enter: ").strip() or None
    fim = input("Data final   (YYYY-MM-DD) ou Enter: ").strip() or None
    # Validação simples
    for d in (ini, fim):
        if d and (len(d) != 10 or d[4] != "-" or d[7] != "-"):
            print("Data inválida. Use o formato YYYY-MM-DD.")
            return
    extrato(estado, ini, fim)

def exportar_csv(estado: dict, caminho: str | None = None) -> None:
    if caminho is None:
        caminho = f"extrato_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    campos = ["momento", "tipo", "valor"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for t in estado["transacoes"]:
            w.writerow({**t, "valor": f"{t['valor']:.2f}"})
    print(f"Extrato exportado para '{caminho}'.")

def resetar(estado: dict) -> None:
    confirma = input("Tem certeza que deseja zerar saldo e histórico? (digite 'SIM'): ").strip().upper()
    if confirma == "SIM":
        estado["saldo"] = dinheiro("0")
        estado["transacoes"].clear()
        if ARQUIVO_DADOS.exists():
            try:
                ARQUIVO_DADOS.unlink()
            except Exception:
                pass
        print("Conta e histórico resetados.")
    else:
        print("Operação cancelada.")

def main() -> None:
    estado = carregar_estado()
    print(f"Bem-vindo! Saldo atual: {MOEDA} {estado['saldo']:.2f}")
    print(f"Limites: saque até {MOEDA} {LIMITE_SAQUE_VALOR:.2f} | {LIMITE_SAQUES_DIA} saques/dia.\n")

    while True:
        opcao = input(MENU).strip().lower()
        if   opcao == "d": depositar(estado)
        elif opcao == "s": sacar(estado)
        elif opcao == "e": extrato(estado)
        elif opcao == "f": extrato_por_periodo(estado)
        elif opcao == "x": exportar_csv(estado)
        elif opcao == "r": resetar(estado)
        elif opcao == "q":
            salvar_estado(estado)
            print("Até mais! Dados salvos.")
            break
        else:
            print("Operação inválida.")

        # Salva automaticamente após cada operação bem-sucedida
        try:
            salvar_estado(estado)
        except Exception:
            # Não interrompe a sessão por falha de IO eventual
            pass

if __name__ == "__main__":
    main()
