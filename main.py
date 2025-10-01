import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *
from call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    When the user asks about the code project - they are referring to 
    the working directory. So, you should typically start by looking at 
    the project's files, and figuring out how to run the project and how 
    to run its tests, you'll always want to test the tests and the actual project
    to verify that behavior is working.

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("Usage: python main.py \"your prompt here\"")
        sys.exit(1)
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    messages = [
      types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file,
    ]
    )
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )   
    max_iters = 20
    for i in range(0, max_iters):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=config,
        )
        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
        
        if response.function_calls:
            for function_call_part in response.function_calls:
                result =call_function(function_call_part, verbose)
                messages.append(result)
        else: 

            print(response.text)
            return
    
   
    

main()