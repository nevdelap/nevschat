#!/usr/bin/env python
# pylint: disable=missing-module-docstring

import openai
import wikipedia

PAGES = 350

print()

for page in range(PAGES):
    try:
        random_title = wikipedia.random(1)
        summary = wikipedia.page(random_title).summary
        print(f"Title({page + 1}): {random_title.strip()}\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Translate the following text into
                        French, Spanish, and Japanese.

                        {summary}
                    """
                }
            ],
        )
        print(f"Original: {summary.strip()}\n")
        print(response.choices[0].message.content.strip() + "\n")

    except Exception:  # pylint: disable=broad-exception-caught  # nosec
        pass
