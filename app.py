import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

# MARCADOR VISUAL DE ATUALIZAÇÃO
st.markdown("<h1 style='color: #1E90FF;'>🚀 VERSÃO 2.0 - SISTEMA ATUALIZADO</h1>", unsafe_allow_html=True)
st.sidebar.title("Dr. Reginaldo Oliveira")
st.sidebar.write("OAB/SC 57.879")

uploaded_file = st.file_uploader("Suba o relatório aqui", type=None)

if uploaded_file is not None:
    try:
        # Tenta ler ignorando erros e testando codificações comuns em SC (Latin-1)
        # O seu arquivo real que analisei precisa pular a linha 0
        df = pd.read_csv(uploaded_file, skiprows=1, sep=',', encoding='ISO-8859-1', on_bad_lines='skip')
        
        # Limpa nomes de colunas
        df.columns = [str(c).strip() for c in df.columns]
        
        # Busca a coluna 'Réu(s)' que está no seu arquivo original
        col_reu = 'Réu(s)' if 'Réu(s)' in df.columns else None
        
        if col_reu:
            reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
            df['Prioridade'] = df[col_reu].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success("✅ Leitura realizada com sucesso!")
            st.dataframe(resultado)
        else:
            st.warning("Arquivo lido, mas a coluna 'Réu(s)' não foi encontrada.")
            st.write("Colunas no arquivo:", df.columns.tolist())
            
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
