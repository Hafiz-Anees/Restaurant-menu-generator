import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load local .env (for local development)
load_dotenv()

# Get Groq API Key (Streamlit Secrets first, then .env)
groq_api_key = None

if "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]
else:
    groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.6,
    api_key=groq_api_key
)


def get_name_item(cuisine):

    # Prompt for restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="""
Give me a decent name for a restaurant that serves {cuisine} cuisine.

Rules:
- Provide ONLY the name
- No explanation
- No bullet points
- No numbers
- Just the name itself
"""
    )

    name_chain = prompt_template_name | llm | StrOutputParser()

    # Prompt for menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="""
Suggest some menu items for the restaurant named {restaurant_name}.

Rules:
- Return only the food items
- Format them as a simple list
- Do not include descriptions
"""
    )

    food_item_chain = prompt_template_items | llm | StrOutputParser()

    # Generate restaurant name
    restaurant_name = name_chain.invoke({"cuisine": cuisine})

    # Generate menu items
    menu_items = food_item_chain.invoke({"restaurant_name": restaurant_name})

    return {
        "restaurant_name": restaurant_name.strip(),
        "menu_items": menu_items.strip()
    }


# Test locally
if __name__ == "__main__":
    print(get_name_item("Pakistani"))
