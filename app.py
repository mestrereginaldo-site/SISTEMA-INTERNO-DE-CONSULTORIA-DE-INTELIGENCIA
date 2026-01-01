import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>✅ SISTEMA ATUALIZADO - MODO COMPATIBILIDADE</h1>", unsafe_allow_html=True)
st.sidebar.write("Dr. Reginaldo Oliveira | OAB/SC 57.879")

uploaded_file = st.file_uploader("Suba o arquivo original do Tribunal (sem abrir no Excel)", type=None)

if uploaded_file is not None:
    try:
        # Lendo o arquivo ignorando erros de formatação do Excel antigo
        raw_data = uploaded_file.getvalue().decode('latin-1', errors='ignore')
        
        # O segredo: vamos quebrar o texto manualmente
        lines = raw_data.splitlines()
        
        # Procuramos a linha onde os dados realmente começam (que contém 'Número Processo')
        start_line = 0
        for i, line in enumerate(lines):
            if 'Número Processo' in line:
                start_line = i
                break
        
        # Criamos o DataFrame a partir da linha correta
        data = '\n'.join(lines[start_line:])
        df = pd.read_csv(io.StringIO(data), sep=',', on_bad_lines='skip')
        
        # Limpamos as colunas
        df.columns = [c.strip() for c in df.columns]

        if 'Réu(s)' in df.columns:
            # Lista de Réus de Ouro baseada na sua lógica [cite: 2025-12-24]
            reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
            df['Prioridade'] = df['Réu(s)'].astype(str).str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success(f"Sistema leu {len(df)} processos com sucesso!")
            st.subheader("🚀 Oportunidades Identificadas")
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Último Evento', 'Valor da Causa']])
        else:
            st.warning("Arquivo carregado, mas as colunas não foram identificadas. Mostrando dados brutos:")
            st.dataframe(df.head())

    except Exception as e:
        st.error(f"Erro de compatibilidade: {e}")
