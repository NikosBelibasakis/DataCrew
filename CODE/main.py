import gradio as gr
from dotenv import load_dotenv
from agents import Runner
from datacrew_agents.analysis_scoping import analysis_scoping_agent

load_dotenv()


def create_analysis_scope(business_problem, analysis_goal):

    user_input = f"""
Business Problem:
{business_problem}

Analysis Goal:
{analysis_goal}
"""

    result = Runner.run_sync(
        analysis_scoping_agent,
        user_input
    )

    scope = result.final_output

    return scope.model_dump_json(indent=2)


with gr.Blocks(title="DataCrew") as demo:
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

    submit_button = gr.Button("Create Analysis Scope")

    output = gr.Code(
        label="Analysis Scope",
        language="json"
    )

    submit_button.click(
        fn=create_analysis_scope,
        inputs=[business_problem, analysis_goal],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch()