import gradio as gr
from dotenv import load_dotenv
from agents import Runner
from pydantic import BaseModel
from datacrew_agents.analysis_scoping import (
    analysis_scoping_agent,
    AnalysisScope,
)

from datacrew_agents.data_prep import (
    data_preparation_agent,
    desktop_commander,
    DataPreparationResult,
)

from datacrew_agents.analysis_report import (
    analysis_report_agent,
    AnalysisReportResult,
)


load_dotenv()


class DataCrewState(BaseModel):
    analysis_scope: AnalysisScope | None = None
    preparation_result: DataPreparationResult | None = None
    analysis_result: AnalysisReportResult | None = None


async def run_workflow(business_problem, analysis_goal, state):

    # ------------------------------
    # 1. Analysis Scoping Agent
    # ------------------------------

    user_input = f"""
Business Problem:
{business_problem}

Analysis Goal:
{analysis_goal}
"""

    scope_result = await Runner.run(
        analysis_scoping_agent,
        user_input
    )

    state.analysis_scope = scope_result.final_output


    # ------------------------------
    # 2. Data Preparation Agent
    # ------------------------------

    preparation_input = f"""
Analysis Scope:

{state.analysis_scope.model_dump_json(indent=2)}

Use this analysis scope to prepare the available data.
"""


    # Desktop Commander is required by both
    # the Preparation and Analysis agents
    async with desktop_commander:

        preparation_result = await Runner.run(
            data_preparation_agent,
            preparation_input,
            max_turns=30
        )

        state.preparation_result = preparation_result.final_output


        # ------------------------------
        # 3. Data Analysis & Reporting Agent
        # ------------------------------

        analysis_input = f"""
Analysis Scope:

{state.analysis_scope.model_dump_json(indent=2)}

Data Preparation Result:

{state.preparation_result.model_dump_json(indent=2)}

Use the analysis scope and the prepared data information
to perform the data analysis and generate the final PowerPoint report.
"""

        analysis_result = await Runner.run(
            analysis_report_agent,
            analysis_input,
            max_turns=40
        )

        state.analysis_result = analysis_result.final_output


    return (
        state,
        state.analysis_scope.model_dump_json(indent=2),
        state.preparation_result.model_dump_json(indent=2),
        state.analysis_result.model_dump_json(indent=2),
    )


with gr.Blocks(title="DataCrew") as demo:

    state = gr.State(DataCrewState())

    gr.Markdown("# DataCrew")
    gr.Markdown("AI Multi-Agent Data Analysis System")

    business_problem = gr.Textbox(
        label="Business Problem",
        placeholder="Describe the business problem you want to investigate...",
        lines=4
    )

    analysis_goal = gr.Textbox(
        label="Analysis Goal",
        placeholder="Describe what you want the analysis to achieve...",
        lines=4
    )

    submit_button = gr.Button("Start Analysis")


    scope_output = gr.Code(
        label="Analysis Scope",
        language="json"
    )

    preparation_output = gr.Code(
        label="Data Preparation Result",
        language="json"
    )

    analysis_output = gr.Code(
        label="Analysis & Reporting Result",
        language="json"
    )


    submit_button.click(
        fn=run_workflow,
        inputs=[
            business_problem,
            analysis_goal,
            state
        ],
        outputs=[
            state,
            scope_output,
            preparation_output,
            analysis_output
        ]
    )


if __name__ == "__main__":
    demo.launch()