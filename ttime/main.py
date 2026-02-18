#IMPORTS
import argparse
import time
import os
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from pyfiglet import Figlet
from playsound3 import playsound

#PARSER ARGS
parser = argparse.ArgumentParser(
                    prog="tTime",
                    description="Working countdown timer in the terminal.")
parser.add_argument('-H', '--hours', type=int, default=0, help="Hours to count down")
parser.add_argument('-M', '--minutes', type=int, default=0, help="Minutes to count down")
parser.add_argument('-S', '--seconds', type=int, default=0, help="Seconds to count down")
parser.add_argument('-f', '--font', type=str, default='big', help="Font to draw the timer with")
parser.add_argument('-fc', '--fontColor', type=str, default='white', help="Color of the font")
parser.add_argument('-bc', '--borderColor', type=str, default='white', help="Color of the border")

#FUNCTIONS
def main():
    
    #VARIABLES
    layout = Layout()
    args = parser.parse_args()
    tTime = (args.hours * 60 * 60) + (args.minutes * 60) + args.seconds
    sTime = time.time()
    eTime = sTime + tTime
    f = Figlet(font=args.font)
    timerPan = Panel(Text.from_markup(f"[{args.fontColor}]00:00:00", justify="center"))
    workingDir = os.path.dirname(os.path.abspath(__file__))
    beepFile = os.path.join(workingDir, "beeps.wav")
    
    #LOGIC
    with Live(layout, screen=True) as live:
        
        while True:
            
            rTime = eTime - time.time()
            
            if rTime < 0:
                break
            
            rTimeH = int(rTime // 3600)
            rTimeM = int((rTime // 60) % 60)
            rTimeS = int(rTime % 60)
            rTimeText = f"{rTimeH:0>2} : {rTimeM:0>2} : {rTimeS:0>2}"
            
            tText = f.renderText(rTimeText)
            asciiArt = Text(tText, style=args.fontColor, justify="left")
            asciiPan = Panel(asciiArt, border_style=args.borderColor)
            layout.update(Align.center(asciiPan, vertical="middle"))
            
            live.update(layout)
            
            time.sleep(0.1)

        try:
            flashState = True
            fTxt = f.renderText("Time's Up!")
            count = 0
            while True:
                if flashState == True:
                    layout.update((Align.center(f"[bold red]{fTxt}", vertical="middle")))
                    live.update(layout)
                else:
                    layout.update((Align.center(f"[bold white]{fTxt}", vertical="middle")))
                    live.update(layout)
                if count == 0:
                    beep = playsound(beepFile, block=False)

                count += 1
                if count >= 5:
                    count = 0

                flashState = not flashState
                time.sleep(.5)

        except KeyboardInterrupt:
            print("")
    
if __name__ == "__main__":
    main()
    
