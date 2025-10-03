import { agent, agentGraph, agentMcp } from '@inkeep/agents-sdk';
import { weatherMcpTool } from '../tools/weather-mcp';

/**
 * Basic Weather Graph
 * 
 * This agent can answer basic weather related questions, such as "what is the weather in Tokyo?"
 * 
 * This agent works by asking the coordinates agent for the coordinates of the given location and then passing those coordinates to the weather forecast agent to get the weather forecast.
 */

// Agents
const weatherAssistant = agent({
  id: 'weather-assistant',
  name: 'Weather assistant',
  description: 'Responsible for routing between the coordinates agent and weather forecast agent',
  prompt:
    'You are a helpful assistant. When the user asks about the weather in a given location, first ask the coordinates agent for the coordinates, and then pass those coordinates to the weather forecast agent to get the weather forecast. If the user does not ask about weather related questions, politely decline to answer and redirect the user to a weather related question.',
  canDelegateTo: () => [weatherForecaster, coordinatesAgent],
});

const weatherForecaster = agent({
  id: 'weather-forecaster',
  name: 'Weather forecaster',
  description:
    'This agent is responsible for taking in coordinates and returning the forecast for the weather at that location',
  prompt:
    'You are a helpful assistant responsible for taking in coordinates and returning the forecast for that location using your forecasting tool',
  canUse: () => [agentMcp({ server: weatherMcpTool, selectedTools: ["get_weather_forecast"] })],
});

const coordinatesAgent = agent({
  id: 'get-coordinates-agent',
  name: 'Coordinates agent',
  description: 'Responsible for converting location or address into coordinates',
  prompt:
    'You are a helpful assistant responsible for converting location or address into coordinates using your coordinate converter tool',
  canUse: () => [agentMcp({ server: weatherMcpTool, selectedTools: ["get_coordinates"] })],
});

// Agent Graph
export const weatherBasicGraph = agentGraph({
  id: 'weather-graph-basic',
  name: 'Weather graph basic',
  description: 'Asks for the weather forecast for the given location',
  defaultAgent: weatherAssistant,
  agents: () => [weatherAssistant, weatherForecaster, coordinatesAgent],
});