# trilha-python-dio_training
Treinamento/Contribuição
Banco CLI

Aplicativo de linha de comando para operações bancárias simples: depósito, saque com limites, extrato detalhado, filtro por período, exportação CSV e persistência local.
Construído apenas com biblioteca padrão do Python.

✨ Recursos

Precisão financeira com Decimal (nada de centavos “fantasmas”).

Saque com limites: valor máximo por saque e número máximo diário.

Extrato detalhado com data/hora e filtro por período (YYYY-MM-DD).

Exportação do extrato para CSV.

Persistência automática em conta.json.

Código organizado por funções, fácil de testar e manter.

🧱 Requisitos

Python 3.10+

Nenhuma dependência externa (só stdlib).

🚀 Como executar

Salve o arquivo principal como banco_cli.py (conteúdo igual ao deste repositório) e rode:

python banco_cli.py


Ao iniciar, você verá o menu:

[d] Depositar
[s] Sacar
[e] Extrato
[f] Extrato por período
[x] Exportar extrato (CSV)
[r] Resetar dados
[q] Sair
=> 

🧭 Comandos do menu

d — Depositar: solicita um valor > 0, atualiza saldo e registra no extrato.

s — Sacar: respeita saldo, limite por saque e limite de saques por dia.

e — Extrato: lista todas as movimentações e mostra o saldo atual.

f — Extrato por período: filtra por datas (formato YYYY-MM-DD).

x — Exportar extrato (CSV): gera extrato_YYYYMMDD_HHMMSS.csv.

r — Resetar dados: zera saldo e histórico (pede confirmação).

q — Sair: salva dados e encerra.

⚙️ Configurações rápidas

No topo do arquivo (banco_cli.py), você pode ajustar:

ARQUIVO_DADOS = Path("conta.json")   # arquivo de persistência
MOEDA = "R$"                         # símbolo da moeda
LIMITE_SAQUE_VALOR = Decimal("500.00")
LIMITE_SAQUES_DIA = 3

🧪 Exemplo de uso
=> d
Informe o valor do depósito: 200
Depósito efetuado: R$ 200.00 | Saldo: R$ 200.00

=> s
Informe o valor do saque: 50
Saque efetuado: R$ 50.00 | Saldo: R$ 150.00

=> e

================ EXTRATO ================
2025-08-29 13:05:11  DEPÓSITO  +R$ 200.00
2025-08-29 13:06:02  SAQUE     -R$ 50.00

Saldo atual: R$ 150.00
=========================================

Filtro por período
=> f
Data inicial (YYYY-MM-DD) ou Enter: 2025-08-29
Data final   (YYYY-MM-DD) ou Enter:

Exportação CSV
=> x
Extrato exportado para 'extrato_20250829_130812.csv'.

🗂️ Estrutura gerada
.
├─ banco_cli.py
├─ conta.json                  # gerado automaticamente (persistência)
└─ extrato_YYYYMMDD_HHMMSS.csv # gerado ao exportar

🧹 Tratamento de erros & validações

Conversão segura de valores com Decimal e normalização com 2 casas (dinheiro()).

Mensagens claras para valores inválidos e violações de limites.

Salvamento automático após operações bem-sucedidas (com tolerância a falhas de I/O).

🧭 Roadmap (ideias futuras)

Autenticação por PIN.

Multi-contas em um único arquivo (ou diretório).

Transferências entre contas.

Testes unitários (pytest) com simulação de entradas.

Tema “bonito” no terminal usando rich (opcional).

📝 Licença

Este projeto pode ser distribuído sob a licença MIT (adicione um arquivo LICENSE se desejar).

Commit sugerido
feat: adiciona banco_cli.py com operações bancárias em CLI (depósito, saque, extrato, CSV e persistência)

PR (Pull Request) — descrição sugerida

Implementa sistema bancário em CLI usando apenas stdlib.

Inclui controle de limites por saque e por dia.

Extrato com data/hora, filtro por período e exportação CSV.

Persistência automática em conta.json.

Código modular, pronto para testes e extensões.

Como testar:

Executar python banco_cli.py.

Realizar um depósito, um saque e gerar extrato.

Testar f (filtro por período) e x (CSV).

Verificar criação de conta.json e do CSV exportado.
