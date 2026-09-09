from agents import Agent
from agents.mcp import MCPServerStdio
from pydantic import BaseModel, Field


DATA_ROOT = r"C:\Users\user\Desktop\UNI\PROJECTS\DataCrew\github\DataCrew\DATA"


class DataPreparationResult(BaseModel):

    data_overview: str = Field(
        description="A concise overview of the raw datasets discovered and inspected."
    )

    preparation_actions: list[str] = Field(
        description="The cleaning, transformation, integration, or restructuring actions performed on the data."
    )

    prepared_data_description: str = Field(
        description=(
            "A concise description of the cleaned and analysis-ready data "
            "available in the Cleaned_DATA directory, including the main "
            "datasets, their structure, and the information relevant to "
            "the next analysis phase."
        )
    )


desktop_commander = MCPServerStdio(
    name="Desktop Commander",
    params={
        "command": "npx",
        "args": [
            "-y",
            "@wonderwhy-er/desktop-commander@0.2.47"
        ],
    },
    cache_tools_list=True
)


DATA_PREPARATION_INSTRUCTIONS = f"""
You are the Data Preparation Agent of DataCrew.

Your role is to perform the Prepare and Process phases
of the data analysis workflow.

All raw data is located inside:

{DATA_ROOT}

You will also receive the analysis scope produced by the
Analysis Scoping Agent. Use the business problem, analysis goal,
and key analytical questions to guide your preparation work.

Your tasks are to:

1. Inspect the DATA directory and its subdirectories.
2. Locate and read the available data dictionary, README,
   metadata file, or similar documentation.
3. Inspect the relevant datasets.
4. Understand their structure, fields, types, relationships,
   and data quality.
5. Perform all necessary data preparation using Python and pandas,
   including cleaning, type conversion, missing-value handling,
   duplicate handling, filtering, joins, transformations,
   restructuring, or other required processing.
6. Create a Cleaned_DATA directory inside DATA if it does not exist.
7. Save only the cleaned and analysis-ready datasets inside Cleaned_DATA.
8. Return a concise description of the raw data found,
   the preparation work performed, and the final cleaned data.

Do not perform business analysis.
Do not generate insights, visualizations, or recommendations.
"""


data_preparation_agent = Agent(
    name="Data Preparation Agent",
    instructions=DATA_PREPARATION_INSTRUCTIONS,
    model="gpt-5.6-luna",
    output_type=DataPreparationResult,
    mcp_servers=[desktop_commander],
)