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
#                                  AGENT CLASS DEFINITION                                        #
##################################################################################################

class SudokuSolverAgent:

    def __init__(self, board: List[List[int]], model: str = "gpt-4-turbo", temperature: float = 0):
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("❌ OPENAI_API_KEY not found in .env file.")

        self.board = board
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
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
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

    def solve_step_by_step(self):
        logger.info("\n🤖 Starting agent-driven solving...\n")
        instruction = """You are a Sudoku-solving agent.
        Use the available tools to view the board and apply moves step-by-step.
        Repeat this until the puzzle is solved or you cannot proceed.
        Print only your thoughts and tools usage as you go.
        """

        start = time.perf_counter()
        self.agent.run(instruction)
        end = time.perf_counter()

        self.time_taken = round(end - start, 4)
        logger.info(f"\n✅ Agent finished after {self.steps} steps.")
        logger.info(f"⏱️ Time taken: {self.time_taken:.4f} seconds")

    def is_solved(self) -> bool:
        return all(all(cell != 0 for cell in row) for row in self.board)

