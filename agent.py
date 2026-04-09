import os
import logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- Setup Logging and Environment ---

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_name = os.getenv("MODEL", "gemini-2.0-flash")


# --- Tool: Save user's input text to agent state ---

def save_text_to_state(
    tool_context: ToolContext, text: str
) -> dict[str, str]:
    """
    Saves the user's submitted text into agent state so
    downstream agents in the workflow can access it.

    Args:
        text: The raw text provided by the user for summarization.

    Returns:
        A status dict indicating success.
    """
    tool_context.state["INPUT_TEXT"] = text
    logger.info(f"[State updated] Saved INPUT_TEXT ({len(text)} chars)")
    return {"status": "success"}


# --- Agent 1: Summarizer ---
# Reads the raw text from state and produces a concise summary.

summarizer_agent = Agent(
    name="summarizer",
    model=model_name,
    description="Reads the user's raw text and produces a concise, accurate summary.",
    instruction="""
    You are an expert text summarizer. Your job is to read the INPUT_TEXT below
    and produce a clear, concise summary.

    Rules:
    - Capture the key points and main ideas.
    - Keep the summary to 3-5 sentences unless the text is very short.
    - Do not add any information that is not in the original text.
    - Write in plain, easy-to-understand language.

    INPUT_TEXT:
    { INPUT_TEXT }
    """,
    output_key="summary_draft",
)


# --- Agent 2: Quality Checker ---
# Reviews the draft summary for clarity and completeness.

quality_checker_agent = Agent(
    name="quality_checker",
    model=model_name,
    description="Reviews the draft summary and refines it into a final polished response.",
    instruction="""
    You are a quality assurance editor. You receive a draft summary and your task is to:

    1. Check that the summary is clear and well-written.
    2. Fix any grammar or awkward phrasing.
    3. Ensure it reads naturally as a standalone paragraph.
    4. Add a short label at the top: **Summary:** before the text.

    Output ONLY the final polished summary (with the label). Nothing else.

    DRAFT SUMMARY:
    { summary_draft }
    """,
)


# --- Workflow: Sequential pipeline ---

summarizer_workflow = SequentialAgent(
    name="summarizer_workflow",
    description="Runs the summarization pipeline: first summarizes, then quality-checks.",
    sub_agents=[
        summarizer_agent,       # Step 1: Generate summary
        quality_checker_agent,  # Step 2: Polish and format
    ],
)


# --- Root Agent: Entry point ---
# Greets the user, collects their text, then hands off to the workflow.

root_agent = Agent(
    name="text_summarizer_bot",
    model=model_name,
    description="An AI agent that accepts any text and returns a clean, concise summary.",
    instruction="""
    You are a friendly Text Summarizer Bot.

    When the conversation starts, greet the user with:
    "Hello! I'm your Text Summarizer. Paste any text — an article, email, report,
    or any passage — and I'll give you a clear, concise summary."

    When the user provides text:
    - Use the 'save_text_to_state' tool to save their text.
    - After saving, immediately transfer control to the 'summarizer_workflow' agent.

    Do not attempt to summarize the text yourself.
    """,
    tools=[save_text_to_state],
    sub_agents=[summarizer_workflow],
)