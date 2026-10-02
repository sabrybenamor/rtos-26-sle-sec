# RTOS Labs

**Instructor:** Chadlia Jerad  
**Academic year:** 2026-2027

Lab assignments for the **Real-Time Operating Systems** course at ENSI. The labs are added here one by one during the semester. Each lab has its own folder, with a README that gives the objective, the requirements, the steps, the checker, how to submit, and the grading.

## Labs

| Lab | Topic | Platform |
|---|---|---|
| [Lab 1](lab1/) | Clock-driven scheduling: a structured cyclic executive for a helicopter flight controller | Linux (POSIX timers and signals) |

More labs will be added (pushed by the instructor) during the semester. Run `git pull` to get them.

## Repository Layout

```
rtos-26/
├── README.md        this file
├── collaborators.txt   your group and its members (fill in)
├── LICENSE
├── .github/         automatic checks (do not modify)
└── labN/
    ├── README.md    the lab: objective, steps, checking, grading
    ├── labN_answers.md
    └── ...          templates, provided sources, Makefile, scripts/
```

Do **not** modify, delete, or rename the files at the root of the repository (except `collaborators.txt`), including hidden files and `.github/`. In every lab, the README lists the files you must complete and the files you must **not** modify. Those lab files are restored to their original version when your work is checked.

## Rules for All Labs

### Group work
Unless a lab says otherwise, labs can be completed **individually, in pairs, or in groups of three**. Fill in `collaborators.txt`, at the root of the repository, with your group and its members before your first submission. Every member of the group must be able to explain the whole lab if the lab has an oral check.

### Oral check
Labs may end with an oral check. If so, you run the checker in front of the instructor, explain your code, and make a small live change. If you cannot explain or modify your own code, the code points are not awarded.

### Using AI assistants
You may use an AI assistant to **understand**: ask it to explain a concept, a system call, a compiler error, or a checker message. You may not use it to **write** the code you must implement or your answers.
Declare any AI use in the question of each answers file that asks for it. Declared use is not penalized; undeclared use is. Answers are reviewed for signs of AI generation.

### Similarity check
All submissions undergo a **similarity check**. Any attempt to copy a colleague's work results in a **complete reset of the grade for both parties**.

## License

BSD 2-Clause. See [LICENSE](LICENSE).
