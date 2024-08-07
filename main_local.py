import streamlit as st
import pandas as pd
from funcoes import captura_produtos, captura_contatos, captura_cobrancas
from funcoes_tratamento import trata_listas, trata_cobrancas
from supabase import create_client, Client

st.set_page_config(layout="wide")

access_token_hubspot = st.secrets["access_token"]
app_token_assinas = st.secrets["app_token_assinas"]
access_token_assinas = st.secrets["access_token_assinas"]
url_supabase = st.secrets["url_supabase"]
key_supabase = st.secrets["key_supabase"]

headers_hubspot = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {access_token_hubspot}"
}

headers_assinaturas = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'app_token': f"{app_token_assinas}",
    'access_token': f"{access_token_assinas}"
}

@st.cache_resource
def init_connection():
    url = url_supabase
    key = key_supabase
    return create_client(url, key)

supabase = init_connection()

@st.cache_resource
def run_query():
    return supabase.table("clientes-sl").select("*").execute()

rows = run_query()
if rows.data:
    banco = pd.DataFrame(rows.data)

def buscar_no_dataframe(df, criterio):
    resultado = df[
        df.apply(lambda row: row.astype(str).str.contains(criterio, case=False).any(), axis=1)
    ]
    return resultado


# Função para exibir detalhes do cliente
@st.dialog("Detalhes do cliente", width="large")
def consulta_cliente(index):
    cliente = banco.iloc[index]
    st.subheader("Dados gerais")
    st.write(cliente)
    ids_assinaturas = trata_listas(cliente['id_sacado_sac'])
    ids_hubspot = trata_listas(cliente['hs_object_id'])
    lista_produtos = []
    lista_cobrancas = []

    for id in ids_assinaturas:
        produtos = captura_produtos(id, headers_assinaturas)
        cobrancas = captura_cobrancas(id, headers_assinaturas)
        lista_produtos.extend(produtos)
        lista_cobrancas.extend(cobrancas)

    produtos = pd.DataFrame(lista_produtos)
    st.subheader('Produtos SaaS')
    st.write(produtos)
    lista_contatos = []

    for id in ids_hubspot:
        contatos = captura_contatos(id, headers_hubspot)
        lista_contatos.extend(contatos)

    contatos = pd.DataFrame(lista_contatos)
    st.subheader('Pessoas')
    with st.expander('Ver pessoas'):
        st.write(contatos)

    cobrancas = trata_cobrancas(lista_cobrancas)
    st.subheader('Cobranças')
    with st.expander('Ver últimas cobranças'):
        st.write(cobrancas)


# Inicializando session state para armazenar o índice do cliente
if 'cliente_index' not in st.session_state:
    st.session_state.cliente_index = None

# Formulário de busca
with st.form(key='formulario'):
    st.header("Busca de clientes")
    st.write("Busque seu cliente por Razão Social, Nome Fantasia, Licença, CNPJ (apenas números), E-mail (apenas números). É possível encontrar as informações com apenas parte da palavra na busca.")
    busca = st.text_input("Busque seu cliente:")
    botao = st.form_submit_button(label="Buscar")

if botao:
    # Realizar a busca e armazenar resultados no session state
    st.session_state.resultado = buscar_no_dataframe(banco, busca)

if 'resultado' in st.session_state:
    resultado = st.session_state.resultado
    st.header('Resultado da busca 🔎', divider=True)

    for index, row in resultado.iterrows():
         st.subheader(f"Razão social: {row['st_nome_sac']}")
         st.markdown(f"Licença(s): {row['st_identificador_plc']}")
         st.write(f"Plano(s): {row['st_nome_pla']}")

         if st.button("ver mais", key=f"detalhes_{index}"):
            st.session_state.cliente_index = index

         st.divider()

# Mostrar detalhes do cliente se um botão foi clicado
if st.session_state.cliente_index is not None:
    consulta_cliente(st.session_state.cliente_index)
