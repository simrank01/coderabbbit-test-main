import base64

import json

import requests

from pathlib import Path





class LiteLLMClient:

    def __init__(self, endpoint: str, bearer_token: str, model: str):

        self.endpoint = endpoint.rstrip("/")

        self.model = model

        self.headers = {

            "Authorization": f"Bearer {bearer_token}",

            "Content-Type": "application/json"

        }



    def chat(self, system_prompt: str, user_prompt: str) -> str:

        payload = {

            "model": self.model,

            "messages": [

                {"role": "system", "content": system_prompt},

                {"role": "user", "content": user_prompt}

            ],

            "temperature": 0.1

        }



        response = requests.post(

            self.endpoint,

            headers=self.headers,

            json=payload,

            timeout=120

        )



        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]



    def chat_with_image(

        self,

        system_prompt: str,

        user_prompt: str,

        image_url: str

        ) -> str:

        payload = {

            "model": self.model,

            "messages": [

                {"role": "system", "content": system_prompt},

                {

                    "role": "user",

                    "content": [

                        {"type": "text", "text": user_prompt},

                        {

                            "type": "image_url",

                            "image_url": {

                                "url": image_url

                            }

                        }

                    ]

                }

            ],

            "temperature": 0.1

        }



        response = requests.post(

            self.endpoint,

            headers=self.headers,

            json=payload,

            timeout=180

        )



        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]



