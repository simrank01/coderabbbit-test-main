import base64

import json

import requests

from pathlib import Path
import os




class LiteLLMClient:
    CUSTOM_API_BASE = os.getenv("AI_API_BASE")
    MODEL_NAME = "AEM" 
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


    def __init__(self):

        self.endpoint = CUSTOM_API_BASE.rstrip("/")

        self.model = MODEL_NAME

        self.headers = {

            "Authorization": f"Bearer {ANTHROPIC_API_KEY}",

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



