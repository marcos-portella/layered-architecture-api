import pandas as pd

dados = {
    'cidade': ['SP', 'RJ', 'BH', 'SP', 'RJ', 'Curitiba'],
    'vendas': [100, 200, 150, 300, 50, 400],
    'motoristas': [10, 20, 12, 15, 5, 25],
    'data': [
        '2026-01-01', '2026-01-01', '2026-01-02',
        '2026-01-02', '2026-01-03', '2026-01-03'
    ]
}

df = pd.DataFrame(dados)

df["vendas_por_motorista"] = df["vendas"] / df["motoristas"]

resumo = df.groupby("cidade").agg(
    {"vendas": "sum", "vendas_por_motorista": "mean"}
)

resumo.sort_values(by='vendas', ascending=False)

print(resumo)
