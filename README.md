# Optimization Framework for Knapsack Problems Using Multi-Variable Branching and Genetic Programming

A Python-based framework leveraging SCIP for solving hard knapsack problem instances using a custom multi-variable branching strategies. The framework supports the integration of genetic programming techniques to guide the branching process. Parallel solving of multiple instances is supported for large-scale experimentation.

### Prerequisites

- Python >= 3.10
- GCC compiler

### Configuration

```shell
git clone https://github.com/Guillaume-Helbecque/scip-rl.git
cd scip-rl
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### Usage

Run the main solver script with options to generate and solve instances:

```bash
python main.py [options]
```

The available options are listed below.

#### Instance parameters:

- **`-n`**: number of items
  - any positive integer (`100` by default)

- **`-t`**: type of instance
  - `1`: uncorrelated
  - `2`: weakly correlated
  - `3`: strongly correlated
  - `4`: inverse strongly correlated
  - `5`: almost strongly correlated
  - `6`: subset sum
  - `9`: uncorrelated with similar weights
  - `11`: uncorrelated spanner, span(2,10) (default)
  - `12`: weakly correlated spanner, span(2,10)
  - `13`: strongly correlated spanner, span(2,10)
  - `14`: multiple strongly correlated, mstr(3R/10,2R/10,6)
  - `15`: profit ceiling, pceil(3)
  - `16`: circle, circle(2/3)

- **`-r`**: range of coefficients
  - any positive integer (`1000` by default)

- **`-s`**: number of instances in series
  - any positive integer (`100` by default)

- **`-i`**: index of the instance within the series
  - any positive integer (`1` by default)

#### Solver parameters:

- **`--timelimit`**: time limit for SCIP solving (seconds)
  - any positive integer (`None` by default)

- **`-b`**: branching rule index
  - `0`: SCIP default strong branching rule
  - `1`: custom strong branching rule
  - `2`: custom multi-variable strong branching rule
  - `3`: custom multi-variable strong branching rule with GP function

- **`--nv`**: size of branching set (only if `-b 2`)
  - any positive integer (`1` by default)

- **`--parmode`**: enable parallel solving of instances using all available CPU cores (only if `--solve-all`)

#### Output parameters:

- **`--no-output`**: disable standard output

- **`--save-output`**: save output in a file

- **`--check-output`**: check whether the SCIP solution matches the known optimal one, if one exists

- **`--solve-all`**: solve all instances in series (`-i` is ignored)
