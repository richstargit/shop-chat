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
    #1.เอาเมนูจาก prompt ชื่อตัวแปร products
    #2.ทำการจัดรูปแบบข้อความ loop
    #เมนู\n-ชานม\n-ชาไทย (ุจะลองใส่ตัว topping ไปด้วยก็ได้นะ)
    #3.เก็บใส่ตัวแปร result
    return{
  "fulfillmentMessages": [
    {
      "text": {
        "text": ["เมนู"]
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
