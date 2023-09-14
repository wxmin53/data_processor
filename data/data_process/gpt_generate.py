import openai


class GptRequest():
    def __init__(self):
        pass

    def request_gpt(self, prompt):
        # 请求 api
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # print(response)
        choices = response.get('choices', [])
        if len(choices) > 0:
            finish_reason = choices[0].get("finish_reason", '')
            if finish_reason == 'stop':
                answer = choices[0].get("message", {}).get("content", '')
                return answer
        return None


if __name__ == "__main__":
    pass
