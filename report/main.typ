#import "@preview/charged-ieee:0.1.4": ieee
#import "sections/abstract.typ": abstract
#import "sections/introduction.typ": introduction
#import "sections/related-work.typ": related-work
#import "sections/threat-model.typ": threat-model
#import "sections/proposed-system.typ": proposed-system
#import "sections/our-solution.typ": our-solution
#import "sections/methodology.typ": methodology
#import "sections/results-and-discussions.typ": results-and-discussions
#import "sections/conclusions-and-future-work.typ": conclusions-and-future-work

#show bibliography: set std.bibliography(title: text(10pt)[Referências])

#show: ieee.with(
  title: [A Lightweight IoT Cryptojacking Detection Mechanism in Heterogeneous Smart Home Networks],
  abstract: abstract,
  authors: yaml("authors.yml"),
  bibliography: bibliography("refs.bib"),
)

#introduction
#related-work
#threat-model
#proposed-system
#our-solution
#methodology
#results-and-discussions
#conclusions-and-future-work
