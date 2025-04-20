import ollama
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from prompt import template,products

model = OllamaLLM(model="mistral")

prompt = ChatPromptTemplate.from_template(template)
# inputdata = input("enter:")
# messages = prompt.format_messages(product=products,input=inputdata)

# # ส่งเข้าโมเดลโดยตรง
# res = model.invoke(messages)
# print(res)

def order(message):
    messages = prompt.format_messages(product=products,input=message)
    res = model.invoke(messages)
    return res
