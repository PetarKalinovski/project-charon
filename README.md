# This is a copy of my Loka internship captstone project

# 🛶 Charon: The Personal Ferryman

> *Guiding you across the river of daily complexities*  
> Your intelligent orchestrator for work, leisure, and life management

Charon is a multi-agent AI system that serves as your personal assistant, intelligently managing both productive work tasks and personal leisure time. Named after the mythological ferryman who guided souls across the river Styx, Charon navigates the complexities of your schedule and helps you make optimal decisions about how to spend your time.

## ✨ Features

### 🧠 Multi-Agent Intelligence
- **Specialized Agents**: Each agent has domain expertise (work, leisure, files, calendar, etc.)
- **Intelligent Routing**: Automatically determines which agents to consult based on your request
- **Contextual Coordination**: Agents work together to provide comprehensive assistance

### 🎯 Core Capabilities
- **📅 Smart Scheduling**: Analyzes your calendar to find optimal time slots and schedules activities
- **📚 Personal Content Curation**: Manages your books, movies, YouTube subscriptions, and Substack newsletters
- **💻 Development Workflow**: Integrates with GitHub, analyzes local projects, estimates development time
- **🗓️ Calendar Management**: Full Google Calendar integration for viewing and creating events
- **📝 Journal & Sleep Tracking**: Personal insights and habit tracking
- **🎙️ Multimodal Interface**: Voice input (STT) and voice output (TTS) with customizable voices

### 🏗️ Architecture
```
Big Boss Orchestrator Agent
├── Task Agent (Work & Productivity)
│   ├── File Search Agent
│   ├── GitHub Agent
│   └── Google Calendar Agent
└── Home Agent (Leisure & Entertainment)
    ├── Books Agent
    ├── Movies Agent
    └── Recommender Agent
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- uv package manager
- Git

### Setup
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd charon
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the configuration wizard**
   ```bash
   uv run charon.py setup
   ```

4. **Set up environment variables** (see [Environment Variables](#environment-variables) section)

5. **Configure Google Calendar** (see [Google Calendar Setup](#google-calendar-setup) section)

6. **Start Charon**
   ```bash
   uv run charon.py chat
   ```

## 🔧 Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required: Language Model API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Required: GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token

# Optional: Movie Information
OMDB_API_KEY=your_omdb_api_key

# Optional: YouTube Integration
YOUTUBE_API_KEY=your_youtube_api_key  # Needed for YouTube recommendations

# Optional: Voice Features
ELEVENLABS_API_KEY=your_elevenlabs_api_key  # For speech-to-text

# AWS Credentials (if using Bedrock models)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### API Key Sources:
- **OpenRouter**: Get from [openrouter.ai](https://openrouter.ai/)
- **GitHub**: Create a Personal Access Token in GitHub Settings → Developer Settings
- **OMDB**: Free API key from [omdbapi.com](http://www.omdbapi.com/apikey.aspx)
- **ElevenLabs**: Get from [elevenlabs.io](https://elevenlabs.io/) (optional, for STT)

## 📅 Google Calendar Setup

Charon integrates with Google Calendar for intelligent scheduling. Here's how to set it up:

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

### 2. Create Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Configure OAuth consent screen if prompted:
   - Choose "External" user type
   - Fill required fields (app name, user support email, developer contact)
   - Add your email to test users
4. Create OAuth client ID:
   - Application type: "Desktop application"
   - Name: "Charon Calendar Integration"
5. Download the credentials JSON file

### 3. Configure Charon
1. Rename the downloaded file to `credentials.json`
2. Place it in your project root directory
3. On first calendar use, Charon will open a browser for authorization
4. Grant calendar permissions
5. Credentials will be saved as `google_credentials.json` for future use

### Required Calendar Scopes
Charon requires these Google Calendar permissions:
- `https://www.googleapis.com/auth/calendar.events` - Create and modify events
- `https://www.googleapis.com/auth/calendar` - Read calendar data

## 🎮 Usage

### Command Line Interface
```bash
# Start interactive chat
uv run charon.py chat

# Start with minimal UI
uv run charon.py chat --minimal

# Disable audio output
uv run charon.py chat --no-audio

# Run setup wizard
uv run charon.py setup
```

### Example Interactions

**Work & Productivity:**
```
You: "I need to implement authentication for my React app. How long will it take and when can I schedule it?"

Charon: 🔄 Consulting Task Agent
        Analyzing your project structure and GitHub repository...
        
        Based on your current React app structure, implementing authentication will take approximately 4-6 hours:
        
        Looking at your calendar, I found perfect time slots:
        • Tomorrow 9:00 AM - 1:00 PM (4 hours) - Great for focused development
        • Thursday 2:00 PM - 4:00 PM (2 hours) - For testing and refinement
        
        Shall I block these times for "React Authentication Implementation"?
```

**Leisure & Entertainment:**
```
You: "I have 2 hours free tonight. What should I do?"

Charon: 🔄 Consulting Home Agent
        I see you're free from 7:00-9:00 PM tonight! Here are some perfect options:
        
        📚 **Reading**: Start "The Seven Husbands of Evelyn Hugo" - you loved similar character-driven stories
        🎬 **Movie**: "The Grand Budapest Hotel" (99 mins) - matches your taste for visual storytelling  
        📺 **YouTube**: 3-4 videos from your subscribed channels about AI and productivity
        
        What sounds most appealing for your evening wind-down?
```

**Mixed Planning:**
```
You: "Balance my development work with reading time this week"

Charon: Let me coordinate your work schedule with leisure time...
        
        🔄 Consulting Task Agent for work commitments
        🔄 Consulting Home Agent for reading recommendations
        
        **This Week's Balanced Schedule:**
        
        **Work Focus Blocks:**
        • Mon/Wed/Fri: 9 AM - 12 PM (Morning coding sessions)
        • Tue/Thu: 2 PM - 5 PM (Afternoon development)
        
        **Reading Sessions:**
        • Daily: 8:00-8:30 PM (30min evening reading)
        • Weekend: Sat 10 AM - 12 PM (2hr deep reading)
        
        I've scheduled "The Midnight Library" for your evening sessions based on your recent preferences. Sound good?
```

### Voice Commands
With audio enabled, you can speak naturally to Charon:
- "What's on my calendar today?"
- "Find me something good to read"
- "Block two hours for coding tomorrow morning"

### Session Management
```bash
# In chat, use these commands:
sessions                    # Show all sessions
charon-switch-session <id>  # Switch to different session
audio on/off               # Toggle voice output
status                     # Show system status
help                       # Show available commands
```

## 🏛️ Architecture Details

### Agent Hierarchy

**Big Boss Orchestrator Agent**
- Main entry point and request router
- Analyzes user intent (work vs leisure)
- Coordinates between Task Agent and Home Agent
- Manages journal entries and sleep tracking

**Task Agent** (Work & Productivity)
- Delegates to File Search Agent for local project analysis
- Delegates to GitHub Agent for repository management
- Delegates to Calendar Agent for work scheduling

**Home Agent** (Leisure & Entertainment)
- Delegates to Books Agent for reading recommendations
- Delegates to Movies Agent for viewing suggestions
- Delegates to Recommender Agent for content curation
- Integrates with Calendar Agent for leisure scheduling

### Key Features

**Smart Context Switching**
- Charon remembers context within conversations
- Seamlessly transitions between work and personal assistance
- Maintains session history for continuity

**Intelligent Time Management**
- Analyzes calendar patterns and availability
- Suggests optimal time blocks for different activities
- Considers energy levels, context switching, and buffer time

**Personal Learning**
- Journal integration captures preferences and patterns
- Learns from your ratings and choices
- Adapts recommendations based on your habits

## 🗂️ File Structure

```
charon/
├── config/
│   ├── project-config.yaml         # Main configuration
│   └── project-config-generated.yaml  # Generated from setup
├── data/
│   ├── book_list.json             # Personal book library
│   ├── movie_and_show.json        # Movie/TV watchlist
│   ├── sleep_tracking.json        # Sleep data
│   ├── sessions/                  # Conversation history
│   ├── substack_newsletters.json  # Newsletter subscriptions
│   └── youtube_channels.json      # YouTube subscriptions
├── src/
│   ├── agents/                    # Specialized agents
│   │   ├── big_boss_orchestrator_agent.py
│   │   ├── task_agent.py
│   │   ├── home_agent.py
│   │   ├── file_search_agent.py
│   │   ├── github_agent.py
│   │   ├── google_calendar_agent.py
│   │   ├── books_agent.py
│   │   ├── movies_agent.py
│   │   └── recommender_agent.py
│   ├── cli/                       # Command-line interface
│   │   └── charon_cli.py          # Main CLI application
│   ├── constants/                 # Application constants
│   │   └── directories.py         # Directory scanning constants
│   ├── models/                    # Data models (reserved for future use)
│   ├── pipelines/                 # Agent runner scripts
│   │   ├── running_big_boss_orchestrator.py
│   │   ├── running_task_agent.py
│   │   ├── running_home_agent.py
│   │   └── running_*.py           # Individual agent runners
│   ├── playground/                # Experimental and testing code
│   │   ├── playing_with_kokoro_tts.py
│   │   └── playing_with_nova_sonic.py
│   ├── schemas/                   # Data validation schemas
│   │   ├── config_schema.py       # Configuration validation
│   │   ├── calendar_agent_returns_schema.py
│   │   ├── file_search_returns_schemas.py
│   │   └── *.py                   # Other validation schemas
│   ├── tools/                     # Agent tools and functions
│   │   ├── big_boss_orchestrator_tools.py
│   │   ├── task_agent_tools.py
│   │   ├── home_agent_tools.py
│   │   ├── celander_tools.py      # Google Calendar integration
│   │   ├── file_search_tools.py
│   │   ├── books_tools.py
│   │   ├── movies_tools.py
│   │   ├── recommender_agent_tools.py
│   │   └── sleep_tracking_tools.py
│   └── utils/                     # Utilities and helpers
│       ├── config_loader.py       # Configuration loading
│       ├── directory_scanning.py  # File system utilities
│       ├── google_calendar_auth.py # Google OAuth handling
│       ├── tts_manager.py         # Text-to-speech management
│       ├── tts_callback_handler.py # TTS integration
│       ├── demonic_voice_processor.py # Voice effects
│       ├── substack_api_utils.py  # Substack integration
│       ├── youtube_api_utils.py   # YouTube API utilities
│       ├── prompts.py             # Agent system prompts
│       └── callback_hanlder_subagents.py # UI callbacks
├── credentials.json               # Google OAuth credentials
├── google_credentials.json        # Google access tokens
└── .env                          # Environment variables
```

## 🙏 References & Acknowledgments

- **Calendar Integration**: Calendar tools and agent implementation adapted from [PersonalAgents](https://github.com/JoelKong/PersonalAgents) by JoelKong
- **Strands Framework**: Built using the [strands-agents](https://github.com/strands-ai/strands) framework
- **Kokoro TTS**: Text-to-speech functionality using [Kokoro](https://github.com/hexgrad/kokoro) voice synthesis
- **Google Calendar API**: Integration with Google Calendar for scheduling
- **GitHub MCP**: GitHub integration using Model Context Protocol
- **Voice Effects**: Demonic voice processing for thematic audio output

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

**Common Issues:**

1. **TTS Not Working**: Ensure Kokoro dependencies are installed: `pip install kokoro-tts`
2. **Calendar Auth Failed**: Delete `google_credentials.json` and re-authenticate
3. **GitHub Access Issues**: Verify your GITHUB_TOKEN has necessary repository permissions
4. **Model API Errors**: Check your API keys and rate limits

**Getting Help:**
- Check the logs in your terminal for detailed error messages
- Verify all environment variables are set correctly
- Ensure all required APIs are enabled and have valid credentials

---

*"Just as Charon navigated treacherous waters, this agent navigates your complex schedule."* 🛶⚡
