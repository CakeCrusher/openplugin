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
};
