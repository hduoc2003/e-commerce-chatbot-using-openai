# %%
import json
import os
from typing import Any
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

from gen_product_list import gen_product_list

# %%
# Input API keys
load_dotenv()

MY_OPENAI_KEY = os.getenv('MY_OPENAI_KEY')
openai_client = OpenAI(
    api_key=MY_OPENAI_KEY,
)

# %%
# Customize your product list if necessary.
# gen_product_list()
with open("product_list.json", "r") as r:
  product_list = json.loads(r.read())

context = [{'role': 'system',
            'content': f"""
Bạn là ShopBot, trợ lý AI cho shop thời trang trực tuyến của tôi - Lmao.

Vai trò của bạn là hỗ trợ khách hàng duyệt sản phẩm, cung cấp thông tin và hướng dẫn họ thực hiện quy trình thanh toán.

Hãy thân thiện và hữu ích trong các tương tác của bạn.

Chúng tôi cung cấp nhiều loại sản phẩm thuộc nhiều danh mục như Quần áo nữ, Quần áo nam, Phụ kiện, Bộ sưu tập trẻ em, Giày dép và các sản phẩm Quần áo năng động.

Hãy thoải mái hỏi khách hàng về sở thích của họ, giới thiệu sản phẩm và thông báo cho họ về bất kỳ chương trình khuyến mãi nào đang diễn ra.

Danh sách sản phẩm hiện tại được giới hạn như sau:

```{product_list[0:5]}```

Làm cho trải nghiệm mua sắm trở nên thú vị và khuyến khích khách hàng liên hệ nếu họ có bất kỳ câu hỏi nào hoặc cần hỗ trợ.
"""}]

# %%
# Create a Chatbot
def get_completion_from_messages(messages, model="gpt-3.5-turbo"):

    chat_completion = openai_client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion.choices[0].message.content

app = Flask(__name__)
CORS(app, origins="*",  supports_credentials=True)

@app.post("/chatbot")
def get_msg():
    data: Any = request.json
    conversation: list[str] = data.get('conversation')
    for (i, msg) in enumerate(conversation):
        context.append({'role': 'user' if i % 2 == 0 else 'assistant', 'content':f"{msg}"})

    response = get_completion_from_messages(context)
    for _ in range(0, len(conversation)):
        context.pop()
    return jsonify(response)

app.run(port=3000, host="127.0.0.1", debug=True)


