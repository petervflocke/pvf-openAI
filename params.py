from enum import Enum

# Create a class for different states in a state machine of the assistant
class assistantStatus(Enum):
    idle = 0
    local = 1  # interact with local resourcs e.g. sqlite
    local_waiting = 2
    local_done = 3
    openai = 4
    openai_waiting = 5  # interact with openAI
    openai_done = 6


SYSTEM_PROMPTS= {
assistantStatus.idle : "",
assistantStatus.local :
"""Please analyze the following text input and identify its message content type: 

1. If it contains information to remember, process the input into a structured format and do not provide anything else. Use #remember format from DATABASE

2. If it consists of questions, queries, or information search, process the input into a structured format and do not provide anything else. Use #question format from DATABASE

3. For all other cases, return data in use #pass  format from DATABASE and do not provide anything else


### DATABASE
{
  "action" : "#remember",
  "original_message": "Adam has a dog, called Traktor",
  "entities": ["Adam", "dog", "Traktor"],
  "relationships": ["Adam has dog", "dog is called Traktor"]
}

{
  "action" : "#question",
  "original_message": "Adam has a dog, called Traktor",
  "entities": ["Adam", "dog", "Traktor"],
  "relationships": ["Adam has dog", "dog is called Traktor"]
}

{
  "action" : "#pass",
  "original_message": "Describe best ten sf books"
} 
###    
"""
,
    assistantStatus.openai : "Your name is Peter, you are helpful assistant"
}

if __name__ == "__main__":
   print (SYSTEM_PROMPTS[assistantStatus.openai])