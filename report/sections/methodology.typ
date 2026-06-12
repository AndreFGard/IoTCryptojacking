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


#let methodology = [
  = Metodologia

  == Dados usados pelo artigo de referência

  // #todo(done: true)[ Por que eles foram escolhidos? O que eles representam?]

  // #todo(done: true)[ Como os conjuntos de treino, validação e teste foram formados? ]

  // #todo()[ Há quantos dados em cada classe nos conjuntos de treino, validação e teste? ]

  // #todo(done: true)[ Quais foram os dados usados para avaliar o sistema proposto?]

  Os dados utilizados e desenvolvidos em @iotcryptojacking contém colunas associadas a coleta de dados, mas, para fins de treinamento, somente o tempo entre pacotes e o tamanho deles é considerado.

  === Dados Maliciosos
  Foram coletados pelos próprios autores, reproduzindo o cenário de uma rede residencial de _IoT_. Então, os dados foram separados entre os tipos de dispositivos, entre ataques binários e baseados em navegador - que foram separados de acordo com o provedor do _script_ de mineração - e estratégia de lucro envolvidos, capturando uma variedade significativa, como se vê em @fig:dist-malicioso. Foi necessário criar este novo _dataset_ devido a falta de outros que abordem Cryptojacking em um ambiente pensado em _IoT_. Como esperado, dispositivos mais fortes produzem mais tráfego, estando mais representados que os mais fracos.
  #figure(
    {
      let data = csv("../data/malicious_dist.csv")
      table(
        columns: (1fr, 1.2fr, 1.2fr, 1.2fr),
        align: (left, left, left, right, right),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1, -1).flatten().map(x => if x == "" { [] } else { x }),
        table.hline(y: 12, stroke: 0.5pt),
        ..data.last().map(x => [*#x*]),
        table.hline(y: 13, stroke: 0.5pt),
      )
    },
    caption: [N. de pacotes maliciosos por dispositivo, estratégia e tipo de ataque.],
  ) <fig:dist-malicioso>

  #figure(
    image("../imagens/malicious_distribution.png", width: 90%),
    caption: [Distribuição de pacotes maliciosos por dispositivo e tipo de ataque, em escala logarítmica.],
  ) <fig:dist-malicioso-img>

  === Dados benignos
  A princípio, foi usado em @iotcryptojacking um dataset benigno já publicamente disponível. No entanto, os autores criaram ainda outro dataset benigno, garantindo a padronização dos tipos de dispositivo usados, além de uma diversidae grande do tipo de tráfego benigno produzido. Nesse caso, para cada dispositivo, foram simulados usos voltados para _downloads_, uso ocioso, uso interativo, navegação _Web_ e consumo de vídeos, exceto no caso do WebOS, para o qual só foram coletados dados de transmissão de vídeos, de forma consistente com o seu uso real, como apresentado em @fig:dist-benigno.

  #figure(
    image("../imagens/benign_distribution.png", width: 90%),
    caption: [Distribuição de pacotes benignos (_benign-2_) por dispositivo e atividade.],
  ) <fig:dist-benigno>

  #figure(
    align(center + horizon, {
      let data = csv("../data/benign_dist.csv")
      table(
        columns: (1.2fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1.2fr),
        align: (left, right, right, right, right, right, right),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1, -1).flatten().map(x => if x == "-" or x == "" { [-] } else { x }),
        table.hline(y: 5, stroke: 0.5pt),
        ..data.last().map(x => [*#x*]),
        table.hline(y: 6, stroke: 0.5pt),
      )
    }),
    caption: [Distribuição de pacotes benignos (_benign-2_) por dispositivo e atividade, valores absolutos.],
  ) <tab:dist-benigno>

  //tabela com a quantidade de dados por classe em treino,teste (lembrar de reforçar que usa cross validation)

  === Preprocessamento
  Foram criadas janelas de 10 pacotes e sem sobreposição. Então, a biblioteca _tsfresh_ @tsfresh foi usada para extrair centenas de características automaticamente, as quais são selecionadas com base numa tabela de relevância. Depois, as janelas são separadas em treino e teste aleatoriamente, e _Cross-Validation_ é usada quando necessário. No entanto, é importante destacar que, na maioria dos cenários, o cálculo da relevância é feito antes da separação dos dados, o que representa um risco de vazamento de dados.

  A @tab:divisao-dados-split apresenta a quantidade de pacotes e janelas por classe, bem como o n. de janelas por split. Os dados benignos são consideravelmente maiores, e o desbalanceamento aumenta ainda mais nos estudos em que os tipos e estratégias de ataque são separados.

  #figure(
    {
      let data = csv("../data/split_dist.csv")
      table(
        columns: (auto, auto, auto, auto, auto, auto),
        align: (left, right, right, right, right, right),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1, -1).flatten().map(x => if x == "" { [] } else { x }),
        table.hline(y: 3, stroke: 0.5pt),
        ..data.last().map(x => [*#x*]),
        table.hline(y: 4, stroke: 0.5pt),
      )
    },
    caption: [Divisão das janelas de dados (10 pacotes por janela) do conjunto de dados completo para treino/validação e teste.],
  ) <tab:divisao-dados-split>


  == Novo conjunto de dados escolhido

  O novo conjunto de dados foi o "_Cryptojacking Network Traffic 2021_" (CNT21) @CNT21, disponibilizado publicamente pela Mendeley Data. O conjunto contém diversos fluxos de rede com exemplos de tráfego usual (usando aplicativos como _Youtube_, _Skype_ e serviços _Office_) e causado por criptomoedas (_Bitcoin_, _Bytecoin_ e _Monero_). Todos os fluxos são divididos entre tráfego de entrada e saída, e também há variações com VPNs e sem.

  Adicionalmente, todo o tráfego de criptomoedas está dividido em _full node_ (ou seja, um servidor que armazena o histórico completo da blockchain e valida transações de forma independente) e _miner_ (que contém o tráfego gerado pela mineração delas). O tráfego do _full node_ foge do escopo de _cryptojacking_ em dispositivos IoT, e portanto foi utilizado apenas os conjuntos do _miner_ para a avaliação do modelo, os quais foram rotulados como malignos.

  O _dataset_ foi escolhido por se encaixar perfeitamente na proposta do artigo de referência, tendo sido fornecidos ao modelo apenas as _features_ de tempo e tamanho do pacote, mas com uma variedade extra que enriquece a avaliação. Além disso, a inclusão de tráfego afetado por VPNs, uma técnica de obfuscação de tráfego não considerada anteriormente, também avalia a robustez do sistema proposto.

  A distribuição das amostras por atividade é apresentada em @fig:cnt21-activity enquanto a distribuição por tipo de VPN é apresentada em @fig:cnt21-vpn. O desbalanceamento entre classes benignas e maliciosas é severo, o que exige métricas robustas ao desbalanceamento e o ajuste de pesos de classe durante o treinamento.

  #figure(
    image("../imagens/activity_variables.png", width: 90%),
    caption: [Distribuição de janelas no CNT21 por atividade, separadas por classe (benigno vs. malicioso).],
  ) <fig:cnt21-activity>


  #figure(
    image("../imagens/vpn_variables.png", width: 90%),
    caption: [Distribuição de janelas no CNT21 por tipo de VPN, separadas por classe (benigno vs. malicioso).],
  ) <fig:cnt21-vpn>

  == Preprocessamento <metodol_ours>

  Inicialmente, os dados são agrupados baseados na sua fonte ("_activity_") e no tipo de VPN, se presente, distribuindo as classes igualmente entre os _splits_. Em seguida, dentro de cada grupo, são criadas janelas com o mesmo tamanho usado em @iotcryptojacking. Após esse processamento, elas são divididas sequencialmente em conjuntos de treino, validação e teste, evitando vazamento temporal de dados. Então, os respectivos conjuntos dos grupos são unidos, e @tab:divisao-dados-split-novo mostra a distribuição exata desses dados.

  #figure(
    {
      let data = csv("../data/split2.csv")
      set text(size: 8.5pt)
      table(
        columns: (auto, auto, auto, auto, auto, auto),
        align: (left, right, right, right, right, right),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header(..data.at(0).map(x => [*#x*])),
        table.hline(y: 1, stroke: 0.5pt),
        ..data.slice(1, -1).flatten().map(x => if x == "" { [] } else { x }),
        table.hline(y: 3, stroke: 0.5pt),
        ..data.last().map(x => [*#x*]),
        table.hline(y: 4, stroke: 0.5pt),
      )
    },
    caption: [Divisão das janelas entre treino, validação e teste no novo _dataset_],
  ) <tab:divisao-dados-split-novo>

  === Extração de Features

  Após a divisão, é feita a extração de _features_ nos dados. Como em @iotcryptojacking, usou-se a biblioteca _tsfresh_, que calcula centenas de característícas das duas colunas. Posteriormente, é testada a relevância das novas _features_ para a maliciosidade, mantendo apenas as mais relevantes (onde $"p_value" < 0,05$). Desta forma, foram selecionadas 416 features.

  === Modelo e Tuning de Hiperparâmetros

  Mantivemos o uso de SVM para seguir a mesma abordagem do artigo de referência. No entanto, como os dados são diferentes, realizamos um novo processo de tunagem de hiperparâmetros.

  Fizemos uma busca em grade usando o conjunto de validação, testando as seguintes combinações:
  - C: $1$ e $2$;
  - Kernel: Linear, Polinomial, RBF e Sigmoide;
  - Gamma: Scale e Auto;
  - Pesos das classes (_class\_weight_): Balanced e None.

  O desbalanceamento severo é um problema claro nos dois datasets, já que o tráfego benigno contínuo é muito maior que o tráfego de mineração. Isso influencia diretamente o treinamento. Por isso, incluímos o parâmetro class_weight="balanced" na busca, ajustando o peso das classes de forma a amenizar os efeitos da super-representação de uma classe. Nesse sentido, o uso do F1 Macro ao invés do F1 Ponderado também é crucial#footnote[Uma métrica Macro, como o F1 Macro, une o F1 de ambas as classes com uma média simples, invariante a desbalanceamento, enquanto as métricas ponderadas (_weighted_) aumentam o peso de uma classe na métrica final de acordo com a sua representatividade], pois esse é mais robusto ao desbalanceamento.

]
