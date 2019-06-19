# Robert Baratheon - Bobby B

![BOW YA SHITS](https://i.redd.it/k7k0lnlihdiz.jpg)

This bot - ahem, will reply with a random Bobby-B (he's not sentient, yet) quote on your GitHub issues, when summoned.

## How to install?
1. Go to the Github repository in which you want Bobby-B to participate.
2. Click on the settings tab. The repository settings, not the user settings.
3. Go to webhooks, and click on the button: `Add webhook`.
4. Enter the payload URL as: https://bobby-b-bott.herokuapp.com/
5. Content type should be as `application/json`
6. Enter a random secret key (which you will be using on Heroku)(don't forget it)
7. Select `Let me select individual events.` and select `issues` and `Issue Comments`.
8. Add the webhook!

Further steps TBA...
