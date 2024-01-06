from openai import OpenAI


def your_api_key():
    with open('config/Your_API_KEY.txt', 'r') as file:
        api_key = file.readline()
    return api_key


def book_sentence_translation(title, author, sentence, word,
                              language_in_progress_of_learning='English', language='Polish'):
    openapi_key = your_api_key()
    client = OpenAI(api_key=openapi_key)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"You are a translator of {language_in_progress_of_learning} and {language}. "
                     f"You analyze the content of the book \"{title}\" written by {author}, and based on it, "
                     f"you translate the received sentences in accordance with the context."
                     "\n###\n"
                     f"Write informatively in a literary style fitting for {author}. Pay attention to the word "
                     f"\"{word}\""
        },
        {
          "role": "user",
          "content": f"Translate the sentence into {language}: \"{sentence}\""
        }
      ],
      temperature=0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["###"]
    )

    return response.choices[0].message.content


def book_word_translation(title, author, sentence, word, language_in_progress_of_learning='English', language='Polish'):
    openapi_key = your_api_key()
    client = OpenAI(api_key=openapi_key)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
            "role": "system",
            "content": f"You are a translator of {language_in_progress_of_learning} and {language}. You analyze the "
                       f"content of the book \"{title}\" written by {author}, and based on it, "
                       f"you translate the received word in accordance with the context in sentence: \"{sentence}\"."
                       "\n###\n"
                       f"If \"{word}\" is not in its base form, use lemmatization."
                       f"Pay attention to the sentence: \"{sentence}\""
                       f"Provide a maximum of 3 translation suggestions. "
                       f"Display the translation in the following pattern: \"lemmatizated word: translated word\""
        },
        {
          "role": "user",
          "content": f"Translate the word into {language}: \"{word}\". "
        }
      ],
      temperature=0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["###"]
    )

    return response.choices[0].message.content


def article_word_translation(sentence, word, language_in_progress_of_learning='English', language='Polish'):
    openapi_key = your_api_key()
    client = OpenAI(api_key=openapi_key)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"You are a translator of {language_in_progress_of_learning} and {language}. You translate "
                     f"the received word in accordance with the context in sentence: \"{sentence}\""
                     "\n###\n"
                     f"If \"{word}\" is not in its base form, use lemmatization."
                     f"Pay attention to the sentence: \"{sentence}\""
                     f"Provide a maximum of 3 translation suggestions. "
                     f"Display the translation in the following pattern: \"lemmatizated word: translated word\""
        },
        {
          "role": "user",
          "content": f"Translate the word into {language}: \"{word}\""
        }
      ],
      temperature=0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["###"]
    )

    return response.choices[0].message.content


def article_sentence_translation(sentence, word, language_in_progress_of_learning='English', language='Polish'):
    openapi_key = your_api_key()
    client = OpenAI(api_key=openapi_key)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": f"You are a translator of {language_in_progress_of_learning} and {language}. You analyze "
                     f"the content of the sentence: \"{sentence}\", and based on it, you translate the received "
                     "sentences in accordance with the context."
                     "\n###\n"
                     f"Write informatively in a literary style fitting for journalist. Pay attention to the word "
                     f"\"{word}\""
        },
        {
          "role": "user",
          "content": f"Translate the sentence into {language}: \"{sentence}\""
        }
      ],
      temperature=0,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["###"]
    )

    return response.choices[0].message.content
    pass
