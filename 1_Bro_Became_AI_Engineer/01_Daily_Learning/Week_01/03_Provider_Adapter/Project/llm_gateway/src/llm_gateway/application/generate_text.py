from llm_gateway.ports.llm import LLMPort

class GenerateText:

    def __init__(self,llm : LLMPort):
        self.llm = llm



    async def execute(self,prompt : str) -> str:
        response = await self.llm.generate(prompt)


        return response