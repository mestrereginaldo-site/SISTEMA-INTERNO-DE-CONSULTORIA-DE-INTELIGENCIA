import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistema Interno - Auditoria Jurídica IA", layout="wide")

st.title("⚖️ Painel de Inteligência de Ativos")
st.subheader("Ferramenta Interna de Saneamento de Carteira")

# Upload da Planilha do Cliente
uploaded_file = st.file_uploader("Suba a planilha do cliente (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Lógica de Réus de Ouro (Acompanhamento de Sucesso)
    reus_ricos = ['BANCO', 'SEGURADORA', 'TELECOM', 'OLX', 'MAGAZINE', 'SA', 'ITAU', 'BRADESCO']
    df['Prioridade'] = df['Reu'].str.contains('|'.join(reus_ricos), case=False, na=False)
    
    # Cálculo de Inércia e Atualização (Baseado em Padrões de Liquidez)
    df['Ultima_Movimentacao'] = pd.to_datetime(df['Ultima_Movimentacao'])
    hoje = pd.to_datetime(datetime.now().date())
    df['Dias_Parado'] = (hoje - df['Ultima_Movimentacao']).dt.days
    df['Valor_Corrigido'] = df['Valor_Causa'] * (1 + (0.01 * (df['Dias_Parado'] // 30)))

    # Filtros para o seu Relatório Final
    filtro = df[(df['Prioridade'] == True) & (df['Dias_Parado'] > 90)]
    
    st.write("### 🚀 Oportunidades de Liquidez Imediata Identificadas")
    st.dataframe(filtro.sort_values(by='Valor_Corrigido', ascending=False))
    
    # Botão para você exportar e enviar ao cliente
    st.download_button("Baixar Relatório para Envio", data=filtro.to_csv().encode('utf-8'), file_name="relatorio_final.csv")
