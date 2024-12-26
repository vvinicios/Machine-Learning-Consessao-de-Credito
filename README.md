# Machine-Learning-Consessao-de-Credito
Este projeto tem como objetivo desenvolver um modelo preditivo baseado em machine learning para auxiliar na análise de risco de crédito, utilizando dados históricos para identificar padrões que possam indicar a probabilidade de inadimplência.

Através deste repositório, documentarei cada etapa do processo, desde a coleta e preparação dos dados até a criação, validação e Deploy do modelo, também passarei por etapas de criar uma API para servir o modelo usando Python e, por fim, a criação da interface visual onde o Analista Financeiro digitará todas as informações do cliente.

### 1. Tratamento inicial do banco de dados utilizando SQL
Nesta etapa, o objetivo é preparar os dados para análise, garantindo que estejam consistentes e prontos para uso. As ações realizadas incluem:

- Compreensão das fontes de dados: Estudo das tabelas disponíveis e suas relações, incluindo identificação de chaves primárias e estrangeiras.
- Conexão ao banco de dados: Utilização do PostgreSQL para acessar e manipular os dados.
- Normalização do banco de dados: Ajustes no esquema de dados para eliminar redundâncias e garantir integridade.
- Transformação de data de nascimento em idade: Extração do número correspondente à idade de cada pessoa.
- Criação de categorias de atraso: Inclusão de um parâmetro categórico que identifica registros com atraso em alguma fatura, facilitando futuras análises.
