import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditoria Jurídica Universal", layout="wide")

st.sidebar.title("Dr. Reginaldo Oliveira")
st.sidebar.write("OAB/SC 57.879")

st.title("⚖️ Sistema de Auditoria Multi-Tribunais")

uploaded_file = st.file_uploader("Selecione qualquer relatório de processos (CSV ou Excel)", type=None)

if uploaded_file is not None:
    df = None
    # TENTATIVA AUTOMÁTICA DE LEITURA (Motor Universal)
    for encoding in ['utf-8', 'iso-8859-1', 'latin-1']:
        for separator in [',', ';', '\t']:
            try:
                uploaded_file.seek(0)
                # O segredo: procuramos a linha onde os dados realmente começam
                temp_df = pd.read_csv(uploaded_file, sep=separator, encoding=encoding, nrows=50, on_bad_lines='skip')
                
                # Se achamos colunas comuns, este é o formato certo!
                colunas_comuns = ['Número', 'Processo', 'Réu', 'Parte', 'Valor']
                if any(c.lower() in str(temp_df.columns).lower() for c in colunas_comuns):
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep=separator, encoding=encoding, skiprows=1, on_bad_lines='skip')
                    break
            except:
                continue
        if df is not None: break

    if df is not None:
        # Limpeza universal de colunas
        df.columns = [str(c).strip() for c in df.columns]
        
        # BUSCA INTELIGENTE: Procura a coluna do Réu, não importa o nome
        col_reu = next((c for c in df.columns if 'réu' in c.lower() or 'parte passiva' in c.lower()), None)
        
        if col_reu:
            reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'TELEFONICA', 'INSS']
            df['Prioridade'] = df[col_reu].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success("✅ Arquivo processado com sucesso!")
            st.write(f"### 🚀 Oportunidades de Liquidez em: {uploaded_file.name}")
            st.dataframe(resultado)
        else:
            st.warning("Arquivo lido, mas não identifiquei a coluna de 'Réus'. Veja os dados:")
            st.dataframe(df)
    else:
        st.error("Não foi possível ler este formato automaticamente. Tente salvar como CSV padrão no Excel.")
