#let todo(done: false, body) = {
  [
    #text(
      fill: if done { green } else { red },
      {
        sym.square.filled
        body
      },
    )

  ]
}

#let results-and-discussions = [
  = Resultados e discussões

  Apresentar e analisar os resultados obtidos comparando-os com os resultados de outros trabalhos. Utilizar gráficos e tabelas. Atentar para *não apenas descrever os resultados apresentados*, mas também para *explicá-los e discuti-los*.

  == Resultados reprodução do artigo de referência
  Reproduzimos o processo de treinamento dos modelos de @iotcryptojacking utilizando o mesmo dataset. Preservamos o comportamento do código usado em @iotcryptojacking, mas desenvolvemos uma estrutura mais adequada para o treinamento em um _cluster_ e a disponibilizamos em @gitprojeto.

  - Nos dados usados pelo artigo de referência

  No cenário 8, os resultados foram efetivamente idênticos aos apresentados no artigo, como se vê em @tab:cenario8.

  #figure(
    table(
      columns: (2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*dataset*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*teste ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Timely Balanced], [0.99], [0.99], [0.99], [0.99], [0.95],
      [Timely Balanced (Oversampled)], [0.97], [0.97], [0.97], [0.97], [0.99],
      [Server x Server], [0.98], [0.98], [0.98], [0.98], [0.99],
      [Laptop x Laptop], [0.99], [0.99], [0.99], [0.99], [0.99],
      [Raspberry x Raspberry], [0.97], [0.97], [0.97], [0.97], [0.96],
      [WebOS x WebOS], [0.97], [0.97], [0.97], [0.97], [0.99],
      table.hline(y: 7, stroke: 0.5pt),
    ),
    caption: [Resultados da reprodução *Cenário 8*],
  ) <tab:cenario8>



  - No novo conjunto de dados escolhido

  Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  == Resultados proposta de melhoria do artigo de referência (CASO FEITA)

  - Nos dados usados pelo artigo de referência
  - No novo conjunto de dados escolhido

  Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  Comparar e discutir os resultados da proposta de melhoria com os resultados obtidos com a reprodução do artigo de referência.

  == discussões
  - apontar os erros q percebemos no artiigp
]
