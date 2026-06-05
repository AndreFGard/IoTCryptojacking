#import "@preview/lovelace:0.3.0": *

#let proposed-system = [
  = Sistema proposto pelo artigo de referência

  Apresentar o sistema proposto para detecção de intrusão OU ataque adversarial. Utilizar figuras e/ou algoritmos e/ou equações para descrever o sistema proposto.

  - Quais os componentes da solução? Quais suas entradas e saídas? O que eles fazem? Como eles o fazem?
  - Quais métodos ou algoritmos estão sendo propostos ou empregados e por que?

  No @alg:cap é apresentado um exemplo de algoritmo.

  #figure(
    kind: "algorithm",
    supplement: [Alg.],
    pseudocode-list[
      - *Require* $n >= 0$
      - *Ensure* $y = x^n$
      - $y <- 1$
      - $X <- x$
      - $N <- n$
      - *while* $N != 0$ *do*
        - *if* $N$ is even *then*
          - $X <- X times X$
          - $N <- N / 2$ #h(1em) // Exemplo de comentário
        - *else*
          - $y <- y times X$
          - $N <- N - 1$
    ],
    caption: [Algoritmo com legenda],
  ) <alg:cap>
]