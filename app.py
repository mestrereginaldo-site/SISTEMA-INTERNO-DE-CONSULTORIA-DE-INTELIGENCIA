import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistema Interno - Dr. Reginaldo Oliveira", layout="wide")

# Cabeçalho com sua Identidade Profissional
st.sidebar.title("Consultoria de Dados")
st.sidebar.write(f"**Dr. Reginaldo Oliveira**")
st.sidebar.write("OAB/SC 57.879")
st.sidebar.write("advogadonomade.com.br")

st.title("⚖️ Diagnóstico de Liquidez e Auditoria de Ativos")
st.markdown("---")

# Abas para organizar o trabalho: 1 para Grandes Carteiras e 1 para Teste de 10 Processos
tab1, tab2 = st.tabs(["📊 Auditoria de Carteira (CSV)", "🔍 Diagnóstico Rápido (10 Casos)"])

with tab1:
    st.header("Upload de Base Completa")
    uploaded_file = st.file_uploader("Suba a planilha do cliente em formato CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Lógica de Réus de Ouro (Acompanhamento de Sucesso)
        reus_ricos = ['BANCO', 'SEGURADORA', 'TELECOM', 'OLX', 'MAGAZINE', 'SA', 'ITAU', 'BRADESCO', 'S/A', 'S.A']
        df['Prioridade'] = df['Reu'].str.contains('|'.join(reus_ricos), case=False, na=False)
        
        # Cálculo de Inércia e Atualização
        df['Ultima_Movimentacao'] = pd.to_datetime(df['Ultima_Movimentacao'])
        hoje = pd.to_datetime(datetime.now().date())
        df['Dias_Parado'] = (hoje - df['Ultima_Movimentacao']).dt.days
        df['Valor_Corrigido'] = df['Valor_Causa'] * (1 + (0.01 * (df['Dias_Parado'] // 30)))

        filtro = df[(df['Prioridade'] == True) & (df['Dias_Parado'] > 90)]
        
        st.write("### 🚀 Oportunidades Identificadas")
        st.dataframe(filtro.sort_values(by='Valor_Corrigido', ascending=False))
        st.download_button("Baixar Relatório em CSV", data=filtro.to_csv().encode('utf-8'), file_name="auditoria_final.csv")

with tab2:
    st.header("Análise de Amostra Gratuita")
    st.write("Insira os dados dos processos enviados para diagnóstico rápido.")
    
    # Criando uma tabela editável para você preencher na hora
    df_amostra = pd.DataFrame(
        [
            {"Número": "5001543-30.2022.8.24.0036", "Réu": "OLX LTDA", "Valor_Causa": 15000.00},
            {"Número": "", "Réu": "", "Valor_Causa": 0.00},
        ]
    )
    
    tabela_editavel = st.data_editor(df_amostra, num_rows="dynamic")
    
    if st.button("Gerar Diagnóstico de Amostra"):
        # Lógica simplificada de liquidez
        tabela_editavel['Potencial_Liquidez'] = tabela_editavel['Valor_Causa'] * 1.35 # Estimativa de 35% (Juros + Sucumbência)
        st.success("Diagnóstico concluído com base nos padrões de liquidez identificados.")
        st.dataframe(tabela_editavel)
