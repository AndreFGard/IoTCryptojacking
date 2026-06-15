#let conclusions-and-future-work = [
  = Conclusões e trabalhos futuros

== Conclusões
  Este trabalho reproduziu e validou o sistema de detecção de cryptojacking em IoT baseado exclusivamente em análise de tráfego de rede implementado em @iotcryptojacking. Os resultados ficaram muito alinhados com os esperados, confirmando a eficácia da abordagem: acurácia de 98–99% no dataset original e F1 Macro de 0.96 no novo dataset (CNT21), com 30.996 amostras.

=== Principais contribuições
  A reprodução confirmou a hipótese central do artigo e gerou três achados adicionais: a identificação e correção de um vazamento de dados na seleção de features em @iotcryptojacking, conforme detalhado em @preprocessamento-deles; a análise do impacto de VPNs sobre o sistema proposto, que reduzem o desempenho em 2–4%; e a adoção de ponderação de classes com F1 Macro para lidar com o severo desbalanceamento de 1:58 entre tráfego benigno e malicioso.

  === Limitações identificadas

  Com a reprodução dos cenários de @iotcryptojacking, nota-se que o desempenho é bastante dependente da composição dos dados benignos, pois o Kernel RBF varia 0.60-0.82 entre datasets, por exemplo.
  
  Além disso, a visibilidade de tráfego em um roteador central inviabiliza o sistema em uma rede segmentada, que também possuem naturalmente uma composição de tráfego diferenciada, então outro sistema precisaria ser elaborado.
  
  Outro desafio do mecanismo proposto é o grande desbalanceamento dos dados de treino, o que dificulta a avaliação efetiva das técnicas, como elaborado na seção de resultados, bem como o treinamento em si. Nesse sentido, o uso de uma extração de features tão ampla e relativamente demorada, utilizando mais de 400 características, em alguns cenários, também é um desafio para o treinamento, além de dificultar a aplicabilidade em cenários em tempo real.

  Apesar das limitações, o trabalho estabelece um algoritmo sólido  e com bom desempenho para detecção agnóstica de cryptojacking em IoT, com resultados transferíveis a novos contextos sem grandes dificuldades.

== Propostas de melhoria
Como observado, houve uma perda no dataset novo, mais desafiador, quando foram implementadas as propostas de melhoria. Embora o _Pycatch22_ e o _RandomForest_ tenham obtido resultados  satisfatórios em geral, consideradas as concessões e benefícios envolvidos, além de melhoras no desempenho em alguns cenários do dataset original, o estudo de outras estratégias mais robustas e abrangentes, particularmente na escolha de modelos, se mostra necessário.

  == Trabalhos futuros
 
 Considerados os pontos acimas, se mostra interessante a avaliação de modelos de _Deep Learning_, que diminuem a necessidade de extração de features manual e podem possuir uma capacidade de generalização maior, além de uma robustez alta a grandes datasets. Além disso, uma estratégia baseada em deteção de anomalias poderia ser benéfica, considerando o desbalanceamento observado.
]