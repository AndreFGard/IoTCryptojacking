#let related-work = [
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
]