from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os
from order import order
from linebot.v3.messaging import (
    MessagingApi, Configuration, ApiClient, PushMessageRequest, TextMessage
)
import asyncio
import json
import prompt

load_dotenv()
access = os.getenv("ACCESS_TOKEN")
configuration = Configuration(access_token=access)
app = FastAPI()

@app.post("/web")
async def dialogflow_webhook(req: Request):
    body = await req.json()
    user_input = body['queryResult']['queryText']
    user_id = body['originalDetectIntentRequest']['payload']['data']['source']['userId']
    parameters = body['queryResult']['parameters']
    intent = body['queryResult']['intent']['displayName']
    if intent=='order_input':
        asyncio.create_task(process_order(user_input, user_id))
    elif intent=='Menu':
        result = await get_menu()
        print(result)
        return result
    return {
        "ok"
    }

async def get_menu():
    menu = prompt.products #เอาเมนูจาก prompt ชื่อตัวแปร products
    topping = prompt.toppings #เอาเมนูจาก prompt ชื่อตัวแปร toppings
    result = "รายการ\n" 
    for item in menu:
        result += '- ' + item + '\n' #เก็บใส่ตัวแปร result
        print(item) #ทำการจัดรูปแบบข้อความ loop
    #เมนู\n-ชานม\n-ชาไทย 
    
    result += "\nท้อปปิ้ง\n" 
    for item in topping:
        result += '- ' + item + '\n' 
        print(item) #เมนู\n-ชานม\n-ชาไทย (ุลองใส่ตัว topping ไปด้วย)
        
    return{
  "fulfillmentMessages": [
    {
      "text": {
        "text": [result]
      }
    }
  ]
}

async def process_order(message, user_id):
    res = order(message)  # อาจใช้ await ถ้า async
    result = ""
    for item in json.loads(res):
        result += item['product'] + ' x' + str(item['amount']) + '\ntopping: ' + item['topping'] + '\n'
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=str(result))]
            )
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
