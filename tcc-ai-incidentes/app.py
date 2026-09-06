import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

DB = Path(__file__).resolve().parent / "outputs" / "dw_incidentes.sqlite"
st.set_page_config(page_title="Incidentes de IA — TCC", layout="wide")
st.title("Incidentes de Inteligência Artificial")
st.caption("Protótipo analítico do TCC — quatro macrocategorias e recorte Brasil.")
if not DB.exists():
    st.error("Banco não encontrado. Execute primeiro o pipeline.py.")
    st.stop()
conn = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM fato_incidente", conn)
conn.close()

cats = ["Todas"] + sorted(df["Categoria_TCC"].dropna().unique().tolist())
cat = st.sidebar.selectbox("Categoria", cats)
brasil = st.sidebar.checkbox("Somente casos do Brasil")
if cat != "Todas": df = df[df["Categoria_TCC"] == cat]
if brasil: df = df[df["Caso_Brasil"] == 1]

c1,c2,c3 = st.columns(3)
c1.metric("Incidentes", len(df))
c2.metric("Categorias", df["Categoria_TCC"].nunique())
c3.metric("Casos Brasil", int(df["Caso_Brasil"].sum()) if len(df) else 0)

st.subheader("Frequência por categoria")
freq = df["Categoria_TCC"].value_counts().rename_axis("Categoria").to_frame("Incidentes")
st.bar_chart(freq)

st.subheader("Registros")
cols=[c for c in ["incidente_id","data","Título","Subdomínio de Risco","Categoria_TCC","Caso_Brasil"] if c in df.columns]
st.dataframe(df[cols].sort_values("data", ascending=False), use_container_width=True, hide_index=True)
