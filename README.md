# Piper ATC

A small script to make ATC for X-Plane more natural sounding.

## Supported ATCs

- X-Plane 12 built-in
- 124thATC
- Pilot2ATC

## Requirements

- Windows, Linux (or Unix-like), macOS
- Python 3.13+
- Ability to install modules globally or locally
- Piper voices located in the ```voices``` inside the directory of these scripts.

It is my strong recommendation to create a virtual environment in the folder of these scripts. Then, navigate into the directory where this script is located, and run:

```pip install -f ./requirements.txt```

This will install all modules you need.

## Piper voices

Should you not have it, create the folder "voices" in this folder - meaning, where you have placed the scripts from this repo.

Additionally, and naturally, you will need a set of Piper voices. As I like to keep this in english language (as it should be for ATC communications), you should acquire all en-US and en-GB voices from here: https://huggingface.co/rhasspy/piper-voices/tree/main . Download the entire archive as zip, extract it somewhere and navigate into the "en" folder.

There you will find two sub-folders: en-GB and en-US.

Navigate into each one separately and copy the folders into the "voices" folder which I just mentioned.

## Configuration

Now, you will need to make a few adjustments.

### 124thATC

Open the file 124thATC.py from this repo.

First, adjust your callsign and flight number. Must match what you entered in the config of 124th ATC.

Then, adjust the path to the standard log file of X-Plane 12. Currently, it is my installation path - so you will have to change that.

And finally, you will need to pick a "captain's" or "first officer" voice - if you want to hear that. If not, the setting above your choice of voice will disable verbal readbacks and requests, and only plays ATC communications.

If you want to hear your requests as well, choose a voice. To speed things up for you, you can go to https://rhasspy.github.io/piper-samples/ and have a listen to the voices that are available. Then, put in what you want.

### Pilot2ATC

You will first need to enable logging into a text file within the application itself. This text file can be anywhere you like - but you need to know where it is.

You will also need to reduce the volume of speech within the application to 0%. Otherwise you will hear PiperATC and the sound from Pilot2ATC. You will probably not want that.

Open pilot2atc.py in your favorite text editor. Adjust your callsign and flight number at the top. Must match what you entered in the config of Pilot2ATC.

Finally, you will need to pick a "captain's" or "first officer" voice - if you want to hear that. If not, the setting above your choice of voice will disable verbal readbacks and requests, and only plays ATC communications.

If you want to hear your requests as well, choose a voice. To speed things up for you, you can go to https://rhasspy.github.io/piper-samples/ and have a listen to the voices that are available. Then, put in what you want.


### X-Plane ATC

Theoretically works, but it is not real-time as I found out. You can try this script but I found it be immersion-breaking if the ATC transmission is not happening when it happens in the simulator. This is due to the log file not being populated on an ATC transmission... for whatever reason.


## Sound output

I do not yet have the option to choose a sound device for output... so it is best if you pick the audio device for X-Plane exterior sounds first - then select your headphone output in your sound settings - THEN start the script. This should give you a relatively realistic experience.

## Running

- Strong recommendation: start X-Plane first, and then be in your cockpit.
- Open a terminal window of your choice, navigate to this folder and do a

```python ./[script to run]```

So for example with 124thATC:

```python ./124thATC.py```

Adjust if you have a virtual environment.

You should now hear your ATC with Piper TTS voices.