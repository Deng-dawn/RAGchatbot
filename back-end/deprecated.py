# ZeroShotAgent used, deprecated
# # retrieval qa chain
# # just place into the chain rather than summarization
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=vectordb.as_retriever()
# )
# print("QA chain Created")
#
# qa.run(user_query)
# convert retrieval chain to a tool
# tools = [
#     Tool(
#         name='Knowledge Base',
#         func=qa_chain.run,
#         description=(
#             'use this tool when answering general knowledge queries to get '
#             'more information about the topic'
#         )
#     )
# ]
# print("Knowledge base tool created from qa chain")
#
# prompt = ZeroShotAgent.create_prompt(
#     tools,
#     prefix=exts.PREFIX,
#     suffix=exts.SUFFIX,
#     input_variables=["input", "chat_history", "agent_scratchpad"],
# )
#
# llm_chain = LLMChain(
#     llm=llm,
#     prompt=prompt
# )
#
# print("LLM chain created from prompt")
# agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
# agent_exe = AgentExecutor.from_agent_and_tools(agent=agent,
#                                                tools=tools,
#                                                verbose=True,
#                                                max_iterations=3,
#                                                # max_execution_time=max_execution_time,
#                                                early_stopping_method="force",
#                                                memory=memory)
# print("Agent executor created")
# response = agent_exe.invoke(user_query)