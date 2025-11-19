from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

result = client.images.generate(
    model="dall-e-2",
    prompt="""{ "id": 6, "name": "Good, Weaver and Hill Tennis Racket", "description": "Unleash your potential with Good, Weaver & Hill's Tennis Racket! Crafted from durable mesh material, this racket caters to beginners, offering an ideal balance of power and control for every swing. Choose from multiple size options, ensuring a perfect fit for all players. Start your tennis journey on the right court with our training rackets - versatile, reliable, and ready to help you weave through the competition!", "category": "Sports", "price": 648.08, "stock_quantity": 75, "brand": "Good, Weaver and Hill", "sku": "SPO-000006", "weight": 3.04, "dimensions": { "length": 42.1, "width": 46.8, "height": 7.1 }, "rating": 4.4, "review_count": 218, "is_active": true, "features": { "material": "Mesh", "size_range": "Multiple sizes available", "performance": "Beginner suitable", "sport": "Training" }, "created_at": "2025-06-02 22:09:34.446510", "updated_at": "2024-12-25 08:34:12.910385" },""",
    size="512x512",
)

print(result.data[0].url)
