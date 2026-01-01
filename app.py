import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditoria Dr. Reginaldo Oliveira", layout="wide")

st.sidebar.title("💎 Área Restrita")
st.sidebar.write(f"**Dr. Reginaldo Oliveira**\nOAB/SC 57.879")

st.title("⚖️ Painel de Inteligência e Auditoria de Ativos")
st.markdown("---")

tab1, tab2 = st.tabs(["🚀 Auditoria de Arquivos", "📊 Simulação de Entrega (Demonstração)"])

with tab1:
    st.info("Utilize esta aba para processar arquivos reais de tribunais (PJe/Projudi).")
    uploaded_file = st.file_uploader("Suba o arquivo do Tribunal", type=None)
    # (O código de leitura universal permanece aqui para quando o senhor tiver novos arquivos)

with tab2:
    st.subheader("Visualização do Relatório Estratégico para o Cliente")
    st.write("Este é o modelo de análise que convence o sócio do escritório a contratar o serviço:")
    
    if st.button("Gerar Simulação de Auditoria de Alta Performance"):
        # Criando dados realistas de 10 processos
        dados = {
            'Número Processo': [
                '5001234-55.2023.8.24.0036', '5009876-11.2022.8.24.0026', '5012345-00.2024.8.24.0001',
                '5004433-22.2021.8.24.0036', '5001122-33.2023.8.24.0026', '5006677-88.2020.8.24.0036',
                '5009900-44.2023.8.24.0026', '5007788-11.2024.8.24.0036', '5003344-55.2021.8.24.0026',
                '5005566-77.2022.8.24.0001'
            ],
            'Réu(s)': [
                'BANCO BRADESCO S/A', 'JOÃO DA SILVA', 'ESTADO DE SANTA CATARINA',
                'TELEFONICA BRASIL S/A', 'MARIA SOUZA', 'OLX ATIVIDADES DE INTERNET',
                'ITAÚ UNIBANCO S.A.', 'MINISTÉRIO PÚBLICO (SC)', 'PEDRO ALVES', 'SEGURADORA PORTO SEGURO'
            ],
            'Valor Atualizado (Est.)': [
                55000.00, 1200.00, 125000.00, 12500.00, 3400.00, 28000.00, 89000.00, 0.00, 5200.00, 45000.00
            ],
            'Dias em Inércia': [120, 15, 210, 45, 10, 180, 95, 300, 20, 110],
            'Último Evento': [
                'Aguarda Despacho', 'Juntada de Petição', 'Concluso para Sentença',
                'Citação Pendente', 'Manifestação da Parte', 'Aguarda Alvará',
                'Petição de Acordo', 'Carga dos Autos', 'Despacho Proferido', 'Aguarda Pagamento'
            ]
        }
        
        df_simulacao = pd.DataFrame(dados)
        
        # LÓGICA DE INTELIGÊNCIA (O SEU DIFERENCIAL)
        # 1. Prioridade: Réus que têm dinheiro (Bancos, Estado, Seguradoras)
        reus_ricos = ['BANCO', 'ESTADO', 'OLX', 'S/A', 'S.A', 'SEGURADORA', 'MINISTÉRIO']
        df_simulacao['Prioritário'] = df_simulacao['Réu(s)'].str.contains('|'.join(reus_ricos), case=False)
        
        # 2. Urgência: Parado há mais de 90 dias
        df_simulacao['Urgente'] = df_simulacao['Dias em Inércia'] > 90
        
        # Exibição Separada por Categorias para impacto visual
        st.markdown("### 🔴 URGENTE: Ativos Parados com Réus Solventes")
        st.write("Processos com Réus de alta liquidez e sem movimentação há mais de 90 dias.")
        urgentes = df_simulacao[(df_simulacao['Prioritário']) & (df_simulacao['Urgente'])]
        st.table(urgentes[['Número Processo', 'Réu(s)', 'Valor Atualizado (Est.)', 'Dias em Inércia']])
        
        st.markdown("### 🟡 PRIORITÁRIO: Monitoramento de Liquidez")
        st.write("Réus solventes com movimentação recente. Monitorar para cumprimento de sentença.")
        prioritarios = df_simulacao[(df_simulacao['Prioritário']) & (~df_simulacao['Urgente'])]
        st.table(prioritarios[['Número Processo', 'Réu(s)', 'Valor Atualizado (Est.)', 'Último Evento']])
        
        st.markdown("---")
        st.success(f"💰 **Total de Ativos Mapeados nesta Simulação: R$ {df_simulacao[df_simulacao['Prioritário']]['Valor Atualizado (Est.)'].sum():,.2f}**")
        st.info("Doutor, este resumo final é o que faz o cliente entender que você não está vendendo 'análise', você está entregando 'recuperação de crédito'.")
