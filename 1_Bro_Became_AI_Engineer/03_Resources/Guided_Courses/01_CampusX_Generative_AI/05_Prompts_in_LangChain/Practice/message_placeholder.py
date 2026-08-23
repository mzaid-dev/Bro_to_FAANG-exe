from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

# chat template 
chat_template = ChatPromptTemplate([
    ('system' , 'you are a helpfull customer support aggent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human' , '{query}'),
    
])


chat_history = []

# load chat history
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

# print(chat_history)

# create prompt
prompt = chat_template.invoke({
    'chat_history' : chat_history,
    'query' : HumanMessage(content='where is my refund')
})


print(prompt)