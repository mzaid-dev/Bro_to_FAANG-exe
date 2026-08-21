from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_template = ChatPromptTemplate([
    (
        'system', 'You are a helpfull {domain} expert'
    ),
    (
        'human',"Explain in simple terms, what is {topic}"
    )
])


prompt = chat_template.invoke({
    'domain' : "Senior Developer",
    'topic' : 'What is decorator in python'
})

print(prompt)