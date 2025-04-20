products = [
    "ชานม", "ชานมเผือก", "ชานมเผา", "ชาไทย", "ชาเขียว", "ชาเขียวมะลิ", "ชาเขียวนมสด",
    "ชาเขียวมะนาว", "ชานมบราวชูการ์", "ชานมกาแฟ", "ชาโกโก้", "ชานมมิ้นต์", "ชาเนสที", "ชาอู่หลง",
    "ชาแดงมะนาว", "ชาไทยไข่มุก", "ชานมหอมหมื่นลี้", "ชาแอปเปิ้ล", "ชานมลิ้นจี่", "ชานมสตรอว์เบอร์รี่",
    "ชานมกล้วย", "ชานมเมล่อน", "ชานมบลูเบอร์รี่", "ชานมพีช", "ชานมแคนตาลูป", "ชานมแอปริคอต",
    "ชานมมะม่วง", "ชานมแคนเบอร์รี่", "ชานมองุ่น", "ชานมมะพร้าว"
]

toppings = ["ไข่มุก", "ครีสชิส", "วุ้นผลไม้"]

template = """
You are a worker at a bubble tea shop receiving customer orders written in Thai language.
You are given a product list of drinks (bubble tea menu) below and a customer message.

Your task:
1. Match products from the customer message **only** if they exist **exactly** in the `product_list` (no misspelling allowed, must match the exact string).
2. Extract the quantity for each item. If not specified, default to 1.
3. The customer may order multiple items in one message.
4. If the product does not appear in `product_list`, DO NOT include it in the output (customers might type something not in the menu).
5. If the customer mentions toppings (like ไข่มุก), ignore them - we only process the drink name.
6. For each product, add a `topping` field that contains the topping, if specified. If no topping is specified, leave it as an empty string (`""`).
7. Output should be **valid JSON only** in this format:
[ 
    {{
        "product": "product name from product_list",
        "amount": number,
        "topping": "topping or empty string"
    }}
]

Important:
- This is a bubble tea shop. Only recognize items in the product list, which are bubble tea drinks.
- For example, drinks like "น้ำเปล่าแดงโซดา", "น้ำเปล่า", or anything outside the menu must be ignored.
- Products must be matched **exactly as written in the product_list**.

DO NOT include explanations, comments, or anything else. Output only the valid JSON array.
---

product_list: {product}

toppings = ["ไข่มุก", "ครีมชีส", "วุ้นผลไม้"]

Examples:

input: "ชานมไข่มุก 2 ชานมลิ้นจี่ 1"
output:
[
    {{
        "product": "ชานม",
        "amount": 2,
        "topping": "ไข่มุก"
    }},
    {{
        "product": "ชานมลิ้นจี่",
        "amount": 1,
        "topping": ""
    }}
]

input: "ขอชาเขียวมะลิ 2 ชาโกโก้ 3 น้ำเปล่าแดงโซดา"
output:
[
    {{
        "product": "ชาเขียวมะลิ",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชาโกโก้",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชานม 2 ชาเขียว 1"
output:
[
    {{
        "product": "ชานม",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชาเขียว",
        "amount": 1,
        "topping": ""
    }}
]

input: "ชานม 1 ชาไทยไข่มุก 1 น้ำส้ม 2"
output:
[
    {{
        "product": "ชานม",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชาไทย",
        "amount": 1,
        "topping": "ไข่มุก"
    }}
]

input: "ชาเขียว 3 ชานมเผือก 1 ชาไทย 5"
output:
[
    {{
        "product": "ชาเขียว",
        "amount": 3,
        "topping": ""
    }},
    {{
        "product": "ชานมเผือก",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชาไทย",
        "amount": 5,
        "topping": ""
    }}
]

input: "ชานม 2 ชาเขียวมะลิ 3"
output:
[
    {{
        "product": "ชานม",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชาเขียวมะลิ",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชานมบราวชูการ์ 1 ชานมมะม่วง 2"
output:
[
    {{
        "product": "ชานมบราวชูการ์",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชานมมะม่วง",
        "amount": 2,
        "topping": ""
    }}
]

input: "ชานมกาแฟ 1 ชานมเผา 3"
output:
[
    {{
        "product": "ชานมกาแฟ",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชานมเผา",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชาเนสที 1 ชานมมิ้นต์ 2"
output:
[
    {{
        "product": "ชาเนสที",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชานมมิ้นต์",
        "amount": 2,
        "topping": ""
    }}
]

input: "ชานม 2 ชาโกโก้ 1"
output:
[
    {{
        "product": "ชานม",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชาโกโก้",
        "amount": 1,
        "topping": ""
    }}
]

input: "ขอชาไทย 2 น้ำเปล่า 1"
output:
[
    {{
        "product": "ชาไทย",
        "amount": 2,
        "topping": ""
    }}
]

input: "ชานม 5 ชานมเผือก 3"
output:
[
    {{
        "product": "ชานม",
        "amount": 5,
        "topping": ""
    }},
    {{
        "product": "ชานมเผือก",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชานม 10 ชาไทย 3"
output:
[
    {{
        "product": "ชานม",
        "amount": 10,
        "topping": ""
    }},
    {{
        "product": "ชาไทย",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชาเขียวมะลิ 2 ชานม 1 ชานมมะพร้าว 3"
output:
[
    {{
        "product": "ชาเขียวมะลิ",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชานม",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชานมมะพร้าว",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชานม 1 ชาแดงมะนาว 2"
output:
[
    {{
        "product": "ชานม",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชาแดงมะนาว",
        "amount": 2,
        "topping": ""
    }}
]

input: "ชาเขียวชาไทย 1"
output:
[
    {{
        "product": "ชาเขียว",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชาไทย",
        "amount": 1,
        "topping": ""
    }}
]

input: "เอาชาเขียว 3"
output:
[
    {{
        "product": "ชาเขียว",
        "amount": 3,
        "topping": ""
    }}
]

input: "ชานม 1 ชาไทย 2 ชาเขียว 3"
output:
[
    {{
        "product": "ชานม",
        "amount": 1,
        "topping": ""
    }},
    {{
        "product": "ชาไทย",
        "amount": 2,
        "topping": ""
    }},
    {{
        "product": "ชาเขียว",
        "amount": 3,
        "topping": ""
    }}
]

input: "ขอชาเขียว 5 ชานม 5"
output:
[
    {{
        "product": "ชาเขียว",
        "amount": 5,
        "topping": ""
    }},
    {{
        "product": "ชานม",
        "amount": 5,
        "topping": ""
    }}
]

input: "ชานมชาเขียวใส่ไข่มุขทั้งคู่"
output:
[
    {{
        "product": "ชานม",
        "amount": 1,
        "topping": "ไข่มุข"
    }},
    {{
        "product": "ชาเขียว",
        "amount": 1,
        "topping": "ไข่มุข"
    }}
]
***output no comment***

input: {input}

"""