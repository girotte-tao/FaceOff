"""
  Start the ollama service before you use this client.
"""
import ollama
import base64


class OllamaClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.messages = []
        self.instruct = ''

    def set_instruct(self, instruct: str):
        self.instruct = instruct
        self.messages.append({
            'role': 'system',
            'content': instruct
        })

    def add_message(self, role: str, content: str, images=None):
        if images:
            self.messages.append({
                'role': role,
                'content': content,
                'images': images
            })
        else:
            self.messages.append({
                'role': role,
                'content': content
            })


    def chat(self):
        if not self.messages:
            raise ValueError("Please set instruct before chatting.")
        response = ollama.chat(model=self.model_name, messages=self.messages)

        return response['message']['content']

    def free_context(self):
        self.messages = []
        self.messages.append({
            'role': 'system',
            'content': self.instruct
        })

    def one_round_chat(self, user_message: str):
        self.add_message("user", user_message)
        response = self.chat()
        self.free_context()
        # print(response)
        return response

    def one_round_chat_with_image(self, user_message: str, image_path: str):
        base64_image = self.encode_image(image_path)
        msg_content = f"{user_message}\n\n![Image](data:image/jpeg;base64,{base64_image})"

        self.add_message("user", user_message, [image_path])
        response = self.chat()
        self.free_context()
        # print(response)
        return response


    def encode_image(self, image_path):
        """Getting the base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")




