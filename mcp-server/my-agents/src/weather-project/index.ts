import { weatherBasicGraph } from './graphs/weather-basic.js';
import { weatherIntermediateGraph } from './graphs/weather-intermediate.ts';
import { weatherAdvancedGraph } from './graphs/weather-advanced.ts';
import { project } from '@inkeep/agents-sdk';

export const myProject = project({
  id: 'weather-project',
  name: 'Weather Project',
  description: 'Weather project template',
  graphs: () => [weatherBasicGraph, weatherIntermediateGraph, weatherAdvancedGraph],
  models: {
    'base': {
      'model': 'openai/gpt-4.1-2025-04-14'
    },
    'structuredOutput': {
      'model': 'openai/gpt-4.1-mini-2025-04-14'
    },
    'summarizer': {
      'model': 'openai/gpt-4.1-nano-2025-04-14'
    }
  }
});