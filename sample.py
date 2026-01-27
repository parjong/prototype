from logging import getLogger
from pprint import pp

from bs4 import BeautifulSoup
from langchain_core.output_parsers import JsonOutputParser
from google import genai
import requests
from py_markdown_table.markdown_table import markdown_table


logger = getLogger(__name__)

output_parser = JsonOutputParser()

def get(url: str):
    response = requests.get(url)
    response.raise_for_status()

    full_content = response.text

    soup = BeautifulSoup(full_content, 'html.parser')

    title = soup.title.text.strip() if soup.title else "UNKNOWN"

    logger.debug(title)
    logger.debug(full_content)

    return (response, title)


def check(response):
    contents = "\n".join([ "### HTML Content",
                 "```",
                 response.text,
                 "```",
                 "### Task",
                 "Create a JSON result which includes when this HTML content is posted, and concise title of this page",
                 "e.g. { \"date\": \"YYYY/MM/DD\", \"title\": \"content title\" }"
                ])

    client = genai.Client()

    # https://ai.google.dev/gemini-api/docs/quickstart
    # https://ai.google.dev/gemini-api/docs/text-generation#multi-turn-conversations
    # https://ai.google.dev/api/generate-content
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=contents
    )

    # https://ai.google.dev/gemini-api/docs/prompting-strategies
    logger.debug(response)

    return output_parser.parse(response.text)

cases = []
cases.append("https://news.hada.io/topic?id=26122")
cases.append("https://evan-moon.github.io/2026/01/25/types-as-proofs-typescript-hidden-math/")
cases.append("https://huggingface.co/blog/nvidia/nemotron-speech-asr-scaling-voice-agents")
cases.append("https://zdnet.co.kr/view/?no=20260127135335")
cases.append("https://kr.linkedin.com/posts/geonho-shin-139155167_ax%EB%A5%BC-%EC%84%B1%EA%B3%B5%EC%8B%9C%ED%82%AC-%EC%88%98-%EC%9E%88%EB%8B%A4%EB%A9%B4-%EC%B0%A8%EB%9D%BC%EB%A6%AC-%EC%B0%BD%EC%97%85%EC%9D%84-%ED%95%98%EB%8A%94-%EA%B2%8C-%EB%82%AB%EB%8B%A4-%EC%A7%80%EB%82%9C-1%EB%85%84%EA%B0%84-activity-7421674203805859840-Pw3V")
cases.append("https://brunch.co.kr/@cmjung/16")
cases.append("https://block.github.io/goose/blog/2026/01/04/how-i-taught-my-agent-my-design-taste/")

data= []

for url in cases:
    resp, title = get(url)
    d = check(resp)
    data.append({"url": url, "bs4.title": title, "gemini.date": d["date"], "gemini.title": d["title"]})

pp(data)
