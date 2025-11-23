#local package is treated when there is __init__.py file in a folder

from setuptools import find_packages , setup;
# meta info regarding package
setup(
    name="mcqgenerator",
    version="0.0.1",
    author="karan dutt sharma",
    author_email="sharmakarandutt2004@gmail.com",
    install_requires=["openai","langchain",'streamlit',"python.dotenv","PyPDF2"],
    packages=find_packages()
)