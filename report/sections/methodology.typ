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
  Foram coletados pelos próprios autores, reproduzindo o cenário de uma rede residencial de _IoT_. Então, os dados foram separados entre os tipos de dispositivos, entre ataques binários e baseados em navegador - que foram separados de acordo com o provedor do _script_ de mineração - e estratégia de lucro envolvidos, capturando uma variedade significativa. Foi necessário criar este novo _dataset_ devido a falta de outros que abordem Cryptojacking em um ambiente pensado em _IoT_.
  //(tabela com n de pacotes (n de linhas) de cada arquivo, com colunas pros 3 componentes, bem como total pra cada componente e total global)

  === Dados benignos
  A princípio, foi usado em @iotcryptojacking um dataset benigno já publicamente disponível. No entanto, os autores criaram ainda outro dataset benigno, garantindo a padronização dos tipos de dispositivo usados, além de uma diversidae grande do tipo de tráfego benigno produzido. Nesse caso, para cada dispositivo, foram simulados usos voltados para _downloads_, uso ocioso, uso interativo, navegação _Web_ e consumo de vídeos, exceto no caso do WebOS, para o qual só foram coletados dados de transmissão de vídeos, de forma consistente com o seu uso real.

  //(tabela com n de pacotes (n de linhas) de cada arquivo, com colunas pros 3 componentes, bem como total pra cada componente e total global)


  === Preprocessamento
  Foram criadas janelas de 10 pacotes e sem sobreposição. Então, uma biblioteca@tsfresh foi usada para extrair centenas de características automaticamente, as quais são selecionadas com base numa tabela de relevância. Depois, as janelas são separadas em treino e teste aleatoriamente, e _Cross-Validation_ é usada quando necessário. Na maioria das avaliações, é valido destacar, o cálculo da relevância é feito antes da separação dos dados, o que representa um risco de vazamento de dados.
  //(tabela com n de pacotes para cada split)


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
