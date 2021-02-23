from lib.pysoarlib import *
import os


curdir = os.path.dirname(os.path.realpath(__file__))


rule_agent = SoarAgent(
    agent_name="hello world",
    write_to_stdout=True,
    spawn_debugger=False,
    agent_source=curdir + "/1_hello_world.soar",
    # How much detail to print when sourcing files: none, summary, or full
    # source_output="summary",
)
# Add a connector to see the stdout from the agent
rule_agent.add_connector("simple", AgentConnector(rule_agent))
rule_agent.connect()
rule_agent.execute_command("run")
rule_agent.kill()

print("\n\n3.2:: Running hello world operator...")

# this time, load in from a config file. it populates the fields
# 'write_to_stdout' for us
operator_agent = SoarAgent(
    agent_source="1_hello_world_operator.soar",
    config_filename='default.config',
    root_dir=curdir,
)
operator_agent.add_connector("hw-operator", AgentConnector(operator_agent))
operator_agent.connect()
operator_agent.execute_command("run")
# view all attributes and values that have s1 as their identifier
operator_agent.execute_command("print s1", print_res=True)

print("""
The attributes ^io, ^superstate, and ^type are created automatically before the program runs.
The 'operator' attribute is created when the hello-world operator (o1) is selected.
""")

# Depth of 2
operator_agent.execute_command("print s1 -d 2", print_res=True)

# print can be abbrevated to p
print("""
View the augmentation of o1...
""")
operator_agent.execute_command("p o1", print_res=True)

print("""
View the augmentation of I1...
  There are two attributes: ^input-link and ^output-link
  input-link: where an agent's sensory information is available in WM
  output-link: where action commands must be created for the agent to move in its world
""")
operator_agent.execute_command("p I1", print_res=True)

operator_agent.kill()
