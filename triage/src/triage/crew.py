from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from triage.tools.exception_tools import summarize_stack_trace
from triage.tools.log_parser import extract_errors
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Triage():
    """Triage crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def bug_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['bug_classifier'], # type: ignore[index]
            tools=[extract_errors, summarize_stack_trace],
            verbose=True
        )

    @agent
    def severity_assessor(self) -> Agent:
        return Agent(
            config=self.agents_config['severity_assessor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def owner_router(self) -> Agent:
        return Agent(
            config=self.agents_config['owner_router'], # type: ignore[index]
            verbose=True
        )

    @agent
    def triage_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['triage_summarizer'], # type: ignore[index]
            verbose=True
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task


    @task
    def classify_defect(self) -> Task:
        return Task(
            config=self.tasks_config['classify_defect'], # type: ignore[index]
        )

    @task
    def assign_severity(self) -> Task:
        return Task(
            config=self.tasks_config['assign_severity'], # type: ignore[index]
        )

    @task
    def route_to_owner(self) -> Task:
        return Task(
            config=self.tasks_config['route_to_owner'], # type: ignore[index]
        )

    @task
    def summarize_triage(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_triage'], # type: ignore[index]
        )



    @crew
    def crew(self) -> Crew:
        """Creates the Triage crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
