# Project Structure

## Directory Layout

```
Circuit Maker/
├── circuit_generator.py      # Circuit expression parser and truth table generator
├── main.py                    # Circuit finder/optimizer with BFS algorithm
├── utils.py                   # Shared utility functions and gate definitions
├── circuit.txt                # Input: Circuit expressions to generate/find
├── README.md                  # Comprehensive documentation
├── TODO                       # Development task tracker
├── .gitignore                 # Git ignore patterns
├── I-O/                       # Input/Output data directory
│   ├── input.csv             # Generated: All input combinations
│   ├── output.csv            # Generated: Target output values
│   ├── gates_list.csv        # Configuration: Available gates and complexity
│   ├── ALLGATES.csv          # Full gate library reference
│   └── output_COPY.csv       # Backup output file
└── test/                      # Testing and experimentation
    ├── test copy.py          # Test scripts
    ├── test.ipynb            # Jupyter notebook for testing
    ├── input copy.csv        # Test input data
    ├── output copy.csv       # Test output data
    ├── test.csv              # Test data
    ├── truth_table_detailed.csv  # Detailed truth table outputs
    └── *.log                 # Various test execution logs
```

## Core Components

### 1. Circuit Generator (`circuit_generator.py`)
**Purpose**: Parse circuit expressions and generate truth tables

**Key Responsibilities**:
- Parse circuit.txt with three supported formats (single, multi-unnamed, named)
- Extract input variables from expressions
- Evaluate gate functions recursively
- Generate all 2^N input combinations
- Write input.csv and output.csv files
- Display formatted truth tables to console

**Key Functions**:
- Gate implementations (NOT, AND2-4, OR2-4, NAND2-4, NOR2-4, XOR2, XNOR2)
- Expression parsing and variable extraction
- CSV generation with proper column ordering

### 2. Circuit Finder (`main.py`)
**Purpose**: Find optimal circuit implementations using BFS

**Key Responsibilities**:
- Load input/output specifications from CSV files
- Load available gate library from gates_list.csv
- Implement BFS algorithm to search circuit space
- Track visited states to avoid redundant computation
- Generate and test circuit candidates
- Output found solutions with complexity metrics

**Key Functions**:
- BFS circuit search algorithm
- State management and deduplication
- Multi-output circuit optimization
- Solution validation and reporting

### 3. Utilities (`utils.py`)
**Purpose**: Shared functions and gate definitions

**Key Responsibilities**:
- Define all logic gate operations
- Provide gate evaluation functions
- Shared helper utilities for both generator and finder

**Key Functions**:
- Gate operation implementations
- Common utility functions

## Data Flow Architecture

```
circuit.txt
    ↓
[circuit_generator.py]
    ↓
I-O/input.csv + I-O/output.csv
    ↓
[main.py] ← I-O/gates_list.csv
    ↓
Circuit Solutions (console output)
```

## Architectural Patterns

### 1. Separation of Concerns
- **Generation**: circuit_generator.py handles expression parsing and truth table creation
- **Synthesis**: main.py handles circuit finding and optimization
- **Utilities**: utils.py provides shared gate definitions

### 2. CSV-Based Data Exchange
- Standardized CSV format for inputs, outputs, and gate libraries
- Enables easy integration with external tools
- Human-readable and editable data files

### 3. BFS Search Strategy
- Breadth-first exploration ensures optimal solutions found first
- State deduplication prevents redundant computation
- Complexity-based pruning limits search space

### 4. Modular Gate Library
- Gates defined in gates_list.csv for easy customization
- Complexity values guide optimization
- Support for variable input counts (1-4 inputs)

## Component Relationships

- **circuit_generator.py** → Produces data consumed by **main.py**
- **utils.py** → Shared by both generator and finder
- **I-O/ directory** → Central data exchange point
- **circuit.txt** → Single source of truth for circuit specifications
- **gates_list.csv** → Configures available gates for synthesis

## Configuration Files

### circuit.txt
Defines circuit expressions in one of three formats:
- Single expression with optional complexity annotation
- Multiple unnamed expressions (auto-numbered outputs)
- Named expressions with `OutputName : Expression` format

### I-O/gates_list.csv
Defines available gates for circuit synthesis:
- Columns: gate_name, num_inputs, complexity
- Controls which gates the finder can use
- Complexity values guide optimization decisions
