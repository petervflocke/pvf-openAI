
SYSTEM_PROMPTS= [
    1 : """Please analyze the following text input and identify its message content type: 

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
""",
    2 : "Your name is Peter, you are helpful assistent"
]