import requests, json
import pandas as pd

# Função de captura de produtos a partir do assinaturas
def captura_produtos(id_sacado, headers):
    url = f"https://api.superlogica.net/v2/financeiro/assinaturas?ID_SACADO_SAC={id_sacado}&pagina=1&itensPorPagina=50&comContrato=&avulsas="
    response = requests.get(url, headers=headers).json()
    assinaturas = response[0]['data']
    produtos = []

    for assinatura in assinaturas:
        assin = {}

        assin['licença'] = assinatura['st_identificador_plc']
        assin['nome do plano'] = assinatura['st_nome_pla']
        assin['categoria do plano'] = assinatura['st_nome_gpl']
        assin['data de inicio'] = assinatura['dt_contrato_plc']
        if assinatura['dt_cancelamento_plc'] == '':
            assin['status'] = 'ativo'
        else:
            assin['status'] = 'inativo'
            assin['cancelamento'] = assinatura['dt_cancelamento_plc']
        if assinatura['fl_periodicidade_pla'] == '1':
            assin['periodicidade'] = 'anual'
        else:
            assin['periodicidade'] = 'mensal'

        for produto in assinatura['mensalidade']:
            descricao = produto.get('st_descricao_prd', '').lower()
            valor_mens = produto.get('st_valor_mens')

            if 'taxa de licenciamento' in descricao:
                assin['produto'] = "ERP"
                assin['mensalidade'] = valor_mens
            elif 'owli' in descricao:
                assin['produto'] = "Owli"
                assin['mensalidade'] = valor_mens
            elif 'crm cobranças' in descricao:
                assin['produto'] = "CRM Cobranças"
                assin['mensalidade'] = valor_mens
            elif 'descontos' in descricao:
                assin['desconto'] = valor_mens

        produtos.append(assin)
    return produtos

# Função de captura de contatos a partir do ID da empresa no Hubspot
def captura_contatos(headers_hubspot, id_empresa):
    url = f"https://api.hubapi.com/crm/v4/objects/companies/{id_empresa}/associations/contact"
    response = requests.get(url, headers=headers_hubspot).json()
    contatos = response['results']
    lista_contatos = []
    for contato in contatos:
        lista_contatos.append(f"{contato['toObjectId']}")

    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"

    data = {
        "limit": 100,
        "after": None,
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_object_id",
                        "operator": "IN",
                        "values": lista_contatos
                    }]
            }
        ]
    }

    response = requests.post(url, headers=headers_hubspot, data=json.dumps(data)).json()
    return response['results']

# Função de captura negócios a partir de data
def captura_negocios_desde_data(headers_hubspot, id_empresa, data_formatada):
    url = f"https://api.hubapi.com/crm/v4/objects/companies/{id_empresa}/associations/deal"
    response = requests.get(url, headers=headers_hubspot).json()
    negocios = response['results']
    lista_negocios = []
    for negocio in negocios:
        lista_negocios.append(f"{negocio['toObjectId']}")

    url = "https://api.hubapi.com/crm/v3/objects/deals/search"

    data = {
      "limit": 100,
      "after": None,
      "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_object_id",
                        "operator": "IN",
                        "values": lista_negocios
                    },
                    {
                        "propertyName": "createdate",
                        "operator": "GTE",
                        "value": data_formatada # Criar condicional de últimos 12 meses
                    },
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers_hubspot, data=json.dumps(data)).json()
    return response['results']

# Função de captura de tickets
def captura_tickets(headers_hubspot, id_empresa):
    url = f"https://api.hubapi.com/crm/v4/objects/companies/{id_empresa}/associations/ticket"
    response = requests.get(url, headers=headers_hubspot).json()
    tickets = response['results']
    lista_tickets = []
    for ticket in tickets:
        lista_tickets.append(f"{ticket['toObjectId']}")

    url = "https://api.hubapi.com/crm/v3/objects/tickets/search"

    data = {
        "limit": 100,
        "after": None,
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_object_id",
                        "operator": "IN",
                        "values": lista_tickets
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers_hubspot, data=json.dumps(data)).json()
    return response['results']

# Função de captura de tarefas a partir de data
def captura_tarefas_desde_data(headers_hubspot, id_empresa, data_formatada):
    url = f"https://api.hubapi.com/crm/v4/objects/companies/{id_empresa}/associations/task"
    response = requests.get(url, headers=headers_hubspot).json()
    tarefas = response['results']
    lista_tarefas = []
    for tarefa in tarefas:
        lista_tarefas.append(f"{tarefa['toObjectId']}")

    url = "https://api.hubapi.com/crm/v3/objects/tasks/search"

    data = {
        "limit": 100,
        "after": None,
        "properties": ['hs_task_status', 'hs_task_subject', 'hs_createdate', 'hs_task_type', 'hs_lastmodifieddate', 'hs_created_by', 'hs_pipeline', 'hs_pipeline_stage', 'hubspot_owner_id'],
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_object_id",
                        "operator": "IN",
                        "values": lista_tarefas
                    },
                    {
                        "propertyName": "hs_createdate",
                        "operator": "GTE",
                        "value": data_formatada
                    },
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers_hubspot, data=json.dumps(data)).json()
    return response['results']

# Função de captura de reuniões a partir de data
def captura_reunioes_desde_data(headers_hubspot, id_empresa, data_formatada):
    url = f"https://api.hubapi.com/crm/v4/objects/companies/{id_empresa}/associations/meeting"
    response = requests.get(url, headers=headers_hubspot).json()
    reunioes = response['results']
    lista_reunioes = []
    for reuniao in reunioes:
        lista_reunioes.append(f"{reuniao['toObjectId']}")

    url = "https://api.hubapi.com/crm/v3/objects/meetings/search"

    data = {
        "limit": 100,
        "after": None,
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_object_id",
                        "operator": "IN",
                        "values": lista_reunioes
                    },
                    {
                        "propertyName": "hs_createdate",
                        "operator": "GTE",
                        "value": data_formatada
                    },
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers_hubspot, data=json.dumps(data)).json()
    return response['results']

# Função de captura dos pipelines do Hubspot
def captura_pipelines(headers_hubspot, tipo):
    url = f"https://api.hubapi.com/crm/v3/pipelines/{tipo}"

    # Define os parâmetros da query string da requisição
    params = {
        "includeInactive": "false"
    }

    # Faz a requisição GET para o endpoint da API do Hubspot
    response = requests.get(url, headers=headers_hubspot, params=params)

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        # Extrai a lista de pipelines da resposta da API e imprime na tela os nomes e IDs de cada pipeline
        pipelines = response.json().get("results")
        for pipeline in pipelines:
            print(f"Nome: {pipeline.get('label')}, ID: {pipeline.get('id')}")
        return pipelines
    else:
        # Imprime uma mensagem de erro caso a requisição não tenha sido bem sucedida
        print(f"Erro ao buscar os pipelines: {response.status_code} - {response.text}")

# Função de captura dos owners do Hubspot
def captura_owners(headers_hubspot):
    # Configurar a URL da solicitação GET para a endpoint da Owners API
    url = "https://api.hubapi.com/owners/v2/owners"

    # Fazer a solicitação GET para a API
    response = requests.get(url, headers=headers_hubspot)
    df = pd.DataFrame(response.json())

    owners = df.loc[:,['ownerId', 'firstName', 'lastName',	'email', 'isActive']]
    return owners

# Função de captura dos tickets no Zendesk pelo e-mail
def captura_tickets_email(email, headers_zendesk):
    url = "https://condominios.zendesk.com/api/v2/search.json"

    params = {
        'query': f"type:ticket brand_id:360000535754 requester:{email} created>2024-08-01T10:30:00Z",
    }

    all_results = []

    response = requests.request("GET", url, headers=headers_zendesk, params=params)
    returned = json.loads(response.content)
    all_results.extend(returned['results'])

    while returned['next_page'] is not None:
        url = returned['next_page']
        response = requests.request("GET", url, headers=headers_zendesk)
        returned = json.loads(response.content)
        all_results.extend(returned['results'])
    
    return all_results