##-------------------------------------------------------#
#   Tomás Ryan  
#   TomasRyanMann@gmail.com
#   twitchChatController
#--------------------------------------------------------#
#   01/07    version 1.0
#       Initial version created, reads chat and gets a 
#       asscociated from items
#--------------------------------------------------------#
from twitchio.ext import commands
import pyvjoy
import asyncio
# set the controller to be used to be the 1st vJoy controller
chatPad = pyvjoy.VJoyDevice(1)
waitTime = 0.2
walkTime = 2
# set the controls as the button to be pressed
controlButtonDic = {
    'a':1,
    'b':2,
    'x':3,
    'y':4,
    'start':5,
    'select':6}
# set the axis values of x axis
axisXDic = {

    'left':1,
    'right':32767}
# set the axis values of the y axis
axisYDic = {
    'up':1,
    'down':32767}
# get the text of the message gotten from twitch chat, and 
# check it against all the valid responses, and if its a valid 
# response then call the method to enter said input
async def parseInput(messageText):
    loop = asyncio.get_event_loop()
    lowerMessageText = str(messageText).lower()
    result = controlButtonDic.get(lowerMessageText, 0);
    if result != 0:
            loop.create_task(buttonPress(result))
            return
    result = axisXDic.get(lowerMessageText, 0);
    if result != 0:
            loop.create_task(axisXPress(result))
            return
    result = axisYDic.get(lowerMessageText, 0);
    if result != 0:
            loop.create_task(axisYPress(result))
            return
    
# a button press
async def buttonPress(button):
    chatPad.set_button(button, 1)
    await asyncio.sleep(waitTime)
    chatPad.set_button(button, 0)
    
#a x axis input
async def axisXPress(axisValue):
    chatPad.set_axis(pyvjoy.HID_USAGE_X, axisValue)
    await asyncio.sleep(walkTime)
    chatPad.set_axis(pyvjoy.HID_USAGE_X, 16384)
    
#a y axis input
async def axisYPress(axisValue):
    chatPad.set_axis(pyvjoy.HID_USAGE_Y, axisValue)
    await asyncio.sleep(walkTime)
    chatPad.set_axis(pyvjoy.HID_USAGE_Y, 16384)
    
    
    
class Bot(commands.Bot):
    # put in the details of the account the bot will be using here
    def __init__(self):
        # super().__init__(irc_token='oauth:', client_id='', nick='', prefix='!', initial_channels=[''])

    # on ready press all buttons and see if they work
    async def event_ready(self):
        for key in controlButtonDic:
            print(key + ' testing...')
            await parseInput(key)
        for key in axisXDic:
            print(key + ' testing...')
            await parseInput(key)
        for key in axisYDic:
            print(key + ' testing...')
            await parseInput(key)
        print('Test complete')
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print('Message Received')
        print(message.content)
        await parseInput(message.content)
        await self.handle_commands(message)


bot = Bot()
bot.run()