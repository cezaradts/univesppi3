"""Classificação dos incidentes nas quatro macrocategorias do TCC."""
from pathlib import Path
import pandas as pd

CATEGORIAS = [
    "Riscos Sistêmicos e Econômicos",
    "Riscos de Segurança e Uso Malicioso",
    "Impactos Socioculturais e Éticos",
    "Falhas Técnicas de Desempenho",
]

def carregar_mapeamento(path):
    m = pd.read_csv(path, encoding="utf-8-sig")
    m["subdominio"] = m["subdominio"].astype(str).str.strip()
    m["categoria"] = m["categoria"].astype(str).str.strip()
    if set(m["categoria"]) - set(CATEGORIAS):
        raise ValueError("Há categorias fora da taxonomia do TCC.")
    if m["subdominio"].duplicated().any():
        raise ValueError("Há subdomínios duplicados no mapeamento.")
    return dict(zip(m["subdominio"], m["categoria"]))

def classificar_dataframe(df, coluna_subdominio="Subdomínio de Risco", mapping=None):
    if coluna_subdominio not in df.columns:
        raise ValueError(f"Coluna obrigatória ausente: {coluna_subdominio}")
    out = df.copy()
    out["Categoria_TCC"] = out[coluna_subdominio].astype("string").str.strip().map(mapping)
    faltantes = out[out["Categoria_TCC"].isna()][coluna_subdominio].dropna().unique().tolist()
    if faltantes:
        raise ValueError(f"Subdomínios sem mapeamento: {faltantes}")
    return out

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    mapping = carregar_mapeamento(base / "mapeamento_subdominios.csv")
    entrada = base / "data" / "Dados Tratados.xlsx"
    saida = base / "outputs" / "incidentes_classificados.xlsx"
    df = pd.read_excel(entrada, sheet_name="Incidentes")
    classificar_dataframe(df, mapping=mapping).to_excel(saida, index=False)
    print(f"Arquivo gerado: {saida}")
