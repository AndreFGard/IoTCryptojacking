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
      columns: 1,
      column-gutter: 1em,
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
    ),
    caption: [N. de pacotes maliciosos por dispositivo, estratégia e tipo de ataque (original vs. pós-poda por endereço MAC).],
  ) <fig:dist-malicioso>

  === Dados benignos
  A princípio, foi usado em @iotcryptojacking um dataset benigno já publicamente disponível. No entanto, os autores criaram ainda outro dataset benigno, garantindo a padronização dos tipos de dispositivo usados, além de uma diversidae grande do tipo de tráfego benigno produzido. Nesse caso, para cada dispositivo, foram simulados usos voltados para _downloads_, uso ocioso, uso interativo, navegação _Web_ e consumo de vídeos, exceto no caso do WebOS, para o qual só foram coletados dados de transmissão de vídeos, de forma consistente com o seu uso real, como apresentado em @fig:dist-benigno.

  #figure(
    //image("../imagens/benign_distribution.png", width: 100%),
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
    caption: [Distribuição de pacotes benignos (benign-2) por dispositivo e atividade.],
  ) <fig:dist-benigno>

  //tabela com a quantidade de dados por classe em treino,teste (lembrar de reforçar que usa cross validation)

  === Preprocessamento
  Foram criadas janelas de 10 pacotes e sem sobreposição. Então, uma biblioteca@tsfresh foi usada para extrair centenas de características automaticamente, as quais são selecionadas com base numa tabela de relevância. Depois, as janelas são separadas em treino e teste aleatoriamente, e _Cross-Validation_ é usada quando necessário. No entanto, é importante destacar que, na maioria dos cenários, o cálculo da relevância é feito antes da separação dos dados, o que representa um risco de vazamento de dados.

  A @tab:divisao-dados-split apresenta a quantidade de pacotes e janelas por classe, bem como o n. de janelas por split. Os dados benignos são consideravelmente maiores, e o desbalanceamento aumenta ainda mais nos estudos em que os tipos e estratégias de ataque são separados.

  #figure(
    {
      let data = csv("../data/split_dist.csv")
      table(
        columns: (auto, auto,auto, auto, auto, auto),
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
