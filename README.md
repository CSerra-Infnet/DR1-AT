# AT - Sport Analytics

![Poster](/prints/DR1-AT-1.png)

O uso de dados no esporte, especialmente no futebol, tem se tornado essencial para análise de desempenho, estratégias táticas e decisões de gestão. Uma partida de futebol pode gerar milhões de dados, desde estatísticas detalhadas como passes, chutes e movimentações dos jogadores, até dados mais complexos sobre a performance de uma equipe. Utilizar esses dados para criar visualizações interativas e informativas permite que técnicos, analistas, gestores e até mesmo fãs tomem decisões mais embasadas.

O mercado de Sport Analytics está em franco crescimento, como podemos constatar a partir do gráfico abaixo:

![Grafico](/prints/DR1-AT-2.png)

<b>Neste projeto, você terá a oportunidade de criar um dashboard interativo usando Streamlit e as bibliotecas StatsBombPy e mplsoccer. O objetivo do seu dashboard é responder a alguma pergunta que você tenha sobre futebol ⚽.</b> Isso pode ser algo como:

- Qual jogador deu mais passes em um determinado campeonato?
- Como o número de gols marcados por uma equipe se relaciona com sua quantidade de chutes?
- Quais foram os principais eventos de uma partida específica?

Seja criativo e defina uma pergunta clara que você deseja responder usando dados reais de futebol. Utilize diversas visualizações e opções do streamlit no seu desenvolvimento. Abaixo segue um roteiro de atividades. 

## Tarefas a serem realizadas

1. **Preparar o ambiente de desenvolvimento:**

- [x] Crie um ambiente virtual para seu projeto utilizando uma ferramenta como venv, virtualenv ou pipenv.
- [x] Instale as bibliotecas necessárias (Streamlit, statsbombpy, mplsoccer, matplotlib, entre outras).

2. **Estruturar o projeto:**
- [x] Crie um repositório no GitHub para hospedar o código do seu projeto.
- [x] Garanta que o repositório contenha um arquivo requirements.txt com as dependências necessárias para rodar o projeto.
- [x] Organize o código de forma clara, criando funções separadas para carregar os dados, gerar as visualizações e construir a interface do dashboard.

3. **Definir a estrutura do dashboard:**

- [x] Desenvolva uma interface interativa em Streamlit que permita ao usuário selecionar:
- [x] Um campeonato específico.
- [x] Uma temporada (ano).
- [x] Uma partida ou jogador para análise.
- [x] Organize o layout do dashboard em colunas, usando columns, sidebars, containers e tabs para melhorar a usabilidade.

4. **Obter dados e exibir informações básicas**
- [x] Use a biblioteca StatsBombPy para carregar dados de competições, temporadas, partidas e jogadores.
- [x] Mostre, em uma página do dashboard, as seguintes informações:
- [x] Nome da competição, temporada e partida selecionada.
- [x] Estatísticas básicas da partida (gols, chutes, passes, etc.).
- [x] Um DataFrame exibindo os eventos da partida, como passes, finalizações e desarmes.

5. **Criar visualizações de dados**
- [x] Utilize a biblioteca mplsoccer para gerar um mapa de passes e mapa de chutes para uma partida específica. Garanta que o gráfico seja interativo, com legendas e informações que ajudem a interpretar os dados.
- [x] Crie visualizações adicionais com Matplotlib e Seaborn para explorar relações entre as estatísticas de uma partida ou de um jogador (por exemplo, relação entre número de passes e gols).
- [x] Utilize a biblioteca mplsoccer para novas visualizações de acordo com sua galeria (https://mplsoccer.readthedocs.io/en/latest/gallery/index.html)

6. **Adicionar interatividade**
- [x] Adicione seletores de jogadores e botões de filtro que permitam ao usuário visualizar apenas eventos relacionados a um jogador específico.
- [x] Inclua botões de download que permitam ao usuário baixar os dados filtrados da partida em formato CSV.
- [x] Utilize barras de progresso e spinners para informar ao usuário que os dados estão sendo carregados ou processados.

7. **Incluir métricas e indicadores**
- [x] Exiba indicadores numéricos usando a função metric() do Streamlit para mostrar, por exemplo:
- [x] Total de gols da partida.
- [x] Quantidade de passes bem-sucedidos de um jogador.
- [x] Taxa de conversão de chutes em gol.
- [x] Personalize esses indicadores com cores que realcem os valores mais importantes.

8. **Criar formulários interativos**
- [x] Desenvolva formulários simples que permitam ao usuário escolher, por exemplo, a quantidade de eventos a serem visualizados, o intervalo de tempo de uma partida ou a comparação entre dois jogadores.
- [x] Use elementos como caixas de texto, dropdowns, radio buttons e checkboxes para tornar a interação mais fluida.

9. **Implementar funcionalidades avançadas**
- [x] Utilize o Cache do Streamlit para otimizar o carregamento de dados, especialmente se estiver utilizando bases de dados grandes.
- Armazene o estado da sessão do usuário utilizando Session State, garantindo que a interação do usuário não seja perdida quando ele navegar entre páginas.

10. **Publicar o projeto**
- [x] Realize o deploy da aplicação utilizando o Streamlit Community Cloud. Verifique se o deploy foi bem-sucedido e que todas as funcionalidades estão funcionando conforme esperado.
- [x] Compartilhe o link da aplicação publicada e o repositório no GitHub.


Este projeto oferece uma oportunidade de aplicar as habilidades de desenvolvimento front-end com Python e de cientista de dados, que utiliza seus conhecimentos para resolver problemas reais, como a análise de dados esportivos (sports analytics), combinando dados reais de futebol com visualizações interativas aplicáveis a cenários reais de tomada de decisão e análise.

Boa sorte no Assessment e saudações rubro-negras ⚽