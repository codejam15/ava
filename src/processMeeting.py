from models import agent
from models import responsemodel

def callLLM(prompt: str)->responsemodel.MeetingResponseModel:
    return agent.llm.run_sync(prompt).output

def processTranscript(prompt : str):
    response = callLLM(prompt)
   # page = createPage(response)
    greetings = "Hello Tearesponsemodel.GroupResponseModelm! Thank you all for attending today's reunion. \n"
    link = "Here is the link to the confluence page: \n"    
    feedback = "Some overall feedback regarding a few points: "
   # linkURL = constructURL(page.id)
