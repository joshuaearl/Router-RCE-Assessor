## What does it do

Using Python with asyncio and aiohttp it scans a block of IP addresses on port 80 and collects responses searching for devices with known RCE vulnerabilties.

## What was the inspiration for the project

After seeing this DEF CON talk (<a href="https://www.youtube.com/watch?v=nX9JXI4l3-E">DEF CON 22 - Mass Scanning the Internet</a>) I set out to see how easy it was to find open or vulnerable end points on the internet.

## Install

1) Install Python
2) Install the following dependancies, open the terminal & run:
pip install asyncio
pip install aiohttp

## Run

Open terminal and run: python routerAssess.py

## Note

A lot of the modules still need to be finished and quite a bit needs refactoring.

## LICENSE

GNU GPLv3