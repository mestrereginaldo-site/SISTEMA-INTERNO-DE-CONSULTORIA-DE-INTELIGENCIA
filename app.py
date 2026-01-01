import streamlit as st
import pandas as pd
import io

# Configuração de Autoridade
st.set_page_config(page_title="Auditoria de Ativos - Dr. Reginaldo Oliveira", layout="wide")

st.sidebar.title("💎 Área Restrita")
st.sidebar.write(f"**Dr. Reginaldo Oliveira**\nOAB/SC 57.879")
st.sidebar.markdown("---")
st.sidebar.info("Sistema de Inteligência Jurídica para Saneamento de Carteiras e Identificação de Ativos.")

st.title("⚖️ Painel de Inteligência de Ativos Judiciais")
st.markdown("---")

# Interface Principal
tab1, tab2 = st.tabs(["🚀 Auditoria de Arquivos", "📑 Instruções e Padrões"])

with tab1:
    uploaded_file = st.file_uploader("Arraste aqui o relatório do Tribunal (PJe, Projudi, eProc)", type=None)

    if uploaded_file is not None:
        try:
            # Motor de leitura universal (ignora erros de codificação)
            content = uploaded_file.getvalue().decode('latin-1', errors='ignore')
            df = pd.read_csv(io.StringIO(content), sep=None, engine='python', on_bad_lines='skip')
            
            # Limpeza de colunas
            df.columns = [str(c).strip() for c in df.columns]
            
            st.success("✅ Arquivo processado com sucesso!")
            
            # Filtro Estratégico (Sua Lógica 44-33-49 [cite: 2025-12-24])
            alvos = ['BANCO', 'SEGURADORA', 'OLX', 'ESTADO', 'MUNICIPIO', 'INSS', 'S/A', 'S.A']
            
            # Busca dinâmica por coluna de Réu
            col_reu = next((c for c in df.columns if 'réu' in c.lower() or 'parte passiva' in c.lower()), None)
            
            if col_reu:
                df['Prioridade'] = df[col_reu].astype(str).str.contains('|'.join(alvos), case=False, na=False)
                resultado = df[df['Prioridade'] == True]
                
                st.subheader("🎯 Oportunidades de Liquidez Identificadas")
                st.dataframe(resultado)
            else:
                st.warning("Coluna de Réus não identificada. Veja a base completa abaixo:")
                st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

    # BOTÃO DE TESTE (Para você ver funcionando agora!)
    st.markdown("---")
    if st.button("Simular Auditoria de Teste (Sem Arquivo)"):
        data_teste = {
            'Número Processo': ['5001234-55.2023.8.24.0036', '5009876-11.2022.8.24.0026', '5012345-00.2024.8.24.0001'],
            'Réu(s)': ['BANCO DO BRASIL S/A', 'JOÃO DA SILVA', 'ESTADO DE SANTA CATARINA'],
            'Valor da Causa': [55000.00, 1200.00, 125000.00],
            'Status': ['Aguarda Despacho', 'Arquivado', 'Citação Pendente']
        }
        df_teste = pd.DataFrame(data_teste)
        st.write("### 🔍 Exemplo de como o sistema apresentará os resultados ao seu cliente:")
        # Aplica o filtro na simulação
        df_teste['Prioridade'] = df_teste['Réu(s)'].str.contains('BANCO|ESTADO', case=False)
        st.dataframe(df_teste[df_teste['Prioridade'] == True])
        st.info("Este é o padrão visual que o Dr. Guilherme Hertel verá na sua consultoria.")

with tab2:
    st.write("### Padrões de Sucesso da Auditoria")
    st.write("1. **Identificação de Réus Solventes**: Foco em Bancos e Entidades Públicas.")
    st.write("2. **Saneamento de Inércia**: Processos parados há mais de 90 dias.")
    st.write("3. **Cálculo de Atualização**: Estimativa de juros e sucumbência para provisionamento.")
