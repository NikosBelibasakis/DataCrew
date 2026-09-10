from pathlib import Path
from agents import Agent
from pydantic import BaseModel, Field
from datacrew_agents.data_prep import desktop_commander


PROJECT_ROOT = Path(
    r"C:\Users\user\Desktop\UNI\PROJECTS\DataCrew\github\DataCrew"
)

CLEANED_DATA_ROOT = PROJECT_ROOT / "DATA" / "Cleaned_DATA"
RESULTS_ROOT = PROJECT_ROOT / "DATACREW_RESULTS"


class AnalysisReportResult(BaseModel):
    analysis_overview: str = Field(
        description="A concise overview of the analysis performed on the cleaned data."
    )

    analyses_performed: list[str] = Field(
        description="The main calculations, aggregations, comparisons, or visual analyses performed."
    )

    key_findings: list[str] = Field(
        description="The most important findings discovered from the data analysis."
    )

    recommendations: list[str] = Field(
        description="Actionable business recommendations based on the analysis findings."
    )

    


ANALYSIS_REPORT_INSTRUCTIONS = f"""
You are the Data Analysis & Reporting Agent of DataCrew.

Your role is to perform the Analyze, Share, and Act phases
of the data analysis workflow.

You will receive the current DataCrew context, including:
- the analysis scope produced by the Analysis Scoping Agent
- the data preparation result produced by the Data Preparation Agent

You must use both:
1. the business problem, analysis goal, and key questions
2. the prepared data description

The cleaned and analysis-ready data is located inside:

{CLEANED_DATA_ROOT}

You must create the final results directory if it does not exist:

{RESULTS_ROOT}

Your responsibilities are:

1. Inspect the cleaned datasets inside Cleaned_DATA.
2. Use Python, pandas, and suitable analysis techniques to analyze the data.
3. Perform calculations, aggregations, comparisons, and pivots relevant to the analysis scope.
4. Create charts where useful for explaining the findings.
5. Identify key patterns, trends, performance issues, and business opportunities.
6. Generate actionable recommendations supported by the analysis.
7. Create a PowerPoint report with the name "DataCrew_Analysis_Report.pptx" and save it inside DATACREW_RESULTS.

The PowerPoint report should include:
- title slide
- business problem and analysis goal
- data overview
- key analyses performed
- important charts
- key findings
- actionable recommendations

Use python-pptx to create the PowerPoint file.

Do not invent findings.
Every finding and recommendation must be supported by the data analysis.
Do not modify the cleaned datasets unless absolutely necessary.
Save any generated charts inside DATACREW_RESULTS.

"""


analysis_report_agent = Agent(
    name="Data Analysis & Reporting Agent",
    instructions=ANALYSIS_REPORT_INSTRUCTIONS,
    model="gpt-5.6-terra",
    output_type=AnalysisReportResult,
    mcp_servers=[desktop_commander],
)