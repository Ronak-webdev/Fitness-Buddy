"""
Db2Client — wraps IBM Db2 on Cloud for all database operations.

ALL database calls in this project MUST go through this module (AGENTS.md rule).
MemoryAgent is the only agent that calls this class directly.

The client uses ibm_db_dbi (PEP 249 interface) for synchronous DB access,
wrapped in asyncio.run_in_executor so the FastAPI event loop is never blocked.

On startup, call await Db2Client.connect() once (done in backend/main.py).
"""

import asyncio
import logging
import json
from datetime import datetime, date
from typing import Optional
from functools import partial

from backend.config import settings
from backend.models.user import UserProfile, FitnessLevel, FitnessGoal
from backend.models.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)

# We guard the ibm_db import so tests (which mock this module) don't need the C extension
try:
    import ibm_db_dbi as ibm_db
    IBM_DB_AVAILABLE = True
except ImportError:
    ibm_db = None  # type: ignore
    IBM_DB_AVAILABLE = False
    logger.warning("ibm_db_dbi not available — Db2Client will not work without it.")


class Db2Client:
    """
    Async-friendly IBM Db2 on Cloud client.

    All public methods are async. They delegate to sync ibm_db calls
    via asyncio.get_event_loop().run_in_executor() so the event loop
    is never blocked.
    """

    def __init__(
        self,
        dsn: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self._connection = None
        self._dsn: str = dsn if dsn is not None else settings.db2_dsn
        self._user: str = user if user is not None else settings.db2_user
        self._password: str = password if password is not None else settings.db2_password
        
        # In-memory fallbacks for local dev without credentials
        self._fallback_users = {}
        self._fallback_chat = {}
        self._fallback_logs = {}
        
        logger.info("Db2Client created (not yet connected).")

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Open the Db2 connection. Call once at app startup."""
        if not IBM_DB_AVAILABLE or not self._dsn:
            logger.warning("Db2 connection skipped (missing ibm_db or credentials). Using in-memory fallback for local dev.")
            return
            
        loop = asyncio.get_event_loop()
        try:
            self._connection = await loop.run_in_executor(
                None, partial(ibm_db.connect, self._dsn, "", "")
            )
            logger.info("Db2 connection established.")
        except Exception as exc:
            logger.error("Failed to connect to Db2: %s. Using in-memory fallback.", exc)
            self._connection = None

    async def disconnect(self) -> None:
        """Close the Db2 connection. Call on app shutdown."""
        if self._connection:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._connection.close)
            self._connection = None
            logger.info("Db2 connection closed.")

    def _cursor(self):
        """Return a fresh cursor from the active connection."""
        if not self._connection:
            raise RuntimeError("Db2Client is not connected.")
        return self._connection.cursor()

    # ------------------------------------------------------------------
    # User profile operations
    # ------------------------------------------------------------------

    async def save_profile(self, profile: UserProfile) -> bool:
        """
        Upsert a user profile row. Returns True on success.
        Uses MERGE (Db2 equivalent of INSERT ON CONFLICT).
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self._sync_save_profile, profile))

    def _sync_save_profile(self, profile: UserProfile) -> bool:
        if not self._connection:
            self._fallback_users[profile.user_id] = profile
            return True
        sql = """
            MERGE INTO users AS target
            USING (VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )) AS source (
                user_id, name, age, fitness_level, primary_goal,
                equipment, dietary_restrictions, current_streak,
                onboarding_complete
            )
            ON target.user_id = source.user_id
            WHEN MATCHED THEN UPDATE SET
                name = source.name,
                age = source.age,
                fitness_level = source.fitness_level,
                primary_goal = source.primary_goal,
                equipment = source.equipment,
                dietary_restrictions = source.dietary_restrictions,
                current_streak = source.current_streak,
                onboarding_complete = source.onboarding_complete,
                updated_at = CURRENT_TIMESTAMP
            WHEN NOT MATCHED THEN INSERT (
                user_id, name, age, fitness_level, primary_goal,
                equipment, dietary_restrictions, current_streak,
                onboarding_complete
            ) VALUES (
                source.user_id, source.name, source.age, source.fitness_level,
                source.primary_goal, source.equipment, source.dietary_restrictions,
                source.current_streak, source.onboarding_complete
            )
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (
                profile.user_id,
                profile.name,
                profile.age,
                profile.fitness_level.value,
                profile.primary_goal.value,
                profile.equipment,
                profile.dietary_restrictions,
                profile.current_streak,
                1 if profile.onboarding_complete else 0,
            ))
            self._connection.commit()
            logger.info("Profile saved for user: %s", profile.user_id)
            return True
        except Exception as exc:
            logger.error("Failed to save profile for %s: %s", profile.user_id, exc)
            self._connection.rollback()
            return False

    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve a user's profile by user_id. Returns None if not found."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self._sync_get_profile, user_id))

    def _sync_get_profile(self, user_id: str) -> Optional[UserProfile]:
        if not self._connection:
            return self._fallback_users.get(user_id)
        sql = """
            SELECT user_id, name, age, fitness_level, primary_goal,
                   equipment, dietary_restrictions, current_streak,
                   onboarding_complete
            FROM users
            WHERE user_id = ?
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return UserProfile(
                user_id=row[0],
                name=row[1],
                age=row[2],
                fitness_level=FitnessLevel(row[3]) if row[3] else FitnessLevel.BEGINNER,
                primary_goal=FitnessGoal(row[4]) if row[4] else FitnessGoal.GENERAL_HEALTH,
                equipment=row[5] or "",
                dietary_restrictions=row[6] or "",
                current_streak=int(row[7]) if row[7] is not None else 0,
                onboarding_complete=bool(row[8]),
            )
        except Exception as exc:
            logger.error("Failed to get profile for %s: %s", user_id, exc)
            return None

    # ------------------------------------------------------------------
    # Chat history operations
    # ------------------------------------------------------------------

    async def save_message(self, user_id: str, message: ChatMessage) -> bool:
        """Persist a single chat message for a user."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self._sync_save_message, user_id, message)
        )

    def _sync_save_message(self, user_id: str, message: ChatMessage) -> bool:
        if not self._connection:
            if user_id not in self._fallback_chat:
                self._fallback_chat[user_id] = []
            self._fallback_chat[user_id].append(message)
            return True
        sql = """
            INSERT INTO chat_history (user_id, role, content, type)
            VALUES (?, ?, ?, ?)
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (
                user_id,
                message.role.value,
                message.content,
                getattr(message, "type", "text"),
            ))
            self._connection.commit()
            return True
        except Exception as exc:
            logger.error("Failed to save message for %s: %s", user_id, exc)
            self._connection.rollback()
            return False

    async def get_history(self, user_id: str, limit: int = 5) -> list[ChatMessage]:
        """
        Retrieve the last `limit` chat messages for a user.
        Limit is capped at 5 to stay within the Granite token budget.
        """
        limit = min(limit, 5)  # Enforce context window cap
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self._sync_get_history, user_id, limit)
        )

    def _sync_get_history(self, user_id: str, limit: int) -> list[ChatMessage]:
        if not self._connection:
            return self._fallback_chat.get(user_id, [])[-limit:]
        sql = """
            SELECT role, content
            FROM (
                SELECT role, content, created_at
                FROM chat_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                FETCH FIRST ? ROWS ONLY
            ) sub
            ORDER BY created_at ASC
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (user_id, limit))
            rows = cur.fetchall()
            return [
                ChatMessage(role=MessageRole(row[0]), content=row[1])
                for row in rows
            ]
        except Exception as exc:
            logger.error("Failed to get history for %s: %s", user_id, exc)
            return []

    # ------------------------------------------------------------------
    # Daily log operations
    # ------------------------------------------------------------------

    async def save_daily_log(
        self,
        user_id: str,
        log_date: date,
        workout_done: bool = False,
        meals_logged: int = 0,
        mood_score: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> bool:
        """Upsert a daily activity log entry."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            partial(
                self._sync_save_daily_log,
                user_id, log_date, workout_done, meals_logged, mood_score, notes
            )
        )

    def _sync_save_daily_log(
        self,
        user_id: str,
        log_date: date,
        workout_done: bool,
        meals_logged: int,
        mood_score: Optional[int],
        notes: Optional[str],
    ) -> bool:
        if not self._connection:
            if user_id not in self._fallback_logs:
                self._fallback_logs[user_id] = {}
            self._fallback_logs[user_id][log_date.isoformat()] = {
                "workout_done": workout_done
            }
            return True
        sql = """
            MERGE INTO daily_logs AS target
            USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (
                user_id, log_date, workout_done, meals_logged, mood_score, notes
            )
            ON target.user_id = source.user_id AND target.log_date = source.log_date
            WHEN MATCHED THEN UPDATE SET
                workout_done = source.workout_done,
                meals_logged = source.meals_logged,
                mood_score = source.mood_score,
                notes = source.notes
            WHEN NOT MATCHED THEN INSERT (
                user_id, log_date, workout_done, meals_logged, mood_score, notes
            ) VALUES (
                source.user_id, source.log_date, source.workout_done,
                source.meals_logged, source.mood_score, source.notes
            )
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (
                user_id,
                log_date.isoformat(),
                1 if workout_done else 0,
                meals_logged,
                mood_score,
                notes,
            ))
            self._connection.commit()
            return True
        except Exception as exc:
            logger.error("Failed to save daily log for %s: %s", user_id, exc)
            self._connection.rollback()
            return False

    async def get_streak(self, user_id: str) -> int:
        """
        Calculate consecutive days the user logged activity.
        Returns 0 if no logs exist.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self._sync_get_streak, user_id))

    def _sync_get_streak(self, user_id: str) -> int:
        if not self._connection:
            user_logs = self._fallback_logs.get(user_id, {})
            streak = 0
            check_date = date.today()
            for _ in range(30):
                day_str = check_date.isoformat()
                if user_logs.get(day_str, {}).get("workout_done"):
                    streak += 1
                    check_date = date.fromordinal(check_date.toordinal() - 1)
                else:
                    if streak > 0 or check_date != date.today():
                        break
                    check_date = date.fromordinal(check_date.toordinal() - 1)
            return streak
        sql = """
            SELECT log_date FROM daily_logs
            WHERE user_id = ? AND workout_done = 1
            ORDER BY log_date DESC
            FETCH FIRST 30 ROWS ONLY
        """
        try:
            cur = self._cursor()
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            if not rows:
                return 0
            streak = 0
            check_date = date.today()
            for row in rows:
                log_date = date.fromisoformat(str(row[0]).split()[0])
                if log_date == check_date or log_date == check_date:
                    streak += 1
                    check_date = date.fromordinal(check_date.toordinal() - 1)
                else:
                    break
            return streak
        except Exception as exc:
            logger.error("Failed to get streak for %s: %s", user_id, exc)
            return 0
