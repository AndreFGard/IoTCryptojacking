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

#let result-table(first-col, rows, first-col-width: 3fr) = table(
  columns: (first-col-width, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center),
  stroke: none,
  table.hline(y: 0, stroke: 0.5pt),
  table.header([*#first-col*], [*Acc.*], [*Prec.*], [*Recall*], [*F1*], [*ROC*]),
  table.hline(y: 1, stroke: 0.5pt),
  ..rows,
  table.hline(stroke: 0.5pt),
)

#let results-and-discussions = [
  = Resultados e discussões

  == Resultados da reprodução do artigo de referência
  Nesta subseção reproduzimos @gitprojeto o pipeline de treinamento do artigo de @iotcryptojacking usando o mesmo dataset, as mesmas métricas e a mesma divisão entre treino e teste. A implementação foi preservada em termos de comportamento, mas executada em uma estrutura mais adequada para _cluster_ e análise reprodutível.

  Os resultados foram organizados em três blocos: desempenho geral dos classificadores, sensibilidade ao comportamento do atacante e sensibilidade ao grau de comprometimento da rede. Os modelos utilizados são _Logistic Regression_ (LogReg), _K-Nearest Neighbors_ (KNN), _Support Vector Machine_ (SVM) e _Gaussian Naive Bayes_ (GNB), com 75% dos dados para treino, 25% para teste, _5-fold cross-validation_ e parâmetros padrão do scikit-learn. A partir do Cenário 1, analisamos apenas os resultados do SVM, como no artigo original.

  === Maliciosos vs. Benignos (1)

  No primeiro conjunto de experimentos, foram usados dados de tráfego de rede de um repositório público para a classe dos benignos, o _dataset_ consiste de diversas atividades de usuário: interativa, transferência de dados em massa, navegação na web, reprodução de vídeo e comportamento ocioso. 
  
  Neste experimento foram testados os seguintes cenários:

  - S0: Desenvolvendo um mecanismo de detecção de cryptojacking
  - Avaliação com diferentes comportamentos adversários:
    - S1: Server vs. Desktop vs. IoT
    - S2: Agressivo vs. Robusto vs. Furtivo
    - S3: In-browser vs. Binary

  - Modelos adversários baseado na quantidade de dispositivos comprometidos na rede doméstica inteligente:
    - S4: Totalmente comprometido (Todos)
    - S5: Parcialmente comprometidos (Laptop + IoT)
    - S6: Único dispositivo comprometido (IoT)
    - S7: Dispositivos IoT comprometidos (IoT + IoT)

  Os resultados obtidos estão estruturados nas tabelas a seguir, os valores apresentados são as médias das 5 execuções de cada modelo.

  ==== Cenário 0 - Todos as configurações combinadas

  Esse cenário funciona como um _baseline_ para medir o quanto o detector consegue separar tráfego cotidiano de padrões associados ao cryptojacking.

  #figure(
    result-table(
      [*Modelo*],
      ([LogReg], [0.97], [0.97], [0.97], [0.97], [0.99],
       [KNN], [0.98], [0.98], [0.98], [0.98], [0.99],
       [SVM], [0.98], [0.98], [0.98], [0.98], [0.99],
       [GNB], [0.95], [0.95], [0.95], [0.95], [0.97]),
      first-col-width: 1.2fr,
    ),
    caption: [Resultados da reprodução *Cenário 0*],
  ) <tab:mal-vs-ben-1-cenario-0>

  A @tab:mal-vs-ben-1-cenario-0 mostra que a formulação original já separa bem tráfego benigno e malicioso, com resultados semelhantes ao artigo original, a diferença entre os classificadores é pequena e o SVM permanece entre os melhores resultados, o que justifica seu uso como modelo principal nos cenários seguintes.

  ==== Cenário 1 - Server vs. Desktop vs. IoT

  O Cenário 1 testa o impacto do tipo de dispositivo comprometido.

  #figure(
    result-table(
      [*Dispositivo*],
      ([Server], [0.99], [0.99], [0.99], [0.99], [1.00],
       [Desktop], [0.98], [0.98], [0.98], [0.98], [1.00],
       [IoT], [0.92], [0.93], [0.92], [0.92], [0.97]),
    ),
    caption: [Resultados da reprodução *Cenário 1* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-1>

  Server e Desktop são mais fáceis de detectar, enquanto o IoT apresenta a maior dificuldade, o que é coerente com seu tráfego mais ruidoso e menos volumoso. A queda do IoT em relação ao Server e ao Desktop sugere que a assinatura de mineração é menos clara em dispositivos com menos recursos, reforçando que o modelo aprende melhor padrões de tráfego mais estáveis.

  ==== Cenário 2 - Agressiva (Throttle 100%) vs. Robusta (Throttle 50%) vs. Furtiva (Throttle 10%)

  O parâmetro de _throttle_ representa a fração de CPU dedicada à mineração. Quanto menor esse valor, mais furtivo é o ataque e mais difícil tende a ser a separação entre as classes.

  #figure(
    result-table(
      [*Estratégia*],
      ([Agressiva (100%)], [0.98], [0.98], [0.98], [0.98], [1.00],
       [Robusta (50%)], [0.81], [0.81], [0.81], [0.81], [0.89],
       [Furtiva (10%)], [0.91], [0.91], [0.91], [0.91], [0.97]),
    ),
    caption: [Resultados do *Cenário 2* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-2>

  O comportamento qualitativo do artigo é preservado, o ataque agressivo é o mais detectável e o ataque robusto é o mais difícil de separar, com o modo furtivo em posição intermediária. A divergência principal aparece justamente no modo robusto, o que aponta para sensibilidade à composição exata dos dados usados na reprodução.

  Uma diferença importante encontrada na comparação foi o tamanho do dataset reportado no artigo em relação ao conteúdo real dos arquivos. O texto menciona 27.915 amostras benignas e 26.669 maliciosas, mas o conjunto disponível contém 10.453 benignas e 9.925 maliciosas. Essa diferença ajuda a explicar por que o desempenho reproduzido não coincide totalmente com o publicado de 0.87 e 0.94.

  ==== Cenário 3 - In-Browser vs. Binary

  Este cenário compara duas formas de mineração com perfis distintos de tráfego. O ataque binário concentra mais sinais de rede e, por isso, tende a ser mais fácil de detectar do que o in-browser.
  
  #figure(
    result-table(
      [*Tipo*],
      ([In-Browser], [0.95], [0.95], [0.95], [0.95], [0.99],
       [Binary], [0.99], [0.99], [0.99], [0.99], [1.00]),
    ),
    caption: [Resultados do *Cenário 3* (SVM)],
  ) <tab:mal-vs-ben-1-cenario-3>

  Assim como no artigo, o resultado confirma o padrão esperado, o tráfego binário é mais característico e mais simples de distinguir do benigno, enquanto o in-browser se aproxima mais do comportamento cotidiano da rede.

  ==== Cenários 4 a 7 - Níveis de Comprometimento da Rede

  Os Cenários 4 a 7 avaliam como a taxa de comprometimento da rede altera a detectabilidade do ataque. 

  #figure(
    result-table(
      [*Cenário*],
      ([Fully Compromised], [0.98], [0.98], [0.98], [0.98], [0.99],
       [Partially Compromised], [0.98], [0.98], [0.98], [0.98], [1.00],
       [Single Compromised], [0.91], [0.91], [0.91], [0.91], [0.97],
       [IoT Compromised], [0.90], [0.90], [0.90], [0.90], [0.96]),
      first-col-width: 3fr,
    ),
    caption: [Resultados dos *Cenários 4 a 7* (SVM)],
  ) <tab:mal-vs-ben-1-cenarios-4a7>

  Em geral, quanto mais concentrado o tráfego malicioso em dispositivos IoT, mais difícil a separação, quando a rede inteira está comprometida, o padrão fica mais evidente. O resultado é consistente com a hipótese do artigo, cenários com mais dispositivos comprometidos tendem a gerar mais tráfego anômalo e, portanto, são mais fáceis de identificar. Já os cenários com apenas IoT exigem mais atenção, pois o volume de tráfego é menor e se confunde mais facilmente com atividade legítima.

  === Maliciosos vs. Benignos (2)

  Para avaliar a sensibilidade do modelo à escolha da classe benigna, os cenários de 1 a
  7 foram repetidos utilizando o _dataset benign-2_ coletado pelos próprios autores do
  artigo @iotcryptojacking. Este _dataset_ contém capturas dos mesmos dispositivos usados
  nos experimentos maliciosos (Laptop, Raspberry Pi, Server e WebOS), tornando a
  separação entre classes mais realista e próxima de condições reais de operação.

  No Cenário 1 (@tab:mb2-cenario1), os resultados por dispositivo ficaram dentro de 0.01
  do artigo para Server e Desktop. O servidor continua com acurácia máxima (0.99), pois
  seu tráfego de mineração binária é o mais volumoso e homogêneo do dataset, mais de
  1.2 milhões de pacotes maliciosos, gerando features estatísticas altamente
  discriminativas. O dispositivo IoT (Raspberry Pi) apresenta a menor acurácia (0.94),
  reflexo de seus recursos limitados que produzem padrões de mineração menos regulares
  e mais próximos do benign.

  #figure(
    result-table(
      [*Dispositivo*],
      ([Servidor], [0.99], [0.99], [0.99], [0.99], [1.00],
       [Desktop], [0.95], [0.95], [0.95], [0.95], [0.98],
       [IoT], [0.94], [0.94], [0.94], [0.94], [0.98]),
    ),
    caption: [Resultados da reprodução *Cenário 1* _benign-2_],
  ) <tab:mb2-cenario1>

  O Cenário 2 (@tab:mb2-cenario2) avalia estratégias de lucro do atacante via _throttle_.
  Nossos resultados seguem o mesmo padrão qualitativo do artigo: o ataque furtivo (10%)
  obtém a menor acurácia (0.86), enquanto o robusto (50%) supera o agressivo (100%).
  A queda no modo furtivo é a mais relevante, a 10% de _throttle_, o volume de tráfego
  gerado se aproxima do tráfego benigno em frequência e tamanho de pacotes, reduzindo a
  separabilidade das classes. A diferença mais acentuada em relação ao artigo ocorre
  justamente nesse cenário (-0.02), o que é coerente com a maior dificuldade de
  separação imposta pelo _benign-2_.

  #figure(
    result-table(
      [*Estratégia*],
      ([Agressivo (100%)], [0.94], [0.94], [0.94], [0.94], [0.98],
       [Robusto (50%)], [0.96], [0.96], [0.96], [0.96], [0.99],
       [Furtivo (10%)], [0.86], [0.87], [0.86], [0.86], [0.93]),
    ),
    caption: [Resultados da reprodução *Cenário 2* _benign-2_],
  ) <tab:mb2-cenario2>

  No Cenário 3 (@tab:mb2-cenario3), os resultados são praticamente idênticos ao artigo.
  O malware binário (_host-based_) é detectado com maior acurácia que em navegador
  (_in-browser_), confirmando que o tráfego binário é mais volumoso e característico.
  O minerador binário não emprega técnicas de ocultação de rede, gerando padrões
  altamente distinguíveis, o minerador in-browser, por sua vez, limita ativamente o uso
  de CPU, produzindo tráfego mais irregular e próximo ao benigno.

  #figure(
    result-table(
      [*Tipo*],
      ([_In-browser_], [0.96], [0.96], [0.96], [0.96], [0.99],
       [_Binary_], [0.97], [0.97], [0.97], [0.97], [1.00]),
    ),
    caption: [Resultados da reprodução *Cenário 3* _benign-2_],
  ) <tab:mb2-cenario3>

  Os Cenários 4 a 7 (@tab:mb2-cenarios4a7) avaliam graus de comprometimento da rede
  doméstica. A diferença mais relevante está no Cenário 4 (totalmente comprometido), onde
  obtivemos 0.95 contra 0.98 do artigo (-0.03), atribuível ao maior desbalanceamento de
  classes com _benign-2_. Os demais cenários ficaram dentro de 0.01 do artigo.

  #figure(
    result-table(
      [*Cenário*],
      ([Fully Compromised], [0.95], [0.95], [0.95], [0.95], [0.99],
       [Partially Compromised], [0.97], [0.97], [0.97], [0.97], [0.99],
       [Single Compromised], [0.96], [0.96], [0.96], [0.96], [0.99],
       [IoT Compromised], [0.95], [0.95], [0.95], [0.95], [0.99]),
    ),
    caption: [Resultados da reprodução *Cenários 4 a 7* _benign-2_],
  ) <tab:mb2-cenarios4a7>

  === Dataset desbalanceado

  O Cenário 8 confirma que o pipeline reproduz o comportamento do artigo também em bases desbalanceadas. Os números ficam praticamente idênticos ao texto original, o que é um bom sinal de consistência do método.

  #figure(
    result-table(
      [*Dataset*],
      ([Timely Balanced], [0.99], [0.99], [0.99], [0.99], [0.95],
       [Timely Balanced (Oversampled)], [0.97], [0.97], [0.97], [0.97], [0.99],
       [Server x Server], [0.98], [0.98], [0.98], [0.98], [0.99],
       [Laptop x Laptop], [0.99], [0.99], [0.99], [0.99], [0.99],
       [Raspberry x Raspberry], [0.97], [0.97], [0.97], [0.97], [0.96],
       [WebOS x WebOS], [0.97], [0.97], [0.97], [0.97], [0.99]),
    ),
    caption: [Resultados da reprodução *Cenário 8*],
  ) <tab:cenario8>

  === Transferabilidade

  O Cenário 9 avalia a generalização entre contextos de mineração distintos: o modelo é treinado em um tipo de tráfego e testado em outro, o que é uma forma direta de medir transferabilidade.

  #figure(
    result-table(
      [*Experimento*],
      ([Service Provider-1], [0.92], [0.93], [0.92], [0.92], [—],
       [Service Provider-2], [0.75], [0.92], [0.75], [0.80], [—],
       [Binary-1], [0.87], [0.83], [0.87], [0.82], [—],
       [Binary-In-Browser-1], [0.89], [0.90], [0.89], [0.87], [—],
       [Binary-In-Browser-2], [0.99], [0.99], [0.99], [0.99], [—],
       [Binary-In-Browser-3], [0.99], [0.99], [0.99], [0.99], [—],
       [In-Browser-1], [0.99], [0.99], [0.99], [0.99], [—],
       [In-Browser-2], [0.99], [0.99], [0.99], [0.99], [—]),
      first-col-width: 2.4fr,
    ),
    caption: [Resultados da reprodução — *Cenário 9*],
  ) <tab:transfer-codigo>

  Os resultados da reprodução correspondem aos do artigo em 6 dos 8 experimentos, com
  diferença máxima de 0.02 em acurácia. Nos dois casos com maior divergência (Service Provider-1 e Service Provider-2) os desvios são de +0.05 e +0.06 em acurácia,
  respectivamente.

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
    caption: [Resultados da reprodução *Cenário 10*],
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

  Com a reprodução do método de @iotcryptojacking no novo _dataset_, @tab:our-svc-tune apresenta os resultados obtidos com a tunagem de hiperparâmetros. 

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

  O kernel foi o parâmetro mais determinante para o desempenho do modelo, com RBF e Poly obtendo resultados próximos, apesar de o primeiro treinar mais rápido. Além disso, o parâmetro C também foi importante, e o peso das classes se mostrou útil para lidar com o desbalanceamento.

  === Resultados finais <result_ours>

  A configuração que maximizou o F1 Macro no conjunto de validação foi o SVM com kernel RBF, C=2, gamma=auto e pesos balanceados, sendo ela a escolhida de forma definitiva. Os resultados no conjunto de teste são apresentados em @tab:our-svc-best.

  O modelo obteve desempenho quase perfeito na classe benigna (F1 = 0.99), reflexo do grande volume de amostras benignas disponíveis para treinamento. Para a classe maliciosa, o recall de 0.95 indica que apenas 5% dos ataques não foram detectados, embora a precisão de 88% indique uma quantidade considerável de falsos positivos. O F1 Macro de 0.96 confirma que o modelo equilibra bem as duas classes, apesar do desbalanceamento acentuado. Portanto, pode-se concluir que o desempenho do modelo foi satisfatório.

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
      [*Média Macro*],     [*0.94*], [*0.97*], [*0.96*], [30.996],
      [*Média Ponderada*],  [1.00], [1.00], [1.00], [30.996],
      table.hline(stroke: 0.5pt),
    ),
    caption: [Relatório de classificação do melhor SVM (RBF, C=2, gamma=auto, pesos balanceados) no conjunto de teste do novo dataset.],
  ) <tab:our-svc-best>

  Em @tab:vpn_acc_mali, vemos que as VPNs são uma ferramenta de obfuscação de _cryptojacking_ com efetividade considerável, aumentando a dificuldade de classificação dos pacotes maliciosos.
#figure(
    {
      let data = csv("../data/vpn_to_acc_mali.csv")
      table(
        columns: (auto, auto, auto, auto),
        align: (center, center, center, center),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1).flatten().map(x => x),
        table.hline(stroke: 0.5pt),
      )
    },
    caption: [Acurácia e erro na classe maligna por VPN],
  ) <tab:vpn_acc_mali>


  === Discussão
  Os resultados descritos acima ilustram o desafio não só de treinar, mas especialmente de avaliar dados com um desabalanceamento tão grande quanto o em questão. É evidente que a média ponderada de qualquer métrica é enganosa em casos como este, enquanto a simples ilustrou melhor o cenário geral do desempenho do modelo. Ademais, este _dataset_ se mostrou mais desafiador que o apresentado em @iotcryptojacking, apesar de ter sido coletado em dispositivos mais poderosos.

  //Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  // == Resultados proposta de melhoria do artigo de referência (CASO FEITA)

  // - Nos dados usados pelo artigo de referência
  // - No novo conjunto de dados escolhido

  // Utilizar gráficos e tabelas. Atentar para não apenas descrever os resultados apresentados, mas também para explicá-los e discuti-los.

  // Comparar e discutir os resultados da proposta de melhoria com os resultados obtidos com a reprodução do artigo de referência.

  // == discussões
  // - apontar os erros q percebemos no artiigp
]
