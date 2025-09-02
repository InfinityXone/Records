from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def load_promptwriter():
    llm = ChatOpenAI(temperature=0.7, model="gpt-4")

    tools = []  # Add tools here if needed

    # System prompt must include agent_scratchpad
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are PromptWriter, the autonomous cognitive architect inside the Infinity X One multi-agent system. You reason, build, and orchestrate new agents with precision."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}")
    ])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

