from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
import os , json , pandas as pd 
from dotenv import load_dotenv
from src.mcqgenerator.utills import getTableData

# load keys as environment variables
# it set the .env file and stores all the imp keys
load_dotenv()
key=os.getenv("API_KEY")

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo",temperature=0.5)
with open("response.json","r") as f:
    response_json=json.load(f)

Template1="""
Text:{text}
you are an expert MCQ maker.given the above text,it is your job to \
create a quiz on {number} multiple questions for {subject} student in {ton}\
make sure the question are not repeated and check all the question to be conformned\
make sure ot format your response like response_json below and use it as a guide.\
ensure to make {number} MCQ's \
{response_json}
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","ton","response_json"],
    template=Template1
)

quizChain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)

# to check the quiz that we generate is correct or not?
# to evaluate we did.
Template2="""you are an expert english grammarian and writer.given a multiple choice question for {subject}\
    you need to evaluate the complexity of the grammer and give the complete analysis of quiz. only use at max 50 words for coplexity analysis. \
    if the quiz is not at per with the cognitive and analytical abilities of the student,\
    update the quiz question which need to be changed and change the tone such that it perfectly fits the student abilities.\
    Quiz_MCQ's:{quiz}
    check from an expert english writer of the above quiz:
    """

quiz_evalation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template=Template2
)

reviewChain=LLMChain(llm=llm,prompt=quiz_evalation_prompt,output_key="review",verbose=True)

#here we join both chain as sequential chain
generate_evaluate_chain=SequentialChain(chains=[quizChain,reviewChain],input_variables=["text","number","subject","ton","response_json"],output_variables=["quiz","review"],verbose=True)

# # generate quix based on any data testing model 
# with open("D://programs//genAi_project//data.txt","r",encoding="utf-8")as f:
#     content=f.read()

# content
# NUMBER=5
# SUBJECT="Ai"
# TON="SIMPLE"
# RESPONSE=response_json

# #based on content we have to generate mcq:
# # important method:
# with get_openai_callback() as cb:
#     result = generate_evaluate_chain({
#         "text": content,
#         "number": NUMBER,
#         "subject": SUBJECT,
#         "ton": TON,
#         "response_json": json.dumps(RESPONSE)
#     })
# print(f"total token:{cb.total_tokens}")
# print(f"prompt token:{cb.prompt_tokens}")
# print(f"completion token:{cb.completion_tokens}")
# print(f"total cost:{cb.total_cost}")

# # here firstly get the result.quiz  in str format and then load into json format 
# quiz=result.get("quiz")
# print(getTableData(quiz))