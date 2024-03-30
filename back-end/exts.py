# ========== constants ==========
WEBSITE_URL = "https://www.partselect.com/"

MATCH_NUM_FROM_DB = 3
SIMILARITY_THRESHOLD = 0.6

CHATBOT_ERROR = "Sorry I could not find relevant information."
# ========== system paths ==========
CHROMA_PATH = "./chromadb"
SESSION_PATH = "./session_data"

# Session config
SESSION_TYPE = "filesystem"
SESSION_DURA = 20


# ========== prompts ========
# PREFIX = """
# Have a conversation with a human, answering the following questions as best you can.
# You have access to the following tools:"""
#
# SUFFIX = """Begin!"
# {chat_history}
# Question: {input}
# {agent_scratchpad}"""

# add memory to chatbots
INSTRUCTIONS_TO_SYSTEM = """
Given a chat history and the latest user question
which might reference context in the chat history, formulate a standalone question.
This question should be understood without history. DO NOT answer the question,
just reformulate it if needed and otherwise return it as is.
"""

QA_SYSTEM_PROMPT = """
You are an website customer service assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, provide a summary of the context. DO NOT generate your answer.


{context}
"""
