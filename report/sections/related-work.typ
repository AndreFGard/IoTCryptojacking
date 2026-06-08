#let related-work = [
  = Trabalhos relacionados
  A literatura sobre cryptojacking divide-se em duas frentes principais: a análise do ecossistema e o desenvolvimento de métodos de detecção. Pesquisas iniciais, como as de Huang et al. @bitcoin-mining-in-binary, focaram na análise de amostras de mineradores de _Bitcoin_ em formato binário, enquanto estudos posteriores, como o de Eskandari et al. @browser-cryptojacking, investigaram a proliferação de bibliotecas como a _Coinhive_ em milhares de sites para mineração de Monero, dada a popularização da mineração via navegador. Outros estudos, como os de Meland et el. @cryptojacking-attacks, Papadopoulos et al. @overheads-of-cryptojacking e Holz et al. @user-exposure-to-cryptojacking contribuíram avaliando o impacto direto e o custo operacional (_overhead_) que esses ataques impõem aos dispositivos e usuários finais. Adicionalmente, Bijmans et al. @exploitation-of-routers identificaram campanhas em escala de internet e novos vetores de ataque, como a infecção de roteadores _MikroTikS_.

  No que tange à detecção, as soluções existentes frequentemente utilizavam características dinâmicas do sistema. Petrov et al. @neural-networks-detection propuseram o sistema _CoinPolice_ para detectar cryptojacking utilizando redes neurais. No entanto, como apontado nas referências, o uso de características como eventos de CPU, atividade da memória e tempo de compilação do JavaScript não são viáveis para IoT, pois a maioria dos dispositivos IoT não permitem ser programados para coletar dados do navegador ou do hardware.

  Dentre os métodos baseados em rede, Rodriguez e Posegga @api-based-detection desenvolveram o _RAPID_, focado em detecção de mineradores em navegador com base na API. Muñoz et al. @netflow-ipfix-network trabalharam com medidas de rede como _netflow_ e _ipfix_. Mais recentemente, Neto et al. @incremental-deteccion apresentaram o _Minecap_, que utiliza aprendizado incremental com coleta dos dados feita em um ambiente emulado, o que limita a precisão contra ataques sofisticados. Diferente desses trabalhos, a solução proposta no artigo de referência é a primeira na área de detecção de cryptojacking a analisar diferentes estratégias de lucro do atacante, como por exemplo o uso de throttling para ataques furtivos, e variadas configurações de rede doméstica comprometida, o que afeta diretamente a eficácia da detecção e preenche uma lacuna deixada pelos estudos anteriores.
  
  A @tab:trabalhos-relacionados sumariza os principais métodos encontrados na literatura, destacando suas contribuições e limitações em comparação com a solução proposta.

#figure( 
  table( 
    columns: (1.2fr, 1fr, 1fr, 1fr), 
    align: (left, left, left, left), 
    stroke: none, 
    table.hline(y: 0, stroke: 0.5pt), 
    table.header([*Trabalhos*], [*Método*], [*Vantagens*], [*Desvantagens*]), 
    table.hline(y: 1, stroke: 0.5pt), 
    [Huang et al.], [Análise de amostras binárias], [Foco pioneiro na análise de mineradores de Bitcoin.], [Restrito ao formato binário clássico.], 
    [Eskandari et al.], [Análise de bibliotecas JS (Coinhive)], [Estudo de larga escala sobre proliferação em sites.], [Limitado a mineradores baseados em navegador.], 
    [Meland et al., Papadopoulos et al., Holz et al.], [Avaliação de impacto e custo operacional], [Medição precisa do overhead imposto aos usuários.], [Foco em análise de impacto, não em mecanismos de detecção.], 
    [Bijmans et al.], [Análise de campanhas em escala], [Identificação de novos vetores em roteadores MikroTik], [Foco em infraestrutura de botnets, não em detecção local.], 
    [Petrov et al.], [Redes Neurais e eventos de sistema], [Alta eficácia usando eventos de CPU e memória.], [Inviável para IoT (dispositivos "caixa-preta").], 
    [Rodriguez e Posegga], [Baseado em API], [Detecção eficaz de mineradores no navegador.], [Depende de recursos que muitos dispositivos IoT não possuem.], 
    [Muñoz et al.], [Medidas de rede (Netflow/IPFIX)], [Monitoramento não invasivo via tráfego de rede.], [Usa conjunto reduzido de características estatísticas.], 
    [Neto et al.], [Aprendizado incremental], [Capacidade de bloqueio em redes definidas por software.], [Dados coletados apenas em ambiente emulado.], 
    [Artigo Original de Referência], [Análise estatística de séries temporais (SVM)], [Agnóstico; 99% de acurácia; analisa ataques furtivos e IoT.], [Exige visibilidade do tráfego no roteador central.], 
    table.hline(y: 10, stroke: 0.5pt), 
  ), 
  caption: [Comparação dos trabalhos relacionados],
) <tab:trabalhos-relacionados>

]