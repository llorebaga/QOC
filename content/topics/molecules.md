---
updated: 2026-10-12
status: draft
key_papers:
  - key: tannor1985control
    note: Pump–dump control — timing two pulses to steer a wave packet toward a chosen reaction product.
  - key: brumer1986control
    note: Coherent control by interfering quantum pathways to a common final state.
  - key: judson1992teaching
    note: Learning control — let the experiment itself optimize the laser pulse, with a learning algorithm in the loop.
  - key: assion1998chemical
    note: Feedback-optimized femtosecond pulses change the branching ratio of a real chemical reaction.
  - key: koch2019rotation
    note: Review of quantum control of molecular rotation, from alignment to chirality and ultracold molecules.
  - key: brif2010control
    note: Review of the control of quantum phenomena, with molecular control as a central thread.
---

**Molecular control** uses tailored light to steer the dynamics of molecules — breaking a chosen bond, selecting a
reaction product, exciting a vibrational or rotational state, aligning or orienting the molecule, telling enantiomers
apart. It is one of the historical roots of quantum optimal control, and several of the field's ideas and algorithms
were born here [@gordon1997active; @rabitz2000whither; @brif2010control].

## Origins

Two schemes started the field in the 1980s. Tannor and Rice proposed timing a pump and a dump pulse so that a wave
packet reaches the desired reaction channel [@tannor1985control; @tannor1986coherent]. Brumer and Shapiro proposed
interfering several quantum pathways that lead to the same final state, so that the relative phase of the fields
decides the outcome [@brumer1986control]. Optimal control theory generalized both: the field is the solution of a
variational problem [@shi1988optimal; @peirce1988optimal; @kosloff1989wavepacket]. Monotonically convergent
algorithms of the [[krotov|Krotov]] type were developed for these problems [@somloi1993controlled; @zhu1998rapid].
See [[problem-formulation]].

## Learning control in the laboratory

Molecular Hamiltonians are rarely known well enough for open-loop design. Judson and Rabitz proposed letting the
experiment itself evaluate candidate pulses, with a learning algorithm choosing the next ones [@judson1992teaching].
Femtosecond pulse shapers based on spatial light modulators made this practical [@weiner2000shaping]. Notable
results:

- Feedback-optimized phase-shaped pulses changed the branching ratio of a photodissociation reaction
  [@assion1998chemical].
- Optimally tailored strong-field pulses selectively broke and rearranged chemical bonds [@levis2001selective].
- Shaped pulses controlled the flow of energy in a biological light-harvesting complex [@herek2002harvesting].
- The spectral phase of a femtosecond pulse controls two-photon transitions through interference, so that shaped
  pulses can either excite efficiently or leave the transition dark [@meshulach1998twophoton].

Why learning control works so often is explained by the structure of [[control-landscapes|control landscapes]],
which for controllable systems are free of traps [@rabitz2004landscape]. See [[closed-loop]] and [[gradient-free]].

## Rotation, alignment and chirality

Molecular rotation is well suited to control: its Hamiltonian has few, accurately known parameters
[@koch2019rotation]. Strong non-resonant laser pulses align and orient molecules
[@stapelfeldt2003aligning]. For chiral molecules, phase-controlled microwave pulses that drive a closed loop of three
rotational transitions detect enantiomers [@patterson2013chiral]. They can also transfer one enantiomer selectively
to a higher rotational state [@eibenberger2017chiral].

## Ultracold molecules

At ultracold temperatures, molecules can be controlled state by state. A single STIRAP step transferred weakly bound
KRb molecules to their rovibrational ground state, producing a dense gas of polar molecules [@ni2008polar]. Coherent
control of photoassociation, which forms molecules from atom pairs with shaped light, has been reviewed in
[@koch2012photoassociation]. Optimal control has also been used to design laser cooling of internal molecular degrees
of freedom [@bartana1997cooling]. See [[adiabatic-passage]].

## Limitations

- Polyatomic molecules have many coupled degrees of freedom. Accurate potential surfaces and dipole moments are
  rarely available, which restricts open-loop design.
- In condensed phases, fast dephasing limits coherent control to short times.
- Pulses found by learning control are often hard to interpret, and strong fields compete with ionization.
