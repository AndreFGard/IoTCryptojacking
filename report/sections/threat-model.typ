#let threat-model = [
  = Modelo de ameaça

  // Apresentar os ataques considerados para o trabalho. Utilizar figuras e/ou algoritmos e/ou equações para descrever os comportamentos dos ataques considerados. Também especificar as premissas consideradas para que a execução dos ataques seja possível.

  // Na @eq:equacao-da-reta é apresentado um exemplo de equação com a equação de uma reta.

  // $ y = a x + b $ <eq:equacao-da-reta>

  Como já mencionado, o trabalho considera ataques de _cryptojacking_ em dispositivos IoT. Esses ataques podem ser diferenciados pelo método de infecção:
  
  === Pelo navegador
  nessa modalidade os atacantes se aproveitam das vulnerabilidades que páginas _web_ possuem quanto à injeção de código malicioso, permitindo que o _script_ fornecido seja executado enquanto a aplicação (geralmente, páginas de conteúdo pirata) for usada. Para a geração do dataset foi criada uma página _WordPress_ que executava _scripts_ de diferentes provedores (como _Webmine.io_ e _WebminePool_) em suas páginas.

  === Baseado em host
  aqui, o programa de mineração é inserido diretamente no dispositivo do _host_ para executar o _malware_, tipicamente permitindo maior uso do poder computacional do usuário, visto que o _malware_ está embutido na máquina. Para a geração do _dataset_, o minerador _MinerGate_ foi baixado nos dispositivos.

  Também é possível disinguí-los pela fonte do minerador:

  === Via provedor de serviço
  nesse caso, é usado um serviço feito por terceiros que administra a distribuição de tarefas e recompensas. É consideravelmente mais fácil de usar porém não deixa o atacante controlar completamente seu ataque, e fornece menor anonimidade. Serviços como _Webmine_ foram usados na captura dos dados.

  === Command and Control (C&C)
  o C&C é um computador, geralmente baseado em nuvem, controlado pelo atacante que envia diretamente comandos para dispositivos infectados, definindo seu comportamento. Para a captura, foi criado um C&C próprio que enviava tarefas em intervalos de 2 minutos, focado na criptomoeda Monero.
  #figure(
    image("../data/cec.png"),
    caption: [Modelo de um Cryptojacking C&C]
  )
  Para que a execução desses ataques seja possível é necessário considerar algumas premissas:
  - O dispositivo alvo já está comprometido ou é capaz de executar o código malicioso: isso significa que a vítima acessa uma página que carrega _scripts_ de mineração ou que o _malware_ binário consegue ser instalado e executado no sistema;
  - O dispositivo possui conectividade com a internet e é capaz de estabelecer comunicação com a infraestrutura de mineração: premissa necessária para a comunicação com o servidor remoto ocorrer;
  - Existe infraestrutura externa capaz de coordenar o ataque: seja um provedor externo ou o servidor próprio, sempre é necessário que haja uma entidade coordenando o processo de mineração.
  
]