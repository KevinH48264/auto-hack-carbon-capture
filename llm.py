# Using LLM to generate topics
# Improvement: add rate limiting error handling so you don't hardcode the wait time. To catch errors, use these catch exceptions from BabyAGI: https://github.com/yoheinakajima/babyagi/blob/main/babyagi.py

# imports
import dotenv
import os
import openai
import time

dotenv.load_dotenv()
# openai.api_key = os.getenv("OPENAI_GPT4_API_KEY")
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = # Your Azure OpenAI resource's endpoint value.
openai.api_key = # Your Azure OpenAI key

# models
EMBEDDING_MODEL = "text-embedding-ada-003"
GPT_MODEL = "gpt-35-turbo-16k"
# GPT_MODEL = "gpt-4"

# for bulk openai message, no stream
def chat_openai_high_temp(prompt="Tell me to ask you a prompt", model=GPT_MODEL, chat_history=[], temperature=0):
    # define message conversation for model
    if chat_history:
        messages = chat_history
    else:
        messages = [
            {"role": "system", "content": "You are a helpful and educated carbon capture research consultant and an educated and helpful researcher and programmer. Answer as correctly, clearly, and concisely as possible. You give first-rate answers."},
        ]
    messages.append({"role": "user", "content": prompt})

    # create the chat completion
    print("Prompt: ", prompt)
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.0,
    )
    print("Completion info: ", completion)
    text_answer = completion["choices"][0]["message"]["content"]

    # updated conversation history
    messages.append({"role": "assistant", "content": text_answer})

    return text_answer, messages

def chat_openai(prompt="Tell me to ask you a prompt", model=GPT_MODEL, chat_history=[], temperature=0, verbose=False):
    # To deal with rate limits, just wait
    while True:
        try:
            # define message conversation for model
            messages = [
                {"role": "system", "content": "You are a helpful and educated carbon capture research consultant and an educated and helpful researcher and programmer. Answer as correctly, clearly, and concisely as possible. You give first-rate answers."},
            ]
            if chat_history:
                messages += chat_history
            messages.append({"role": "user", "content": prompt})

            # create the chat completion
            if verbose:
                print("Prompt messages: ", messages)
            completion = openai.ChatCompletion.create(
                engine=GPT_MODEL,
                messages=messages,
                temperature=temperature,
            )
            if verbose:
                print("Completion info: ", completion)
            text_answer = completion["choices"][0]["message"]["content"]

            # updated conversation history
            messages.append({"role": "assistant", "content": text_answer})
            return text_answer, messages
        except openai.error.RateLimitError:
            print(
                "   *** The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.Timeout:
            print(
                "   *** OpenAI API timeout occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIError:
            print(
                "   *** OpenAI API error occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIConnectionError:
            print(
                "   *** OpenAI API connection error occurred. Check your network settings, proxy configuration, SSL certificates, or firewall rules. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.InvalidRequestError:
            print(
                "   *** OpenAI API invalid request. Check the documentation for the specific API method you are calling and make sure you are sending valid and complete parameters. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.ServiceUnavailableError:
            print(
                "   *** OpenAI API service unavailable. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        else:
            break