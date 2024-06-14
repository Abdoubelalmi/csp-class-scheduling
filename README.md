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
Current Parameters
------------------
Number of days: 5
Number of teachers: 18
Number of groups: 6
Number of classrooms: 42
Number of modules: 17

Important Notes
---------------
- The code contains random shuffling of some variables, so performance results may vary.
- In some cases, the execution can take a very long time (because there is a recursive enumeration of solutions), so it is better not to wait for the end, but to start again.
- The schedule can be built both in a fraction of a second and in tens of minutes, depending on the random order of selection of values in the problem. Randomness is necessary to avoid long monotonous calculations.
- If you reduce some parameters (for example, the number of modules per group), the code will run faster.

Description of Completed Tasks
-------------------------------
All restrictions on the problem remain the same as from the previous laboratory (genetic algorithm).

Used Heuristics
---------------
✅ Minimum Remaining Values (MRV): Selects the group for the class that has the largest number of assigned neighbors (classes running at the same time, but in a different group/teacher).
✅ Degree Heuristic: Chooses the class with the largest degree - that is, the one that has the most unfilled neighbors, and therefore is involved in the largest number of constraints.
✅ Least Constraining Value (LCV) Heuristic: Instead of classes (variables), teachers/subjects/audiences (values) are selected in such a way that the choice of a teacher for one group imposes the least constraints on another group.
✅ Forward Checking: When choosing values, a check is made to see if these values will not break the corresponding restrictions in the future (similar to rejecting unacceptable values from the domain of a variable).
✅ Constraint Propagation: Adds the possibility of rejecting the values of variable A that lead to the inadmissibility of all values of variable B, where A and B are connected by an arc. This method was not used in benchmarking because it can only be useful at higher parameter values, which significantly slow down benchmarking.

Benchmarking Results
--------------------
Each version of the algorithm was run 100 times (subjects per group = 4). If the limit check was performed more than a million times (several tens of seconds), then the run is considered long, and its duration is not included in the speed (time per run).

Algorithm                  | Time per run (s) | Number of long runs
-------------------------- | ---------------- | -------------------
Simple Backtracking        | 1.787            | 69
Minimum Remaining Values (MRV) | 1.15         | 66
Degree Heuristic           | 0.82             | 94
LCV Heuristic              | -                | 100
Forward Checking           | 3.648            | 61

Combined Heuristics
--------------------
Forward Checking and MRV show the best results. Therefore, a test was conducted using both of these methods simultaneously (as they modify different parts of the program). The results are as follows:

Time per run: 2.41 s
Number of long runs: 57/100

This combination performs better than any other individual heuristic.

Additional Notes
----------------
The heuristics used in the algorithm improve the efficiency and feasibility of generating a valid class schedule.
Future improvements could include refining the constraint propagation and exploring other heuristic combinations to further reduce the number of long runs.
Feel free to explore the code and modify parameters to suit your specific scheduling needs.
