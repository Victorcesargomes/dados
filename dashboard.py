import pandas as pd
import random
import folium
from streamlit_folium import folium_static
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px


# Definir estilo padrão para os gráficos
plt.style.use('seaborn-whitegrid')

# Definir tema do Streamlit
st.set_page_config(
    page_title="Dashboard de Pizzas",
    layout="wide",
    page_icon="🍕",
    initial_sidebar_state="expanded"
)

logo_image = "VV.png"
st.image(logo_image, width=600)

# Dados fictícios para as colunas
valores_pizza = [random.randint(10, 50) for _ in range(30)]
nomes_clientes = ['Cliente {}'.format(i+1) for i in range(30)]
idades = [random.randint(18, 65) for _ in range(30)]
cidades = ['Abreu e Lima', 'Paulista', 'Igarassu'] * 10
bairros = ['Bairro 1', 'Bairro 2', 'Bairro 3', 'Bairro 4', 'Bairro 5'] * 6
num_compras_mes = [random.randint(1, 10) for _ in range(30)]
latitude = [random.uniform(-7.84625, -7.9775) for _ in range(30)]  # Latitudes aproximadas para Abreu e Lima, Paulista e Igarassu
longitude = [random.uniform(-34.806, -34.898) for _ in range(30)]  # Longitudes aproximadas para Abreu e Lima, Paulista e Igarassu

# Criação do DataFrame
data = {
    'VALOR_PIZZA': valores_pizza,
    'NOME_CLIENTE': nomes_clientes,
    'IDADE': idades,
    'CIDADE': cidades,
    'BAIRRO': bairros,
    'NUMERO_COMPRAS_MES': num_compras_mes,
    'LATITUDE': latitude,
    'LONGITUDE': longitude
}

df = pd.DataFrame(data)

# Exibindo o DataFrame
#print(df)

# Indicadores
maior_compras_mes = df.loc[df['NUMERO_COMPRAS_MES'].idxmax()]
maior_preco_pizza = df.loc[df['VALOR_PIZZA'].idxmax()]
cliente_mais_compras = df.loc[df['NUMERO_COMPRAS_MES'].idxmax(), 'NOME_CLIENTE']
cidade_mais_clientes = df['CIDADE'].value_counts().idxmax()
# Agrupar os dados por cidade e calcular o faturamento total de pizzas em cada cidade
#faturamento_por_cidade = df.groupby('CIDADE')['VALOR_PIZZA'].sum()
faturamento_por_cidade = df.groupby('CIDADE')['VALOR_PIZZA'].sum().reset_index()

# Configurando layout em uma única coluna
#col1, col2, col3 = st.columns(3)

# Coluna 1 (indicador de cliente com mais compras)
#with col1:
 #  st.markdown('<style>div.stButton > button:first-child {border-radius: 50%;}</style>', unsafe_allow_html=True)
 #  st.markdown(f'''
  #      <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
   #         <p style="margin-bottom: 10px; font-size: 14px; font-weight: bold; color: #555;">Cliente com mais compras no mês</p>
    #        <button class="stButton" style="background-color: #F63366; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;">{cliente_mais_compras}</button>
     #   </div>
    #''', unsafe_allow_html=True)

# Coluna 2 (indicador de maior preço da pizza)
#with col2:
 #    st.markdown('<style>div.stButton > button:first-child {border-radius: 50%;}</style>', unsafe_allow_html=True)
  #   st.markdown(f'''
   #     <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
    #        <p style="margin-bottom: 10px; font-size: 14px; font-weight: bold; color: #555;">Pizza com maior preço</p>
     #       <button class="stButton" style="background-color: #FFBB33; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;">R${maior_preco_pizza['VALOR_PIZZA']}</button>
      #  </div>
    #''', unsafe_allow_html=True)

# Coluna 3 (indicador de cidade com mais clientes)
#with col3:
 #   st.markdown('<style>div.stButton > button:first-child {border-radius: 50%;}</style>', unsafe_allow_html=True)
  #  st.markdown(f'''
   #     <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
    #        <p style="margin-bottom: 10px; font-size: 14px; font-weight: bold; color: #555;">Município com mais clientes</p>
     #       <button class="stButton" style="background-color: #33B2FF; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;">{cidade_mais_clientes }</button>
      #  </div>
    #''', unsafe_allow_html=True)
# Exibindo o mapa no Streamlit
#st.title('Mapa de Clientes')
#folium_static(mapa)

# Configurando layout em uma única linha (indicadores na parte esquerda, mapa na parte direita)
st.markdown('<style>div.row-widget.stHorizontal {flex-wrap: nowrap;}</style>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

# Coluna 1 (indicador do cliente com mais compras no mês)
with col1:
      st.markdown(f'''
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <p style="margin-bottom: 5px; font-size: 14px; font-weight: bold; color: #555; text-align: center;">Cliente com maior quantidade de compras no mês</p>
            <button class="stButton" 
                    style="background-color: #F63366; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;" 
                    title="Quantidade de Compras: {maior_compras_mes['NUMERO_COMPRAS_MES']}">
                {cliente_mais_compras}
            </button>
        </div>
    ''', unsafe_allow_html=True)

# Coluna 2 (indicador do maior preço da pizza)
with col2:
    st.markdown('<style>div.stButton > button:first-child {border-radius: 50%;}</style>', unsafe_allow_html=True)
    st.markdown(f'''
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <p style="margin-bottom: 10px; font-size: 14px; font-weight: bold; color: #555;">Valor da Pizza mais cara do estabelecimento</p>
            <button class="stButton" style="background-color: #FFBB33; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;">R${maior_preco_pizza['VALOR_PIZZA']}</button>
        </div>
    ''', unsafe_allow_html=True)

# Coluna 3 (indicador do município com mais clientes)
with col3:
    st.markdown(f'''
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <p style="margin-bottom: 5px; font-size: 14px; font-weight: bold; color: #555; text-align: center;">Município com a maior quantidade de clientes</p>
            <button class="stButton" style="background-color: #33B2FF; color: white; width: 200px; height: 200px; font-size: 24px; border-radius: 50%;">{cidade_mais_clientes}</button>
        </div>
    ''', unsafe_allow_html=True)

with col4:
    # Criar uma lista de cores para o gráfico de pizza
    # Criar uma lista de cores para o gráfico de pizza
    cores = ['#FF7070', '#FFAA70', '#FFD670', '#FFFA70', '#D6FF70']

    fig = px.pie(faturamento_por_cidade, values='VALOR_PIZZA', names='CIDADE')
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=cores))
    fig.update_layout(
        title='Participação das Cidades no Faturamento',
        width=600,
        height=400,

        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12)
)
    fig.update_layout(
    #plot_bgcolor='white',
    #paper_bgcolor='white',
    title_font_color='#555',
    legend_font_color='#555',
    legend_title_font_color='#555',
    font_color='#555',
    hoverlabel=dict(
        font=dict(color='#555')
    )
)

    st.plotly_chart(fig)


st.markdown("---")


# Configurando layout em uma única linha (gráficos lado a lado)
col1, col2 = st.columns(2)

# Gráfico de barras do valor total da pizza por cidade
with col1:
    #st.subheader('Valor Total de Pizzas Vendidas por Cidade')
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    df_cidades = df.groupby('CIDADE')['VALOR_PIZZA'].sum().reset_index()
    fig1 = px.bar(df_cidades, x='CIDADE', y='VALOR_PIZZA', color='CIDADE',
                  labels={'CIDADE': 'Cidade', 'VALOR_PIZZA': 'Valor Total de Pizzas Vendidas'},
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig1.update_layout(title='Valor Total de Pizzas Vendidas por Cidade',
                       xaxis_title='Cidade',
                       yaxis_title='Valor Total de Pizzas Vendidas',
                       legend_title='Cidade')
    fig1.update_traces(textposition='outside')
    fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig1.update_xaxes(tickangle=45, tickfont=dict(size=10))
    st.plotly_chart(fig1)
# Gráfico de barras do número de compras por mês agrupados por cliente
with col2:
    #st.subheader('Número de Compras por Mês (Agrupados por Cliente)')
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    df_clientes = df.groupby('NOME_CLIENTE')['NUMERO_COMPRAS_MES'].sum().reset_index()
    fig2 = px.bar(df_clientes, x='NUMERO_COMPRAS_MES', y='NOME_CLIENTE', color='NOME_CLIENTE',
                  labels={'NUMERO_COMPRAS_MES': 'Número de Compras', 'NOME_CLIENTE': 'Cliente'},
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(title='Número de Compras por Mês (Agrupados por Cliente)',
                       xaxis_title='Número de Compras',
                       yaxis_title='Cliente',
                       legend_title='Cliente')
    fig2.update_traces(textposition='outside')
    fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig2.update_yaxes(tickangle=45, tickfont=dict(size=10))
    st.plotly_chart(fig2)
# Exibindo o mapa no Streamlit
#st.title('Mapa de Clientes')
#folium_static(mapa)
# Exibindo o mapa no Streamlit
#st.title('Mapa de Clientes')
#with col4:
st.markdown("---")



# Criando o mapa
mapa = folium.Map(location=[-7.9047, -34.9026], zoom_start=12)  # Localização central do mapa

# Adicionando marcadores ao mapa
for _, row in df.iterrows():
    valor_pizza = row['VALOR_PIZZA']
    nome_cliente = row['NOME_CLIENTE']
    idade = row['IDADE']
    cidade = row['CIDADE']
    bairro = row['BAIRRO']
    num_compras_mes = row['NUMERO_COMPRAS_MES']
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    
    popup_html = f'''
    <strong>Nome:</strong> {nome_cliente}<br>
    <strong>Valor da Pizza:</strong> R${valor_pizza}<br>
    <strong>Idade:</strong> {idade}<br>
    <strong>Número de Compras por Mês:</strong> {num_compras_mes}
    '''
    
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_html,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mapa)

# Configurações do estilo do mapa
folium.TileLayer('openstreetmap').add_to(mapa)  # Camada base do mapa
folium.TileLayer('cartodbpositron').add_to(mapa)  # Camada de fundo claro
folium.TileLayer('cartodbdark_matter').add_to(mapa)  # Camada de fundo escuro
folium.LayerControl().add_to(mapa)  # Controle de camadas

# Exibindo o mapa no Streamlit
st.header('Mapa de Clientes')
folium_static(mapa, width=1400, height=600)  # Tamanho e posição ajustados

# Gráficos e outras seções do painel...

