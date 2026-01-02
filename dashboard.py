import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 Dashboard de Vendas E-commerce")

# 2. Carregamento dos Dados
def carregar_dados():
    arquivos = glob.glob("vendas_*.xlsx")
    lista_de_tabelas = []
    
    if not arquivos:
        return None
        
    for arquivo in arquivos:
        df_temp = pd.read_excel(arquivo)
        lista_de_tabelas.append(df_temp)
        
    df_total = pd.concat(lista_de_tabelas, ignore_index=True)
    df_total['Faturamento'] = df_total['quantidade'] * df_total['valor_unitario']
    return df_total

df = carregar_dados()

if df is None:
    st.error("❌ Nenhum arquivo de vendas encontrado na pasta!")
else:
    # 3. Métricas Principais
    col1, col2, col3 = st.columns(3)
    
    total_faturamento = df['Faturamento'].sum()
    total_vendas = df['quantidade'].sum()
    melhor_filial = df.groupby('filial')['Faturamento'].sum().idxmax()
    
    col1.metric("💰 Faturamento Total", f"R$ {total_faturamento:,.2f}")
    col2.metric("📦 Total Itens Vendidos", total_vendas)
    col3.metric("🏆 Melhor Filial", melhor_filial)

    st.divider()

    # 4. Gráficos Interativos (Plotly)
    col_grafico1, col_grafico2 = st.columns(2)
    
    # Gráfico 1: Faturamento por Filial
    with col_grafico1:
        st.subheader("Faturamento por Filial")
        vendas_filial = df.groupby('filial')[['Faturamento']].sum().reset_index()
        
        fig_faturamento = px.bar(
            vendas_filial, 
            x='filial', 
            y='Faturamento',
            title='Faturamento por Filial',
            color='filial',
            text_auto='.2s'
        )
        st.plotly_chart(fig_faturamento, use_container_width=True)

    # Gráfico 2: Ranking de Produtos
    with col_grafico2:
        st.subheader("Ranking de Produtos")
        vendas_produto = df.groupby('produto')[['quantidade']].sum().reset_index()
        vendas_produto = vendas_produto.sort_values(by='quantidade', ascending=True)
        
        fig_produtos = px.bar(
            vendas_produto, 
            x='quantidade', 
            y='produto', 
            orientation='h',
            title='Ranking de Produtos',
            color='quantidade',
            text_auto=True
        )
        st.plotly_chart(fig_produtos, use_container_width=True)

    # 5. Filtro Interativo
    st.divider()
    st.subheader("🔍 Filtro de Dados")
    
    filial_selecionada = st.selectbox("Escolha uma Filial:", df['filial'].unique())
    df_filtrado = df[df['filial'] == filial_selecionada]
    
    st.write(f"Mostrando vendas de: **{filial_selecionada}**")
    st.dataframe(df_filtrado, use_container_width=True)