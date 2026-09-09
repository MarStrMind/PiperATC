import sys
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import time
import glob
from xpapi import *

# -------------------------------------------------------------------
# Your call sign
# -------------------------------------------------------------------
atc_callsign = "DF"
atc_flightno = "MST"

# -------------------------------------------------------------------
# Do you want to see ATC messages in the console also?
# -------------------------------------------------------------------
atc_show_responses = True

# -------------------------------------------------------------------
# Define where your Pilot2ATC log is located.
# Remember to enable this in the software.
# -------------------------------------------------------------------
p2atc_log = "C:\\MarStr\\Simulator\\12\\Output\\Pilot2ATC_Log.txt"

# -------------------------------------------------------------------
# 124thATC is within X-Plane's log - adjust folder as needed
# -------------------------------------------------------------------
onetwofouratc_log = "C:\\Users\\windo\\Simulator\\12\\Log.txt"

# The plane you are flying
onetwofouratc_plane = ["Cirrus", "Vision Jet"]

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

if len(sys.argv) < 2:
    print("[ERR] No module specified. Exiting.")
    exit()

module = ""

if sys.argv[1] == "--pilot2atc":
    module = "Pilot2ATC"

if sys.argv[1] == "--124thatc":
    module = "124thATC"


# If we get here, we can probably use a module
print("  ")
print( "░█████████  ░██████░█████████  ░██████████ ░█████████        ░███    ░██████████  ░██████  ")
print( "░██     ░██   ░██  ░██     ░██ ░██         ░██     ░██      ░██░██       ░██     ░██   ░██ ")
print( "░██     ░██   ░██  ░██     ░██ ░██         ░██     ░██     ░██  ░██      ░██    ░██        ")
print( "░█████████    ░██  ░█████████  ░█████████  ░█████████     ░█████████     ░██    ░██        ")
print( "░██           ░██  ░██         ░██         ░██   ░██      ░██    ░██     ░██    ░██        ")
print( "░██           ░██  ░██         ░██         ░██    ░██     ░██    ░██     ░██     ░██   ░██ ")
print( "░██         ░██████░██         ░██████████ ░██     ░██    ░██    ░██     ░██      ░██████  ")
print("  ")
print(" Making X-Plane ATC sound more natural")
print(" ---------------------------------------------- ")
print(" Developed by MarStrMind")
print(" License: MIT")
print(" ---------------------------------------------- ")
print(" Module: " + module)
print(" ---------------------------------------------- ")

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

# Some things for phonetics

number_replace = [
    ("0", "Zero "),
    ("1", "One "),
    ("2", "Two "),
    ("3", "Three "),
    ("4", "Four "),
    ("5", "Fiver "),
    ("6", "Six "),
    ("7", "Seven "),
    ("8", "Eight "),
    ("9", "Niner "),
    ("IFR", "I F R "),
    ("VFR", "V F R ")
]

decimal_replace = [
    (".0", "decimal Zero "),
    (".1", "decimal One "),
    (".2", "decimal Two "),
    (".3", "decimal Three "),
    (".4", "decimal Four "),
    (".5", "decimal Fiver "),
    (".6", "decimal Six "),
    (".7", "decimal Seven "),
    (".8", "decimal Eight "),
    (".9", "decimal Niner ")
]


# Some additions we can smuggle in to make some interactions even more realistic

clearance_additionals = [
    "Give me a moment. ",
    "Hold on a second, let me check something real quick. ",
    "I'll be right with you. ",
    "One second, I'll be right with you. ",
    "Stand by, let me pull your flight plan. ",
    "Give me a moment, I’m coordinating. ",
    "Hang on, I’ll get back to you. "
]

handoff_additionals = [
    "Good day. ",
    "Have a nice flight. ",
    "Alright. ",
    "See you. ",
    "So long. "
]

# Current line and last line read from the log file
curline  = 0
lastline = 0

# Colorful console
colorama_init()

# ATC voices folder
atc_voices = glob.glob(".\\voices\\*")

# Initial empty ATC voice
atc_voice = ""

# We assume you listen to ATC on COM1
cur_freq = ""

# ICAO codes
icao_codes = []
icao_file = open("./icao.txt")
icao_lines = icao_file.readlines()
for icao in icao_lines:
    icao = icao.replace("\n", "")
    if icao != "":
        icao_codes.append(icao)
print (" Loaded " + str(len(icao_codes)) + " ICAO codes")
print("")


# COM1 frequency
xpapi = mst_xplane_api()
xpdrefs = xpapi.xp_request("get", "datarefs")
com1id = xpapi.find_dataref_id("sim/cockpit/radios/com1_freq_hz", xpdrefs["data"])
print(" Connected to X-Plane API")
print(" ---------------------------------------------- ")


# ---------------------------------------
# 124TH ATC
# ---------------------------------------
if sys.argv[1] == "--124thatc":

    # Monitor mode
    if len(sys.argv) == 3 and sys.argv[2] == "--monitor":
        print("")
        print(" -- MONITOR MODE -- ")
        print("")
        print(" ---------------------------------------------- ")
        while True:
            atc_log = open(onetwofouratc_log)
            lines = atc_log.readlines()
            curline = 0
            for line in lines:
                if "124thATC" in line and "Communication: " in line and curline > lastline:
                    lastline = curline
                    thisline = line.replace("\n", "")
                    linedata = thisline.split(": ")
                    lineparts = linedata[2].split(" ")
                    speaker = 0
                    if lineparts[0] == atc_callsign and lineparts[1] == atc_flightno:
                        speaker = 1
                    else:
                        speaker = 0
                    
                    if speaker == 1:
                        print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + linedata[1] + f'{Style.RESET_ALL}')
                        print(" ------------------------------------------------------- ")
                    if speaker == 0:
                        print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + linedata[2] + f'{Style.RESET_ALL}')
                        print(" ------------------------------------------------------- ")
                curline = curline+1
            time.sleep(1)

    import os
    import wave
    import random
    from random import randrange
    import pygame
    import numpy as np
    from pydub import AudioSegment as am
    from scipy.io.wavfile import write
    from piper import PiperVoice

    if len(sys.argv) < 3:    
        controller_changed = True

        initial_call = True

        # We only need to load this once
        pilotvoice = PiperVoice.load("./voices/" + atc_pilot_voice + "/" + atc_pilot_quality + "/en_US-"+atc_pilot_voice+"-"+atc_pilot_quality+".onnx")

        # Init pygame and its mixer
        pygame.init()
        pygame.mixer.init()

        # The click at the end of a transmission
        click = pygame.mixer.Sound("./audio/endclick.wav")

        # A variable to determine whether or not the controller is rather busy
        # This may change at any time, at random
        controller_busy = False

        while True:
            atc_log = open(onetwofouratc_log)
            lines = atc_log.readlines()
            curline = 0
            for line in lines:
                if "124thATC" in line and "Communication: " in line and curline > lastline:

                    # If he/she is busy, some additional sentences may be spoken for added realism
                    controller_busy = random.choice([True, False])
                    
                    freq = xpapi.get_value_from_dref_id(com1id)
                    
                    if cur_freq == "" or cur_freq != freq["data"]:
                        cur_freq = freq["data"]
                        controller_changed = True
                    else:
                        controller_changed = False

                    lastline = curline
                    thisline = line.replace("\n", "")
                    linedata = thisline.split(": ")
                    speaker = 0
                    
                    nato1_phonetic = ""
                    nato2_phonetic = ""

                    speakline = ""

                    linedata[2] = linedata[2].encode('latin-1').decode('utf-8')
                    
                    lineparts = linedata[2].split(" ")
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

                            plnrpl = randrange(1, 11)
                            if plnrpl in {1, 3, 6, 9}:
                                spkln = ""
                                for lp in lineparts:
                                    spkln = spkln + lp + " "
                                
                                rpl = ""
                                rpl2 = randrange(1, 11)
                                if rpl2 in {1, 4, 8, 10}:
                                    rpl = onetwofouratc_plane[0] + " " + onetwofouratc_plane[1]
                                spkln = spkln.replace("good morning", rpl)
                                spkln = spkln.replace("good afternoon", rpl)
                                spkln = spkln.replace("good evening", rpl)
                                linedata[2] = linedata[2].replace("good morning", rpl)
                                linedata[2] = linedata[2].replace("good afternoon", rpl)
                                linedata[2] = linedata[2].replace("good evening", rpl)
                                lineparts = spkln.split(" ")

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

                            plnrpl = randrange(1, 11)
                            if plnrpl in {1, 3, 6, 9}:
                                spkln = ""
                                for lp in lineparts:
                                    spkln = spkln + lp + " "
                                
                                rpl = ""
                                rpl2 = randrange(1, 11)
                                if rpl2 in {1, 4, 8, 10}:
                                    rpl = onetwofouratc_plane[0] + " " + onetwofouratc_plane[1]
                                spkln = spkln.replace("good morning", rpl)
                                spkln = spkln.replace("good afternoon", rpl)
                                spkln = spkln.replace("good evening", rpl)
                                linedata[2] = linedata[2].replace("good morning", rpl)
                                linedata[2] = linedata[2].replace("good afternoon", rpl)
                                linedata[2] = linedata[2].replace("good evening", rpl)
                                lineparts = spkln.split(" ")

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
                    for d in decimal_replace:
                        speakline = speakline.replace(d[0], d[1])
                    for d in number_replace:
                        speakline = speakline.replace(d[0], d[1])

                    for icao in icao_codes:
                        if icao in speakline:
                            ltr = list(icao)
                            newstr = ""
                            for l in ltr:
                                newstr = newstr + l + " "
                            speakline = speakline.replace(icao, newstr)
                            break

                    # Let's define that here
                    busyline = clearance_additionals[randrange(0, len(clearance_additionals))]

                    if atc_show_responses == True:
                        if speaker == 0:
                            print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + linedata[2] + f'{Style.RESET_ALL}')
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
                        
                        # Controller may add your plane type to announcements
                        add_plane = randrange(0, 11)
                        if add_plane == 3 or add_plane == 5 or add_plane == 7:
                            speakline = onetwofouratc_plane[1] + " " + speakline
                            linedata[2] = onetwofouratc_plane[1] + " " + linedata[2]

                        # We can add some "goodbye" realism to the end
                        add_goodbye = randrange(0, 11)
                        if " contact " in linedata[2] and " on " in linedata[2]:
                            if add_goodbye == 3 or add_goodbye == 5 or add_goodbye == 7:
                                gb = handoff_additionals[randrange(0, len(handoff_additionals))]
                                speakline = speakline + " " + gb
                                linedata[2] = linedata[2] + " " + gb

                        with wave.open("audio/t_atc.wav", "wb") as wav_file:
                            atcvoice.synthesize_wav(speakline, wav_file)

                        # Sneak in some realism...

                        # At initial request or when controller was changed,
                        # we can make the controller appear busy
                        if initial_call == True or controller_changed == True:
                            if controller_busy == True:
                                if atc_show_responses == True:
                                    print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + busyline + f'{Style.RESET_ALL}')
                                    print(" ------------------------------------------------------- ")
                                with wave.open("audio/t_atc_busy.wav", "wb") as wav_busy_file:
                                    atcvoice.synthesize_wav(busyline, wav_busy_file)
                                busysound = am.from_file("audio/t_atc_busy.wav", format='wav')
                                busysound = busysound.set_frame_rate(8000)
                                busysound.export("audio/atcbusy.wav", format='wav')

                                bs = pygame.mixer.Sound("audio/atcbusy.wav")
                                b = int(bs.get_length()) + 1
                                noisebusy = np.random.normal(0, 1, 8000 * b)
                                # Normalize the white noise
                                noisebusy = noisebusy / np.max(np.abs(noisebusy))
                                # Convert the white noise to a 16-bit format
                                noisebusy = (noisebusy * 2**15).astype(np.int16)
                                # Save that file too
                                write('audio/noisebusy.wav', 8000, noisebusy)

                                pygame.mixer.Channel(0).play(bs)
                                # Set white noise volume to 10%
                                pygame.mixer.Channel(1).set_volume(0.05)
                                # Place white noise in Channel 1
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio/noisebusy.wav'))

                                while pygame.mixer.Channel(0).get_busy():
                                    time.sleep(0.1)
                                
                                pygame.mixer.Channel(0).set_volume(0.4)
                                pygame.mixer.Channel(0).play(click)

                                while pygame.mixer.Channel(0).get_busy():
                                    time.sleep(0.1)

                                time.sleep(random.uniform(1.9, 3.2))

                        sound = am.from_file("audio/t_atc.wav", format='wav')
                        sound = sound.set_frame_rate(8000)
                        sound.export("audio/atc.wav", format='wav')
                    

                    # Console output
                    if atc_show_responses == True:
                        if speaker == 1:
                            print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + linedata[2] + f'{Style.RESET_ALL}')
                            print(" ------------------------------------------------------- ")
                    
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


# ---------------------------------------
# PILOT2ATC
# ---------------------------------------

if sys.argv[1] == "--pilot2atc":

    # Monitor mode
    if len(sys.argv) == 3 and sys.argv[2] == "--monitor":
        print("")
        print(" -- MONITOR MODE -- ")
        print("")
        print(" ---------------------------------------------- ")
        while True:
            atc_log = open(p2atc_log)
            lines = atc_log.readlines()
            curline = 0
            for line in lines:
                if "ATC: " in line and curline > lastline:
                    lastline = curline
                    thisline = line.replace("\n", "")
                    linedata = thisline.split("ATC: ")
                    print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + linedata[1] + f'{Style.RESET_ALL}')
                    print(" ------------------------------------------------------- ")
                curline = curline+1
            time.sleep(1)

    import os
    import wave
    import random
    from random import randrange
    import pygame
    import numpy as np
    from pydub import AudioSegment as am
    from scipy.io.wavfile import write
    from piper import PiperVoice

    if len(sys.argv) < 3:    
        controller_changed = False

        # We only need to load this once
        pilotvoice = PiperVoice.load("./voices/" + atc_pilot_voice + "/" + atc_pilot_quality + "/en_US-"+atc_pilot_voice+"-"+atc_pilot_quality+".onnx")

        # Init pygame and its mixer
        pygame.init()
        pygame.mixer.init()

        # The click at the end of a transmission
        click = pygame.mixer.Sound("./audio/endclick.wav")

        while True:
            atc_log = open(p2atc_log)
            lines = atc_log.readlines()
            curline = 0
            for line in lines:
                if ("ATC: " in line or "Pilot: " in line) and curline > lastline:

                    freq = xpapi.get_value_from_dref_id(com1id)
                    
                    if cur_freq == "" or cur_freq != freq["data"]:
                        cur_freq = freq["data"]
                        controller_changed = True
                    else:
                        controller_changed = False

                    lastline = curline
                    thisline = line.replace("\n", "")
                    linedata = []
                    if "ATC: " in line:
                        linedata = thisline.split("ATC: ")
                    if "Pilot: " in line:
                        linedata = thisline.split("Pilot: ")
                    
                    nato1_phonetic = ""
                    nato2_phonetic = ""

                    speakline = ""

                    linedata[1] = linedata[1].encode('latin-1').decode('utf-8')
                    
                    lineparts = linedata[1].split(" ")
                    lineparts[1] = lineparts[1].replace(",", "")
                    
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

                    for d in decimal_replace:
                        speakline = speakline.replace(d[0], d[1])
                    for d in number_replace:
                        speakline = speakline.replace(d[0], d[1])

                    for icao in icao_codes:
                        if icao in speakline:
                            ltr = list(icao)
                            newstr = ""
                            for l in ltr:
                                newstr = newstr + l + " "
                            speakline = speakline.replace(icao, newstr)
                            break

                    if atc_show_responses == True:
                            #print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + speakline + f'{Style.RESET_ALL}')
                        if "ATC: " in line:
                            print(f' {Fore.GREEN}[ ATC ] {Fore.CYAN}' + linedata[1] + f'{Style.RESET_ALL}')
                            print(" ------------------------------------------------------- ")
                        if "Pilot: " in line:
                            print(f' {Fore.YELLOW}[PILOT] {Fore.WHITE}' + linedata[1] + f'{Style.RESET_ALL}')
                            print(" ------------------------------------------------------- ")

                    if "ATC: " in line:
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

                    if atc_captain_voice == True and "Pilot: " in line:
                        with wave.open("audio/t_pilot.wav", "wb") as wav_file:
                            pilotvoice.synthesize_wav(speakline, wav_file)

                        sound = am.from_file("audio/t_pilot.wav", format='wav')
                        sound = sound.set_frame_rate(8000)
                        sound.export("audio/pilot.wav", format='wav')
                    
                    # Get length of spoken audio.
                    t = None
                    if "ATC: " in line:
                        t = pygame.mixer.Sound("audio/atc.wav")
                    if atc_captain_voice == True and "Pilot: " in line:
                        t = pygame.mixer.Sound("audio/pilot.wav")

                    if t is not None:
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
