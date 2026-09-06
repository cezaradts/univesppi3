"""Detecção reprodutível dos incidentes ocorridos no Brasil."""
import re
import pandas as pd

COLUNAS_TEXTO = [
    "Título", "Descrição", "Prejudicados", "Sistemas Envolvidos",
    "Implantadores.1", "Implantadores.2", "Implantadores.3", "Implantadores.4",
    "Implantadores.5", "Implantadores.6", "Implantadores.7", "Desenvolvedor.1.1",
    "Desenvolvedor.1.2", "Desenvolvedor.2", "Desenvolvedor.3", "Desenvolvedor.4",
    "Desenvolvedor.5", "Região/Localidade", "Cidade", "Código do País"
]
TERMOS_BRASIL = [
    r"\bBrasil\b", r"\bBrazil\b", r"\bbrasileiro(?:s|as)?\b", r"\bBrazilian\b",
    r"\bBahia\b", r"\bSão Paulo\b", r"\bSao Paulo\b", r"\bRio de Janeiro\b",
    r"\bMinas Gerais\b", r"\bGoiás\b", r"\bGoias\b", r"\bParaná\b", r"\bParana\b",
    r"\bPernambuco\b", r"\bCeará\b", r"\bCeara\b", r"\bAmazonas\b", r"\bPará\b",
    r"\bParaíba\b", r"\bParaiba\b", r"\bSanta Catarina\b", r"\bRio Grande do Sul\b",
    r"\bDistrito Federal\b", r"\bBrasília\b", r"\bBrasilia\b", r"\bSalvador\b",
    r"\bRecife\b", r"\bFortaleza\b", r"\bCuritiba\b", r"\bBelo Horizonte\b",
    r"\bPorto Alegre\b", r"\bCampinas\b"
]
PADRAO = re.compile("|".join(TERMOS_BRASIL), flags=re.IGNORECASE)

# Exemplo de exceção documentada: menção a São Paulo apenas como sede de uma
# empresa/agência não transforma automaticamente o evento em incidente brasileiro.
EXCLUSOES = {
    1304: "A menção a São Paulo refere-se à localização da agência; o evento descrito ocorreu no contexto dos EUA."
}

def evidencia_brasil(row):
    if str(row.get("Código do País", "")).strip().upper() == "BR":
        return True
    texto = " ".join(str(row.get(c, "")) for c in COLUNAS_TEXTO if c in row.index)
    return bool(PADRAO.search(texto))

def separar_brasil(df):
    out = df.copy()
    out["Brasil_evidencia"] = out.apply(evidencia_brasil, axis=1)
    out["Brasil_excluido_manual"] = out["ID Incidente"].isin(EXCLUSOES)
    out["Caso_Brasil"] = out["Brasil_evidencia"] & ~out["Brasil_excluido_manual"]
    return out
