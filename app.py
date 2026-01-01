import streamlit as st
import pandas as pd

# Título da aba do navegador
st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")

st.sidebar.title("Dr. Reginaldo Oliveira")
st.sidebar.write("OAB/SC 57.879")

# Título visual para você confirmar a atualização
st.title("⚖️ Auditoria IA - VERSÃO 2.0 (Motor Universal)")

# Aceita qualquer arquivo
uploaded_file = st.file_uploader("Selecione o relatório", type=None)

if uploaded_file is not None:
    df = None
    # TESTA DIFERENTES FORMAS DE LER O ARQUIVO
    # O seu arquivo do eProc tem lixo na linha 0, por isso testamos skiprows
    for skip in [1, 0, 2]:
        for enc in ['iso-8859-1', 'utf-8', 'latin-1']:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, skiprows=skip, sep=',', encoding=enc, on_bad_lines='skip')
                
                # Verifica se encontrou a coluna de Réu (que é o que precisamos)
                if any('réu' in str(c).lower() for c in df.columns):
                    break
            except:
                continue
        if df is not None and any('réu' in str(c).lower() for c in df.columns):
            break

    if df is not None:
        # Limpa nomes de colunas
        df.columns = [str(c).strip() for c in df.columns]
        
        # Localiza a coluna do Réu dinamicamente
        col_reu = next((c for c in df.columns if 'réu' in c.lower()), None)
        
        if col_reu:
            # Lista de alvos estratégicos baseada na sua lógica de padrões [cite: 2025-12-24]
            reus_ricos = ['BANCO', 'SEGURADORA', 'OLX', 'S/A', 'S.A', 'MUNICIPIO', 'ESTADO', 'MINISTERIO', 'TELEFONICA', 'INSS']
            
            # Filtra os "Réus de Ouro" que acompanham o lucro [cite: 2025-12-24]
            df['Prioridade'] = df[col_reu].str.contains('|'.join(reus_ricos), case=False, na=False)
            resultado = df[df['Prioridade'] == True]
            
            st.success("✅ Arquivo Lido com Sucesso!")
            st.write(f"### 🚀 Oportunidades Identificadas")
            st.dataframe(resultado)
        else:
            st.warning("Arquivo lido, mas a coluna 'Réu(s)' não foi detectada. Tente exportar novamente do Tribunal.")
            st.write("Colunas encontradas:", df.columns.tolist())
    else:
        st.error("Erro crítico: O sistema não conseguiu decifrar este arquivo. Verifique se ele não está vazio.")
