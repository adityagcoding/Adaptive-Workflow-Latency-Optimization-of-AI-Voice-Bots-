"""
config.py
Central Configuration Manager for Adaptive Workflow & Latency Optimization Voice Bot.
Loads environment variables from .env and provides type-annotated application settings.
"""

import os
from pathlib import Path
from dataclasses import dataclass

# Attempt loading dotenv if installed, otherwise provide safe fallback
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        # Minimal manual parser fallback
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())


@dataclass
class AppConfig:
    # Execution Mode: BASELINE vs OPTIMIZED
    bot_mode: str = os.getenv("BOT_MODE", "OPTIMIZED").upper()

    # Providers: MOCK | OPENAI | GROQ | DEEPGRAM | ELEVENLABS
    llm_provider: str = os.getenv("LLM_PROVIDER", "MOCK").upper()
    stt_provider: str = os.getenv("STT_PROVIDER", "MOCK").upper()
    tts_provider: str = os.getenv("TTS_PROVIDER", "MOCK").upper()

    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY", "")
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")

    # Voice Personality & Regional Settings (India & Uttar Pradesh)
    voice_name: str = os.getenv("VOICE_NAME", "en-IN-NeerjaNeural")
    voice_region: str = os.getenv("VOICE_REGION", "India / Uttar Pradesh")
    voice_speaking_speed: float = float(os.getenv("VOICE_SPEAKING_SPEED", "1.0"))
    voice_tone: str = os.getenv("VOICE_TONE", "neutral")
    voice_style: str = os.getenv("VOICE_STYLE", "concise")

    # Latency Targets (in milliseconds)
    target_ttft_ms: int = int(os.getenv("TARGET_TTFT_MS", "300"))
    target_ttfa_ms: int = int(os.getenv("TARGET_TTFA_MS", "600"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # Directories
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    logs_file: Path = BASE_DIR / "data" / "conversation_logs.json"

    def is_mock_mode(self) -> bool:
        """Returns True if any core service is in MOCK mode."""
        return any(p == "MOCK" for p in [self.llm_provider, self.stt_provider, self.tts_provider])

    def summary(self) -> dict:
        """Returns a sanitized summary dictionary for display."""
        return {
            "BOT_MODE": self.bot_mode,
            "LLM_PROVIDER": self.llm_provider,
            "STT_PROVIDER": self.stt_provider,
            "TTS_PROVIDER": self.tts_provider,
            "TARGET_TTFT_MS": f"{self.target_ttft_ms} ms",
            "TARGET_TTFA_MS": f"{self.target_ttfa_ms} ms",
            "LOG_LEVEL": self.log_level,
            "VOICE_NAME": self.voice_name,
            "VOICE_REGION": self.voice_region,
            "VOICE_PERSONALITY": f"voice={self.voice_name}, region={self.voice_region}, speed={self.voice_speaking_speed}, tone={self.voice_tone}, style={self.voice_style}"
        }


def load_config() -> AppConfig:
    """Factory function to load and validate configuration."""
    cfg = AppConfig()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    return cfg


# Global configuration instance
config = load_config()
