import warnings, os
import crewai
from IPython.display import Markdown


from crewai_tools import EXASearchTool, ScrapeWebsiteTool
import utils import get_exa_api_key

os.environ["EXA_API_KEY"] = get_exa_api_key()

### START CODE HERE ###

# Create the EXASearchTool instance
exa_search_tool = None(base_url=os.getenv("EXA_BASE_URL"))
# Create the ScrapeWebsiteTool instance
scrape_website_tool = None()

# define the research planner agent
research_planner = crewai.Agent(
    role="Research Planner",
    goal="Analyze queries and break them down into smaller, specific research topics.",
    backstory=(
         "You are a research strategist who excels at breaking down complex questions "
         "into manageable research components. You identify what needs to be researched "
         "and create clear research objectives."
    ),
    verbose=True, # set to True to see detailed agent actions
    max_rpm=150,
    max_iter=15
)

researcher = crewai.Agent(
    role="Internet Researcher",
    goal="Research thoroughly all assigned topics",
    ### START CODE HERE ###
    backstory=(
        "You are an Internet Researcher who excels in searching a topic from the internet thoroughly "
    ),
    # add the 2 tool instances you created
    tools=[None, None],
    ### END CODE HERE ###
    verbose=True,
    max_rpm=150,
    max_iter=15
)

fact_checker = crewai.Agent(
    role="Fact Checker",
    goal=(
        "Verify data for accuracy, identify inconsistencies, "
        "and flag potential misinformation"
    ),
    ### START CODE HERE ###
    backstory=(
        "You are a Fact Checker and excels in verifying the data for accuracy and identifying inconsistencies",
        "The data you are verifying must be flagged for any potential misinformation"
    ),
    tools=[None, None],
    ### END CODE HERE ###
    verbose=True,
    max_rpm=150,
    max_iter=15
)

report_writer = crewai.Agent(
    role="Report Writer",
    goal="Write clear, concise, and well-structured reports based on gathered information",
    ### START CODE HERE ###
    backstory=(
        "You are a Report Writer who excels in writing reports in a professional way",
        "You are following the standard rules of professional writing and have the ability to format the data in different shapes including tables"
    ),
    ### END CODE HERE ###
    verbose=True, max_rpm=150,
    max_iter=15
)

# define the create research plan task
create_research_plan_task = crewai.Task(
    description=(
        "Based on the user's query, break it down into specific topics and key questions, "
        "and create a focused research plan."
        "The user's query is: {user_query}"
    ),
    expected_output=(
        "A research plan with main research topics to investigate, "
        "key questions for each topic, and success criteria for the research."
        ),
    agent=research_planner,
)

# define the gather research data task
gather_research_data_task = crewai.Task(
    description=(
        "Using the research plan, collect information on all identified topics. "
        "Cite all sources used."
    ),
    ### START CODE HERE ###
    expected_output=(
        "Based on the research plan, prepare the information collected on all identified topics ",
        "Organize the information collected on all identified topics along the way with citations."
    ),
    agent=researcher
    ### END CODE HERE ###
)

# define the verify information quality task
verify_information_quality_task = crewai.Task(
    description=(
        "Review all collected research. Identify any conflicting information, "
        "potential misinformation, or gaps that need addressing."
    ),
    ### START CODE HERE ###
    expected_output=(
        "Review all collected research. Identify any conflicting information, "
        "potential misinformation, or gaps that need addressing."
    ),
    agent=fact_checker
    ### END CODE HERE ###
)

# define the write final report task
write_final_report_task = crewai.Task(
    description=(
        "Create a comprehensive report that answers the original query using all verified research data. "
        "Structure it with clear sections, include citations, and provide actionable insights."
    ),
    ### START CODE HERE ###
    expected_output=(
        "Create a comprehensive report that answers the original query using all verified research data. "
        "Structure it with clear sections, include citations, and provide actionable insights."
    ),
    agent=report_writer
    ### END CODE HERE ###
)

# create the crew with the defined agents and tasks
crew = crewai.Crew(
    ### START CODE HERE ###
    agents=[research_planner, researcher, fact_checker, report_writer],
    tasks=[create_research_plan_task, gather_research_data_task, verify_information_quality_task, write_final_report_task]
    ###
)

# Write your query, which will be used as input for the tasks.
user_query = ""

result = crew.kickoff(
    inputs={
        "user_query": user_query,
    }
)

Markdown(result.raw)

### END CODE HERE ###