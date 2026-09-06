# TCC — Incidentes de Inteligência Artificial

Protótipo reprodutível para o TCC “Sistema Web de Emissão de Relatórios de Intercorrências geradas pelo uso de Inteligência Artificial: Conhecendo os Riscos”.

## Funções

- Classificação determinística dos 21 subdomínios da planilha em quatro macrocategorias do TCC.
- Identificação dos casos brasileiros por código de país ou evidência textual explícita.
- Geração de frequências global x Brasil.
- Criação de banco SQLite para consulta analítica.
- Painel opcional em Streamlit.

## Categorias

1. Riscos Sistêmicos e Econômicos
2. Riscos de Segurança e Uso Malicioso
3. Impactos Socioculturais e Éticos
4. Falhas Técnicas de Desempenho

## Execução

```bash
pip install -r requirements.txt
python pipeline.py --input "data/Dados Tratados.xlsx"
streamlit run app.py
```

A planilha não é versionada no repositório. Coloque `Dados Tratados.xlsx` em `data/` localmente.

Com a planilha analisada no TCC: 1.496 registros e 6 casos identificados no Brasil.