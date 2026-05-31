#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/lovelace:0.3.0": *

#show bibliography: set std.bibliography(title: text(10pt)[Referências])

#show: ieee.with(
  title: [IF848 Detecção de Intrusão \ Template para relatório de projeto (SUBSTITUIR PELO TÍTULO DO PROJETO)],
  abstract: [
    Breve apresentação do contexto do trabalho, problema a ser abordado, soluções existentes, método proposto e resultados obtidos.
  ],
  authors: yaml("authors.yml"),
  bibliography: bibliography("refs.bib"),
)

= Introdução

Deverá abordar a motivação, justificativa e principais contribuições do trabalho em questão. Alguns pontos que devem ser abordados de forma *breve*, são:

- Qual o problema que está sendo investigado?
- Por que ele é interessante?
- Por que foi necessário que o artigo de referência propusesse tal solução?
- Quais as soluções existentes e suas desvantangens?
- O que está sendo proposto para resolver o problema em questão?
- As principais contribuições do trabalho em formato de lista.

Exemplo: as principais contribuições deste template de relatório são:

- Facilitar a escrita do relatório do projeto da disciplina de detecção de intrusão;
- Explicar brevemente os conteúdos a serem abordados em cada seção do relatório.

= Trabalhos relacionados

Apresentar alguns dos artigos existentes na literatura sobre o tema que está sendo trabalhado, suas *principais contribuições e limitações*.

Este é um exemplo de citação @IEEEhowto:kopka.

É interessante apresentar uma tabela no final desta seção sumarizando os artigos citados anteriormente, suas vantagens, contribuições e desvantagens. Na @tab:tabela-exemplo é apresentado um exemplo de tabela.

#figure(
  table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    align: (left, left, center, center),
    stroke: none,
    table.hline(y: 0, stroke: 0.5pt),
    table.header([*Trabalhos*], [*Método*], [*Vantagens*], [*Desvantagens*]),
    table.hline(y: 1, stroke: 0.5pt),
    [Trabalho A], [Método X], [A], [D],
    [Trabalho B], [Método Y], [G], [J],
    table.hline(y: 3, stroke: 0.5pt),
  ),
  caption: [Exemplo de tabela],
) <tab:tabela-exemplo>

= Modelo de ameaça (SE APLICÁVEL)

Apresentar os ataques considerados para o trabalho. Utilizar figuras e/ou algoritmos e/ou equações para descrever os comportamentos dos ataques considerados. Também especificar as premissas consideradas para que a execução dos ataques seja possível.

Na @eq:equacao-da-reta é apresentado um exemplo de equação com a equação de uma reta.

$ y = a x + b $ <eq:equacao-da-reta>

Na @fig:logo-cin é apresentado um exemplo de figura com a logo do centro de informática.

#figure(
  image("imagens/VC.png", width: 80%),
  caption: [Logo do centro.],
) <fig:logo-cin>

= Sistema proposto pelo artigo de referência

Apresentar o sistema proposto para detecção de intrusão OU ataque adversarial. Utilizar figuras e/ou algoritmos e/ou equações para descrever o sistema proposto.

- Quais os componentes da solução? Quais suas entradas e saídas? O que eles fazem? Como eles o fazem?
- Quais métodos ou algoritmos estão sendo propostos ou empregados e por que?

No @alg:cap é apresentado um exemplo de algoritmo.

#figure(
  kind: "algorithm",
  supplement: [Alg.],
  pseudocode-list[
    - *Require* $n >= 0$
    - *Ensure* $y = x^n$
    - $y <- 1$
    - $X <- x$
    - $N <- n$
    - *while* $N != 0$ *do*
      - *if* $N$ is even *then*
        - $X <- X times X$
        - $N <- N / 2$ #h(1em) // Exemplo de comentário
      - *else*
        - $y <- y times X$
        - $N <- N - 1$
  ],
  caption: [Algoritmo com legenda],
) <alg:cap>

= Solução proposta pela equipe para melhorar a solução do artigo de referência (CASO FEITA)

Apresentar a arquitetura e funcionamento do sistema proposto pelo artigo de referência. Utilizar figuras e/ou algoritmos e/ou equações para descrever o sistema proposto.

- O que espera-se melhorar em relação à solução proposta pelo artigo de referência?
- Quais os componentes da solução? Quais as suas entradas e saídas? O que eles fazem? Como eles o fazem?
- Quais métodos ou algoritmos estão sendo propostos ou empregados e por que?

= Metodologia

Descrever os dados e métricas utilizados para validar as soluções propostas e quais os experimentos realizados. Sobre os dados, descrever:

== Dados usados pelo artigo de referência

Quais foram os dados usados para avaliar o sistema proposto? Por que eles foram escolhidos? O que eles representam? Como os conjuntos de treino, validação e teste foram formados? Há quantos dados em cada classe nos conjuntos de treino, validação e teste?

== Novo conjunto de dados escolhido

Quais foram os dados usados para avaliar o sistema proposto? Por que eles foram escolhidos? O que eles representam? Como os conjuntos de treino, validação e teste foram formados? Há quantos dados em cada classe nos conjuntos de treino, validação e teste?

== Métricas de avaliação

Deverá descrever as métricas de avaliação que serão utilizadas para avaliar os resultados obtidos com a reprodução do artigo. Explicar a motivação de uso das métricas e o que se deseja observar com cada uma delas. Apresentar as equações das métricas consideradas.

= Resultados e discussões

Apresentar e analisar os resultados obtidos comparando-os com os resultados de outros trabalhos. Utilizar gráficos e tabelas. Atentar para *não apenas descrever os resultados apresentados*, mas também para *explicá-los e discuti-los*.

== Resultados reprodução do artigo de referência

- Nos dados usados pelo artigo de referência
- No novo conjunto de dados escolhido

Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

== Resultados proposta de melhoria do artigo de referência (CASO FEITA)

- Nos dados usados pelo artigo de referência
- No novo conjunto de dados escolhido

Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

Comparar e discutir os resultados da proposta de melhoria com os resultados obtidos com a reprodução do artigo de referência.

= Conclusões e trabalhos futuros

Conclusão, principais limitações e problemas do sistema proposto pelo artigo de referência e pela proposta de melhoria (CASO FEITA), e trabalhos futuros.
