import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

banco = pd.read_csv('Banco de dados - Página1.csv')

#visualizacao = banco[['st_nome_sac', 'st_nomeref_sac', 'st_cidade_sac', 'st_identificador_plc']]

def buscar_no_dataframe(df, criterio):
    resultado = df[
        df.apply(lambda row: row.astype(str).str.contains(criterio, case=False).any(), axis=1)
    ]
    return resultado

with st.form(key='formulario'):
    busca = st.text_input("Busque seu cliente")
    botao = st.form_submit_button(label="Buscar")


if botao:
    # Realizar a busca
    resultado = buscar_no_dataframe(banco, busca)
    st.data_editor(
        resultado,
        column_config={
            "st_identificador_plc": st.column_config.ListColumn(
                "Licenças no assinaturas",
                help="The sales volume in the last 6 months",
                width="medium",
            ),
            "st_cgc_sac": st.column_config.NumberColumn(
                "CNPJ ou CPF",
                help="The sales volume in the last 6 months",
                width="medium",
                format='%d'
            ),
        },
        hide_index=True,
    )

else:
    st.data_editor(
        banco,
        column_config={
            "st_identificador_plc": st.column_config.ListColumn(
                "Sales (last 6 months)",
                help="The sales volume in the last 6 months",
                width="medium",
            ),
            "st_cgc_sac": st.column_config.NumberColumn(
                "CNPJ ou CPF",
                help="The sales volume in the last 6 months",
                width="medium",
                format='%d'
            ),
        },
        hide_index=True,
    )


