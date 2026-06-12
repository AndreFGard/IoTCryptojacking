#let conclusions-and-future-work = [
  = Conclusões e trabalhos futuros

  == Conclusões

  Este trabalho reproduziu e validou o sistema de detecção de cryptojacking em IoT baseado exclusivamente em análise de tráfego de rede implementado em @iotcryptojacking. Os resultados confirmam a eficácia da abordagem: acurácia de 98-99% no dataset original e F1 Macro de 0.96 no novo dataset (CNT21) com 30.996 amostras.
  
  === Principais contribuições

  - Validação robusta: Sistema detecta ataques agressivos com 98% F1, ataques binários com 99% e in-browser com 95%, confirmando a hipótese original
  - Descoberta sobre VPN: Primeira análise sistemática mostrando que VPN reduz desempenho em 2-4%, revelando ferramenta de ofuscação moderadamente efetiva
  - Correção metodológica: Identificou-se e corrigiu-se vazamento de dados (feature selection era feito pré-split), implementando abordagem mais rigorosa
  - Tratamento de desbalanceamento: Aplicou-se ponderação de classes e F1 Macro para lidar com proporção 1:58 (benigno:malicioso)

  === Limitações identificadas

  - Infraestrutura: Requer visibilidade de tráfego no roteador central, inviável em redes segmentadas
  - Obfuscação: VPN compromete detectabilidade; ataques sofisticados combinando VPN + throttling furtivo podem contornar
  - Sensibilidade: Performance afetada pela composição de dados benignos (kernel RBF varia 0.60-0.82 entre datasets)
  - Custo computacional: Extração de 700+ features pode ser impraticável em roteadores IoT de baixa potência
  - Desbalanceamento: 12% falsos positivos em dataset desbalanceado, risco de fadiga de alertas

  Apesar das limitações, o trabalho estabelece baseline sólido para detecção agnóstica de cryptojacking em IoT, com resultados transferíveis a novos contextos.

  == Trabalhos futuros

]