  import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>✅ MODO COMPATIBILIDADE ATIVADO</h1>", unsafe_allow_html=True)
st.sidebar.write("Dr. Reginaldo Oliveira | OAB/SC 57.879")

uploaded_file = st.file_uploader("Suba o arquivo original do eProc", type=None)

if uploaded_file is not None:
    try:
        # Lendo o conteúdo bruto
        bytes_data = uploaded_file.getvalue()
        content = bytes_data.decode('latin-1', errors='ignore')
        
        # O SEGREDO: Vamos forçar a leitura tentando os dois separadores comuns ( , e ; )
        try:
            df = pd.read_csv(io.StringIO(content), skiprows=1, sep=',')
            if 'Réu(s)' not in df.columns: raise ValueError
        except:
            df = pd.read_csv(io.StringIO(content), skiprows=1, sep=';')

        # Limpeza de colunas
        df.columns = [str(c).strip() for c in df.columns]

        # Lista de Réus de Ouro (Sua estratégia [cite: 2025-12-24])
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
        
        if 'Réu(s)' in df.columns:
            # Filtro inteligente
            df['Prioridade'] = df['Réu(s)'].astype(str).str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success(f"Doutor, analisamos {len(df)} processos com sucesso!")
            
            st.subheader("🚀 Relatório de Oportunidades (Réus Solventes)")
            # Exibindo o que o seu cliente quer ver
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Último Evento', 'Valor da Causa']])
            
            st.markdown("---")
            st.write("🔍 **Lista completa para conferência:**")
            st.dataframe(df)
        else:
            st.error("Ainda não consegui identificar as colunas. Veja como o arquivo está chegando:")
            st.text(content[:500]) # Mostra o começo do arquivo para diagnóstico

    except Exception as e:
        st.error(f"Erro de leitura: {e}")
