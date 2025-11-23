import os,json,traceback,pandas as pd ,streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.utills import readFile,getTableData
from src.mcqgenerator.mcqGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#read json:
with open('response.json',"r") as f:
    response=json.loads(f.read())

st.title("MCQ's Creator Application")
with st.form("user input"):
    uploaded_file=st.file_uploader("upload pdf or text")
    mcq_count=st.number_input("number of mcq's",min_value=3,max_value=50)
    subject=st.text_input("insert subject",max_chars=20)
    tone=st.text_input("complexity level of questions",max_chars=20,placeholder="simple")
    button=st.form_submit_button("create Quiz")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=readFile(uploaded_file)

                with get_openai_callback() as cb:
                     result = generate_evaluate_chain(
                               {
                                "text": text,
                                "number": mcq_count,
                                "subject": subject,
                                "ton": tone,
                                "response_json": json.dumps(response)
                               }
                            )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("ERROR")
            else:
                print(f"total token:{cb.total_tokens}")
                print(f"prompt token:{cb.prompt_tokens}")
                print(f"completion token:{cb.completion_tokens}")
                print(f"total cost:{cb.total_cost}")
                if isinstance(result,dict):
                    quiz=result.get("quiz",None)
                    if quiz is not None:
                        finalquiz=getTableData(quiz)
                        if finalquiz is not None:
                            df=pd.DataFrame(finalquiz)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review",value=result["review"])
                        else:
                            st.error("error in data table")
                else:
                    st.write(result)
    else:
        st.error("fill all details asked!!!")