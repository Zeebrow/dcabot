# DCABOT
I'm sick and tired of getting ass-blasted by fees from all of the different crypto apps. 
$1.00 fee on a $5.00 order in the Gemini app! Ridiculous!

Meanwhile, Gemini API charges a taker fee of 0.35% - That's $0.0175. And that's the highest the fee goes. Wow.

I could use Robinhood for "free crypto trades", but you don't actually own any crypto you buy with their platform. I'm not about that.

## Why this project sucks
Despite the fact that this project currently works, there are many parts of the code I hope to change some day. Here are a few TODOs:

### main
Way too complex for such a simple function.
Yes, I used dca_bot as a project to learn, but the cost of this has been maintainability. There is a lot of functionality that I have to remember, whereas the functionality should be discernable in as few lines of code as possible (in this case).

### directory structure
For some reason, I decided against putting Virtualenv resources in thier own directory. Chaos.
For future projects, I'll stick to using the venv/ directory in the default directory that `git clone` creates.

I still need to learn more about how to setup directories for importing modules.
cbpro basically puts all source code into a directroy with the same name as what you install with pip: `cbpro`. There's probably a utilitarian reason for this.

### tests
There are none!! I was too lazy to learn! My tests/ directory is what I used for testing how code works. Should use tmp/ for this and .gitignore it.

### configuration
I believe a configuration script should do two things: 1) grab configuration values from a file, and 2) provide those values to the modules that imports it. 
I don't believe that a configuration file should provide functions to a module that imports it. config.py 



## Overview
- Use bot to daily buy $X of crypto

# Tech
The purpose of this project is to learn various tech (on top of accumulating crypto). For lack of a better title, this is an overview of the tools used in the project, in the context of how I'm learning about them.
For example, I understand "logging" isn't what you might think of as a tool, but it is something I'm learning how to do with Python. So I included it in as a tech topic.

## Python 3
Topics:
- Directory and file structure
- Best-practices for coding
- Logging
- Configuration and secrets management

## ELK stack integration
To give me a head start for things I will be working with professionally.
Topics:
- Elasticsearch
	- Parse logs to build a searchable database of information. E.g. Search through a list of all buy orders, and return the price each was bought at.
	- NOTE: add line `-Djava.net.preferIPv4Stack=true` in jvm.options
- Logstash
	- Using a Logstash custom logging.Handler to write logs directly to Logstash. 
- Kibana
	- ???
