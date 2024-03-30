

# A Basic RAG Chatbot Implementation



## ✨Features:

1. Frontend and backend seperation: 
   
   Makes the functionality clean and easy to scale.

![](/Users/dawn/Library/Application%20Support/marktext/images/2024-03-29-22-08-27-image.png)

2. A chatbot with memory:
   
   Flask session is used to store user chat history.
   
   

3. Use customized knowledge base for vector store:
   
   For this project, it only scrapes the homepage of [PartSelect](https://www.partselect.com/) for demo. You may either use your own database, PDF, or a website sitemap for better performance. You may also scrape pages under different product catergories and store vectors into Chroma database.
   
   Check `/back-end/generateVectorStore.py` for the detailed implementation.

4. RAG chain:
   
   ![](/Users/dawn/Library/Application%20Support/marktext/images/2024-03-29-22-34-37-image.png)



## ⚠️Shortcomings:

1. Single user at current stage.

2. Only collected data from homepage.

3. To improve prompts.

4. As the Instalily task required, the chatbot is only used for Refrigerator and Dishwasher products. It should define several preset questions button in the front to better acheive the goal.



## 🎬Short Demo (silent):

[RAGchatbot demo - 29 March 2024 | Loom](https://www.loom.com/share/13797209fad4485c9e1e515421d392c9?sid=828c9f59-675e-4b30-8fce-a5c961b3a2ca)





## 📚Reference:

[Using langchain for Question Answering on Own Data](https://medium.com/@onkarmishra/using-langchain-for-question-answering-on-own-data-3af0a82789ed)

[Chatbot Memory: Retrieval Augmented Generation (RAG) Chain | LangChain | Python | Ask PDF Documents - YouTube](https://www.youtube.com/watch?v=PtO44wwqi0M)

[Is there any way to combine chatbot and question answering over docs? · Issue #2185 · langchain-ai/langchain · GitHub](https://github.com/langchain-ai/langchain/issues/2185)


