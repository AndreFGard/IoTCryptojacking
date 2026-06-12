#let conclusions-and-future-work = [
  = Conclusões e trabalhos futuros

== Conclusões
  Este trabalho reproduziu e validou o sistema de detecção de cryptojacking em IoT baseado exclusivamente em análise de tráfego de rede implementado em @iotcryptojacking. Os resultados ficaram muito alinhados com os esperados, confirmando a eficácia da abordagem: acurácia de 98–99% no dataset original e F1 Macro de 0.96 no novo dataset (CNT21), com 30.996 amostras.

=== Principais contribuições
  A reprodução confirmou a hipótese central do artigo e gerou três achados adicionais: a identificação e correção de um vazamento de dados na seleção de features em @iotcryptojacking, conforme detalhado em @preprocessamento-deles; a análise do impacto de VPNs sobre o sistema proposto, que reduzem o desempenho em 2–4%; e a adoção de ponderação de classes com F1 Macro para lidar com o severo desbalanceamento de 1:58 entre tráfego benigno e malicioso.

  === Limitações identificadas

  Durante a reprodução dos cenários de @iotcryptojacking, mesmo dispondo de um _cluster_ de alto desempenho, a extração de features foi extrememante lenta. Então, considerando que os métodos de seleção de features mantiveram centenas de características, uma extração destas em tempo real seria muito desafiadora. Além disso, o desempenho é bastante dependente da composição dos dados benignos (kernel RBF varia 0.60-0.82 entre datasets), além da visibilidade de tráfego em um roteador central inviabilizar o sistema em uma rede segmentada. Outra deficiência do sistema é o grande desbalanceamento de dados, que dificulta a avaliação efetiva das técnicas, como elaborado.

  Apesar das limitações, o trabalho estabelece baseline sólido para detecção agnóstica de cryptojacking em IoT, com resultados transferíveis a novos contextos.

  == Trabalhos futuros
 
  Tendo em vista as limitações e insuficiências supracitadas, seria de alto interesse para a aplicabilidade desse sistema o teste de modelos baseados em árvore, ao redor dos quais existe um vasto ecossistema facilitando a implementação eficiente em dispositivos de borda. Além disso, a avaliação de sistemas de extração de feature mais eficientes, ou ao menos a elaboração de uma seleção mais restritiva, visando diminuir o custo computacional de treinamento e inferência, também seria muito benéfica.
]