import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema Dr. Reginaldo", layout="wide")

st.sidebar.title("Consultoria de Dados")
st.sidebar.write("Dr. Reginaldo Oliveira - OAB/SC 57.879")

st.title("⚖️ Auditoria de Processos - Dr. Reginaldo")

# REMOVEMOS A RESTRIÇÃO DE EXTENSÃO: Agora ele aceita QUALQUER arquivo para você conseguir selecionar
uploaded_file = st.file_uploader("Selecione o relatório do Tribunal", type=None)

if uploaded_file is not None:
    try:
        # Forçamos a leitura como texto/csv independente da extensão que o Windows/Mac mostre
        df = pd.read_csv(uploaded_file, skiprows=1, sep=',', encoding='utf-8', on_bad_lines='skip')
        
        # Filtro de "Réus de Ouro" focado no seu relatório real
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO PÚBLICO']
        
        # O sistema busca na coluna 'Réu(s)' que vi no seu arquivo
        if 'Réu(s)' in df.columns:
            df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.write("### 🚀 Oportunidades Identificadas")
            if not resultado.empty:
                st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Localidade Judicial', 'Último Evento', 'Valor da Causa']])
                st.success(f"Encontramos {len(resultado)} alvos estratégicos.")
            else:
                st.warning("Nenhum réu de elite identificado. Veja a lista completa abaixo:")
                st.dataframe(df)
        else:
            st.error("Coluna 'Réu(s)' não encontrada. O arquivo parece estar em formato diferente.")
            st.write("Colunas detectadas:", df.columns.tolist())
            
    except Exception as e:
        st.error(f"Erro na leitura: {e}. Tente renomear o arquivo para apenas '.csv' no seu computador.")
