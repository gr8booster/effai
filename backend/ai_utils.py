"""AI utilities for LLM integration with fallback support"""
import os
import logging
from emergentintegrations.llm.chat import LlmChat, UserMessage
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')


class AIProvider:
    """Unified AI provider with OpenAI primary and Claude fallback"""
    
    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature
        self.api_key = EMERGENT_LLM_KEY
    
    async def generate(self, system_message: str, user_message: str, session_id: str = "default") -> str:
        """
        Generate AI response with fallback logic
        
        Args:
            system_message: System prompt
            user_message: User query
            session_id: Unique session identifier
        
        Returns:
            AI-generated text response
        """
        # Try OpenAI first (primary)
        try:
            response = await self._call_openai(system_message, user_message, session_id)
            return response
        except Exception as e:
            logger.warning(f"OpenAI failed: {e}, falling back to Claude")
            
            # Fallback to Claude
            try:
                response = await self._call_claude(system_message, user_message, session_id)
                return response
            except Exception as e2:
                logger.error(f"Claude fallback also failed: {e2}")
                raise Exception(f"All AI providers failed. OpenAI: {e}, Claude: {e2}")
    
    async def _call_openai(self, system_message: str, user_message: str, session_id: str) -> str:
        """Call OpenAI GPT-4.1"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model("openai", "gpt-4.1")
        
        msg = UserMessage(text=user_message)
        response = await chat.send_message(msg)
        return response
    
    async def _call_claude(self, system_message: str, user_message: str, session_id: str) -> str:
        """Call Claude Sonnet 4 as fallback"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        msg = UserMessage(text=user_message)
        response = await chat.send_message(msg)
        return response


async def paraphrase_text(text: str, context: str = "") -> str:
    """
    Paraphrase text for readability using temp=0 (deterministic)
    Used for micro-lessons and user-facing content
    """
    provider = AIProvider(temperature=0.0)
    system = "You are a helpful financial advisor. Paraphrase the following text for clarity and readability. Keep all facts intact, just improve the wording."
    user = f"Context: {context}\n\nText to paraphrase: {text}"
    
    result = await provider.generate(system, user, session_id=f"paraphrase_{hash(text)}")
    return result


async def extract_intent(user_message: str, available_actions: list) -> str:
    """
    Extract user intent from message (deterministic, temp=0)
    Used by EEFai to route requests
    """
    provider = AIProvider(temperature=0.0)
    system = f"""You are an intent classifier for a financial assistance platform.
    Available actions: {', '.join(available_actions)}
    
    Classify the user's message into ONE of these actions. Return ONLY the action name, nothing else.
    """
    
    result = await provider.generate(system, user_message, session_id=f"intent_{hash(user_message)}")
    return result.strip().lower()
