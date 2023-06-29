from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.document_loaders import WebBaseLoader
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_url(url):
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo-16k",
        temperature=0,
        max_tokens=2000,
        openai_api_key=openai.api_key
    )
  
    # Fetch and parse webpage using langchain webbaseloader
    loader = WebBaseLoader(url)
    jd_chunks = loader.load_and_split()
    jd_text = '\n'.join(chunk.page_content for chunk in jd_chunks)
  
    print(jd_text)

    jobs = Object(
        id="job_info",
        descripton="""
            Information about a job as it is provided in the job description.
        """,
        attributes=[
            Text(
                id="job_title",
                description="The job title",
                examples=[("LiveRamp is seeking a leader for the role of Product Intelligence Manager", "Product Intelligence Manager"),( "We’re excited to bring on a Chief of Staff","Chief of Staff"), ("As the Director of Operations, you will drive operational efficiencies", "Director of Operations")],
            ),
            Text(
                id="company",
                description="The name of the company",
                examples=[("Seven Starling is a digital maternal mental health clinic that specializes in treating common perinatal mood", "Seven Starling"), ("Exponent helps people land their dream tech jobs.", "Exponent"), ("The people of Path are what truly define our mission and determine our impact on the world.", "Path")],
            ),
            Text(
                id="location",
                description="The location of the job",
                examples=[("Path is a 100% remote healthtech company", "Remote"), ("The ability to work from any location within the US", "Remote"), ("Location San Diego, California", "San Diego"), ("Full Time Professional Austin, TX, US", "Austin")],
            ),
        ],
        examples=[
            (
                "Persistence AI is seeking a seasoned Chief Operating Officer (COO) to join our executive team in Denver",
                [
                    {"job_title": "Chief Operating Officer", "company": "Persistence AI", "location": "Denver"},
                ],
            ),
            (
                "Pacific Life is investing in bright, agile and diverse talent to contribute to our mission of innovating our business and creating a superior customer experience. We’re actively seeking a talented Senior Business Process Lead to join our Sales Intelligence Team in Newport Beach, CA or Omaha, NE.",
                [
                    {"job_title": "Senior BUsiness Process Lead", "company": "Pacific Life", "location": "Newport Beach"},
                ],
            ),
        ],
        many=True,
    )

    chain = create_extraction_chain(llm, jobs, input_formatter="triple_quotes")
    output = chain.predict_and_parse(text=jd_text)["data"]  

    return output  
