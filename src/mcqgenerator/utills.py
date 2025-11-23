import os ,PyPDF2,json,traceback,pandas as pd

def readFile(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"error in reading the pdf file: {e}")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")    
    else:
        raise Exception("unsupported file format..only pdf and txt file supported")
    
def getTableData(quiz_str):
    try:
        quiz=json.loads(quiz_str)
        quizdata=[]
        # result store in proper format:
        for key,value in quiz.items():
            mcq=value["mcq"]
            options=" | ".join(
                [ 
                f"{option}:{option_value}" for option,option_value in value["options"].items()
                ]      
                )
            correct=value["correct"]
            quizdata.append({"MCQ":mcq,"Choices":options,"Correct":correct})
        df=pd.DataFrame(quizdata)
        return df
    except Exception as e:
        Exception("error due to invalid parameter")

