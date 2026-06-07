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

  Descrever os dados e métricas utilizados para validar as soluções propostas e quais os experimentos realizados. Sobre os dados, descrever:

  == Dados usados pelo artigo de referência

  #todo(done: true)[ Por que eles foram escolhidos? O que eles representam?]

  #todo(done: true)[ Como os conjuntos de treino, validação e teste foram formados? ]

  #todo()[ Há quantos dados em cada classe nos conjuntos de treino, validação e teste? ]

  #todo(done: true)[ Quais foram os dados usados para avaliar o sistema proposto?]

  Os dados utilizados e desenvolvidos em @iotcryptojacking contém colunas associadas a coleta de dados, mas, para fins de treinamento, somente o tempo entre pacotes e o tamanho deles é considerado.

  === Dados Maliciosos
  Foram coletados pelos próprios autores, reproduzindo o cenário de uma rede residencial de _IoT_. Então, os dados foram separados entre os tipos de dispositivos, entre ataques binários e baseados em navegador - que foram separados de acordo com o provedor do _script_ de mineração - e estratégia de lucro envolvidos, capturando uma variedade significativa, como se vê em @fig:dist-malicioso. Foi necessário criar este novo _dataset_ devido a falta de outros que abordem Cryptojacking em um ambiente pensado em _IoT_. Como esperado, dispositivos mais fortes produzem mais tráfego, estando mais representados que os mais fracos.


  #figure(
    grid(
      columns: 2,
      column-gutter: 1em,
      table(
        columns: (1fr, 1.2fr, 1.2fr, 1fr),
        align: (left, left, left, right),
        stroke: none,
        table.hline(y: 0, stroke: 0.5pt),
        table.header([*Dispositivo*], [*Estratégia*], [*Tipo de ataque*], [*N. pacotes*]),
        table.hline(y: 1, stroke: 0.5pt),
        [Desktop], [Aggressive], [Webminepool], [234.272],
        [Raspberry], [nenhuma], [binary], [11.745],
        [Raspberry], [Aggressive], [Webminepool], [19.643],
        [Raspberry], [Robust], [Webminepool], [6.406],
        [Raspberry], [Stealthy], [Webminepool], [9.880],
        [Raspberry], [Aggressive], [webmine], [12.871],
        [Raspberry], [Robust], [webmine], [3.519],
        [Server], [nenhuma], [binary], [1.198.039],
        [Server], [Aggressive], [Webminepool], [2.539],
        [Server], [Robust], [Webminepool], [16.744],
        [WebOS], [nenhuma], [binary], [41.572],
        table.hline(y: 12, stroke: 0.5pt),
      ),
    ),
    caption: [N. de pacotes maliciosos por dispositivo, estratégia e tipo de ataque.],
  ) <fig:dist-malicioso>

  === Dados benignos
  A princípio, foi usado em @iotcryptojacking um dataset benigno já publicamente disponível. No entanto, os autores criaram ainda outro dataset benigno, garantindo a padronização dos tipos de dispositivo usados, além de uma diversidae grande do tipo de tráfego benigno produzido. Nesse caso, para cada dispositivo, foram simulados usos voltados para _downloads_, uso ocioso, uso interativo, navegação _Web_ e consumo de vídeos, exceto no caso do WebOS, para o qual só foram coletados dados de transmissão de vídeos, de forma consistente com o seu uso real, como apresentado em @fig:dist-benigno.

  #figure(
    //image("../imagens/benign_distribution.png", width: 100%),
    align(center + horizon, table(
      columns: (1.2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, right, right, right, right, right),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Dispositivo*], [*Download*], [*Ocioso*], [*Interativo*], [*Vídeo*], [*Web*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Laptop], [442.866], [113.602], [81.681], [29.010], [99.235],
      [Raspberry], [276.808], [73], [104.241], [57.205], [123.298],
      [Server], [564.831], [13.459], [123.728], [109.497], [43.713],
      [WebOS], [-], [-], [-], [177.704], [-],
      table.hline(y: 5, stroke: 0.5pt),
    )),
    caption: [Distribuição de pacotes benignos por dispositivo e atividade.],
  ) <fig:dist-benigno>

  //tabela com a quantidade de dados por classe em treino,teste (lembrar de reforçar que usa cross validation)

  === Preprocessamento
  Foram criadas janelas de 10 pacotes e sem sobreposição. Então, uma biblioteca@tsfresh foi usada para extrair centenas de características automaticamente, as quais são selecionadas com base numa tabela de relevância. Depois, as janelas são separadas em treino e teste aleatoriamente, e _Cross-Validation_ é usada quando necessário. No entanto, é importante destacar que, na maioria dos cenários, o cálculo da relevância é feito antes da separação dos dados, o que representa um risco de vazamento de dados.
  //(tabela com n de pacotes para cada split)

  A @tab:divisao-dados-split apresenta a quantidade de janelas (cada uma contendo 10 pacotes) para cada classe e a divisão correspondente entre os conjuntos de treino/validação e teste para cada um dos experimentos que compõem o Cenário 8.

  #figure(
    table(
      columns: (1.5fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      align: (left, right, right, right, right, right),
      stroke: none,
      table.hline(y: 0, stroke: 0.5pt),
      table.header([*Experimento*], [*Malicioso*], [*Benigno*], [*Treino/Val*], [*Teste*], [*Total*]),
      table.hline(y: 1, stroke: 0.5pt),
      [Timely], [974], [163.468], [123.331], [41.111], [164.442],
      [Timely (Oversampled)], [236.095], [236.095], [354.142], [118.048], [472.190],
      [Laptop vs. Laptop], [23.427], [76.639], [75.049], [25.017], [100.066],
      [Raspberry vs. Raspberry], [6.406], [56.162], [46.926], [15.642], [62.568],
      [Server vs. Server], [121.732], [29.039], [113.078], [37.693], [150.771],
      [WebOS vs. WebOS], [4.157], [17.770], [16.445], [5.482], [21.927],
      table.hline(y: 7, stroke: 0.5pt),
    ),
    caption: [N. de janelas (10 pacotes) por split],
  ) <tab:divisao-dados-split>


  == Novo conjunto de dados escolhido

  #todo()[ Quais foram os dados usados para avaliar o sistema proposto?]

  #todo()[ Por que eles foram escolhidos? O que eles representam?]

  == Preprocessamento

  #todo()[Como os conjuntos de treino, validação e teste foram formados?]

  #todo()[ Há quantos dados em cada classe nos conjuntos de treino, validação e teste?]

  === Extração de Features

  #todo()[ catch22]
  #todo()[ tsfresh]

  == Métricas de avaliação

  Deverá descrever as métricas de avaliação que serão utilizadas para avaliar os resultados obtidos com a reprodução do artigo. Explicar a motivação de uso das métricas e o que se deseja observar com cada uma delas. Apresentar as equações das métricas consideradas.
]
