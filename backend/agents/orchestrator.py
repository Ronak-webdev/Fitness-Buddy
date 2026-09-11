"""
OrchestratorAgent — classifies user intent and routes to the right specialist agent.

Routing strategy:
  1. Keyword matching (fast, no LLM tokens) for common patterns.
  2. Granite-based classification only for ambiguous messages.

This is the single entry point for all chat requests.
"""
import json
import logging
from enum import Enum

from backend.agents.base_agent import BaseAgent
from backend.agents.workout_agent import WorkoutAgent, WORKOUT_KEYWORDS
from backend.agents.nutrition_agent import NutritionAgent, NUTRITION_KEYWORDS
from backend.agents.motivation_agent import MotivationAgent, MOTIVATION_KEYWORDS
from backend.agents.profile_agent import ProfileAgent, PROFILE_KEYWORDS
from backend.agents.memory_agent import MemoryAgent
from backend.llm.granite_client import GraniteClient
from backend.models.user import UserProfile
from backend.models.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)


class Intent(str, Enum):
    WORKOUT = "workout"
    NUTRITION = "nutrition"
    MOTIVATION = "motivation"
    PROFILE = "profile"
    GENERAL = "general"


class OrchestratorAgent(BaseAgent):
    """
    Routes incoming chat messages to the appropriate specialist agent.

    All specialist agents are injected at construction time (no globals),
    making the orchestrator fully testable.
    """

    def __init__(
        self,
        granite_client: GraniteClient,
        workout_agent: WorkoutAgent | None = None,
        nutrition_agent: NutritionAgent | None = None,
        motivation_agent: MotivationAgent | None = None,
        profile_agent: ProfileAgent | None = None,
        memory_agent: MemoryAgent | None = None,
    ) -> None:
        self.llm = granite_client
        self.workout_agent = workout_agent or WorkoutAgent(granite_client)
        self.nutrition_agent = nutrition_agent or NutritionAgent(granite_client)
        self.motivation_agent = motivation_agent or MotivationAgent(granite_client)
        self.profile_agent = profile_agent or ProfileAgent(granite_client)
        self.memory_agent = memory_agent  # Optional — used for streak data

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def run(
        self,
        user_message: str,
        user_profile: UserProfile | None,
        chat_history: list[ChatMessage],
    ) -> dict:
        """
        Main dispatch loop:
          1. Check if this is a new user needing onboarding.
          2. Classify intent via keywords → Granite fallback.
          3. Route to the appropriate agent.
          4. Return the agent's response dict.
        """
        # New user — always onboard first
        if user_profile is None:
            return await self.profile_agent.run(
                user_message=user_message,
                user_profile=None,
                chat_history=chat_history,
            )

        # Classify intent
        intent = self._classify_by_keywords(user_message)
        if intent == Intent.GENERAL:
            # Fall back to Granite classification for ambiguous messages
            intent = await self._classify_with_granite(user_message)

        logger.info("Orchestrator routing intent=%s for message: %s", intent.value, user_message[:60])

        # Route to specialist
        if intent == Intent.WORKOUT:
            return await self.workout_agent.run(user_message, user_profile, chat_history)

        elif intent == Intent.NUTRITION:
            return await self.nutrition_agent.run(user_message, user_profile, chat_history)

        elif intent == Intent.MOTIVATION:
            streak = 0
            if self.memory_agent:
                streak = await self.memory_agent.get_streak(user_profile.user_id)
            return await self.motivation_agent.run(user_message, user_profile, chat_history, streak)

        elif intent == Intent.PROFILE:
            return await self.profile_agent.run(user_message, user_profile, chat_history)

        else:
            # General / unknown — ask Granite for a conversational response
            return await self._general_response(user_message, user_profile, chat_history)

    # ------------------------------------------------------------------
    # Intent classification
    # ------------------------------------------------------------------

    def _classify_by_keywords(self, message: str) -> Intent:
        """
        Fast keyword-based classifier. Returns Intent.GENERAL if ambiguous or greeting.
        Exported as a public method so tests can call it directly.
        """
        msg = message.lower()
        cleaned_msg = "".join(c for c in msg if c.isalnum() or c.isspace()).strip()

        # Score each intent by how many keywords match
        scores = {
            Intent.WORKOUT: sum(1 for kw in WORKOUT_KEYWORDS if kw in msg),
            Intent.NUTRITION: sum(1 for kw in NUTRITION_KEYWORDS if kw in msg),
            Intent.MOTIVATION: sum(1 for kw in MOTIVATION_KEYWORDS if kw in msg),
            Intent.PROFILE: sum(1 for kw in PROFILE_KEYWORDS if kw in msg),
        }

        # Handle common greetings directly as GENERAL if no specialist keywords exist
        greetings = {
            "hi", "hello", "hey", "hola", "namaste", "greetings", "good morning",
            "good afternoon", "good evening", "howdy", "sup", "yo"
        }
        if cleaned_msg in greetings or any(cleaned_msg.startswith(g + " ") for g in greetings):
            if max(scores.values()) == 0:
                return Intent.GENERAL

        best_intent = max(scores, key=lambda k: scores[k])
        best_score = scores[best_intent]

        if best_score == 0:
            return Intent.GENERAL
        # Tie-break: prefer WORKOUT > NUTRITION > MOTIVATION > PROFILE
        return best_intent

    async def _classify_with_granite(self, message: str) -> Intent:
        """
        Ask Granite to classify the intent when keywords are inconclusive.
        Uses minimal tokens — expects a single word response.
        """
        prompt = (
            f'Classify the following user message into one category: '
            f'workout, nutrition, motivation, profile, or general.\n'
            f'Message: "{message}"\n'
            f'Answer with exactly one word (the category name):'
        )
        try:
            raw = await self.llm.generate(prompt=prompt, temperature=0.0, max_new_tokens=5)
            raw = raw.strip().lower().split()[0] if raw.strip() else "general"
            return Intent(raw) if raw in Intent._value2member_map_ else Intent.GENERAL
        except Exception as exc:
            logger.warning("Granite classification failed: %s — defaulting to GENERAL", exc)
            return Intent.GENERAL

    # ------------------------------------------------------------------
    # General conversation fallback
    # ------------------------------------------------------------------

    async def _general_response(
        self,
        user_message: str,
        profile: UserProfile,
        history: list[ChatMessage],
    ) -> dict:
        """Handles messages that don't match any specialist intent."""
        history_text = "\n".join(
            f"{m.role.capitalize()}: {m.content}" for m in history[-3:]
        ) if history else ""

        prompt = f"""You are Fitness Buddy, a friendly AI wellness coach.
User name: {profile.name}
User goal: {profile.primary_goal.value}

Recent conversation:
{history_text}

User: {user_message}

Respond helpfully and concisely (2-4 sentences). If unsure how to help,
gently guide the user to ask about workouts, meals, or motivation."""

        response = await self.llm.generate(prompt=prompt, temperature=0.7, max_new_tokens=200)
        cleaned = response.strip()

        # Defensive guard: If response happens to be a raw JSON string, convert to friendly text
        if cleaned.startswith("{") and cleaned.endswith("}"):
            try:
                parsed = json.loads(cleaned)
                if "title" in parsed:
                    cleaned = f"Hello {profile.name}! 👋 I am your AI Fitness Buddy coach. How can I assist your health journey today? Feel free to ask for a custom workout, healthy meal ideas, or daily motivation!"
                elif "message" in parsed:
                    cleaned = str(parsed["message"])
                elif "notes" in parsed:
                    cleaned = str(parsed["notes"])
            except Exception:
                pass

        return {
            "type": "text",
            "message": cleaned,
            "data": None,
        }

