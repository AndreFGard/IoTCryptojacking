#let introduction = [
  = Introdução
  Com a ascensão das tecnologias de blockchain e o modelo de consenso de Prova de Trabalho (PoW), o cryptojacking consolidou-se como uma ameaça cibernética lucrativa, onde atacantes sequestram o poder de processamento de terceiros para minerar criptomoedas sem consentimento. O problema investigado no trabalho de referência é a detecção dessa atividade maliciosa em redes domésticas inteligentes (IoT), ambientes que se tornaram alvos preferenciais devido à sua presença massiva, conectividade constante e vulnerabilidades críticas, como o uso de senhas padrão e a falta de autenticação robusta.

  Este tema é de alto interesse acadêmico e prático pois a diversidade de fabricantes e protocolos na IoT torna complexo o desenvolvimento de defesas unificadas. Diferente de computadores tradicionais, dispositivos IoT operam frequentemente como caixas-pretas, o que impossibilita a instalação de ferramentas locais para monitorar eventos de hardware ou scripts de navegador, justificando a necessidade de uma solução que não interfira no software ou hardware do dispositivo.

  As soluções existentes, como listas de bloqueio e análise estática, possuem desvantagens significativas: são facilmente burladas por mudanças frequentes de domínio, técnicas de ofuscação de código e não conseguem lidar com malwares binários baseados em host. Para resolver essas limitações, o artigo de referência propõe um mecanismo de detecção leve e independente de dispositivo, fundamentado exclusivamente em características do tráfego de rede coletadas no roteador. O sistema utiliza metadados básicos de endereço MAC, carimbo de tempo e comprimento do pacote para alimentar modelos de aprendizado de máquina capazes de identificar padrões de mineração de forma agnóstica.

  As principais contribuições do trabalho são:

  - Algoritmo de detecção preciso e eficiente: Proposição de um sistema capaz de detectar cryptojacking baseado em navegador e em host com 99% de acurácia, utilizando apenas uma hora de dados de treinamento.
  - Análise de comportamentos adversários: Investigação inédita de diferentes estratégias de lucro (agressiva, robusta e furtiva) e o impacto de diversos níveis de comprometimento da rede (redes total ou parcialmente infectadas).
  - Técnicas de implementação em IoT: Desenvolvimento de métodos para implementar cryptojacking em novas categorias de dispositivos, como Smart TVs rodando WebOS.
  - Apoio à pesquisa aberta: Disponibilização pública do conjunto de dados (6,4 milhões de pacotes) e do código-fonte para permitir a reprodução e o avanço de estudos na área.
]