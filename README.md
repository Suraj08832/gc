# Telegram Group Management Bot

A powerful Telegram bot for managing groups with features like bio link protection, message control, sticker management, and copyright protection.

## Features

### Core Features
- **Bio Link Protection**
  - Monitors user bios for links
  - Warns users with unapproved links
  - Auto-mutes after 3 warnings
  - Admin approval system for links

- **Message Control**
  - Deletes edited messages
  - Message deletion with reasons
  - Admin-only message deletion

- **Sticker Management**
  - Group owner approval required
  - Admins need approval too
  - Auto-deletes unapproved stickers

- **Copyright Protection**
  - 85% similarity detection
  - Auto-deletes copied content
  - Shows similarity percentage
  - Can be toggled by admins

- **User Management**
  - Warning system with database storage
  - Mute/unmute functionality
  - Ban/unban commands
  - Auto-ban after 3 warnings

- **Anti-Spam Protection**
  - Message frequency monitoring
  - Configurable thresholds
  - Automatic spam detection

## Setup

### Local Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MongoDB:
   - Install MongoDB on your system
   - Create a database named 'telegram_bot'
   - The bot will automatically create necessary collections

4. Create a `.env` file with your configuration:
   ```
   BOT_TOKEN=your_bot_token_here
   MONGODB_URI=mongodb://localhost:27017/
   OWNER_ID=your_telegram_id
   ```

5. Run the bot:
   ```bash
   python main.py
   ```

### Railway Deployment
1. Fork this repository
2. Create a new project on Railway
3. Add the following environment variables in Railway:
   - `BOT_TOKEN`: Your Telegram bot token
   - `MONGODB_URI`: Your MongoDB connection string
   - `OWNER_ID`: Your Telegram user ID
4. Deploy the project

## Commands

### Admin Commands
- `/approve [user_id]` - Approve bio links
- `/reset_warnings [user_id]` - Reset user warnings
- `/delete [message_id] [reason]` - Delete messages
- `/copyright` - Toggle copyright protection
- `/warn [user_id] [reason]` - Warn a user
- `/mute [user_id] [duration] [reason]` - Mute a user
- `/unmute [user_id]` - Unmute a user
- `/ban [user_id] [reason]` - Ban a user
- `/unban [user_id]` - Unban a user

### Group Owner Commands
- `/approve_sticker [user_id]` - Approve users for stickers

### User Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/info` - Show bot information

## Database Structure

The bot uses MongoDB with the following collections:

- `users`: Stores user information
- `chats`: Stores chat settings
- `warnings`: Stores user warnings
- `mutes`: Stores user mute information
- `settings`: Stores chat-specific settings

## Environment Variables

Required environment variables:
- `BOT_TOKEN`: Your Telegram bot token from @BotFather
- `MONGODB_URI`: MongoDB connection string
- `OWNER_ID`: Your Telegram user ID (optional, for owner-specific commands)

## Contributing
Feel free to contribute to this project by creating issues or pull requests. 