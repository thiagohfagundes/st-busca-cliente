import streamlit as st
import pandas as pd
import math, ast

banco = pd.read_csv('Banco de dados - Página1.csv')

def convert_to_list(string):
    if string in ['nan', '[nan]']:
        return []
    try:
        # Usa ast.literal_eval para avaliar a string de forma segura
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        return []

# Converta a coluna de strings de listas em listas reais
colunas_listas = ['st_nome_pla', 'st_identificador_plc', 'id_sacado_sac', 'cs_erp_responsavel', 'is__cs_responsavel_1']

for coluna in colunas_listas:
    banco[coluna] = banco[coluna].apply(convert_to_list)

st.data_editor(
    banco,
    column_config={
        "st_nome_pla": st.column_config.ListColumn(
            "Nome do plano",
            help="Nome do plano no assinaturas",
        ),
        "st_identificador_plc": st.column_config.ListColumn(
            "Licenças",
            help="Nome das licenças no assinaturas",
        ),
        "id_sacado_sac": st.column_config.ListColumn(
            "ids no Assinaturas",
            help="Números dos Ids no assinaturas",
        ),
    },
)

cliente = banco.iloc[0]

st.write(cliente)