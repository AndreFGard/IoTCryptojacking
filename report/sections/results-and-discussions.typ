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

   A execução do projeto foi dividida em cinco experimentos com classificadores de aprendizado de máquina, dentre eles: _Logistic Regression_ (LogReg), _K-Nearest Neighbors_ (KNN), _Support Vector Machine_ (SVM) e _Gaussian Naive Bayes_ (GNB). Foram utilizados 75% dos dados para treinamento e 25% para teste do classificador, _5-fold cross-validation_ e em todos os modelos foram usados os parâmetros padrão do scikit-learn. Os experimentos foram avaliados usando Acurácia, Precisão, _Recall_, F1 _Score_ e Teste roc. Assim como no artigo original, a partir do cenário 1 foi considerado apenas o classificador SVM para apresentação dos resultados.

  === Maliciosos vs. Benignos (1)

  No primeiro conjunto de experimentos, foram usados dados de tráfego de rede de um repositório público para a classe dos benignos, o _dataset_ consiste de diversas atividades de usuário: interativa, transferência de dados em massa, navegação na web, reprodução de vídeo e comportamento ocioso. 
  
  Neste experimento foram testados os seguintes cenários:

  - S0: Desenvolvendo um mecanismo de detecção de cryptojacking para IoT
  - Avaliação com diferentes comportamentos adversários:
    - S1: Server vs. Desktop vs. IoT
    - S2: Agressivo vs. Robusto vs. Furtivo
    - S3: In-browser vs. Binary

  - Modelos adversários baseado na quantidade de dispositivos comprometidos na rede doméstica inteligente:
    - S4: Totalmente comprometido (Todos)
    - S5: Parcialmente comprometidos (Laptop + IoT)
    - S6: Único dispositivo comprometido (IoT)
    - S7: Dispositivos IoT comprometidos (IoT + IoT)

  Os resultados obtidos estão estruturados nas tabelas a seguir, os valores apresentados são as médias das 5 execuções de cada modelo. De forma geral, os resultados estão semelhantes aos encontrados no artigo de referência, com margem aceitável de até 0.20.

  ==== Cenário 0 - Todos as configurações combinadas

  #figure(
    table(
      columns: (1.2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Modelo*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [LogReg], [0.97], [0.97], [0.97], [0.97], [0.99],
      [KNN], [0.98], [0.98], [0.98], [0.98], [0.99],
      [SVM], [0.98], [0.98], [0.98], [0.98], [0.99],
      [GNB], [0.95], [0.95], [0.95], [0.95], [0.97],
      table.hline(y: 5, stroke: 0.5pt),
    ),
    caption: [Resultados da reprodução *Cenário 0*],
  ) <tab:mal-vs-ben-1-cenario-0>

  ==== Cenário 1 - Server vs. Desktop vs. IoT

  #figure(
    table(
      columns: (2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Dispositivo*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Server], [0.99], [0.99], [0.99], [0.99], [1.00],
      [Desktop], [0.98], [0.98], [0.98], [0.98], [1.00],
      [IoT], [0.92], [0.93], [0.92], [0.92], [0.97],
      table.hline(y: 4, stroke: 0.5pt),
    ),
    caption: [Resultados da reprodução *Cenário 1* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-1>

  ==== Cenário 2 - Agressiva (Throttle 100%) vs. Robusta (Throttle 50%) vs. Furtiva (Throttle 10%)

  Throttle é o quanto da CPU está sendo utilizado para a atividade de cryptojacking.

  #figure(
    table(
      columns: (2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Estratégia*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Agressiva (100%)], [0.98], [0.98], [0.98], [0.98], [1.00],
      [Robusta (50%)], [0.81], [0.81], [0.81], [0.81], [0.89],
      [Furtiva (10%)], [0.91], [0.91], [0.91], [0.91], [0.97],
      table.hline(y: 4, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 2* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-2>

  Nesse cenário, o ataque robusto trouxe resultados diferentes do artigo original que teve acurácia, precisão, recall e f1 score com 0.87 e o teste ROC com 0.94. Um ponto observado nesse caso é uma divergência encontrada no artigo e código dos autores relacionado ao tamanho dos datasets usados, foi mencionado o uso de 27.915 amostras benignas e 26.669 amostras maliciosas, no dataset constam 10.453 amostras benignas e 9.925 maliciosas o que influenciou diretamente nos resultados obtidos.

  ==== Cenário 3 - In-Browser vs. Binary
  
  #figure(
    table(
      columns: (2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Tipo*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [In-Browser], [0.95], [0.95], [0.95], [0.95], [0.99],
      [Binary], [0.99], [0.99], [0.99], [0.99], [1.00],
      table.hline(y: 3, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 3* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-3>

  ==== Cenário 4 - Rede totalmente comprometida (Geral)

  Nesse cenário todos os dispositivos conectados a rede estão comprometidos.

  #figure(
    table(
      columns: (3fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Rede*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Fully Compromised], [0.98], [0.98], [0.98], [0.98], [0.99],
      table.hline(y: 2, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 4* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-4>

  ==== Cenário 5 - Rede parcialmente comprometida (IoT + Laptop)

  Nesse cenário apenas os dispositivos IoT e os Laptop conectados na rede estão comprometidos, utilizando diferentes tipos de _malware_ cryptojacking.

  #figure(
    table(
      columns: (3fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Rede*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Partially Compromised], [0.98], [0.98], [0.98], [0.98], [1.00],
      table.hline(y: 2, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 5* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-5>

  ==== Cenário 6 - Rede unicamente comprometida (IoT)

  Nesse cenário um único dispositivo IoT dentro da rede doméstica está comprometido, o qual executa uma quantidade de mineração limitada.

  #figure(
    table(
      columns: (3fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Rede*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Single Compromised], [0.91], [0.91], [0.91], [0.91], [0.97],
      table.hline(y: 2, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 6* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-6>

  No artigo original os resultados foram de 0.94 para a acurácia, precisão, recall e f1 score, e 0.95 para o teste ROC.

  ==== Cenário 7 - IoT comprometidos (IoT + IoT)

  Nesse cenário todos os dispositivos IoT conectados estão comprometidos, os autores testaram em Raspberry Pi e WebOS Smart TV.

  #figure(
    table(
      columns: (3fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Rede*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [IoT Compromised], [0.90], [0.90], [0.90], [0.90], [0.96],
      table.hline(y: 2, stroke: 0.5pt),
    ),
    caption: [Resultados do *Cenário 7* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-7>

  De forma geral, os resultados mostram que os cenários com mais dispositivos comprometidos são mais facilmente detectáveis enquanto que redes com apenas dispositivos IoT tendem a ser um pouco mais difícil de detectar dado ao volume de tráfego encontrado nesses dispositivos que podem ser confundidos com a atividade de mineração.

  === Maliciosos vs. Benignos (2)

  === Dataset desbalanceado

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

  === Transferabilidade

  === Ajuste de Hiperparâmetros



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
