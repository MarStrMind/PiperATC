# Piper ATC

A small script to make ATC for X-Plane more natural sounding.

## Supported ATCs

- X-Plane 12 built-in
- 124thATC

## Requirements

- Python 3.13+

You will need the following packages in your Python install - either globally or in a virtual environment (venv):

- pygame
- numpy
- pydub
- colorama
- scipy
- piper

Should you not have it, create the folder "voices" in this folder - meaning, where you have placed the scripts from this repo.

Additionally, and naturally, you will need a set of Piper voices. As I like to keep this in english language (as it should be for ATC communications), you should acquire all en-US and en-GB voices from here: https://huggingface.co/rhasspy/piper-voices/tree/main . Download the entire archive as zip, extract it somewhere and navigate into the "en" folder.

There you will find two sub-folders: en-GB and en-US.

Navigate into each one separately and copy the folders into the "voices" folder which I just mentioned.

## Configuration

Now, you will need to make a few adjustments.

Let's use a nicely working example - 124thATC.

Open the file 124thATC.py from this repo.

First, adjust your callsign and flight number. Must match what you entered in the config of 124th ATC.

Then, adjust the path to the standard log file of X-Plane 12. Currently, it is my installation path - so you will have to change that.

And finally, you will need to pick a "captain's" or "first officer" voice - if you want to hear that. If not, the setting above your choice of voice will disable verbal readbacks and requests, and only plays ATC communications.

If you want to hear your requests as well, choose a voice. Do speed things up for you, you can go to https://rhasspy.github.io/piper-samples/ and have a listen to the voices that are available. Then, put in what you want.

## Sound output

I do not yet have the option to choose a sound device for output... so it is best if you pick the audio device for X-Plane exterior sounds first - then select your headphone output in your sound settings - THEN start the script. This should give you a relatively realistic experience.

## Running

Strong recommendation: start X-Plane first.

Then, open a terminal window of your choice, navigate to this folder and do a

python ./[script to run]

So for example with 124thATC:

python ./124thATC.py

Adjust if you have a virtual environment.

## Notes

While X-Plane 12 ATC works, it is not real time. For some reason, the log file from X-Plane does not seem to be updated in real time or in the very least, in small time increments - so I cannot guarantee for this to work well.