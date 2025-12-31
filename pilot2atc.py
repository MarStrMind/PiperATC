import os
import glob
import wave
import random
from random import randrange
import time
import pygame
import numpy as np
from pydub import AudioSegment as am
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from scipy.io.wavfile import write
from piper import PiperVoice


# -------------------------------------------------------------------
# Your call sign
# -------------------------------------------------------------------
atc_callsign = "DF"
#atc_callsign = "MST"
atc_flightno = "MST"
#atc_flightno = "612"

# -------------------------------------------------------------------
# Do you want to see ATC messages in the console also?
# -------------------------------------------------------------------
atc_show_responses = True

# -------------------------------------------------------------------
# Define where your Pilot2ATC log is located.
# Remember to enable this in the software.
# -------------------------------------------------------------------
atc_xplane_log = "C:\\Users\\windo\\Simulator\\12\\Pilot2ATC.txt"
#atc_xplane_log = "./Log_ATC.txt"

# -------------------------------------------------------------------
# The data file containing your tuned frequencies. Need to enable
# that in settings, so we can read from this file.
# -------------------------------------------------------------------
atc_xplane_data = "C:\\Users\\windo\\Simulator\\12\\Data.txt"

# -------------------------------------------------------------------
# Do you want to hear "your voice" when contacting ATC?
# Strong recommendation to leave this at False for Pilot2ATC,
# if you are talking yourself!
# -------------------------------------------------------------------
atc_captain_voice = False

# -------------------------------------------------------------------
# Select your pilot's voice
# See the voices folder and pick one
# -------------------------------------------------------------------
atc_pilot_voice = "hfc_male"
atc_pilot_quality = "medium"

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

# The spaces are intentional
nato_alphabet = [
    ["A", "Alpha "],
    ["B", "Bravo "],
    ["C", "Charlie "],
    ["D", "Delta "],
    ["E", "Echo "],
    ["F", "Foxtrot "],
    ["G", "Golf "],
    ["H", "Hotel "],
    ["I", "India "],
    ["J", "Juliet "],
    ["K", "Kilo "],
    ["L", "Lima "],
    ["M", "Mike "],
    ["N", "November "],
    ["O", "Oscar "],
    ["P", "Papa "],
    ["Q", "Quebec "],
    ["R", "Romeo "],
    ["S", "Sierra "],
    ["T", "Tango "],
    ["U", "Uniform "],
    ["V", "Victor "],
    ["W", "Whiskey "],
    ["X", "Xray "],
    ["Y", "Yankee "],
    ["Z", "Zulu "]
]

colorama_init()

print("  ")
print(" ---------------------------------------------- ")
print("    _  __      ____  __    ___    _   ________   ____  ________  __________ ")
print("   | |/ /     / __ \\/ /   /   |  / | / / ____/  / __ \\/  _/ __ \\/ ____/ __ \\")
print("   |   /_____/ /_/ / /   / /| | /  |/ / __/    / /_/ // // /_/ / __/ / /_/ /")
print("  /   /_____/ ____/ /___/ ___ |/ /|  / /___   / ____// // ____/ /___/ _, _/") 
print(" /_/|_|    /_/   /_____/_/  |_/_/ |_/_____/  /_/   /___/_/   /_____/_/ |_|")
print("  ")
print(" Making X-Plane ATC sound more natural")
print(" ---------------------------------------------- ")
print(" Developed by MarStrMind")
print(" License: MIT")
print(" ---------------------------------------------- ")
print(" Using file: " + atc_xplane_log)
print(" ---------------------------------------------- ")
print(" Module: Pilot2ATC")
print(" ---------------------------------------------- ")

atc_voices = glob.glob(".\\voices\\*")

curline  = 0
lastline = 0
atc_voice = ""
initial_call = True

# We assume you listen to ATC on COM1
cur_freq = ""

# We only need to load this once
pilotvoice = PiperVoice.load("./voices/" + atc_pilot_voice + "/" + atc_pilot_quality + "/en_US-"+atc_pilot_voice+"-"+atc_pilot_quality+".onnx")

# Init pygame and its mixer
pygame.init()
pygame.mixer.init()

# The click at the end of a transmission
click = pygame.mixer.Sound("./audio/endclick.wav")

icao_codes = []
icao_file = open("./icao.txt")
icao_lines = icao_file.readlines()
for icao in icao_lines:
    icao = icao.replace("\n", "")
    if icao != "":
        icao_codes.append(icao)
print (" Loaded " + str(len(icao_codes)) + " ICAO codes")
print("")

while True:
    data_log = open(atc_xplane_data)
    data_lines = data_log.readlines()
    freqdata = data_lines[len(data_lines)-1].split(" |  ")
    freqdata[0] = freqdata[0].replace(" ", "")
    
    controller_changed = False
    if cur_freq == "" or cur_freq != freqdata[0]:
        cur_freq = freqdata[0]
        controller_changed = True
    data_log.close()

    atc_log = open(atc_xplane_log)
    lines = atc_log.readlines()
    curline = 0
    for line in lines:
        if "      ATC: " in line and curline > lastline:
            lastline = curline
            thisline = line.replace("\n", "")
            linedata = thisline.split("      ATC: ")
            speaker = 1
            
            nato1_phonetic = ""
            nato2_phonetic = ""

            speakline = ""

            linedata[1] = linedata[1].encode('latin-1').decode('utf-8')
            
            lineparts = linedata[1].split(" ")
            lineparts[1] = lineparts[1].replace(",", "")
            if lineparts[0] == atc_callsign and lineparts[1] == atc_flightno:
                speaker = 1
                nato1 = list(lineparts[0])
                nato2 = list(lineparts[1])
                for n in nato1:
                    for l in nato_alphabet:
                        if l[0] == n:
                            nato1_phonetic = nato1_phonetic + l[1]
                            break
                for n in nato2:
                    for l in nato_alphabet:
                        if l[0] == n:
                            nato2_phonetic = nato2_phonetic + l[1]
                            break
                        
                lineparts[0] = lineparts[0].replace(atc_callsign, nato1_phonetic)
                lineparts[1] = lineparts[1].replace(atc_flightno, nato2_phonetic)

            else:
                speaker = 0
                if initial_call == False:
                    nato1 = list(lineparts[len(lineparts)-2])
                    nato2 = list(lineparts[len(lineparts)-1])
                    for n in nato1:
                        for l in nato_alphabet:
                            if l[0] == n:
                                nato1_phonetic = nato1_phonetic + l[1]
                                break
                    for n in nato2:
                        for l in nato_alphabet:
                            if l[0] == n:
                                nato2_phonetic = nato2_phonetic + l[1]
                                break
                    
                    lineparts[len(lineparts)-2] = lineparts[len(lineparts)-2].replace(atc_callsign, nato1_phonetic)
                    lineparts[len(lineparts)-1] = lineparts[len(lineparts)-1].replace(atc_flightno, nato2_phonetic)
                else:
                    initial_call = False
                    for lp in range(0, len(lineparts)):
                        if atc_callsign in lineparts[lp]:
                            nato1 = list(lineparts[lp])
                            for n in nato1:
                                for l in nato_alphabet:
                                    if l[0] == n:
                                        nato1_phonetic = nato1_phonetic + l[1]
                                        break
                            lineparts[lp] = lineparts[lp].replace(atc_callsign, nato1_phonetic)
                    for lp in range(0, len(lineparts)):
                        if atc_flightno in lineparts[lp]:
                            nato2 = list(lineparts[lp])
                            for n in nato2:
                                for l in nato_alphabet:
                                    if l[0] == n:
                                        nato2_phonetic = nato2_phonetic + l[1]
                                        break
                            lineparts[lp] = lineparts[lp].replace(atc_flightno, nato2_phonetic)

            for lp in lineparts:
                speakline = speakline + lp + " "


            if atc_voice == "" or controller_changed == True:
                vcfound = False
                while vcfound == False:
                    vc = randrange(0, len(atc_voices))
                    if atc_pilot_voice not in atc_voices[vc]:
                        avc = atc_voices[vc].replace(".\\voices\\", "")
                        atc_voice = avc
                        vcfound = True
            
            
            special_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss', ord('Ä'):'Ae', ord('Ö'):'Oe', ord('Ü'):'Ue'}
            speakline = speakline.translate(special_char_map)

            speakline = speakline.replace(".0", "decimal Zero ")
            speakline = speakline.replace(".1", "decimal One ")
            speakline = speakline.replace(".2", "decimal Two ")
            speakline = speakline.replace(".3", "decimal Three ")
            speakline = speakline.replace(".4", "decimal Four ")
            speakline = speakline.replace(".5", "decimal Fiver ")
            speakline = speakline.replace(".6", "decimal Six ")
            speakline = speakline.replace(".7", "decimal Seven ")
            speakline = speakline.replace(".8", "decimal Eight ")
            speakline = speakline.replace(".9", "decimal Niner ")

            speakline = speakline.replace("0", "Zero ")
            speakline = speakline.replace("1", "One ")
            speakline = speakline.replace("2", "Two ")
            speakline = speakline.replace("3", "Three ")
            speakline = speakline.replace("4", "Four ")
            speakline = speakline.replace("5", "Fiver ")
            speakline = speakline.replace("6", "Six ")
            speakline = speakline.replace("7", "Seven ")
            speakline = speakline.replace("8", "Eight ")
            speakline = speakline.replace("9", "Niner ")
        
            speakline = speakline.replace("IFR", "I F R")
            speakline = speakline.replace("VFR", "V F R")

            for icao in icao_codes:
                if icao in speakline:
                    ltr = list(icao)
                    newstr = ""
                    for l in ltr:
                        newstr = newstr + l + " "
                    speakline = speakline.replace(icao, newstr)
                    break

            if atc_show_responses == True:
                if speaker == 1:
                    #print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + speakline + f'{Style.RESET_ALL}')
                    print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + linedata[1] + f'{Style.RESET_ALL}')
                if speaker == 0:
                    #print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + speakline + f'{Style.RESET_ALL}')
                    print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + linedata[1] + f'{Style.RESET_ALL}')
                print(" ------------------------------------------------------- ")

            if speaker == 0:
                if atc_captain_voice == True:
                    with wave.open("audio/t_pilot.wav", "wb") as wav_file:
                        pilotvoice.synthesize_wav(speakline, wav_file)

                    sound = am.from_file("audio/t_pilot.wav", format='wav')
                    sound = sound.set_frame_rate(8000)
                    sound.export("audio/pilot.wav", format='wav')

            if speaker == 1:
                qlt = ["high", "medium", "low"]
                atcvoice = None
                qlty = -1
                for q in range(0, 3):
                    if os.path.isfile("./voices/"+atc_voice+"/"+qlt[q]+"/en_US-"+atc_voice+"-"+qlt[q]+".onnx") == True:
                        atcvoice = PiperVoice.load("./voices/"+atc_voice+"/"+qlt[q]+"/en_US-"+atc_voice+"-"+qlt[q]+".onnx")
                        qlty = q
                        break
                for q in range(0, 3):
                    if os.path.isfile("./voices/"+atc_voice+"/"+qlt[q]+"/en_GB-"+atc_voice+"-"+qlt[q]+".onnx") == True:
                        atcvoice = PiperVoice.load("./voices/"+atc_voice+"/"+qlt[q]+"/en_GB-"+atc_voice+"-"+qlt[q]+".onnx")
                        qlty = q
                        break
                
                with wave.open("audio/t_atc.wav", "wb") as wav_file:
                    atcvoice.synthesize_wav(speakline, wav_file)

                sound = am.from_file("audio/t_atc.wav", format='wav')
                sound = sound.set_frame_rate(8000)
                sound.export("audio/atc.wav", format='wav')
            

            # Get length of spoken audio.
            t = None
            if speaker == 0 and atc_captain_voice == True:
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
