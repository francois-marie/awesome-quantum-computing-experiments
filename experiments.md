---
layout: default
title: Experiments Data
nav_order: 2
---

# Awesome Quantum Computing Experiments

## Quantum Error Correction (QEC)
The QEC database tracks implementations of quantum error correction codes across different platforms.

### Key Parameters:
- **n**: Total number of physical data qubits
- **k**: Number of logical qubits
- **d**: Code distance

<table id="qec-table" class="display responsive nowrap" width="100%"></table>

## Magic State Distillation (MSD)
Magic state distillation is crucial for fault-tolerant quantum computation, enabling high-fidelity implementation of non-Clifford gates like the T gate.

### Tracked Metrics:
- Implementation Platform
- Distillation Protocol
- Magic State Type (|H>, |T>, |M>, |CZ>)
- Fidelity and Confidence Intervals
- Acceptance Rate (%)
- QEC Code Implementation
- Year

<table id="msd-table" class="display responsive nowrap" width="100%"></table>

## Entangled State Error
This database tracks progress in creating and maintaining high-fidelity entangled states.

### Key Metrics:
- Error Rate
- Platform
- Year

<table id="entangled-table" class="display responsive nowrap" width="100%"></table>

## Physical Qubit Count
Tracking the evolution of physical qubit counts across different quantum computing platforms.

### Tracked Information:
- Platform Type
- Number of Qubits
- Year

<table id="qubit-count-table" class="display responsive nowrap" width="100%"></table>

## Physical Qubit Coherence Times
This database tracks the evolution of coherence times (T1 and T2) across different physical qubit implementations.

### Key Metrics:
- T1 (Energy relaxation time)
- T2 (Dephasing time)
- Platform
- Year

<table id="physical-qubits-table" class="display responsive nowrap" width="100%"></table>

## Contributing

Have a new experiment to add? Check our [Contributing Guide](docs/CONTRIBUTING.md) for instructions on how to submit new entries.

Each experiment entry should include:
- Article Title
- Link (preferably arXiv or DOI)
- Publication Year
- Implementation Platform
- Relevant Measurements
- Additional Notes 