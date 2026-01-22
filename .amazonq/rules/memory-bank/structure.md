# Circuit Maker - Project Structure

## Directory Organization

### Root Directory (`/`)
- **main.py**: Primary application entry point and orchestration logic
- **utils.py**: Core utility functions for circuit operations and data processing
- **log_output.log**: Runtime execution logs and search progress
- **.gitignore**: Version control exclusions (test/, __pycache__/)

### Test Directory (`/test/`)
- **test.py**: Unit tests and validation functions
- **input.csv**: Sample input data for circuit synthesis
- **output.csv**: Expected output specifications
- **gates_list.csv**: Available logic gates configuration
- **simple_input.csv / simple_output.csv**: Simplified test cases
- **or3_table.csv**: Truth table for 3-input OR gate
- **out.log**: Test execution logs

### Configuration Directory (`/.amazonq/rules/memory-bank/`)
- Memory bank documentation files (auto-generated)

## Core Components

### Main Application (main.py)
- Configuration management and file path setup
- Data loading orchestration (inputs, outputs, gates)
- Tree-based search execution and coordination
- Results logging and output formatting

### Utility Layer (utils.py)
- CSV data import/export functions
- Gate definition parsing and management
- Circuit evaluation and truth table generation
- Tree-based search algorithm implementation (single and multi-output)
- CircuitNode class for hierarchical circuit representation

### Test Framework (test/test.py)
- Unit test functions for core operations
- Validation of circuit synthesis results
- Test data generation and management

## Architectural Patterns

### Data Flow Architecture
1. **Input Layer**: CSV files → Python dictionaries
2. **Processing Layer**: Tree-based search with gate combinations
3. **Validation Layer**: Truth table verification
4. **Output Layer**: Circuit expressions and logs

### Search Strategy
- Tree-based exploration of circuit space
- Incremental complexity expansion (1 to max_complexity gates)
- Channel-based algorithm for multi-output optimization
- Complete level exploration before termination (enables signal reuse)
- Shared signal pool across all target outputs
- Comprehensive logging for debugging and analysis