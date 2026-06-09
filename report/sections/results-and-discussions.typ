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

   A execução do projeto foi dividida em cinco experimentos com classificadores de aprendizado de máquina, dentre eles: _Logistic Regression_ (LogReg), _K-Nearest Neighbors_ (KNN), _Support Vector Machine_ (SVM) e _Gaussian Naive Bayes_ (GNB). Foram utilizados 75% dos dados para treinamento e 25% para teste do classificador, _5-fold cross-validation_ e em todos os modelos foram usados os parâmetros padrão do scikit-learn. Os experimentos foram avaliados usando Acurácia, Precisão, _Recall_, F1 _Score_ e Teste roc.


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

  ==== Cenário 0
  

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
