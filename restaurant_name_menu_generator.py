from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Use a current model (e.g., llama-3.1-8b or llama3-70b)
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # ✅ Updated model name
    temperature=0.6
)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_name_item(cuisine):
    # Step 1: Name chain
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="""give me a Descent name for an restaurant for {cuisine} food.
    Rules:
    - Provide ONLY the name
    - No explanation
    - No bullet points
    - No numbers
    - Just the name itself"""
    )

    name_chain = prompt_template_name | llm | StrOutputParser()

    # Step 2: Menu items chain (uses restaurant_name from step 1)
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="""suggest some menu items for the given {restaurant_name} restaurant.
    Rules:
    return the items in the form of list.
    do not provide description about the items
    """
    )

    food_item_chain = prompt_template_items | llm | StrOutputParser()

    # Get restaurant name first
    restaurant_name = name_chain.invoke({"cuisine": cuisine})
    
    # Then get menu items using the restaurant name
    menu_items = food_item_chain.invoke({"restaurant_name": restaurant_name})
    
    # Return as dictionary to match what app.py expects
    return {
        'restaurant_name': restaurant_name,
        'menu_items': menu_items
    }

if __name__ == "__main__":
    print(get_name_item("pakistani"))