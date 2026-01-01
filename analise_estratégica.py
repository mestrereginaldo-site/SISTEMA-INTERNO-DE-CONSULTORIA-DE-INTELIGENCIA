import pandas as pd

# Função para gerar o Relatório de Impacto Imediato
def gerar_diagnostico_10_casos(lista_processos):
    # Dicionário de Réus de Ouro para validação automática
    reus_ouro = ['OLX', 'BANCO', 'TELEFONICA', 'CLARO', 'ITAÚ', 'BRADESCO', 'SEGURADORA']
    
    # Simulação de análise (Aqui você inserirá os dados coletados do tribunal)
    df = pd.DataFrame(lista_processos)
    
    # Identifica se o Réu é Solvente
    df['Solvência'] = df['Réu'].apply(lambda x: 'ALTA' if any(r in x.upper() for r in reus_ouro) else 'MÉDIA')
    
    # Calcula potencial de juros (estimativa de 1% am)
    df['Estimativa_Liquidez'] = df['Valor_Causa'] * 1.30 # Estimativa de 30% de acréscimo médio
    
    return df

# Exemplo de uso para o seu teste:
# processos_teste = [
#    {'Número': '50015433020228240036', 'Réu': 'OLX LTDA', 'Valor_Causa': 15000},
#    {'Número': '00123456720238240001', 'Réu': 'BANCO ITAU', 'Valor_Causa': 45000}
# ]
