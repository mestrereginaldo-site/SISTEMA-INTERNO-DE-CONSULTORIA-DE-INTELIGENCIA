import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

# Se o título abaixo aparecer, o sistema ATUALIZOU
st.markdown("<h1 style='color: #FF4B4B;'>🔥 SISTEMA ATUALIZADO - PROVA REAL</h1>", unsafe_allow_html=True)
st.sidebar.write(f"**Dr. Reginaldo Oliveira**\nOAB/SC 57.879")

uploaded_file = st.file_uploader("Suba aqui o arquivo que você baixou do tribunal", type=None)

if uploaded_file is not None:
    try:
        # Lógica específica para o arquivo que você me enviou
        # Usamos Latin-1 porque é o padrão dos tribunais de SC
        df = pd.read_csv(uploaded_file, skiprows=1, encoding='ISO-8859-1', sep=',')
        
        # Limpando nomes de colunas para evitar erros de espaços
        df.columns = [str(c).strip() for c in df.columns]

        # Lista de Alvos (Réus de Ouro)
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
        
        # Procuramos a coluna Réu(s)
        if 'Réu(s)' in df.columns:
            df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success(f"✅ Sucesso! Analisamos {len(df)} processos.")
            st.subheader("🚀 Ativos com Alta Liquidez Identificados")
            
            # Mostra apenas o que interessa para o cliente
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Localidade Judicial', 'Valor da Causa']])
        else:
            st.error("Coluna 'Réu(s)' não encontrada. O formato do arquivo mudou.")
            st.write("Colunas detectadas:", df.columns.tolist())
            
    except Exception as e:
        st.error(f"Erro técnico: {e}")
