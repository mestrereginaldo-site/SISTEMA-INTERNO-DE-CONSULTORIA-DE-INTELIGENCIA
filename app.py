import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

st.markdown("<h1 style='color: #00FF00;'>✅ SISTEMA ATIVO - VERSÃO FINAL</h1>", unsafe_allow_html=True)
st.sidebar.write("Dr. Reginaldo Oliveira | OAB/SC 57.879")

uploaded_file = st.file_uploader("Suba o arquivo do eProc aqui", type=None)

if uploaded_file is not None:
    try:
        # Forçamos a leitura das primeiras 10 colunas para ignorar erros no fim da linha
        df = pd.read_csv(
            uploaded_file, 
            skiprows=1, 
            encoding='latin-1', 
            sep=',', 
            on_bad_lines='skip',
            usecols=range(10) # Lemos apenas as 10 colunas padrão do eProc
        )
        
        # Nomeando as colunas conforme o seu arquivo real
        df.columns = ['Número Processo', 'Classe', 'Autores Principais', 'Réu(s)', 
                      'Localidade Judicial', 'Assunto', 'Último Evento', 'Data/Hora', 
                      'Data de Distribuição', 'Valor da Causa']

        st.success(f"Sucesso! {len(df)} processos carregados.")

        # FILTRO DE RÉUS DE OURO
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO', 'INSS', 'TELEFONICA']
        
        df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
        resultado = df[df['Prioridade'] == True]
        
        st.subheader("🚀 Oportunidades de Liquidez")
        if not resultado.empty:
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Último Evento', 'Valor da Causa']])
        else:
            st.warning("Nenhum réu da lista de elite encontrado. Veja a lista total:")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        st.info("Dica: Se persistir, abra o arquivo no Excel e salve como 'CSV Separado por Vírgulas'.")
