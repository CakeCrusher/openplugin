import 'isomorphic-fetch';

const SUPPORTED_MODELS = ['gpt-4-0613', 'gpt-3.5-turbo-0613'];

// function getSupportedPlugins() {
//   const filePath = path.join(__dirname, 'plugins.json');
//   const data = fs.readFileSync(filePath, 'utf-8');
//   return JSON.parse(data);
// }

interface OpenPluginArgs {
  earlyAccessToken: string;
  pluginName?: string;
  failSilently?: boolean;
  [chatgptArg: string]: any;
}

export const openpluginCompletion = async (args: OpenPluginArgs) => {
  const {
    earlyAccessToken,
    pluginName,
    failSilently = false,
    ...chatgptArgs
  } = args;

  if (!earlyAccessToken) {
    throw new Error('An early access token must be provided.');
  }

  chatgptArgs.model = chatgptArgs.model || 'gpt-3.5-turbo-0613';
  if (!SUPPORTED_MODELS.includes(chatgptArgs.model)) {
    throw new Error(
      `Unsupported model: ${chatgptArgs.model}. Try 'gpt-4-0613' or 'gpt-3.5-turbo-0613'.`
    );
  }

  // const supportedPlugins = getSupportedPlugins();
  // if (pluginName && !supportedPlugins.hasOwnProperty(pluginName)) {
  //   throw new Error(
  //     `Unsupported plugin '${pluginName}'. For full list of supported plugins, visit https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md .`
  //   );
  // }

  if (!chatgptArgs?.messages) {
    throw new Error(
      'Messages must be passed to the openplugin_completion function.'
    );
  }

  if (chatgptArgs?.messages.length === 0) {
    throw new Error('Messages cannot be empty.');
  }

  const body = {
    early_access_token: earlyAccessToken,
    plugin_name: pluginName,
    ...chatgptArgs,
  };

  try {
    let server = 'https://openplugin-api-30b78451a615.herokuapp.com';
    // server = 'http://127.0.0.1:3000'; // development server

    const response = await fetch(`${server}/chat_completion`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const jsonResponse: any = await response.json();

    if (jsonResponse.error) {
      throw new Error(`Error: ${jsonResponse.error}`);
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return jsonResponse;
  } catch (error) {
    if (failSilently) {
      console.log(error);
      return null;
    } else {
      throw error;
    }
  }
};
