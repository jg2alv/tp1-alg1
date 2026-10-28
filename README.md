# Rain Check: shelter connectivity and critical-point analysis in Python

Rain Check models a rain-soaked festival as a graph of circular shelters. It finds covered routes between two people, identifies connected regions, and detects shelters whose removal would disconnect accessible areas.

## 1. Project information

- **Institution:** Universidade Federal de Minas Gerais (UFMG)
- **Degree:** Ciência da Computação
- **Course:** Algoritmos 1
- **Assignment:** Trabalho Prático 1
- **Semester:** 2025-01

The Python command-line program separates the geometric model from graph analysis. Shelters become vertices; overlapping or tangent circles create connections. Breadth-first search finds the minimum number of shelter transitions between the people and identifies connected components.

A depth-first traversal uses discovery times and low-link values to detect articulation points. An additional two-pass BFS routine estimates distances across connected components. The delivered report combines those three analyses in one output.

## 2. How to run

Prerequisite: Python 3.9 or newer, as specified by the assignment. The single-file implementation has no external dependencies. Run from the repository root:

```sh
python3 main.py
```

The program reads from standard input: the first person's integer coordinates, the second person's integer coordinates, the shelter count, and then one `radius center_x center_y` record per shelter. Both people must be inside supplied shelters. The implementation selects the first shelter containing each person.

Output lines retain the original labels `Parte 1`, `Parte 2`, and `Parte 3`. They represent the route distance, the component-distance estimate, and the number and one-based identifiers of critical shelters, respectively.

## 3. Usage example

Example 01 from the assignment supplies the complete input through standard input:

```sh
python3 main.py <<'EOF'
9 -8
-6 -9
5
3 -4 -4
3 -8 -8
5 7 -3
3 0 0
4 10 -9
EOF
```

The first two lines locate Ana and Bernardo. The next line declares five shelters, followed by their radius and center coordinates. No separate input file is required for this example.

## 4. Implementation decisions

- **Geometric adjacency:** center distance is compared with the sum of radii, so tangency permits a connection as well as overlap.
- **Adjacency lists:** the graph supports shared traversal routines while keeping geometry in the `Point`, `Shelter`, and `Person` classes.
- **Reusable BFS:** optional discovery state lets the same routine support route finding and component discovery.
- **Articulation-point invariants:** the DFS updates low-link values and treats a DFS root separately, avoiding the assumption that every vertex uses the same cut-vertex rule.

## 5. Tests and evaluation

### Verified results

Reference output provided in the assignment for Example 01:

```text
Parte 1: 4
Parte 2: 4
Parte 3: 3 1 3 4
```

The reference identifies a route of four shelter transitions, a maximum shortest-path distance of four, and critical shelters 1, 3, and 4.

The repository includes the implementation and its technical report, but no automated test suite or versioned input fixtures.

## 6. Learning and limitations

The project connects geometric modeling with graph traversal invariants. Handling disconnected regions and the DFS-root case was central to identifying critical shelters consistently. The technical report relates the algorithms to their time and space costs.

Graph construction compares every pair of shelters, so its cost differs from a traversal over an already constructed graph. The two-pass BFS value is an estimate for general graphs rather than a guaranteed exact diameter. DFS uses Python recursion, and the input path assumes that both people have shelter coverage.
