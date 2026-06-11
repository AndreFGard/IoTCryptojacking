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

#let result-table(rows) = table(
  columns: (2.2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center),
  stroke: none,
  table.hline(y: 0, stroke: 0.5pt),
  table.header([*Cenário*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
  table.hline(y: 1, stroke: 0.5pt),
  ..rows,
  table.hline(stroke: 0.5pt),
)

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

  ==== Cenários 4 a 7 - Níveis de Comprometimento da Rede

  Abaixo, descrevemos as diferentes variações de comprometimento de dispositivos na rede avaliadas, cujos resultados estão consolidados na @tab:mal-vs-ben-1-cenarios-4a7.

  Cenário 4 - Rede totalmente comprometida (Geral): \
  - Nesse cenário todos os dispositivos conectados a rede estão comprometidos.

  Cenário 5 - Rede parcialmente comprometida (IoT + Laptop): \
  - Nesse cenário apenas os dispositivos IoT e os Laptop conectados na rede estão comprometidos, utilizando diferentes tipos de _malware_ cryptojacking.

  Cenário 6 - Rede unicamente comprometida (IoT): \
  - Nesse cenário um único dispositivo IoT dentro da rede doméstica está comprometido, o qual executa uma quantidade de mineração limitada. No artigo original os resultados foram de 0.94 para a acurácia, precisão, recall e f1 score, e 0.95 para o teste ROC.

  Cenário 7 - IoT comprometidos (IoT + IoT): \
  - Nesse cenário todos os dispositivos IoT conectados estão comprometidos, os autores testaram em Raspberry Pi e WebOS Smart TV.

  #figure(
    table(
      columns: (3fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Cenário*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Fully Compromised], [0.98], [0.98], [0.98], [0.98], [0.99],
      [Partially Compromised], [0.98], [0.98], [0.98], [0.98], [1.00],
      [Single Compromised], [0.91], [0.91], [0.91], [0.91], [0.97],
      [IoT Compromised], [0.90], [0.90], [0.90], [0.90], [0.96],
      table.hline(y: 5, stroke: 0.5pt),
    ),
    caption: [Resultados dos *Cenários 4 a 7* (SVM)],
  ) <tab:mal-vs-ben-1-cenarios-4a7>

  De forma geral, os resultados mostram que os cenários com mais dispositivos comprometidos são mais facilmente detectáveis enquanto que redes com apenas dispositivos IoT tendem a ser um pouco mais difícil de detectar dado ao volume de tráfego encontrado nesses dispositivos que podem ser confundidos com a atividade de mineração.

  === Maliciosos vs. Benignos (2)

  Para avaliar a sensibilidade do modelo à escolha da classe benigna, os cenários de 1 a
  7 foram repetidos utilizando o _dataset benign-2_ coletado pelos próprios autores do
  artigo @iotcryptojacking. Este _dataset_ contém capturas dos mesmos dispositivos usados
  nos experimentos maliciosos (Laptop, Raspberry Pi, Server e WebOS), tornando a
  separação entre classes mais realista e próxima de condições reais de operação.

  No Cenário 1 (@tab:mb2-cenario1), os resultados por dispositivo ficaram dentro de 0.01
  do artigo para Server e Desktop. O servidor continua com acurácia máxima (0.99), pois
  seu tráfego de mineração binária é o mais volumoso e homogêneo do dataset — mais de
  1.2 milhões de pacotes maliciosos, gerando features estatísticas altamente
  discriminativas. O dispositivo IoT (Raspberry Pi) apresenta a menor acurácia (0.94),
  reflexo de seus recursos limitados que produzem padrões de mineração menos regulares
  e mais próximos do benign.

  #figure(
    result-table((
      [Servidor],        [0.99], [0.99], [0.99], [0.99], [1.00],
      [Desktop],         [0.95], [0.95], [0.95], [0.95], [0.98],
      [IoT], [0.94], [0.94], [0.94], [0.94], [0.98],
    )),
    caption: [Resultados — *Cenário 1* _benign-2_],
  ) <tab:mb2-cenario1>

  O Cenário 2 (@tab:mb2-cenario2) avalia estratégias de lucro do atacante via _throttle_.
  Nossos resultados seguem o mesmo padrão qualitativo do artigo: o ataque furtivo (10%)
  obtém a menor acurácia (0.86), enquanto o robusto (50%) supera o agressivo (100%).
  A queda no modo furtivo é a mais relevante — a 10% de _throttle_, o volume de tráfego
  gerado se aproxima do tráfego benigno em frequência e tamanho de pacotes, reduzindo a
  separabilidade das classes. A diferença mais acentuada em relação ao artigo ocorre
  justamente nesse cenário (-0.02), o que é coerente com a maior dificuldade de
  separação imposta pelo _benign-2_.

  #figure(
    result-table((
      [Agressivo (100%)], [0.94], [0.94], [0.94], [0.94], [0.98],
      [Robusto (50%)],    [0.96], [0.96], [0.96], [0.96], [0.99],
      [Furtivo (10%)],    [0.86], [0.87], [0.86], [0.86], [0.93],
    )),
    caption: [Resultados — *Cenário 2* _benign-2_],
  ) <tab:mb2-cenario2>

  No Cenário 3 (@tab:mb2-cenario3), os resultados são praticamente idênticos ao artigo.
  O malware binário (_host-based_) é detectado com maior acurácia que o no-navegador
  (_in-browser_), confirmando que o tráfego binário é mais volumoso e característico.
  O minerador binário não emprega técnicas de ocultação de rede, gerando padrões
  altamente distinguíveis, o minerador in-browser, por sua vez, limita ativamente o uso
  de CPU, produzindo tráfego mais irregular e próximo ao benigno.

  #figure(
    result-table((
      [No-navegador (_in-browser_)], [0.96], [0.96], [0.96], [0.96], [0.99],
      [Binário (_host-based_)],      [0.97], [0.97], [0.97], [0.97], [1.00],
    )),
    caption: [Resultados — *Cenário 3* _benign-2_],
  ) <tab:mb2-cenario3>

  Os Cenários 4 a 7 (@tab:mb2-cenarios4a7) avaliam graus de comprometimento da rede
  doméstica. A diferença mais relevante está no Cenário 4 (totalmente comprometido), onde
  obtivemos 0.95 contra 0.98 do artigo (-0.03), atribuível ao maior desbalanceamento de
  classes com _benign-2_. Os demais cenários ficaram dentro de 0.01 do artigo.

  #figure(
    result-table((
      [Totalmente comprometida (S4)],    [0.95], [0.95], [0.95], [0.95], [0.99],
      [Parcialmente comprometida (S5)],  [0.97], [0.97], [0.97], [0.97], [0.99],
      [Dispositivo único IoT (S6)],      [0.96], [0.96], [0.96], [0.96], [0.99],
      [IoT comprometida — 2 disp. (S7)], [0.95], [0.95], [0.95], [0.95], [0.99],
    )),
    caption: [Resultados — *Cenários 4 a 7* _benign-2_],
  ) <tab:mb2-cenarios4a7>

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

    O cenário 9 avalia a capacidade de generalização dos modelos treinados em um contexto
  de mineração e testados em outro distinto — por exemplo, treinar com tráfego de um
  serviço de pool e testar com tráfego de mineração in-browser. 

  #figure(
    table(
      columns: (2.4fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Experimento*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Service Provider-1], [0.92], [0.93], [0.92], [0.92], [—],
      [Service Provider-2], [0.75], [0.92], [0.75], [0.80], [—],
      [Binary-1],           [0.87], [0.83], [0.87], [0.82], [—],
      [Binary-In-Browser-1],[0.89], [0.90], [0.89], [0.87], [—],
      [Binary-In-Browser-2],[0.99], [0.99], [0.99], [0.99], [—],
      [Binary-In-Browser-3],[0.99], [0.99], [0.99], [0.99], [—],
      [In-Browser-1],       [0.99], [0.99], [0.99], [0.99], [—],
      [In-Browser-2],       [0.99], [0.99], [0.99], [0.99], [—],
      table.hline(stroke: 0.5pt),
    ),
    caption: [Resultados da reprodução — *Cenário 9*],
  ) <tab:transfer-codigo>

  Os resultados da reprodução correspondem aos do artigo em 6 dos 8 experimentos, com
  diferença máxima de 0.02 em acurácia. Nos dois casos com maior divergência ( Service
  Provider-1 e Service Provider-2 ) os desvios são de +0.05 e +0.06 em acurácia,
  respectivamente, mas continuam dentro de margem aceitável para reprodução de trabalhos
  com aleatoriedade intrínseca.

  A precisão ponderada do Service Provider-2 coincide exatamente com o artigo (0.92),
  indicando que o modelo identifica corretamente os padrões relevantes, a diferença na
  acurácia reflete uma distribuição ligeiramente distinta dos exemplos de teste, não uma
  degradação do modelo. Esses dois experimentos envolvem os únicos cenários com tráfego
  real de serviço de pool (_WebminePool_ e _Webmine Aggressive_), cujas janelas de 10
  pacotes geradas pelo tsfresh são sensíveis à ordem de chegada dos pacotes, pequenas
  diferenças de versão de biblioteca ou de ordenação interna do dataset já justificam
  os desvios observados.

  Nos seis experimentos restantes os valores são praticamente idênticos ao artigo. Os
  experimentos Binary-In-Browser e In-Browser atingem acurácia entre 0.87 e 0.99,
  mostrando que modelos treinados em tráfego binário transferem bem para cenários de
  mineração no navegador, o que se explica pela semelhança nos padrões de acesso a
  endereços de pool mesmo entre implementações distintas. Os experimentos com variantes
  do mesmo tipo de minerador (In-Browser-1 e In-Browser-2) alcançam 0.99, confirmando
  que as features aprendidas são robustas o suficiente para generalizar entre as
  configurações agressiva, robusta e furtiva.

  === Ajuste de Hiperparâmetros

  O Cenário 10 (@tab:cenario10) testa o SVM com parâmetros não-padrão, variando kernel,
  regularização (C) e gamma. Seguindo o artigo, utilizamos o cenário _robusto_ de
  dispositivo IoT como base (_thr\_50\_s2_: Raspberry Pi, WebminePool 50% throttle).

  #figure(
    table(
      columns: (1.4fr, 0.5fr, 0.9fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header(
        [*Kernel*], [*C*], [*Gamma*],
        [*Acc.*], [*Prec.*], [*Recall*], [*F1*],
      ),
      table.hline(y: 1, stroke: 0.5pt),
      [Linear],[1],[Scale],[1.00],[1.00],[1.00],[1.00],
      [Poly],  [1],[Scale],[0.80],[0.81],[0.80],[0.80],
      [RBF],   [1],[Scale],[0.81],[0.81],[0.81],[0.81],
      [Sigmoid],[1],[Scale],[0.62],[0.62],[0.62],[0.62],
      [Linear],[1],[Auto],[1.00],[1.00],[1.00],[1.00],
      [Poly],  [1],[Auto],[0.89],[0.89],[0.89],[0.89],
      [RBF],   [1],[Auto],[0.60],[0.77],[0.60],[0.54],
      [Sigmoid],[1],[Auto],[0.51],[0.26],[0.51],[0.35],
      [Linear],[2],[Scale],[1.00],[1.00],[1.00],[1.00],
      [Poly],  [2],[Scale],[0.83],[0.83],[0.83],[0.83],
      [RBF],   [2],[Scale],[0.82],[0.83],[0.82],[0.82],
      [Sigmoid],[2],[Scale],[0.62],[0.62],[0.62],[0.62],
      [Linear],[2],[Auto],[1.00],[1.00],[1.00],[1.00],
      [Poly],  [2],[Auto],[0.89],[0.89],[0.89],[0.89],
      [RBF],   [2],[Auto],[0.60],[0.77],[0.60],[0.54],
      [Sigmoid],[2],[Auto],[0.51],[0.26],[0.51],[0.35],
      table.hline(stroke: 0.5pt),
    ),
    caption: [Resultados — *Cenário 10*],
  ) <tab:cenario10>

  O padrão qualitativo do artigo é reproduzido com fidelidade: kernels lineares dominam
  (acurácia 1.00 em todos os casos, idêntico ao paper), seguidos pelos kernels poly, e
  sigmoid-auto apresenta o pior desempenho (0.51), alinhado com os 0.52 reportados.

  As divergências quantitativas se concentram nos kernels mais sensíveis à escala da
  distribuição dos dados. Sigmoid-scale obteve 0.62 contra 0.72–0.73 do artigo (Δ ≈
  −0.10), a maior diferença observada. RBF-auto ficou em 0.60 contra 0.66 (Δ ≈ −0.06).
  Esses dois kernels são particularmente afetados pela composição do conjunto benigno,
  pois o artigo não documenta quais arquivos específicos de _benign-1_ foram usados neste
  experimento, nossa seleção dos arquivos pode diferir da original. Os kernels lineares
  e poly, por sua vez, são menos sensíveis à escala absoluta dos valores de feature, o
  que explica sua maior estabilidade na reprodução.

  O valor de C não altera os resultados em nenhuma configuração (as linhas C=1 e C=2 são
  idênticas para todos os kernels), comportamento esperado para um dataset pequeno e bem
  separável como o _thr\_50\_s2_, onde o SVM já encontra margem ampla com C=1.


  == Resultados no novo conjunto de dados

  Com a reprodução do método de @iotcryptojacking, segundo descrito em #text(fill: red)[SUBSTITUA-ME-POR-REFERENCIA], fizemos um ajuste de hiperparâmetros e selecionamos o melhor modelo. 
  Utilizar gráficos e tabelas.

  === Ajuste de Hiperparâmetros

  #figure(
    {
      let data = csv("../data/our_svc_tune_results.csv")
      table(
        columns: (auto, auto, auto, auto, auto, auto),
        align: (left, center, center, center, center, center),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1).flatten().map(x => x),
        table.hline(stroke: 0.5pt),
      )
    },
    caption: [Resultados do ajuste de hiperparâmetros do SVM no novo conjunto de dados.],
  ) <tab:our-svc-tune>

  Vimos que o kernel foi o parâmetro mais determinante pro desempenho dos modelo, com o RBF e Poly obtendo resultados próximos, apesar do treinamento do primeiro ser mais rápido. O parâmetro C também foi importante, e o peso das classes se mostrou útil para lidar com o desbalanceamento.

  === Resultados finais

  A configuração que maximizou o F1 Macro no conjunto de validação foi o SVM com kernel RBF, C=2, gamma=auto e pesos balanceados. Os resultados no conjunto de teste são apresentados em @tab:our-svc-best.

  O modelo obteve desempenho quase perfeito na classe benigna (F1 = 0.99), reflexo do grande volume de amostras benignas disponíveis. Para a classe maliciosa, o recall de 0.95 indica que apenas 5% dos ataques não foram detectados, enquanto a precisão de 88% indica uma quantidade considerável de falsos positivos. O F1 Macro de 0.96 confirma que o modelo equilibra bem as duas classes, apesar do desbalanceamento acentuado, com quase 60x mais janelas benignas que malignas.

  #figure(
    table(
      columns: (2fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, center, center, center, center),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Classe*], [*Prec.*], [*Recall*], [*F1*], [*Suporte*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Benigno],         [0.99], [0.99], [0.99], [30.456],
      [Malicioso],       [0.88], [0.95], [0.91], [540],
      table.hline(stroke: 0.5pt),
      [*Macro avg*],     [*0.94*], [*0.97*], [*0.96*], [30.996],
      [*Weighted avg*],  [1.00], [1.00], [1.00], [30.996],
      table.hline(stroke: 0.5pt),
    ),
    caption: [Relatório de classificação do melhor SVM (RBF, C=2, gamma=auto, pesos balanceados) no conjunto de teste do novo dataset.],
  ) <tab:our-svc-best>

  === Discussão

  //Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  // == Resultados proposta de melhoria do artigo de referência (CASO FEITA)

  // - Nos dados usados pelo artigo de referência
  // - No novo conjunto de dados escolhido

  // Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  // Comparar e discutir os resultados da proposta de melhoria com os resultados obtidos com a reprodução do artigo de referência.

  // == discussões
  // - apontar os erros q percebemos no artiigp
]
