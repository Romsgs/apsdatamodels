"""
main.py

Um script para autenticar com a API da Autodesk, recuperar hubs e projetos, e navegar
através dos elementGroups dentro de projetos selecionados.

Funções:
    - traverse_element_groups: Percorre recursivamente e exibe a hierarquia de elementGroups.
    - main: Orquestra a autenticação, recuperação de hubs, seleção de projetos e navegação pelos elementGroups.

Uso:
    Execute o script e ele processará os projetos listados em `project_list`.
"""

import logging
from autodesk_api import (
    get_access_token,
    get_hubs,
    get_projects,
    get_root_element_group,
    get_element_group_children,
)
import sys

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def traverse_element_groups(access_token, project_id, group_id, level=0):
    """
    Percorre recursivamente e exibe a hierarquia de elementGroups dentro de um projeto.

    Esta função recupera os elementGroups filhos do `group_id` especificado dentro do `project_id` dado
    e imprime seus nomes e IDs. A indentação é utilizada para representar a profundidade de cada grupo na hierarquia.

    Args:
        access_token (str): O token de acesso OAuth 2.0 para autenticação nas requisições à API.
        project_id (str): O identificador único do projeto cujo elementGroups estão sendo percorridos.
        group_id (str): O identificador único do elementGroup atual para recuperar os filhos.
        level (int, opcional): O nível atual de profundidade na hierarquia para fins de indentação.
            Padrão é 0.

    Returns:
        None

    Raises:
        None

    Example:
        traverse_element_groups(access_token, "b.1234", "eg.5678", level=1)
    """
    # Recupera os filhos do group_id atual
    children_data = get_element_group_children(access_token, project_id, group_id)
    if not children_data:
        logging.warning(f"Nenhum filho encontrado para o elementGroup ID: {group_id}")
        return

    children = children_data.get('data', [])
    for child in children:
        group_name = child['attributes'].get('name', 'Grupo Sem Nome')
        child_group_id = child['id']
        indent = '  ' * level
        logging.info(f"{indent}- {group_name} (ID: {child_group_id})")
        # Percorre recursivamente os grupos filhos
        traverse_element_groups(access_token, project_id, child_group_id, level + 1)


def main():
    """
    Função principal para autenticar, recuperar hubs e projetos, e navegar pelos elementGroups dentro de projetos selecionados.

    O fluxo da função realiza os seguintes passos:
        1. Autentica-se com a API da Autodesk para obter um token de acesso.
        2. Recupera a lista de hubs associados à conta autenticada.
        3. Seleciona o primeiro hub (assumindo que há apenas um).
        4. Recupera a lista de projetos dentro do hub selecionado.
        5. Define a lista `project_list` contendo os IDs dos projetos a serem processados.
        6. Para cada projeto na `project_list`, recupera o elementGroup raiz e percorre sua hierarquia.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Uso:
        Execute o script e ele processará os projetos listados em `project_list`.
    """
    # Passo 1: Autenticação e obtenção do token de acesso
    access_token = get_access_token()
    if not access_token:
        logging.error('Encerrando devido à falha na autenticação.')
        return

    # Passo 2: Recuperar hubs
    hubs_data = get_hubs(access_token)
    if not hubs_data:
        logging.error('Encerrando devido à falha na recuperação dos hubs.')
        return

    hubs = hubs_data.get('data', [])
    if not hubs:
        logging.error('Nenhum hub encontrado.')
        return

    # Seleciona o primeiro hub (assumindo que há apenas um)
    selected_hub = hubs[0]
    hub_id = selected_hub['id']
    hub_name = selected_hub['attributes'].get('name', 'Hub Sem Nome')
    logging.info(f'Selected Hub: {hub_name} (ID: {hub_id})')

    # Passo 3: Recuperar projetos do hub selecionado
    projects_data = get_projects(access_token, hub_id)
    if not projects_data:
        logging.error('Encerrando devido à falha na recuperação dos projetos.')
        return

    projects = projects_data.get('data', [])
    if not projects:
        logging.error('Nenhum projeto encontrado no hub selecionado.')
        return

    # Exibir a lista de projetos
    logging.info('\nProjetos Disponíveis:')
    for idx, project in enumerate(projects):
        project_name = project['attributes']['name']
        project_id = project['id']
        logging.info(f'{idx + 1}. {project_name} (ID: {project_id})')

    # Definir a lista de projetos a serem processados
    # Exemplo: processar todos os projetos
    project_list = [project['id'] for project in projects]

    # Se preferir processar apenas alguns projetos, você pode definir manualmente:
    # project_list = [
    #     "a.1234567890abcdef",
    #     "a.abcdef1234567890",
    # ]

    # Passo 4: Iterar sobre a lista de projetos e processar cada um
    for project_id in project_list:
        # Recuperar informações do projeto atual
        project = next((p for p in projects if p['id'] == project_id), None)
        if not project:
            logging.warning(f'Projeto com ID {project_id} não encontrado na lista de projetos.')
            continue

        project_name = project['attributes']['name']
        logging.info(f'\nProcessando Projeto: {project_name} (ID: {project_id})')

        # Recuperar o elementGroup raiz do projeto
        root_group_data = get_root_element_group(access_token, project_id)
        if not root_group_data:
            logging.error(f'Encerrando processamento do projeto {project_name} devido à falha na recuperação do elementGroup raiz.')
            continue

        root_group = root_group_data.get('data', {})
        root_group_id = root_group.get('id')
        root_group_name = root_group['attributes'].get('name', 'Grupo Raiz')

        logging.info(f'\nElementGroup Raiz: {root_group_name} (ID: {root_group_id})\n')

        # Percorrer e exibir a hierarquia de elementGroups
        traverse_element_groups(access_token, project_id, root_group_id)


if __name__ == '__main__':
    main()
