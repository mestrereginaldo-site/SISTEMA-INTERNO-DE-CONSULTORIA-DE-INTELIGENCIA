import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistema Interno - Dr. Reginaldo Oliveira", layout="wide")

st.sidebar.title("Consultoria de Dados")
st.sidebar.write(f"**Dr. Reginaldo Oliveira**")
st.sidebar.write("OAB/SC 57.879")

st.title("⚖️ Diagnóstico de Liquidez (Leitura Real de Relatórios)")
st.markdown("---")

uploaded_file = st.file_uploader("Suba o arquivo 'RelatorioProcessos' (CSV)", type="csv")

if uploaded_file is not None:
    # O seu arquivo tem linhas de cabeçalho extras, vamos pular a primeira linha informativa
    df = pd.read_csv(uploaded_file, skiprows=1)
    
    # Mapeamento para os nomes das colunas do SEU arquivo real
    # Colunas identificadas: 'Número Processo', 'Réu(s)', 'Último Evento', 'Valor da Causa'
    
    reus_ricos = ['BANCO', 'SEGURADORA', 'TELECOM', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO']
    
    # Criando a lógica de filtro baseada no seu arquivo
    df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
    
    # No seu arquivo, o valor da causa está na última coluna
    st.write("### 🚀 Processos com Potencial de Liquidez (Réus Solventes)")
    
    # Filtrando apenas os réus de ouro que aparecem na sua lista
    resultado = df[df['Prioridade'] == True]
    
    if not resultado.empty:
        st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Localidade Judicial', 'Último Evento', 'Valor da Causa']])
        
        # Lógica de acompanhamento: onde há Réu de Ouro, há oportunidade [cite: 2025-12-24]
        st.success(f"Identificamos {len(resultado)} processos com alta probabilidade de execução imediata.")
    else:
        st.warning("Nenhum 'Réu de Ouro' identificado nesta lista específica.")
