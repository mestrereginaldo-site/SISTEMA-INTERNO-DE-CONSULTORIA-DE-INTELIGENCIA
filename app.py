import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>🚀 MODO FINAL - LEITURA DIRETA</h1>", unsafe_allow_html=True)
st.sidebar.write(f"**Dr. Reginaldo Oliveira**\nOAB/SC 57.879\nadvogadonomade.com.br")

uploaded_file = st.file_uploader("Suba o arquivo original do eProc", type=None)

if uploaded_file is not None:
    try:
        # 1. Lemos o arquivo como texto bruto para não depender do Excel antigo
        bytes_data = uploaded_file.getvalue()
        content = bytes_data.decode('latin-1', errors='ignore')
        
        # 2. Pulamos a primeira linha de título e lemos o resto
        linhas = content.splitlines()
        corpo_dados = "\n".join(linhas[1:]) # Pula a linha "Relatório de Processos..."
        
        # 3. O SEGREDO: Usamos o motor de leitura que ignora erros de vírgulas extras
        df = pd.read_csv(io.StringIO(corpo_dados), sep=',', on_bad_lines='skip', encoding='latin-1')
        
        # Limpa os nomes das colunas
        df.columns = [str(c).strip() for c in df.columns]

        # 4. Lista de Elite (Sua estratégia [cite: 2025-12-24])
        # Note que no seu arquivo tem 'MINISTÉRIO PÚBLICO' - ele vai aparecer agora!
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
        
        if 'Réu(s)' in df.columns:
            # Filtro de Prioridade
            df['Prioridade'] = df['Réu(s)'].astype(str).str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success(f"Doutor, processamos os {len(df)} processos do relatório!")
            
            st.subheader("🔥 Ativos de Alta Liquidez Identificados")
            # Exibe as colunas que provam o seu valor para o cliente
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Localidade Judicial', 'Último Evento', 'Valor da Causa']])
            
            st.markdown("---")
            st.write("📂 **Lista Completa para Conferência:**")
            st.dataframe(df)
        else:
            st.error("Não encontrei a coluna 'Réu(s)'. Veja o que o sistema leu:")
            st.write(df.columns.tolist())

    except Exception as e:
        st.error(f"Erro ao processar arquivo do Mac 2012: {e}")
