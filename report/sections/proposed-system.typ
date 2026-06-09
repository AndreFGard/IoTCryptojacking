#import "@preview/lovelace:0.3.0": *

#let proposed-system = [
  = Sistema proposto pelo artigo de referência

  // Apresentar o sistema proposto para detecção de intrusão OU ataque adversarial. Utilizar figuras e/ou algoritmos e/ou equações para descrever o sistema proposto.

  // - Quais os componentes da solução? Quais suas entradas e saídas? O que eles fazem? Como eles o fazem?
  // - Quais métodos ou algoritmos estão sendo propostos ou empregados e por que?

  // No @alg:cap é apresentado um exemplo de algoritmo.

  // #figure(
  //   kind: "algorithm",
  //   supplement: [Alg.],
  //   pseudocode-list[
  //     - *Require* $n >= 0$
  //     - *Ensure* $y = x^n$
  //     - $y <- 1$
  //     - $X <- x$
  //     - $N <- n$
  //     - *while* $N != 0$ *do*
  //       - *if* $N$ is even *then*
  //         - $X <- X times X$
  //         - $N <- N / 2$ #h(1em) // Exemplo de comentário
  //       - *else*
  //         - $y <- y times X$
  //         - $N <- N - 1$
  //   ],
  //   caption: [Algoritmo com legenda],
  // ) <alg:cap>
  A arquitetura é baseada em uma topologia de rede onde todos os dispositivos estão conectados a um roteador central. Além dele, há um computador que utiliza técnicas de espelhamento de porta e envenenamento ARP para coletar informações sobre o tráfego da rede. 

  1. O computador coleta o tráfego da rede e realiza filtragem pelo endereço MAC, retornando o tráfego associado à cada dispositivo, junto dos dados relativos ao tempo (_timestamp_) e tamanho (_packet_length_), identificando os pacotes que obedecem a seguinte condição, para o $i$-ésimo dispositivo:  
    $ ("MAC"_("src") = "MAC"_i) or ("MAC"_("dst") = "MAC"_i) $
  2. É feita a extração de _features_ utilizando _tsfresh_, devolvendo mais de 700 novas _features_ baseadas em séries temporais.
  3. Em seguida, realiza-se a seleção de _features_ por meio do cálculo do _p-value_, recebendo o novo _dataset_ pós-extração e retornando-o mantendo apenas as mais estatisticamente relevantes (onde $"p-value" < 0,05$)
  3. O classificador, um modelo _Support Vector Machine_ (SVM) recebe o _dataset_ e prevê se o dispositivo é maligno (infectado) ou benigno.

  A coleta de dados proposta garante a viabilidade do modelo para sistemas IoT ao tratar exclusivamente de dados de rede, sem exigir informações à nível de hardware ou de scripts de navegador que alguns dispositivos não seriam capazes de fornecer. Enquanto isso, a extração retira o máximo de informação possível desse _dataset_ limitado e a seleção mantém o "peso leve" do modelo. Por fim, o SVM foi selecionado por mostrar melhor performance quando comparado aos outros classificadores testados (KNN, regressão logistíca e _naive bayes_) e por possuir maior estabilidade. 
]