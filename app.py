import streamlit as st

st.set_page_config(page_title="Auditoria Dr. Reginaldo", layout="wide")
st.markdown("<h1 style='color: #00FF00;'>🛡️ MODO INFALÍVEL - LEITURA DIRETA</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Suba o arquivo original do Tribunal", type=None)

if uploaded_file is not None:
    # Lemos como texto puro para evitar erros de Excel/Mac
    content = uploaded_file.getvalue().decode('latin-1', errors='ignore')
    linhas = content.splitlines()
    
    st.success(f"Arquivo carregado! Analisando {len(linhas)} linhas...")

    # Lista de alvos estratégicos
    alvos = ['BANCO', 'SEGURADORA', 'OLX', 'MINISTÉRIO', 'ESTADO', 'MUNICIPIO', 'INSS', 'S/A', 'S.A']
    
    encontrados = []
    for linha in linhas:
        # Se a linha contiver um dos alvos, nós guardamos ela
        if any(alvo in linha.upper() for alvo in alvos):
            encontrados.append(linha)

    if encontrados:
        st.subheader("🚀 Ativos com Alta Liquidez Encontrados")
        for item in encontrados:
            # Limpamos as vírgulas extras para facilitar a leitura visual
            exibicao = item.replace('"', '').replace(',,', ' ')
            st.info(exibicao)
    else:
        st.warning("Nenhum réu estratégico identificado. Tente outro relatório.")
