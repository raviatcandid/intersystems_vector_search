from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import constants as CONSTANTS

# Initialize OpenAI client with API key
openai_client = OpenAI(api_key=CONSTANTS.OPENAI_API_KEY)

def retrieve_response_from_llm(question, combined_vectors):
    """
    Retrieves a response from the OpenAI Language Learning Model (LLM) based on the
    provided question and combined vectors context.
    """
    try:
        message_context = [
            {'role': 'system', 'content': CONSTANTS.PERSONA},
            {'role': 'user', 'content': str(combined_vectors)},
            {'role': 'assistant', 'content': CONSTANTS.ASSISTANT_RESPONSE},
            {'role': 'user', 'content': question}
        ]
        chat_completion = openai_client.chat.completions.create(
            messages=message_context,
            model=CONSTANTS.OPENAI_LLM,
            temperature=0.6,
        )
        answer = chat_completion.choices[0].message.content
        return answer

    except APIConnectionError as e:
        print(f"Connection to OpenAI API failed: {e}")
        return "Connection to OpenAI API failed."

    except RateLimitError as e:
        print(f"Rate limit exceeded for OpenAI API requests: {e}")
        return "Rate limit exceeded for OpenAI API requests."

    except APIError as e:
        print(f"An error was returned by the OpenAI API: {e}")
        return "An error was returned by the OpenAI API."

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."
