##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module defines a LangChain-powered agent that solves a Sudoku puzzle step-by-step.        #
# It uses tools (functions) to view and update the board and reasons through each move           #
# using a GPT-4-based LLM.                                                                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import time
from typing import List
from dotenv import load_dotenv
from utils.logs_config import logger

from langchain.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOpenAI

##################################################################################################
#                                   CONFIGURABLE PARAMETERS                                     #
##################################################################################################

# AI agent model and strategy (used elsewhere in the app)
AGENT_MODEL = "gpt-4-turbo"
AGENT_TYPE = "structured-chat-zero-shot-react-description"

# Prompt used by AI Agent
AGENT_PROMPT = """
You are an expert Sudoku-solving agent.

You must solve the Sudoku grid completely by filling in all empty cells (represented by '.').

Here you have the official rules of Sudoku you MUST follow:

- The puzzle is a 9x9 grid, divided into nine 3x3 boxes.
- Each row must contain all digits from 1 to 9 with no repetition.
- Each column must contain all digits from 1 to 9 with no repetition.
- Each 3x3 box must contain all digits from 1 to 9 with no repetition.

You have access to the following tools:
- ShowBoard → to view the current board.
- PlaceValue → to fill a cell. Input: row,col,value (0-based index).
- RemoveValue → to remove a value you previously placed.

You can use logic or trial-and-error strategies. 
If you place a wrong value, use RemoveValue to undo it.

IMPORTANT:
- Do NOT stop early. Continue until the board is fully filled.
- Do NOT repeat ShowBoard without doing something.
- Make at least 5 attempts before stopping.
- Only print your internal thoughts and tool usage.

Start solving the puzzle now.
"""

##################################################################################################
#                                  AGENT CLASS DEFINITION                                        #
##################################################################################################

class SudokuSolverAgent:

    def __init__(self, board: List[List[int]], model: str = AGENT_MODEL, temperature: float = 0):
        load_dotenv()

        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("❌ OPENAI_API_KEY not found in .env file.")

        self.board = board
        self.original_board = [row.copy() for row in board]
        self.steps = 0

        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.tools = [
            Tool(
                name="ShowBoard",
                func=lambda _: self.format_board(),
                description="Displays the current Sudoku board."
            ),
            Tool(
                name="PlaceValue",
                func=self.place_value,
                description="Places a digit on the board. Input: row,col,value (e.g., 2,4,9)"
            ),
            Tool(
                name="RemoveValue",
                func=self.remove_value,
                description="Removes a value placed by the agent. Input: row,col (e.g., 2,4)"
            )
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AGENT_TYPE,
            #agent="conversational-react-description",
            verbose=True,
            handle_parsing_errors=True
        )

    def format_board(self) -> str:
        lines = []
        for row in self.board:
            line = " ".join(str(cell) if cell != 0 else "." for cell in row)
            lines.append(line)
        return "\n".join(lines)

    def place_value(self, input_str: str) -> str:
        try:
            row, col, val = map(int, input_str.strip().split(","))
            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= val <= 9):
                return "Invalid input: values out of range."
            self.board[row][col] = val
            self.steps += 1
            return f"✅ Placed {val} at ({row},{col})"
        except Exception as e:
            return f"❌ Failed to parse move: {e}"

    def remove_value(self, input_str: str) -> str:
        try:
            row, col = map(int, input_str.strip().split(","))
            if not (0 <= row < 9 and 0 <= col < 9):
                return "Invalid coordinates."
            if self.original_board[row][col] != 0:
                return "Cannot remove original board values."
            self.board[row][col] = 0
            return f"❌ Removed value at ({row},{col})"
        except Exception as e:
            return f"❌ Failed to parse removal: {e}"

    def solve_step_by_step(self):
        logger.info("\n🤖 Starting agent-driven solving...\n")
        instruction = """You are a Sudoku-solving agent.
        Use the available tools to view the board and apply moves step-by-step.
        Repeat this until the puzzle is solved or you cannot proceed.
        Print only your thoughts and tools usage as you go.
        """

        instruction = AGENT_PROMPT

        start = time.perf_counter()
        #self.agent.run(instruction)
        self.agent.run({
            "input": instruction,
            "chat_history": []
        })

        end = time.perf_counter()

        self.time_taken = round(end - start, 4)
        logger.info(f"\n✅ Agent finished after {self.steps} steps.")
        logger.info(f"⏱️ Time taken: {self.time_taken:.4f} seconds")

    def is_solved(self) -> bool:
        return all(all(cell != 0 for cell in row) for row in self.board)

