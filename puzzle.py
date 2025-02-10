import os

config_list = [
    {
        # Let's choose the Mixtral 8x22B model
        "model": "mistral-large-latest",
        # Provide your Mistral AI API key here or put it into the MISTRAL_API_KEY environment variable.
        "api_key": os.environ.get("MISTRAL_API_KEY"),
        # We specify the API Type as 'mistral' so it uses the Mistral AI client class
        "api_type": "mistral",
    }
]

from autogen import ConversableAgent

system_prompt = """
You are playing a puzzle game with the other agent. 
You have to ask the other agent a puzzle question. 
DO NOT TELL the answer upfront with the question.
The other agent may answer the puzzle or may ask you clarification questions.
The other agent may also ask you for hints. In case the other agent
asks clarification questions, you have to answer them. Feel free to provide hints too
but do not give away the answer. The other agent will try to guess the answer.
If the other agent guesses the answer, tell them if they are correct or not.
If the other agent is correct, the game ends. 
If the other agent is incorrect, tell them the correct answer and give an explanation.
"""
agent_with_puzzle = ConversableAgent(
    "puzzle_master",
    system_message=system_prompt,
    llm_config={"config_list": config_list},
    is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
    human_input_mode="NEVER",  # never ask for human input
)

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,  # no LLM used for human proxy
    human_input_mode="ALWAYS",  # always ask for human input
)



def main():
    # Start a chat with the agent with number with an initial guess.
    result = human_proxy.initiate_chat(
        agent_with_puzzle,  # this is the same agent with the number as before
        message="ask me a puzzle question",
    )


if __name__ == '__main__':
    main()