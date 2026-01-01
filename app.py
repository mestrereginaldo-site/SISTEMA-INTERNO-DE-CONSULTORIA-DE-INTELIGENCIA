import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema Dr. Reginaldo", layout="wide")

st.sidebar.title("Consultoria de Dados")
st.sidebar.write("Dr. Reginaldo Oliveira")
st.sidebar.write("OAB/SC 57.879")

st.title("⚖️ Auditoria de Processos Reais")

# O botão de upload que aceita o seu arquivo
uploaded_file = st.file_uploader("Suba o arquivo do Tribunal (CSV)", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        # Lógica para limpar o arquivo do tribunal que tem cabeçalho extra
        # Lemos a partir da linha 1 (skiprows=1) porque a linha 0 é apenas o título do relatório
        df = pd.read_csv(uploaded_file, skiprows=1, sep=',', encoding='utf-8')
        
        # Filtro de "Réus de Ouro" (Empresas e Entidades que pagam)
        reus_ricos = ['BANCO', 'SEGURADORA', 'TELECOM', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTÉRIO']
        
        # Criamos a coluna de prioridade
        df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
        
        st.write("### 🚀 Oportunidades Identificadas na sua Lista")
        
        # Mostramos o resultado filtrado
        resultado = df[df['Prioridade'] == True]
        
        if not resultado.empty:
            st.dataframe(resultado[['Número Processo', 'Réu(s)', 'Localidade Judicial', 'Último Evento', 'Valor da Causa']])
            st.success(f"Sucesso! Encontramos {len(resultado)} processos com réus solventes.")
        else:
            st.warning("Nenhum réu da lista de elite foi encontrado. Mostrando todos para conferência:")
            st.dataframe(df)
            
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}. Certifique-se de que é o arquivo CSV exportado.")
