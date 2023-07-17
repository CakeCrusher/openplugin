import fs from 'fs/promises';
import path from 'path';
import { OpenPlugin } from 'openplugincore';
import { format } from 'date-fns';
import dotenv from 'dotenv';
dotenv.config();

const jsonPath = path.join(process.cwd(), '../openplugins_info.json');
const logPath = path.join(process.cwd(), '../migration.log');

const logToFile = async (message) => {
  const formattedMessage = `${format(new Date(), 'yyyy-MM-dd HH:mm:ss,SSS')} ${message}\n`;
  await fs.appendFile(logPath, formattedMessage);
}

const openpluginWhitelistJsTest = async (openpluginInfo) => {
  const openplugin = new OpenPlugin(undefined, "https://" + openpluginInfo.domain, process.env.OPENAI_API_KEY);
  await openplugin.init();
  
  return openplugin;
}

const openpluginStimulousJsTest = async (openpluginInfo, openplugin) => {
  await openplugin.fetchPlugin({
    prompt: openpluginInfo.stimulous_prompt,
    model: "gpt-3.5-turbo-0613",
    temperature: 0
  });
}

async function main() {
    try {
        const data = await fs.readFile(jsonPath, 'utf-8');
        const openpluginsInfo = JSON.parse(data);

        const openpluginsInfoKeys = Object.keys(openpluginsInfo)
        const openpluginsInfoLength = openpluginsInfoKeys.length
        let idx = 0

        for (const namespace of Object.keys(openpluginsInfo)) {
          logToFile(`${idx} JS Processing ${namespace}`)
          if (idx % 20 === 0) {
            console.log(`${idx} of ${openpluginsInfoLength}`)
          }
            
          const openpluginInfo = openpluginsInfo[namespace]
          const js_info = {
            whitelisted: false,
            stimulated: false,
          }

          if (!openpluginInfo.auth && !openpluginInfo.blacklisted) {
            try {
              const openplugin = await openpluginWhitelistJsTest(openpluginInfo)
              js_info.whitelisted = true
              logToFile(`${namespace} Whitelist Success`)
              try {
                await openpluginStimulousJsTest(openpluginInfo, openplugin)
                js_info.stimulated = true
                logToFile(`${namespace} Stimulate Success`)
              } catch (e) {
                logToFile(`${namespace} Stimulate Error: ${e}`)
              }
            } catch (e) {
              logToFile(`${namespace} Stimulate Error: ${e}`)
            }
          }

          openpluginsInfo[openpluginInfo.namespace] = {
            ...openpluginInfo,
            js_info
          }
          await fs.writeFile(jsonPath, JSON.stringify(openpluginsInfo, null, 2));
          logToFile(`JS ${namespace} Complete`)

          idx += 1
        }
    } catch (err) {
        console.error(`Error reading file from disk: ${err}`);
    }
}

main();
