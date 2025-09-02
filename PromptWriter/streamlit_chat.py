import streamlit as st, json
from agents.promptwriter_agent import load_promptwriter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

st.title("∞ Infinity X One Chat")

pwd = "/opt/infinity_x_one/PromptWriter"
agent = load_promptwriter()
memory = Chroma(
    persist_directory=f"{pwd}/runtime/chroma",
    embedding_function=OpenAIEmbeddings(),
    collection_name="pw_memory"
)

history = ""

if st.button("Load Memory"):
    docs = memory.get(**{"k":3})  # approximate
    st.write(docs)

inp = st.text_input("You:")
if inp:
    st.write(f"You: {inp}")
    resp = agent.run(inp)
    st.write(f"PromptWriter: {resp}")
    memory.add_documents([{"page_content": inp + "\n" + resp}])
