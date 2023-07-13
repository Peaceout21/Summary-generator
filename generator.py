from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
# import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
# from langchain.document_loaders import JSONLoader
# from langchain import LLMChain, OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser



api = 'PASTE OPEN AI API KEY HERE'

""" define schema for output"""

total_work_experience = ResponseSchema(name="total_work_experience",
                             description="total_work_experience")

founder_cofounder_experience = ResponseSchema(name="founder_cofounder_experience",
                                      description="total\
                                          founder_cofounder_experience")

num_companies_founded = ResponseSchema(name="num_companies_founded",
                                    description=" total num_companies_founded")

years_experience_AI_ML = ResponseSchema(name="years_experience_AI_ML",
                                    description=" total years_experience_AI_ML")

name_companies_founded = ResponseSchema(name="name_companies_founded",
                                    description=" total name_companies_founded if any")
bio = ResponseSchema(name="bio",
                                    description=" a short description of profile")


response_schemas = [total_work_experience, 
                    founder_cofounder_experience,
                    num_companies_founded,
                    years_experience_AI_ML,
                    name_companies_founded,
                    bio]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

def main(intake_path):
    # intake_path = "/Users/arjundebnath/Documents/arjun/frontier/Jonathan Wray_relev.txt"

    loader = UnstructuredFileLoader(intake_path)
    intake_form = loader.load()


    embeddings = OpenAIEmbeddings(openai_api_key=api)
    index = FAISS.from_documents(intake_form, embeddings)


    # retriver = index.as_retriever(search_type='similarity',search_kwargs={"k":15})




    template = """
    accurately respond and return the answers as a dict structure {query}?
    """


    prompt = PromptTemplate(
        input_variables=["query"],
        template=template,
    )

    chatbot = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            openai_api_key=api,
            temperature=0, model_name="gpt-3.5-turbo", max_tokens=500
        ), 
        # gpt-3.5-turbo-0301
        chain_type="stuff", 
        # chain_type="map_reduce", 
        # chain_type="refine".
        retriever= index.as_retriever(search_type='similarity',search_kwargs={"k":5}),
    
    )

    query = """
    calculate the 
    1. total work experience in integer
    2.  number of years of experience as founder or co-founder in integer
    3. number of companies founded or co-founded in integer
    4. number of years of experience in positions related to artificial intelligence, data science or machine learning in integer format
    5. names of companies founded or co-founded as list.
    6. Generate a short bio of around 150 words using points 1 to 5 and using skills  
    PS:
    If no data then return None as the value
    Only return dict as the answer and maintain this format 
    {
    "total_work_experience" : "",
    "founder_cofounder_experience" : "",
    "num_companies_founded" : "",
    "years_experience_AI_ML" : "",
    "name_companies_founded" : [],
    "bio" : ""
    }
    """

    op = chatbot.run(
        prompt.format(query=query)
    )
    print(type(op))

    return op



