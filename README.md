<div>
  <img src="https://i.imgur.com/L3giCRt.png" alt="Your alt text" width="125" align="left">
    <h1><a href="https://www.openplugin.io/">OpenPlugin</h1>
  <h3>Integrate with OpenAI's ChatGPT plugins via API.<br/>The same powerful functionality as the ChatGPT api + plugins!</h3>
  <h3></h3>
</div>


[Join Discord Server](https://discord.gg/AfHcVutBUT) 

OpenPlugin official client, [openplugin.io](https://www.openplugin.io/), is now in closed beta!

## Supported plugins [PLUGINS.md](https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md)
<i>demo</i>


https://github.com/CakeCrusher/openplugin/assets/37946988/d35c704d-a007-4e5f-b3ea-03df264c0f4e

## Project structure
This repo contains 4 packages: [(pypi)`openplugincore`](https://github.com/CakeCrusher/openplugin/tree/main/pypi-core), [(npm) `openplugincore`](https://github.com/CakeCrusher/openplugin/tree/main/npm-core/openplugincore) [(pypi)`openpluginclient`](https://github.com/CakeCrusher/openplugin/tree/main/pypi-client), and [(npm)`openpluginclient`](https://github.com/CakeCrusher/openplugin/tree/main/npm-client/openpluginclient).

## Examples
- Bsic demo: https://colab.research.google.com/drive/1-CPYPbrj5tKsG30eUPhxHh1gwqa7wJgj?usp=sharing

## Core
This is the meat of OpenPlugin, it contains all tools you need to interface with ChatGPT plugins as you do on ChatGPT Pro.

### [PyPI Core Package](https://github.com/CakeCrusher/openplugin/tree/main/pypi-core)
### [NPM Core Package](https://github.com/CakeCrusher/openplugin/tree/main/npm-core/openplugincore)

## Client
This outsources the request to an OpenPlugin API that uses `openpluginclient`, so you dont need to worry about the OpenAI api key.
You will need to pass in one of the following `early access token`: `__extra__-c22a34e2-89a8-48b2-8474-c664b577526b`, `__extra__-692df72b-ec3f-49e4-a1ce-fb1fbc34aebd`
### [PyPI Client Package](https://github.com/CakeCrusher/openplugin/tree/main/pypi-client)
### [NPM Client Package](https://github.com/CakeCrusher/openplugin/tree/main/npm-client/openpluginclient)

<i>high level system design / docs</i>

![image](https://github.com/CakeCrusher/openplugin/assets/37946988/63da7efc-c556-495b-8738-9143b3faece1)

## Are you breaching OpenAI Terms of Service by using OpenPlugin?
No, I have gone through the Terms of Service particularly "service terms" and "usage policies" and  here are the takeaways.
As with most marketplace type things, the host, OpenAI, is not accountable for the plugins and their use outside of their platform `chat.openai.com`. They also never mention anything about accessing their data that is not explicitly shown to the user, therefore accessing their plugins' payload (how OpenPlugin gets knows about the marketplace plugins), which is used for them to display the plugins, is not against their ToS.

Primary sources:

https://openai.com/policies/terms-of-use

https://openai.com/policies/usage-policies

https://openai.com/policies/service-terms

## Disclaimer
As OpenPlugin is currently in an alpha state, you may run into errors. Despite some light testing being done by [migrations](https://github.com/CakeCrusher/openplugin-clients/blob/main/migrations/plugin_store/classifier.ipynb) not all plugins are thuroughly tested. If you run into any errors, please report them [here](https://github.com/CakeCrusher/openplugin-clients/issues/new?assignees=CakeCrusher&labels=bug&projects=&template=bug_report.md&title=).

The errors work on a plugin by plugin basis, meaning some will work perfectly while others may not work at all. Some of the errors may be caused by the plugin itself therefore will aso err on [https://chat.openai.com/](https://chat.openai.com/) so double checking would be advisable.



Join Discord for updates: https://discord.gg/AfHcVutBUT



