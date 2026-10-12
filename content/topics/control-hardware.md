---
updated: 2026-10-12
status: draft
key_papers:
  - key: reilly2015interface
    note: Review of the quantum–classical interface of solid-state qubits — the electronics that control and read them.
  - key: ryan2017hardware
    note: Hardware, gateware and software for dynamic experiments with real-time feedback and feed-forward.
  - key: salathe2018latency
    note: FPGA signal processing that turns readout into feedback triggers with low latency.
  - key: stefanazzi2022qick
    note: QICK, an open-source RFSoC-based controller that synthesizes multi-GHz pulses directly.
  - key: xue2021cmos
    note: Cryogenic CMOS control of silicon qubits, a step toward integrating electronics next to the qubits.
  - key: rol2020distortion
    note: Measuring and compensating distortions of flux-control pulses with the qubit itself.
software:
  - name: QICK
    url: https://github.com/openquantumhardware/qick
    note: firmware and software for RFSoC-based qubit control and readout
  - name: Qibolab
    url: https://github.com/qiboteam/qibolab
    note: hardware drivers and pulse execution for several control electronics platforms
---

**Control hardware** is the classical machinery between an optimized pulse and the qubit: waveform generators and
synthesizers, cables, filters and amplifiers, digitizers, FPGAs that make real-time decisions, and the software stack
that schedules and calibrates everything [@reilly2015interface]. Its properties — bandwidth, resolution, latency,
noise, distortion, channel count — are constraints that every optimal-control problem inherits. As processors grow,
the electronics become a scaling problem in their own right.

## From waveform to qubit

- **Generating pulses.** Pulses are usually synthesized at baseband by arbitrary waveform generators and mixed up to
  the qubit frequency. RF system-on-chip devices can now synthesize carriers of several GHz directly. One open
  design, QICK, reached 99.93% average gate fidelity on a transmon [@stefanazzi2022qick].
- **Bandwidth and resolution.** Sample rates and filters limit how fast pulses can change, and the resolution of the
  converters limits how precisely they are set. These limits enter optimal control as constraints or through a
  parametrization in smooth functions; see [[pulse-parametrization]]. Hardware nonlinearities can be included in the
  optimization itself [@hincks2015nonlinear].
- **Distortion.** Cables and filters distort pulses before they reach the device. The qubit can measure the
  distortion, of microwave pulses [@gustavsson2013distortions] or of flux pulses [@rol2020distortion], and the
  measured response can be pre-compensated. The qubit can also act as a vector network analyser of its own control
  line [@jerger2019vna]. See [[model-learning]].

## Real-time control and feedback

Error correction, feedback and adaptive protocols need decisions within a fraction of the coherence time. Dedicated
hardware and gateware feed qubit measurement results back or forward in real time [@ryan2017hardware]. FPGA-based
signal processing demodulates readout, assigns the qubit state and triggers feedback with a latency of about 110 ns
[@salathe2018latency]. Below-threshold surface-code memories ran with a real-time decoder [@google2025threshold], and
neural-network agents have acted on qubits in real time from FPGAs [@reuer2023realtime]. Modular, open FPGA
systems such as QubiC give full access to the control stack [@xu2021qubic]. See [[feedback-control]] and
[[error-correction]].

## Scaling the interface

Every qubit in a dilution refrigerator needs control and readout lines from room temperature. With millions of qubits
the wiring cannot scale, so control electronics are moving closer to the qubits.

- **Cryogenic CMOS.** Cryo-CMOS circuits are designed for operation at a few kelvin [@patra2018cryocmos]. A 28-nm
  cryogenic controller for transmons dissipates less than 2 mW at 3 K [@bardin2019cryocmos]. Cryogenic CMOS has
  controlled silicon spin qubits [@xue2021cmos].
- **Superconducting logic.** Single-flux-quantum circuits could drive qubits directly with bitstreams derived from
  optimal control, measured by a Josephson photon counter at the millikelvin stage [@mcdermott2018sfq].

Such controllers offer fewer degrees of freedom than room-temperature instruments. The 28-nm controller, for example,
implements a 16-word instruction set of XY gates [@bardin2019cryocmos], which restricts the pulses that optimal
control can use.

## Software stacks

Above the electronics sits software that compiles circuits into pulse schedules, calibrates them and analyses
results. It includes pulse-level languages [@cross2022openqasm3], calibration frameworks [@wittler2021c3] and tools
that combine control, characterization and optimization [@ball2021software]. See [[pulse-level-compilation]] and
[[closed-loop]].

## Limitations

- Pulses optimized without the true transfer function of the signal chain fail on hardware, and that transfer
  function drifts with temperature and time.
- Latency adds up from readout, digitization, decision and pulse generation, and limits feedback speed whatever the
  qubit.
- Low-power cryogenic electronics trade flexibility and precision for scalability, and their noise can couple into
  the qubits.
