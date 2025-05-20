# Sudoku Solver Report

**Solved at:** 2025-05-20 19:37:59

## Input Image

<img src="easy_readme.jpg" alt="Sudoku Input" width="400"/>

---

## Parsed Board (Extracted from Image)

| 3 |   | 5 |   | 8 | 4 | 9 |   | 2 |
|---|---|---|---|---|---|---|---|---|
|   | 2 | 9 | 1 | 6 | 3 |   | 5 | 8 |
| 7 | 8 | 1 |   |   |   | 3 | 4 | 6 |
|   |   |   | 2 | 4 | 9 |   |   |   |
| 1 | 9 |   |   | 7 | 8 | 4 | 6 | 3 |
| 5 |   |   | 6 |   |   |   | 7 |   |
| 9 | 7 |   | 3 |   | 6 |   | 2 | 4 |
| 8 | 1 | 3 |   |   | 2 | 6 | 9 |   |
|   |   | 4 |   |   | 7 | 5 | 3 | 1 |

---

## Edited Board (User Corrections Applied) (Edited)

| 3 |   | 6 |   | 8 | 4 | 9 |   | 2 |
|---|---|---|---|---|---|---|---|---|
|   | 2 | 9 | 1 | 6 | 3 |   | 5 | 8 |
| 7 | 8 | 1 |   |   |   | 3 | 4 | 6 |
|   |   |   | 2 | 4 | 9 |   |   |   |
| 1 | 9 |   |   | 7 | 8 | 4 | 6 | 3 |
| 5 |   |   | 6 |   |   |   | 7 |   |
| 9 | 7 |   | 3 |   | 6 |   | 2 | 4 |
| 8 | 1 | 3 |   |   | 2 | 6 | 9 | 7 |
|   |   | 4 |   |   | 7 | 5 | 3 | 1 |

---

## Final Solved Board (Backtracking)

| 3 | 5 | 6 | 7 | 8 | 4 | 9 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
| 4 | 2 | 9 | 1 | 6 | 3 | 7 | 5 | 8 |
| 7 | 8 | 1 | 9 | 2 | 5 | 3 | 4 | 6 |
| 6 | 3 | 7 | 2 | 4 | 9 | 1 | 8 | 5 |
| 1 | 9 | 2 | 5 | 7 | 8 | 4 | 6 | 3 |
| 5 | 4 | 8 | 6 | 3 | 1 | 2 | 7 | 9 |
| 9 | 7 | 5 | 3 | 1 | 6 | 8 | 2 | 4 |
| 8 | 1 | 3 | 4 | 5 | 2 | 6 | 9 | 7 |
| 2 | 6 | 4 | 8 | 9 | 7 | 5 | 3 | 1 |

---

## Final Board State (AI Agent)

| 3 | 5 | 6 | 7 | 8 | 4 | 9 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
|   | 2 | 9 | 1 | 6 | 3 |   | 5 | 8 |
| 7 | 8 | 1 | 2 | 5 | 9 | 3 | 4 | 6 |
| 6 | 4 |   | 2 | 4 | 9 |   | 1 | 5 |
| 1 | 9 | 2 | 3 | 7 | 8 | 4 | 6 | 3 |
| 5 |   |   | 6 |   |   |   | 7 |   |
| 9 | 7 |   | 3 |   | 6 |   | 2 | 4 |
| 8 | 1 | 3 |   |   | 2 | 6 | 9 | 7 |
|   |   | 4 |   |   | 7 | 5 | 3 | 1 |

---

## Comparative Performance Table

| Method       | Solved | Steps | Time (s) |
|--------------|--------|-------|----------|
| Backtracking | Yes | 35 | 0.0006 |
| AI Agent     | No | 12 | 25.7164 |
---

## Full Console Log

```bash
INFO - 📸 Loading Sudoku from: /Users/inigo/Repositorios/AISudokuSolver/inputs/easy.jpg

INFO - 

🧩 Extracted Sudoku Board:

3 . 5 | . 8 4 | 9 . 2 

. 2 9 | 1 6 3 | . 5 8 

7 8 1 | . . . | 3 4 6 

---------------------

. . . | 2 4 9 | . . . 

1 9 . | . 7 8 | 4 6 3 

5 . . | 6 . . | . 7 . 

---------------------

9 7 . | 3 . 6 | . 2 4 

8 1 3 | . . 2 | 6 9 . 

. . 4 | . . 7 | 5 3 1 



✏️  Do you want to edit any cell? (y/n): Enter cell coordinates to edit (format: row,col — example: 0,6): Enter digit to assign (1–9), or 0 to clear the cell: INFO - ✅ Cell updated successfully.

3 . 6 | . 8 4 | 9 . 2 

. 2 9 | 1 6 3 | . 5 8 

7 8 1 | . . . | 3 4 6 

---------------------

. . . | 2 4 9 | . . . 

1 9 . | . 7 8 | 4 6 3 

5 . . | 6 . . | . 7 . 

---------------------

9 7 . | 3 . 6 | . 2 4 

8 1 3 | . . 2 | 6 9 . 

. . 4 | . . 7 | 5 3 1 



✏️  Do you want to edit any cell? (y/n): Enter cell coordinates to edit (format: row,col — example: 0,6): Enter digit to assign (1–9), or 0 to clear the cell: INFO - ✅ Cell updated successfully.

3 . 6 | . 8 4 | 9 . 2 

. 2 9 | 1 6 3 | . 5 8 

7 8 1 | . . . | 3 4 6 

---------------------

. . . | 2 4 9 | . . . 

1 9 . | . 7 8 | 4 6 3 

5 . . | 6 . . | . 7 . 

---------------------

9 7 . | 3 . 6 | . 2 4 

8 1 3 | . . 2 | 6 9 7 

. . 4 | . . 7 | 5 3 1 



✏️  Do you want to edit any cell? (y/n): INFO - 

🧠 Solving with logic-based solver...

3 . 6 | . 8 4 | 9 . 2 

. 2 9 | 1 6 3 | . 5 8 

7 8 1 | . . . | 3 4 6 

---------------------

. . . | 2 4 9 | . . . 

1 9 . | . 7 8 | 4 6 3 

5 . . | 6 . . | . 7 . 

---------------------

9 7 . | 3 . 6 | . 2 4 

8 1 3 | . . 2 | 6 9 7 

. . 4 | . . 7 | 5 3 1 

INFO - 🧠 Steps taken: 35

INFO - ⏱️ Time taken: 0.0006 seconds

INFO - 

✅ Logic Solver: Puzzle solved!

3 5 6 | 7 8 4 | 9 1 2 

4 2 9 | 1 6 3 | 7 5 8 

7 8 1 | 9 2 5 | 3 4 6 

---------------------

6 3 7 | 2 4 9 | 1 8 5 

1 9 2 | 5 7 8 | 4 6 3 

5 4 8 | 6 3 1 | 2 7 9 

---------------------

9 7 5 | 3 1 6 | 8 2 4 

8 1 3 | 4 5 2 | 6 9 7 

2 6 4 | 8 9 7 | 5 3 1 

/Users/inigo/Repositorios/AISudokuSolver/solver/ai_agent_solver.py:76: LangChainDeprecationWarning: The class `ChatOpenAI` was deprecated in LangChain 0.0.10 and will be removed in 1.0. An updated version of the class exists in the :class:`~langchain-openai package and should be used instead. To use it run `pip install -U :class:`~langchain-openai` and import as `from :class:`~langchain_openai import ChatOpenAI``.

  self.llm = ChatOpenAI(model=model, temperature=temperature)

/Users/inigo/Repositorios/AISudokuSolver/solver/ai_agent_solver.py:95: LangChainDeprecationWarning: LangChain agents will continue to be supported, but it is recommended for new use cases to be built with LangGraph. LangGraph offers a more flexible and full-featured framework for building agents, including support for tool-calling, persistence of state, and human-in-the-loop workflows. For details, refer to the `LangGraph documentation <https://langchain-ai.github.io/langgraph/>`_ as well as guides for `Migrating from AgentExecutor <https://python.langchain.com/docs/how_to/migrate_agent/>`_ and LangGraph's `Pre-built ReAct agent <https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/>`_.

  self.agent = initialize_agent(

INFO - 

🤖 Solving with AI Agent...

3 . 6 . 8 4 9 . 2

. 2 9 1 6 3 . 5 8

7 8 1 . . . 3 4 6

. . . 2 4 9 . . .

1 9 . . 7 8 4 6 3

5 . . 6 . . . 7 .

9 7 . 3 . 6 . 2 4

8 1 3 . . 2 6 9 7

. . 4 . . 7 5 3 1

INFO - 

🤖 Starting agent-driven solving...



/Users/inigo/Repositorios/AISudokuSolver/solver/ai_agent_solver.py:146: LangChainDeprecationWarning: The method `Chain.run` was deprecated in langchain 0.1.0 and will be removed in 1.0. Use :meth:`~invoke` instead.

  self.agent.run({





[1m> Entering new AgentExecutor chain...[0m

[32;1m[1;3mAction:

```json

{

  "action": "ShowBoard",

  "action_input": ""

}

```[0m

Observation: [36;1m[1;3m3 . 6 . 8 4 9 . 2

. 2 9 1 6 3 . 5 8

7 8 1 . . . 3 4 6

. . . 2 4 9 . . .

1 9 . . 7 8 4 6 3

5 . . 6 . . . 7 .

9 7 . 3 . 6 . 2 4

8 1 3 . . 2 6 9 7

. . 4 . . 7 5 3 1[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "ShowBoard",

  "action_input": ""

}

```

[0m

Observation: [36;1m[1;3m3 . 6 . 8 4 9 . 2

. 2 9 1 6 3 . 5 8

7 8 1 . . . 3 4 6

. . . 2 4 9 . . .

1 9 . . 7 8 4 6 3

5 . . 6 . . . 7 .

9 7 . 3 . 6 . 2 4

8 1 3 . . 2 6 9 7

. . 4 . . 7 5 3 1[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "ShowBoard",

  "action_input": ""

}

```

[0m

Observation: [36;1m[1;3m3 . 6 . 8 4 9 . 2

. 2 9 1 6 3 . 5 8

7 8 1 . . . 3 4 6

. . . 2 4 9 . . .

1 9 . . 7 8 4 6 3

5 . . 6 . . . 7 .

9 7 . 3 . 6 . 2 4

8 1 3 . . 2 6 9 7

. . 4 . . 7 5 3 1[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "0,1,5"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 5 at (0,1)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "0,3,7"

}

```

[0m

Observation: [33;1m[1;3m✅ Placed 7 at (0,3)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "0,7,1"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 1 at (0,7)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "2,3,2"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 2 at (2,3)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "2,4,5"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 5 at (2,4)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "2,5,9"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 9 at (2,5)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "3,0,6"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 6 at (3,0)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "3,1,4"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 4 at (3,1)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "3,7,1"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 1 at (3,7)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "3,8,5"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 5 at (3,8)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "4,2,2"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 2 at (4,2)[0m

Thought:[32;1m[1;3mAction:

```json

{

  "action": "PlaceValue",

  "action_input": "4,3,3"

}

```[0m

Observation: [33;1m[1;3m✅ Placed 3 at (4,3)[0m

Thought:[32;1m[1;3m[0m



[1m> Finished chain.[0m

INFO - 

✅ Agent finished after 12 steps.

INFO - ⏱️ Time taken: 25.7164 seconds

INFO - 

🧾 Final board by AI Agent:



3 5 6 | 7 8 4 | 9 1 2 

. 2 9 | 1 6 3 | . 5 8 

7 8 1 | 2 5 9 | 3 4 6 

---------------------

6 4 . | 2 4 9 | . 1 5 

1 9 2 | 3 7 8 | 4 6 3 

5 . . | 6 . . | . 7 . 

---------------------

9 7 . | 3 . 6 | . 2 4 

8 1 3 | . . 2 | 6 9 7 

. . 4 | . . 7 | 5 3 1 

```