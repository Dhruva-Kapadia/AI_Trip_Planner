from utils.model_loader import ModelLoader

# from tools.weather_info_tool import WeatherInfoTool
# from tools.place_search_tool import PlaceSearchTool
# from tools.currency_conversion_tool import CurrencyConverterTool
# from tools.expense_calculator_tool import ExpenseCalculatorTool

from prompt_library.prompt import SYSTEM_PROMPT

from langgraph.graph import Stategraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        llm = ModelLoader(model_provider=model_provider).load_llm()
        self.tools = [
            # WeatherInfoTool(),
            # PlaceSearchTool(),
            # CurrencyConverterTool(),
            # ExpenseCalculatorTool()
        ]
        self.system_prompt = SYSTEM_PROMPT
        self.llm_with_tools = llm.bind_tools(self.tools)

    def agent_function(self, state:MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return{"messages": [response]}

    def build_graph(self):
        graph_builder=Stategraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edge("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        graph_builder.compile()
        return graph_builder


    def __call__(self):
        return self.build_graph()