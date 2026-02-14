# Technology Stack

## Programming Languages

### Python 3.x
- Primary language for all components
- Used for circuit generation, parsing, and BFS algorithms
- Standard library dependencies only (no external packages required)

## Core Libraries and Modules

### Standard Library Dependencies
- **csv**: Reading and writing CSV files for I/O data
- **itertools**: Generating binary input combinations (product function)
- **re**: Regular expression parsing for circuit expressions
- **collections**: Deque for BFS implementation, defaultdict for data structures
- **typing**: Type hints for better code clarity (Optional, List, Dict, Set, Tuple)

### Built-in Modules
- **eval()**: Dynamic evaluation of gate expressions
- **os**: File path operations
- **sys**: System-level operations

## File Formats

### CSV (Comma-Separated Values)
- **input.csv**: Binary input combinations (0/1 values)
- **output.csv**: Target output values (0/1 values)
- **gates_list.csv**: Gate library configuration (gate_name, num_inputs, complexity)
- Standard CSV format with headers

### Text Files
- **circuit.txt**: Plain text circuit expressions
- **README.md**: Markdown documentation
- **TODO**: Plain text task list
- **.gitignore**: Git ignore patterns

### Log Files
- **.log files**: Plain text execution logs for debugging

## Development Commands

### Running the Circuit Generator
```bash
python circuit_generator.py
```
- Reads: circuit.txt
- Generates: I-O/input.csv, I-O/output.csv
- Outputs: Truth table to console

### Running the Circuit Finder
```bash
python main.py
```
- Reads: I-O/input.csv, I-O/output.csv, I-O/gates_list.csv
- Outputs: Found circuit solutions to console

### Testing
```bash
python test/test copy.py
```
- Runs test scenarios
- Generates log files in test/ directory

### Interactive Development
```bash
jupyter notebook test/test.ipynb
```
- Interactive testing and experimentation
- Requires Jupyter installation

## Build System

### No Build Required
- Pure Python project with no compilation step
- No package manager configuration (requirements.txt not present)
- Standard library only - no pip install needed

## Development Environment

### Supported Platforms
- Windows (primary development platform based on file paths)
- Linux/macOS compatible (pure Python)

### IDE/Editor Support
- Works with any Python-compatible editor
- Jupyter notebook support for interactive testing
- Amazon Q integration via .amazonq/rules/ directory

## Version Control

### Git
- **.gitignore** configured to exclude:
  - test/ directory
  - __pycache__/ directories
  - *.log files

## Data Structures

### Key Algorithms
- **BFS (Breadth-First Search)**: Circuit synthesis algorithm
- **Recursive Evaluation**: Gate expression evaluation
- **State Deduplication**: Set-based visited state tracking
- **Combinatorial Generation**: itertools.product for input combinations

### Data Representations
- **Binary Values**: 0/1 integers for logic levels
- **Tuples**: Immutable state representation for hashing
- **Lists**: Input/output data storage
- **Dictionaries**: Gate definitions and mappings
- **Sets**: Visited state tracking

## Performance Considerations

### Complexity Management
- Exponential input space: 2^N combinations for N variables
- BFS search space grows with circuit depth
- State deduplication critical for performance
- Complexity-based pruning limits search

### Scalability Limits
- Practical limit: ~10 input variables (1024 rows)
- Search depth configurable to prevent excessive computation
- Memory usage grows with visited states

## Configuration

### gates_list.csv Format
```csv
gate_name,num_inputs,complexity
OR2,2,12
AND2,2,10
NOT,1,3
```
- Defines available gates for synthesis
- Complexity values guide optimization
- Easy to customize gate library

### circuit.txt Formats
1. Single expression: `GATE(inputs) [complexity=N]`
2. Multi-unnamed: One expression per line
3. Named: `OutputName : Expression`

## Logging and Debugging

### Log Files
- **GATES.LOG**: Gate-related debugging
- **log_output.log**: General execution logs
- **test/*.log**: Test execution logs with various verbosity levels

### Console Output
- Truth tables with formatted columns
- Circuit search progress
- Found solutions with complexity metrics
