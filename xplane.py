import os
import glob
import wave
from random import randrange
import time
import pygame
import numpy as np
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from scipy.io.wavfile import write
from piper import PiperVoice


# -------------------------------------------------------------------
# Do you want to see ATC messages in the console also?
# -------------------------------------------------------------------
atc_show_responses = True

# -------------------------------------------------------------------
# Define where your X-Plane log file is located
# This usually sits in the root of your X-Plane folder, named Log.txt
# -------------------------------------------------------------------
atc_xplane_log = "C:\\Users\\windo\\Simulator\\12\\Log_ATC.txt"
#atc_xplane_log = "./Log_ATC.txt"

# -------------------------------------------------------------------
# Do you want to hear "your voice" when contacting ATC?
# -------------------------------------------------------------------
atc_captain_voice = True

# -------------------------------------------------------------------
# Select your pilot's voice
# See the voices folder and pick one
# -------------------------------------------------------------------
atc_pilot_voice = "danny"
atc_pilot_quality = "low"

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

colorama_init()

print("  ")
print(" ---------------------------------------------- ")
print(" X-Plane Piper")
print(" Making X-Plane's ATC sound more natural")
print(" ---------------------------------------------- ")
print(" Developed by MarStrMind")
print(" License: MIT")
print(" ---------------------------------------------- ")
print(" Using file: " + atc_xplane_log)
print(" ---------------------------------------------- ")
print("  ")

atc_voices = glob.glob(".\\voices\\*")

curline  = 0
lastline = 0
pltfreq = ""
last_pltfreq = ""
atc_voice = ""

# We only need to load this once
pilotvoice = PiperVoice.load("./voices/" + atc_pilot_voice + "/" + atc_pilot_quality + "/en_US-"+atc_pilot_voice+"-"+atc_pilot_quality+".onnx")

# Init pygame and its mixer
pygame.init()
pygame.mixer.init()

# The click at the end of a transmission
click = pygame.mixer.Sound("./audio/endclick.wav")

while True:
    atc_log = open(atc_xplane_log)
    lines = atc_log.readlines()
    curline = 0
    for line in lines:
        if " Tx " in line and curline > lastline:
            lastline = curline
            thisline = line.replace("\n", "")
            linedata = thisline.split(": ")
            freqinfo = linedata[1].split(" ")
            speaker = 0
            if "PQ" in linedata[1] or "PR" in linedata[1]:
                speaker = 0
                if pltfreq == "" or freqinfo[3] != pltfreq:
                    pltfreq = freqinfo[3]
                    if last_pltfreq == "":
                        last_pltfreq = freqinfo[3]

            if "CC" in linedata[1]:
                speaker = 1
            
            if atc_voice == "" or last_pltfreq != pltfreq:
                vcfound = False
                while vcfound == False:
                    vc = randrange(0, len(atc_voices))
                    if atc_pilot_voice not in atc_voices[vc]:
                        avc = atc_voices[vc].replace(".\\voices\\", "")
                        atc_voice = avc
                        vcfound = True
            
            speakline = linedata[2].encode('latin-1').decode('utf-8')

            special_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss', ord('Ä'):'Ae', ord('Ö'):'Oe', ord('Ü'):'Ue'}
            speakline = speakline.translate(special_char_map)

            speakline = speakline.replace("0", " Zero ")
            speakline = speakline.replace("1", " One ")
            speakline = speakline.replace("2", " Two ")
            speakline = speakline.replace("3", " Three ")
            speakline = speakline.replace("4", " Four ")
            speakline = speakline.replace("5", " Fiver ")
            speakline = speakline.replace("6", " Six ")
            speakline = speakline.replace("7", " Seven ")
            speakline = speakline.replace("8", " Eight ")
            speakline = speakline.replace("9", " Niner ")

            speakline = speakline.replace("IFR", "I F R")
            speakline = speakline.replace("VFR", "V F R")

            if atc_show_responses == True:
                if speaker == 1:
                    print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + speakline + f'{Style.RESET_ALL}')
                if speaker == 0:
                    print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + speakline + f'{Style.RESET_ALL}')
                print(" ------------------------------------------------------- ")

            if speaker == 0:
                with wave.open("audio/pilot.wav", "wb") as wav_file:
                    pilotvoice.synthesize_wav(speakline, wav_file)

            if speaker == 1:
                qlt = ["high", "medium", "low"]
                atcvoice = None
                qlty = -1
                if qlty == -1:
                    if os.path.isfile("./voices/"+atc_voice+"/"+qlt[0]+"/en_US-"+atc_voice+"-"+qlt[0]+".onnx") == True:
                        atcvoice = PiperVoice.load("./voices/"+atc_voice+"/"+qlt[0]+"/en_US-"+atc_voice+"-"+qlt[0]+".onnx")
                        qlty = 0
                if qlty == -1:
                    if os.path.isfile("./voices/"+atc_voice+"/"+qlt[1]+"/en_US-"+atc_voice+"-"+qlt[1]+".onnx") == True:
                        atcvoice = PiperVoice.load("./voices/"+atc_voice+"/"+qlt[1]+"/en_US-"+atc_voice+"-"+qlt[1]+".onnx")
                        qlty = 1
                if qlty == -1:
                    if os.path.isfile("./voices/"+atc_voice+"/"+qlt[2]+"/en_US-"+atc_voice+"-"+qlt[2]+".onnx") == True:
                        atcvoice = PiperVoice.load("./voices/"+atc_voice+"/"+qlt[2]+"/en_US-"+atc_voice+"-"+qlt[2]+".onnx")
                        qlty = 2
                
                with wave.open("audio/atc.wav", "wb") as wav_file:
                    atcvoice.synthesize_wav(speakline, wav_file)

            # Get length of spoken audio.
            t = None
            if speaker == 0:
                t = pygame.mixer.Sound("audio/pilot.wav")
            if speaker == 1:
                t = pygame.mixer.Sound("audio/atc.wav")
            l = int(t.get_length()) + 1
            # OK. Generate white noise:
            noise = np.random.normal(0, 1, 8000 * l)
            # Normalize the white noise
            noise = noise / np.max(np.abs(noise))
            # Convert the white noise to a 16-bit format
            noise = (noise * 2**15).astype(np.int16)
            # Save that file too
            write('audio/noise.wav', 8000, noise)

            pygame.mixer.Channel(0).play(t)
        
            # Set white noise volume to 10%
            pygame.mixer.Channel(1).set_volume(0.05)
            # Place white noise in Channel 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio/noise.wav'))

            while pygame.mixer.Channel(0).get_busy():
                time.sleep(0.1)
            
            pygame.mixer.Channel(0).set_volume(0.4)
            pygame.mixer.Channel(0).play(click)

            while pygame.mixer.Channel(0).get_busy():
                time.sleep(0.1)

        curline = curline+1

    time.sleep(1)

#PiperVoice.load("./voices/" + atc_pilot_voice + "/low/en_US-"+atc_pilot_voice+"-low.onnx")
#with wave.open("test.wav", "wb") as wav_file:
#    voice.synthesize_wav("Welcome to the world of speech synthesis!", wav_file)


"""
def read_atc_log():
    atc_log = open("./Log_ATC.txt")
    lines = atc_log.readlines()
    for line in lines:
        if " Tx " in line:
            thisline = line.replace("\n", "")
            print(thisline)

read_atc_log()
"""