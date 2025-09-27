from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    first_number: int
    second_number: int
    initial_operation: str
    addition_result: int
    subtraction_result: int
    third_number: int
    final_operation: str
    final_result: int
    
def add(state: AgentState) -> AgentState:
    """This node performs addition operation"""
    
    state['addition_result'] = state['first_number'] + state['second_number']
    return state

def subtract(state: AgentState) -> AgentState:
    """This node performs subtraction operation"""
    
    state['subtraction_result'] = state['first_number'] - state['second_number']
    return state

def multiply(state: AgentState) -> AgentState:
    """This node performs multiplication operation"""
    
    state['final_result'] = state['addition_result'] * state['third_number']
    return state

def divide(state: AgentState) -> AgentState:
    """This node performs division operation"""
    
    state['final_result'] = state['subtraction_result'] / state['third_number']
    return state

def decide_initial_path(state: AgentState) -> AgentState:
    """This node decides the initial path of the graph"""
    
    if state['initial_operation'] == "+":
        return "addition_operation"
    elif state['initial_operation'] == "-":
        return "subtraction_operation"
    
def decide_final_path(state: AgentState) -> AgentState:
    """This node decides the final path of the graph"""
    
    if state['final_operation'] == "*":
        return "multiplication_operation"
    elif state['final_operation'] == "/":
        return "division_operation"
    
graph = StateGraph(AgentState)

graph.add_node("add_nodes", add)
graph.add_node("subtract_nodes", subtract)
graph.add_node("multiply_nodes", multiply)
graph.add_node("divide_nodes", divide)
graph.add_node("initial_router", lambda state:state)
graph.add_node("final_router", lambda state:state)

graph.add_edge(START, "initial_router")

graph.add_conditional_edges(
    "initial_router",
    decide_initial_path,
    {
        "addition_operation": "add_nodes",
        "subtraction_operation": "subtract_nodes"
    }
)

graph.add_edge("add_nodes", "final_router")
graph.add_edge("subtract_nodes", "final_router")

graph.add_conditional_edges(
    "final_router",
    decide_final_path,
    {
        "multiplication_operation": "multiply_nodes",
        "division_operation": "divide_nodes"
    }
)

graph.add_edge("multiply_nodes", END)
graph.add_edge("divide_nodes", END)

app = graph.compile()

print(app.get_graph().print_ascii())

initial_state = AgentState(
    first_number = 20,
    second_number = 10,
    initial_operation = "+",
    third_number = 5,
    final_operation = "*"
)

result = app.invoke(initial_state)