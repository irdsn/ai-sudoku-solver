# Sudoku Solver Report

**Solved at:** 2025-06-18 17:11:53

---

## Solution Overview

LLM summary for the Sudoku puzzle.

---

## Input Image

Original image used to extract the Sudoku board.

<img src="sudoku_input_input.png" alt="Sudoku Input" width="400"/>

---

## Parsed Board (Extracted from Image)

Board generated automatically via OCR and grid detection.

| 5 | 3 |   |   | 7 |   |   |   |   |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |
| 5 | 3 |   |   | 7 |   |   |   |   |

---

## Final Solved Board (Backtracking)

Completed Sudoku board after applying the backtracking algorithm.

| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |
| 5 | 3 | 4 | 6 | 7 | 8 | 9 | 1 | 2 |

---

## Backtracking Performance

Summary of solver performance, including total steps and execution time.

| Solved | Steps | Time (s) |
|--------|-------|----------|
| Yes | 42 | 1.2345 |