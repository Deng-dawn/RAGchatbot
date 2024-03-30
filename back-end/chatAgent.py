from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
import exts
import os

from dotenv import load_dotenv

load_dotenv(".env")
# todo: handle None value when necessary
OPENAI_API_KEY = os.getenv("openai_api_key")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


def extract_vector_store(user_query):
    """
    Load saved chroma vector store from disk.
    Retrieve best matched k results from user query.

    Improvement: May utilize similarity search result for new prompt,
    to provide additional information before querying large language model.
    Here is used for early stopping.

    :param user_query: str
    :return: None if below threshold, else the db
    """
    # load from disk
    embedding_function = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=exts.CHROMA_PATH, embedding_function=embedding_function)

    results = vectordb.similarity_search_with_relevance_scores(user_query, k=exts.MATCH_NUM_FROM_DB)

    # Early stopping
    if len(results) == 0 or results[0][1] < exts.SIMILARITY_THRESHOLD:
        print("Extract DB: Unable to find the relevant result")
        return
    return vectordb


def generate_query_maker_prompt(user_query):
    """
    Prompt to combine the user query and the chat history
    to generate a new user query.

    :param user_query: str
    :return:
    """
    query_maker_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", exts.INSTRUCTIONS_TO_SYSTEM),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", user_query)
        ]
    )
    return query_maker_prompt


def generate_contextualized_question(info: dict):
    """
    If the chat history exists in session, return question chain.
    Otherwise, only take the user query as context.

    :param info: {"chat_history":,"user_query":xxx, "model":llm}
    :return:
    """
    if info.get("chat_history"):
        question_maker_prompt = generate_query_maker_prompt(info.get("user_query"))
        print("Contextualized: Generate new question -> Prompt completed!")

        question_chain = question_maker_prompt | info.get("model") | StrOutputParser()
        print("Contextualized: Generate new question -> Chain completed!")

        # generated_question_for_new_query = question_chain.invoke({"chat_history": info.get("chat_history"),
        #                                      "user_query": "tell me more about it"})
        return question_chain

    print("Contextualized: Use user query, no chat history exists")
    return info.get("user_query")


def create_chatbot_agent(chat_info, vectordb):
    # chat completion llm
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.5,
        openai_api_key=OPENAI_API_KEY
    )
    print("ChatBot Agent: Chat with OpenAI LLM model created.")

    user_query = chat_info.get("user_query")
    if not user_query:
        user_query = "Hi"

    # output_parser = StrOutputParser()
    retriever = vectordb.as_retriever()
    retriever_chain = RunnablePassthrough.assign(context=generate_contextualized_question | retriever)
    # retriever_result = retriever_chain.invoke({"chat_history": [HumanMessage(content="How are you")],
    #                                  "user_query": user_query, "model": llm})

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", exts.QA_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", user_query)
        ]
    )
    print("ChatBot Agent: QA prompt created.")

    rag_chain = (
            retriever_chain
            | qa_prompt
            | llm
    )
    print("ChatBot Agent: RAG chain created.")

    ai_message = rag_chain.invoke({"user_query": chat_info.get("user_query"),
                                   "chat_history": chat_info.get("chat_history"),
                                   "models": llm})

    # append the response for further interaction
    new_chat_history = chat_info.get("chat_history").extend([HumanMessage(content=user_query), ai_message])

    print(f"ChatBot Agent: Success!\nHere is the ai response:{ai_message.content}")
    return ai_message.content, new_chat_history


def run_chat_bot_agent(chat_info: dict):
    """
    Check if user query is relevant to database.
    If not, add current user query and error message to chat history.
    Else:
    Generate retrieval chain from vectordb and question maker chain(memory involved).
    Create a QA prompt for question answering.

    :param chat_info: keys: user_query, chat_history
    :return:
    """
    user_query = chat_info.get("user_query")
    old_chat_history = chat_info.get("chat_history")
    vector_store = extract_vector_store(user_query)

    if not vector_store:
        print(f"ChatBot Agent: Not found in database\nUser query:{user_query}")
        current_chat_history = [HumanMessage(content=user_query), AIMessage(content=exts.CHATBOT_ERROR)]
        return "", old_chat_history.extend(current_chat_history)

    return create_chatbot_agent(chat_info, vector_store)
