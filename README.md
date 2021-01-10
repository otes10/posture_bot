# posture_bot

### Requirements
On your Raspberry Pi, you will need to install the following:
- Every pip install as detailed in the `requirements.txt`
- Tensorflow 2+, [instructions here](https://www.youtube.com/watch?v=GNRg2P8Vqqs)

You will also need access to a [Raspberry Pi Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)!

> Note: due to time constraints, we have not tried building this project from scratch on a brand new Raspberry Pi image, so download at your own risk!

## Project Architecture

### How We built it

The **Discord bot** was built using Python following the Discord API documentation.

The **image taker** was built using Python and communicates to AWS's S3 service to store the data, and it was automated via a Cron task.

The **Posture API** was built using the Flask framework and its RESTful API example codes.

### Design Choices

**Why Raspberry Pi?**

We chose to go with a Raspberry Pi + Camera module due to the following reasons:
- Rapid hardware prototyping: this acts as a proof-of-concept for potential upgrades to USB webcams, or even dedicated PCB modules
- Cheap costs + hobbyist support: you can set up this project for around $150 max. (Pi + Camera module), compared to setting this up with a USB webcam and a dedicated computer ($???)
- Better photo angle: using a Laptop front camera would make it hard to analyze your back posture

**Why Discord bot?**

- Interest: something we wanted to work on!
- Ease of use: Discord bots are something many people have worked with and are starting to be more familiar with

## Our Mission
With the continued presence of COVID-19 in 2021, many students and professionals are now forced to study/work/be productive at home. One particular problem that this has caused is  

## Features
- ✅ Generate daily reports on your back posture!
- ✅ Generate reports based on specific time intervals!

### File Structure
- `api` contains code pertaining to the Flask API endpoint we developed
- `bot` contains code for the Discord bot that communicates with the API
- `model` contains code for the CNN model we trained

## Potential Next Steps...
These are potential next steps/implementations of this project:
- Add a hardware response when bad posture is detected (ie. servo arm slapping the user, buzzer beeping)
- Build dedicated hardware (ie. Pi compute module) for the project
- Utilize a more well-trained model to provide better results about posture
- Provide more features to the Discord bot