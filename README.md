# HackBI-2018 MuseBrainScan

### Winner of Best Hardware Hack at Hack Bishop Ireton 2018

## Inspiration
Disabilities like ALS, Stroke, and ADHD and many others cause speech impairment or even loss. This translates to over 7 million people in the US alone who aren't able to fully use their voice. Our hack hopes to use machine learning to give a voice to these affected people. 

## What it does
BrainScan gives speech impaired people a voice by converting their brain waves into audible speech through the Amazon Alexa. 

## How we built it
Hardware and Data Processing -- Used the Muse BrainSensing Headset to read brainwaves.  
Neural Networks -- Used the python keras library to convert brainwaves into readable text.  
Amazon Web Services -- Used AWS to create an Alexa skill that read out the readable text.  
## Challenges we ran into
We only had 1000 data points, which was not enough to effectively train our neural network model on. This limited the complexity of neural networks we were able to experiment with. 

## Accomplishments that we're proud of
We got our validation accuracy to rise higher than baseline, which was a huge accomplishment for us with regards to the scope of such a short time period.

## What we learned
We learned a lot about Amazon Web Services, specifically about Lambda Functions. Furthermore, we also learned more about the Keras neural network package. 

## What's next for BrainScan
We hope to implement the three step process with synchronous communication and have an instantaneous feedback loop that allows Alexa to say what the person is thinking in real time. 
