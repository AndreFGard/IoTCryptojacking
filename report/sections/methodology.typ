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

  O novo conjunto de dados foi o "_Cryptojacking Network Traffic 2021_" (CNT21), disponibilizado publicamente pela Mendeley Data. O conjunto contém diversos fluxos de rede com exemplos de tráfego usual (usando aplicativos como _Youtube_, _Skype_ e serviços _Office_) e causado por criptomoedas (_Bitcoin_, _Bytecoin_ e _Monero_). Todos os fluxos são divididos entre o tráfego de entrada (_ingoing_) e saída (_outgoing_) e uma parcela deles foi mascarado por uma VPN (_NordVPN_ ou _ExpressVPN_).

  Adicionalmente, todo o tráfego de criptomoedas está dividido em _full node_ (ou seja, um servidor que armazena o histórico completo da blockchain e valida transações de forma independente) e _miner_ (que contém o tráfego gerado pela mineração delas). O tráfego do _full node_ foge do escopo de _cryptojacking_ e portanto foi utilizado apenas os conjuntos do _miner_ para a avaliação do modelo, os quais foram rotulados como malignos.

  O _dataset_ foi escolhido por se encaixar perfeitamente na proposta do artigo de referência, utilizando apenas o fluxo de rede com as _features_ de tempo e tamanho do pacote. Além disso, a inclusão de tráfego afetado por VPNs, algo que não foi experimentado no modelo original, serve como um bom teste para a robustez do sistema proposto.  

  == Preprocessamento

  Inicialmente, os dados são agrupados baseados na sua fonte ("_activity_") e no VPN, caso tenha, para não ocorrer a mistura de tráfego nas janelas. Em seguida, dentro de cada grupo, serão criados blocos sequenciais de dados (as janelas) com tamanho e sobreposição definidas como $10$ e $0$, respectivamente. Após esse processamento, elas são divididas sequencialmente em conjuntos de treino, validação e teste.

  Após o processo ter sido aplicado a cada grupo, eles são agregados no conjunto apropriado (seja treino, validação ou teste). A Table V contém as quantias exatas da divisão.

  #figure(
    {
      let data = csv("../data/split2.csv")
      set text(size: 8.5pt)
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
    caption: [Divisão das janelas de dados (10 pacotes por janela) do conjunto de dados completo para treino, validação e teste no novo _dataset_],
  ) <tab:divisao-dados-split-novo>

  === Extração de Features

  Após a divisão, é feita a extração de _features_ nos dados. Utilizando a biblioteca _tsfresh_ são calculadas centenas de característícas matemáticas das duas colunas. Posteriormente, será testado a relevância das novas _features_ contra a classe alvo (_is_malicious_), mantendo apenas as mais relevantes (onde $"p_value" < 0,05$). 

  === Modelo e Tuning de Hiperparâmetros

  Mantivemos o algoritmo *Support Vector Machine* (SVM) para seguir a mesma abordagem do artigo de referência. No entanto, como os dados são diferentes, realizamos um novo processo de tuning de hiperparâmetros.

  Fizemos uma busca em grade (*Grid Search*) usando o conjunto de validação, testando as seguintes combinações:
  - Custo ($C$): $1$ e $2$;
  - *Kernel*: Linear, Polinomial, RBF e Sigmoide;
  - $gamma$ (Gamma): _Scale_ e _Auto_;
  - Pesos das classes (_class\_weight_): _Balanced_ e _None_.

  O desbalanceamento severo é um problema claro nos dois datasets, já que o tráfego benigno contínuo é muito maior que o tráfego de mineração. Isso influencia diretamente o treinamento. Por isso, incluímos o parâmetro `class_weight="balanced"` na busca. Ele atua ajustando o peso dos erros de acordo com a frequência de cada classe. Na prática, isso força o modelo a dar a devida atenção aos dados maliciosos, evitando que ele tente atingir uma alta acurácia global simplesmente classificando tudo como benigno.
  
  == Métricas de avaliação

  Para essa seção, utiliza-se as seguintes variáveis:
  - TP: _True Positive_, significa que o modelo corretamente previu a instância como maliciosa;
  - FP: _False Positive_, significa que o modelo incorretamente previu a instância como maliciosa;
  - TN: _True Negative_, significa que o modelo corretamente previu a instância como benigna;
  - FN: _False Negative_, significa que o modelo incorretamente previu a instância como benigna;
  
  Para avaliar o desempenho do modelo no novo dataset, foi usado as seguintes métricas:

  - Acurácia: representa a quantidade de previsões corretas do modelo (instâncias maliciosas e benignas). Devido ao desbalanceamento entre as classes, nem sempre representará bem a qualidade do modelo
  $ "Acurácia" = ("TP" + "TN")/("TP"+"FP"+"TN"+"FN") $ <eq:equacao-da-reta>

  - Precisão: a proporção de previsões positivas (maliciosas) corretas
  $ "Precisão" = ("TP")/("TP"+"FP") $ <eq:equacao-da-reta>

  - _Recall_: representa quantas das instâncias maliciosas o modelo conseguiu detectar
  $ "Recall" = ("TP")/("TP"+"FN") $ <eq:equacao-da-reta>

  - F1 _Score_: a média harmônica entre precisão e _recall_. Útil para lidar com classes desbalanceadas, gerando uma métrica única para avaliar o desempenho na classe positiva
  $ "F1 Score" = 2* ("Precisão" * "Recall")/("Precisão" + "Recall") $ <eq:equacao-da-reta>


]
