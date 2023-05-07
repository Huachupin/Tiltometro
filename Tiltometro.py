import os
import requests
import time
from twitchio.ext import commands, routines #https://twitchio.dev/
from dotenv.main import load_dotenv

load_dotenv()
TOKEN = os.environ['TOKEN']
CHANNELS = os.environ['CHANNELS']
NOMBRETIRA = os.environ['NOMBRETIRA']
LONGITUDTIRA= os.environ['LONGITUDTIRA']

class Bot(commands.Bot):

    def __init__(self):        
        super().__init__(token=TOKEN, prefix='!', initial_channels=[CHANNELS])        
        
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')        
        self.contador = int(os.environ['CONTADOR'])
        self.longitud_tira = int(os.environ['LONGITUDTIRA'])
        set_start_leds()
        #wait 3 seconds to start the bot
        time.sleep(3)

    """ async def event_message(self, message):
        #print(f"{message.author.name}: {message.content}")
        await self.procesar_mensaje_chat(message)
    
    async def procesar_mensaje_chat(self, message):        
        #print("messageRAW: ", message.raw_data)
        #print("messageTAGS: ", message.tags)
        print("message: ", message.content)
        print("suib: ", message.tags.get("subscriber"))
        print("mod: ", message.tags.get("mod"))
        print("-----------------------------------------") """            

    #@routines.routine(seconds=5, iterations=13)
    @routines.routine(seconds=5, wait_first=True)
    async def disminuye_tilt():        
        actual_tilt = get_leds_lenght()
        print(f'INTENTO DE DISMINUIR actual_tilt {actual_tilt}')
        if actual_tilt >= 5: 
            print(f'disminuir tilt')
            print(f'actual_tilt {actual_tilt}')
            tilt_decrement(actual_tilt)            

    """ @disminuye_tilt.before_routine
    async def disminuye_tilt_before():
        set_start_leds() """

    disminuye_tilt.start()

    @commands.command(aliases = ("t", "tlt", "til"))
    async def tilt(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        if self.contador <= self.longitud_tira:
            print(f'contador | {self.contador}')
            self.contador = self.contador + 5        
            print(f'contador1 | {self.contador}')
            aumentar_tilt(self.contador)
            #await ctx.send(f'Hola {ctx.author.name} aumentaste en 1 el contador del tiltómetro!')
        if self.contador == self.longitud_tira:
            await ctx.send(f'Hola {ctx.author.name} el contador del tiltónmetro llegó al máximo!')

#function to make an http get request
def aumentar_tilt(contador):    
    url =  f"http://{NOMBRETIRA}.local/win&SS=0&S=0&S2={contador}"
    requests.get(url)
    if contador == 50:
        url =  f"http://{NOMBRETIRA}.local/win&R=255&G=255&B=0" #amarillo
        requests.get(url)
    if contador == 70:
        url =  f"http://{NOMBRETIRA}.local/win&R=255&G=135&B=0" #naranjo
        requests.get(url)
    if contador == 105:
        url =  f"http://{NOMBRETIRA}.local/win&R=255&G=0&B=0" #rojo
        requests.get(url)
    #response = requests.get(url)
    #return response.json()

def set_start_leds():
    print("start leds")
    url =  f"http://{NOMBRETIRA}.local/win&SS=0&S=0&S2=1"
    requests.get(url)
    url =  f"http://{NOMBRETIRA}.local/win&R=0&G=255&B=0" #verde
    requests.get(url) 

def get_leds_lenght():
    url =  f"http://{NOMBRETIRA}.local/json/state"
    state = requests.get(url).json()
    #print(state["seg"][0]["len"])
    return state["seg"][0]["len"]

def tilt_decrement(value):
    url =  f"http://{NOMBRETIRA}.local/win&SS=0&S=0&S2={value - 5}"
    requests.get(url)
    if value < 105 and value > 70:
        url =  f"http://{NOMBRETIRA}.local/win&R=255&G=255&B=0" #amarillo
        requests.get(url)
    if value <= 70 and value > 50:
        url =  f"http://{NOMBRETIRA}.local/win&R=255&G=135&B=0" #naranjo
        requests.get(url)
    if value <= 50:
        url =  f"http://{NOMBRETIRA}.local/win&R=0&G=255&B=0" #verde
        requests.get(url)

bot = Bot()
bot.run()
