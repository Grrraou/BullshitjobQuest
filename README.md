# BullshitjobQuest 🎮

A gamified productivity tracker that turns your daily work activities into an RPG-like experience. Level up your character while performing your regular work tasks!

![image](https://github.com/user-attachments/assets/ba7a2ea3-2268-4d44-aaf7-3feef14c33b7)
![image](https://github.com/user-attachments/assets/173c7bf4-ad49-43a2-986a-56c352337405)


## Features 🌟

- **Real-time Activity Tracking**
  - Key press monitoring
  - Mouse click tracking
  - Mouse movement distance calculation
  - Key combination detection

- **RPG Elements**
  - Experience points (XP) system
  - Level progression
  - Quest system with rewards

- **Statistics Dashboard**
  - Detailed key usage statistics
  - Mouse activity metrics
  - Most used keys and combinations
  - Progress tracking

- **Safe for Work Mode**
  - Disable potentially sensitive features
  - Focus on work-appropriate statistics
  - Customizable privacy settings

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- Windows operating system
- Make (for building)

### Building from Source
```bash
# Clone the repository
git clone https://github.com/Grrraou/BullshitjobQuest.git
cd BullshitjobQuest

# Create and activate virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build the application
make
```

The compiled binary will be available in the `dist` folder.

## Usage 💻

1. Launch the application
2. Keep it running in the background while you work
3. Track your progress through the various tabs:
   - 📊 Stats: View your current statistics
   - 📜 Logs: Check activity history
   - 🎯 Quests: Monitor and complete quests
   - ⚙️ Config: Adjust application settings

## Roadmap 🗺️

### High Priority
- [ ] Fix application icon display in taskbar and window
- [ ] Implement daily quest system with rewards
- [ ] Improve UI responsiveness and performance
- [ ] Dark/Light theme support

### Medium Priority
- [ ] Add auto-clicker functionality
  - Configurable click patterns
  - Time-based scheduling
  - Customizable intervals
- [ ] Implement macro system
  - Record and playback key sequences
  - Custom macro creation interface
  - Macro scheduling options
- [ ] Enhanced statistics
  - Heat maps for key usage

### Future Enhancements
- [ ] Cloud sync for statistics
- [ ] Achievement system
- [ ] Custom quest creation
- [ ] Export statistics in various formats
