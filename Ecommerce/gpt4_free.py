import g4f
from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
)



class GPT4_Free_API:
    
    def __init__(self) -> None:
        
        g4f.debug.logging = True  # Enable logging
        g4f.check_version = False  # Disable automatic version checking
        # print(g4f.version)  # Check version
        # print(g4f.Provider.Ails.params)  # Supported args


    def get_model(self, model = None) :
        if model == "gpt-4":
            return g4f.models.gpt_4
        elif model == 'gpt-3.5-turbo' : # gpt-3.5-turbo
            return g4f.models.gpt_4
        
        return g4f.models.default


    
    def  get_gpt_response(self, prompt, model = None , respon = True) :
        # Streamed completion
        response = g4f.ChatCompletion.create(
            model= self.get_model(model), #"gpt-4", # gpt-3.5-turbo
            # provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": prompt}],
            # stream=False,
        )

        if respon :
            return response

        resp = ''

        for message in response:
            resp += message
        
        return resp[:-1]
