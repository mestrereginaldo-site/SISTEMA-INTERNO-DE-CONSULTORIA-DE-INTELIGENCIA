import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema Dr. Reginaldo", layout="wide")

st.sidebar.title("Consultoria de Dados")
st.sidebar.write("Dr. Reginaldo Oliveira - OAB/SC 57.879")

st.title("⚖️ Auditoria eProc - Dr. Reginaldo")

# Aceita qualquer arquivo para não travar na seleção
uploaded_file = st.file_uploader("Suba o Relatório do eProc (CSV/XLS)", type=None)

if uploaded_file is not None:
    try:
        # Tenta ler com a codificação padrão de tribunais brasileiros (ISO-8859-1)
        # Pulamos a primeira linha que é apenas o título do relatório
        df = pd.read_csv(uploaded_file, skiprows=1, sep=',', encoding='ISO-8859-1', on_bad_lines='skip')
        
        # Limpeza de nomes de colunas (remove espaços extras)
        df.columns = [c.strip() for c in df.columns]

        # Lista de "Réus de Ouro" (Acompanhamento de Sucesso)
        reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTERIO', 'INSS', 'TELEFONICA']
        
        if 'Réu(s)' in df.columns:
            # Identifica os processos com réus solventes
            df['Prioridade'] = df['Réu(s)'].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.write("### 🚀 Oportunidades Identificadas no eProc")
            if not resultado.empty:
                # Mostra o que importa: Número, Réu, Evento e Valor
                colunas_exibir = ['Número Processo', 'Réu(s)', 'Último Evento', 'Valor da Causa']
                st.dataframe(resultado[colunas_exibir])
                st.success(f"Encontramos {len(resultado)} processos estratégicos!")
            else:
                st.warning("Nenhum réu da lista de elite detectado. Veja a lista completa:")
                st.dataframe(df)
        else:
            st.error("Não achei a coluna 'Réu(s)'. Verifique se o arquivo foi exportado corretamente do eProc.")
            st.write("Colunas encontradas no seu arquivo:", df.columns.tolist())
            
    except Exception as e:
        st.error(f"Erro técnico de leitura: {e}")
        st.info("Dica: No eProc, tente exportar como 'CSV' e certifique-se de que o arquivo não está aberto no Excel ao subir.")
