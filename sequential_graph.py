from typing import TypedDict
from langgraph.graph import StateGraph

from IPython.display import Image, display

class AgentState(TypedDict):
    name: str
    age: str
    skills: list[str]
    final: str
    
def first_node(state: AgentState) -> AgentState:
    """This is the first node of our sequence"""
    
    state['final'] = f"Hi {state['name']}! "
    return state

def second_node(state: AgentState) -> AgentState:
    """This is the second node of our sequence"""
    
    state['final'] = state['final'] + f"You are {state['age']} years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """This is the third node of our sequence"""
    
    state['final'] = state['final'] + f" Your skills are as follows: {', '.join(state['skills'])}"
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

# display(Image(app.get_graph().draw_mermaid_png()))
# display(Image(app.get_graph().draw_mermaid_png(
#     max_retries=5,
#     retry_delay=2.0
# )))

print(app.get_graph().print_ascii())

result = app.invoke({"name": "Darshil", "age": "23", "skills": ["Python", "JavaScript", "C++"]})
print(result)