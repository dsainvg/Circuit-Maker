# Product Overview

## Purpose
Circuit Maker is a Python-based tool for digital logic circuit design and optimization. It provides automated generation of truth tables from circuit expressions and intelligent circuit synthesis using breadth-first search algorithms to find optimal implementations using available logic gates.

## Key Features

### Circuit Expression Generator
- Parses circuit expressions from text files into truth tables
- Supports nested gate expressions with arbitrary complexity
- Generates complete input/output CSV files for all possible input combinations
- Handles multiple circuit formats: single expressions, unnamed multi-circuits, and named outputs
- Supports 15+ logic gate types (NOT, AND, OR, NAND, NOR, XOR, XNOR) with 1-4 inputs

### Circuit Finder/Optimizer
- Implements BFS-based circuit synthesis algorithm
- Finds optimal circuit implementations using available gate libraries
- Supports multiple output optimization with shared intermediate signals
- Configurable complexity constraints and search depth limits
- Generates circuits that match target truth tables exactly

### Truth Table Management
- Automatic generation of all binary input combinations (2^N rows for N variables)
- CSV-based input/output format for easy integration
- Console-based truth table visualization
- Support for alphanumeric variable naming (A, B, C or A1, A2, B5, etc.)

## Target Users

### Digital Logic Designers
- Design and verify combinational logic circuits
- Explore alternative implementations with different gate sets
- Optimize circuit complexity and gate count

### Students and Educators
- Learn digital logic design principles
- Visualize circuit behavior through truth tables
- Understand gate-level implementations of logic functions

### Hardware Engineers
- Prototype circuit designs before HDL implementation
- Verify logic equivalence between different implementations
- Explore trade-offs between different gate libraries

## Use Cases

1. **Circuit Verification**: Generate truth tables from circuit expressions to verify correctness
2. **Circuit Synthesis**: Find gate-level implementations for desired logic functions
3. **Design Exploration**: Compare multiple circuit implementations using different gate sets
4. **Educational Tool**: Teach digital logic concepts with visual truth tables
5. **Optimization**: Find minimal-complexity circuits for given specifications
6. **Multi-Output Circuits**: Design circuits with shared logic for multiple outputs (e.g., adders, ALUs)
