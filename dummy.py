from langchain.agents import create_agent
from langchain_groq import ChatGroq

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"It's always sunny in {city}!"

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response["messages"][-1].content)

