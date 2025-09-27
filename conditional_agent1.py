from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int
    
def adder(state:  AgentState) -> AgentState:
    """This node adds this two numbers"""
    
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """This node subtracts the two numbers"""
    
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> AgentState:
    """This node will select the next node of the graph"""
    
    if state['operation'] == "+":
        return "addition_operation"
    elif state['operation'] == "-":
        return "subtraction_operation"
    
graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("router", lambda state:state) # pass through function

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        # Edge name : Node name
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

app = graph.compile()

print(app.get_graph().print_ascii())

initial_state_1 = AgentState(number1=10, operation="+", number2=5)
initial_state_2 = AgentState(number1=10, operation="-", number2=5)
result_1 = app.invoke(initial_state_1)
result_2 = app.invoke(initial_state_2)
print(f"Addition Result: {result_1['finalNumber']}, Subtraction Result: {result_2['finalNumber']}")