from pathlib import Path
import argparse
import sqlite3
import pandas as pd
from classificar_incidentes import carregar_mapeamento, classificar_dataframe
from brasil import separar_brasil

CATEGORIAS = [
    "Riscos Sistêmicos e Econômicos",
    "Riscos de Segurança e Uso Malicioso",
    "Impactos Socioculturais e Éticos",
    "Falhas Técnicas de Desempenho",
]

def build_dw(df, db_path):
    conn = sqlite3.connect(db_path)
    try:
        pd.DataFrame({"categoria": CATEGORIAS}).to_sql("dim_categoria", conn, if_exists="replace", index_label="categoria_id")
        tempo = pd.DataFrame({"data": pd.to_datetime(df["Data"], errors="coerce").dropna().drop_duplicates()})
        tempo["ano"] = tempo["data"].dt.year
        tempo["mes"] = tempo["data"].dt.month
        tempo.to_sql("dim_tempo", conn, if_exists="replace", index=True, index_label="tempo_id")
        cols = ["ID Incidente","Data","Título","Descrição","Subdomínio de Risco","Categoria_TCC","Fontes dos Dados","Região/Localidade","Código do País","Cidade","Caso_Brasil"]
        fact = df[[c for c in cols if c in df.columns]].copy()
        fact = fact.rename(columns={"ID Incidente":"incidente_id", "Data":"data"})
        fact["data"] = pd.to_datetime(fact["data"], errors="coerce").dt.strftime("%Y-%m-%d")
        fact.to_sql("fato_incidente", conn, if_exists="replace", index=False)
    finally:
        conn.close()

def run(input_path, output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    base = Path(__file__).resolve().parent
    mapping = carregar_mapeamento(base / "mapeamento_subdominios.csv")
    df = pd.read_excel(input_path, sheet_name="Incidentes")
    df = classificar_dataframe(df, mapping=mapping)
    df = separar_brasil(df)
    br = df[df["Caso_Brasil"]].copy()
    df.to_csv(output_dir/"incidentes_classificados.csv", index=False, encoding="utf-8-sig")
    br.to_csv(output_dir/"incidentes_brasil.csv", index=False, encoding="utf-8-sig")
    res = pd.DataFrame(index=CATEGORIAS)
    res["Global_n"] = df["Categoria_TCC"].value_counts().reindex(CATEGORIAS, fill_value=0)
    res["Brasil_n"] = br["Categoria_TCC"].value_counts().reindex(CATEGORIAS, fill_value=0)
    res["Global_pct"] = (res["Global_n"] / len(df) * 100).round(2)
    res["Brasil_pct"] = (res["Brasil_n"] / len(br) * 100).round(2)
    res["Diferenca_pp"] = (res["Brasil_pct"] - res["Global_pct"]).round(2)
    res.reset_index(names="Categoria").to_csv(output_dir/"resumo_categorias.csv", index=False, encoding="utf-8-sig")
    build_dw(df, output_dir/"dw_incidentes.sqlite")
    return df, br, res

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", default="outputs")
    args = p.parse_args()
    df, br, res = run(args.input, args.output_dir)
    print(res.to_string(index=False))
    print(f"\nTotal analisado: {len(df)} | Casos Brasil: {len(br)}")
