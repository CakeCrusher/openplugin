type ModelInfo = {
  maxTokens: number;
};
type ModelsInfo = {
  [key: string]: ModelInfo;
};

export const openaiModelsInfo: ModelsInfo = {
  'gpt-3.5-turbo-0613': {
    maxTokens: 4096,
  },
  'gpt-3.5-turbo-16k-0613': {
    maxTokens: 16384,
  },
  'gpt-4-0613': {
    maxTokens: 8192,
  },
  'gpt-4-32k-0613': {
    maxTokens: 32768,
  },
  'gpt-3.5-turbo-1106': {
    maxTokens: 16000,
  },
  'gpt-4-1106-preview': {
    maxTokens: 128000,
  },
};


// openai_models_info = {
//   'gpt-3.5-turbo-0613': {
//       'max_tokens': 4096,
//   },
//   'gpt-3.5-turbo-16k-0613': {
//       'max_tokens': 16384,
//   },
//   'gpt-4-0613': {
//       'max_tokens': 8192,
//   },
//   'gpt-4-32k-0613': {
//       'max_tokens': 32768,
//   },
//   'gpt-3.5-turbo-1106': {
//       'max_tokens': 16000,
//   },
//   'gpt-4-1106-preview': {
//       'max_tokens': 128000,
//   },
// }
