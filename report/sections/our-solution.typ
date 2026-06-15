#let our-solution = [
  = Solução proposta pela equipe para melhorar a solução do artigo de referência (CASO FEITA)

  // Apresentar a arquitetura e funcionamento do sistema proposto pelo artigo de referência. Utilizar figuras e/ou algoritmos e/ou equações para descrever o sistema proposto.

  // - O que espera-se melhorar em relação à solução proposta pelo artigo de referência?
  // - Quais os componentes da solução? Quais as suas entradas e saídas? O que eles fazem? Como eles o fazem?
  // - Quais métodos ou algoritmos estão sendo propostos ou empregados e por que?
  //
  Serão propostas melhorias no preprocessamento dos dados, particularmente na extração de features, e nos algoritmos usados pelo sistema. 

  Como será detalhado na seção de metodologia, identificamos que o _tsfresh_, o método de extração de features usado em @iotcryptojacking, coleta centenas de features com base em cada janela de pacotes, o que torna o treinamento lento mesmo em servidores de alto desempenho, além de ser um desafio em sistemas de baixo poder computacional. Visando mitigar esses pontos negativos, avaliaremos o _Pycatch22_@pycatch22, uma implementação de @ogcatch22, enquanto substituto para o _tsfresh_. Esse sistema selecionou 22 características usando dezenas de datasets de séries temporais, capturando grande parte das suas propriedades para diversas aplicações, e possui uma implementação otimizada, reduzindo também a necessidade de selecionar features.

  Nesse sentido, também se mostra necessário avaliar modelos baseados em árvore, pois existe um ecossistema consolidado, além da própria natureza do seu funcionamento, que facilita a implementação destes em dispositivos de baixo desempenho, além da sua inferência em si ser veloz. Portanto, foi escolhida a floresta aleatória (_Random Forest_) para essa avaliação.
]
