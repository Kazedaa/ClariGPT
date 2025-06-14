import os
os.environ["GROQ_API_KEY"]="GROQ_API_KEY"

from groq import Groq
from abc import ABC, abstractmethod
import requests
import fitz

client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
    )

logs = open("logs.txt",'w')


class Tool(ABC):
    """
    Abstract base class for tools.

    Methods:
    run(input_params):
    Abstract method to run the tool with given input parameters.
    """
    @abstractmethod
    def run(self, input):
        pass

class Finish(Tool):
    """
    A tool to return the final answer or result.

    Methods:
    run(final_answer):
    Returns the final answer provided to it.
    """

    def run(self, final_answer):
        """
        Returns the final answer provided to it.

        Parameters:
        final_answer : str
        The final answer or result that needs to be returned.
        Your final answer should always be either yes, no, before, after or a named entity.
        **DO NOT ANSWER IN SENTENCE**

        Returns:
        final_answer : str
        The same final answer or result.
        """
        # print("Finish")
        try:
            print(final_answer)
            return final_answer
        except Exception as e:
            print(f"An error occurred: {e}",file=logs,flush=True)
            return f"An error occurred: {e}"
    
class AskUser(Tool):
    """
    A tool that prompts the user for assistance in answering a query.

    Methods:
    run(query):
    Prompts the user with a query to obtain user assistance.
    """

    def run(self, query):
        """
        Prompts the user for help and awaits their input. Use this when the retrieved information is
        not useful or whenever you need user assistance for further directions. DO NOT ask the user to analyse
        the information or for the final answer. This tool is onl intended to get directions from the user

        Parameters:
        query : str
        The query string that encapsulates the information or question needing a user response.

        Returns:
        response : str
        The response provided by the user.
        """
        # print("AskUser")
        try:
            return input(query)
        except Exception as e:
            print(f"An error occurred: {e}",file=logs,flush=True)
            return f"An error occurred: {e}"
    
class FetchPaper(Tool):
    """
    A tool that fetches the research paper from the internet.

    Methods:
    run(arxiv_id):
    Returns the path of the PDF.
    """

    def run(self, arxiv_id):
        """
        Fetches the research paper from the internet using the provided arxiv ID.

        Parameters:
        arxiv_id : str
        The arxiv ID of the research paper that needs to be fetched.
        **DO NOT ask the user to analyse the information or for the final answer. This tool is onl intended to get directions from the user**

        Returns:
        path : str
        The path to the PDF of the research paper.
        """
        # print("FetchPaper")
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        save_path = f"{os.getcwd()}/Memory/{arxiv_id}.pdf"
        print("Downloading PDF from:", url, file=logs,flush=True)
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            with open(save_path, "wb") as file:
                file.write(response.content)
            
            return f"Downloaded successfully to {save_path}"
        except requests.RequestException as e:
            print(f"Error downloading PDF: {e}", file=logs,flush=True)
            return f"Error downloading PDF: {e}"
            
        
class Parse(Tool):
    """
    A tool that parses the PDF file and extracts the text from it.
    Methods:
    run(path):
    Parses the PDF file and extracts the text from it.
    """

    def run(self, path):
        """
        Reads the PDF file and extracts the text from it.
        
        Parameters:
        path : str
        The path to the PDF file that needs to be parsed.
        
        Returns:
        text : str
        The extracted text from the PDF file.
        """
        # print("Parse")
        try:
            doc = fitz.open(path)
            text = ""
            for page_num in range(min(1,len(doc))):
                page = doc.load_page(page_num)  # Load page
                text += page.get_text() + "\n"  # Extract text from page

            doc.close()
            
            # Clean text
            clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
            return clean_text
        except Exception as e:
            print(f"An error occurred: {e}",file=logs,flush=True)
            return f"An error occurred: {e}"
            
class AskExpert(Tool):
    """
    This tool can by used to analyse and process text and also SUMMERIZE text.
    The tool asks a question to an expert and returns the answer.
    
    Methods:
    run(query):
    Asks the question to the expert and returns the answer.
    """
    def run(self, query):
        """
        Asks the question to the expert and returns the answer.
        Parameters:
        query : str
        The question that needs to be asked to the expert.
        Returns:
        answer : str
        The answer provided by the expert.
        """
        # print("AskQuestion")
        try:
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            chat_completion = client.chat.completions.create(
                                messages=[
                                    {
                                        "role": "user",
                                        "content": query,
                                    }
                                ],
                                model="llama3-70b-8192",
                            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}",file=logs,flush=True)
            return f"An error occurred: {e}"

