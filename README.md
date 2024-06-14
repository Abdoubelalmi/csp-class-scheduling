# CSP-Class-Scheduling

CSP Class Scheduling problem solved for Intellectual Systems class.

## Code execution instructions

To run the code, you'll need to have Python installed along with the required packages.

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Abdoubelalmi/csp-class-scheduling.git
    cd CSP-Class-Scheduling
    ```

2. **Install the required package:**
    ```sh
    pip install tabulate
    ```

### Running the Code

To execute the code, simply run the `schedule.py` script:
```sh
python schedule.py
```
## Current Parameters

- Number of days: 5
- Number of teachers: 18
- Number of groups: 6
- Number of classrooms: 42
- Number of modules: 17

## Important Notes

- The code employs random shuffling of variables, leading to varied performance results.
- Execution time can vary significantly due to recursive enumeration of solutions.
- Depending on random selection order, schedule generation can range from milliseconds to minutes.
- Adjusting parameters like module count per group can optimize execution speed.

## Completed Tasks Description

All problem constraints remain consistent with previous laboratory implementations (genetic algorithm).

## Used Heuristics

- **Minimum Remaining Values (MRV):** Selects groups based on the largest number of assigned neighboring classes (in different groups/teachers).
- **Degree Heuristic:** Prioritizes classes with the most unfilled neighboring slots, involving higher constraint counts.
- **Least Constraining Value (LCV) Heuristic:** Selects teachers/subjects/audiences to minimize constraints on other groups when assigning values.
- **Forward Checking:** Verifies selected values against future constraints to prevent violations.
- **Constraint Propagation:** Enhances by rejecting values for variable A that invalidate all options for variable B connected by an arc.

## Benchmarking Results

The algorithm underwent 100 runs with subjects per group set to 4. Runs exceeding a million checks were considered lengthy, thus not included in speed calculations.

| Algorithm                    | Time per run (s) | Number of long runs |
|------------------------------|------------------|---------------------|
| Simple Backtracking          | 1.787            | 69                  |
| Minimum Remaining Values (MRV)| 1.15             | 66                  |
| Degree Heuristic             | 0.82             | 94                  |
| LCV Heuristic                | -                | 100                 |
| Forward Checking             | 3.648            | 61                  |

### Combined Heuristics

A combined approach using Forward Checking and MRV yielded superior results:

- Time per run: 2.41 s
- Number of long runs: 57/100

This combination outperformed individual heuristics.

## Additional Notes

- Implemented heuristics significantly enhance schedule generation efficiency.
- Future enhancements may focus on refining constraint propagation and exploring new heuristic combinations for further optimization.
- You are encouraged to explore and adjust code parameters to suit specific scheduling needs.
