# Smart Door Lock Using AI IoT System

A comprehensive smart door lock system built with FastAPI, face recognition, and Raspberry Pi GPIO control. This system provides secure access control through facial recognition, password authentication, and emergency unlock features with real-time notifications via SMS and Telegram.

## 🚀 Features

- **Face Recognition Authentication**: Secure access using trained facial recognition models
- **Password-based Login**: Web interface with master password authentication
- **Emergency Unlock**: Emergency password override system
- **Real-time Camera Feed**: Live video streaming via WebSocket
- **SMS Notifications**: Automated SMS alerts for door events using Bitmoro SMS service
- **Telegram Integration**: Unauthorized access alerts with photo capture sent to admin
- **Servo Motor Control**: Physical door lock/unlock mechanism using PWM
- **Responsive Web Interface**: Modern dark-themed UI for mobile and desktop

## 📋 Prerequisites

- Raspberry Pi (tested on Pi 4)
- USB Camera or Pi Camera module
- Servo motor for lock mechanism
- Python 3.8+
- Active internet connection for SMS and Telegram features

## 🛠️ Hardware Setup

1. **Servo Motor Connection**:
   - Connect servo signal wire to GPIO Pin 11 (Physical pin)
   - Connect power and ground accordingly

2. **Camera Setup**:
   - Connect USB camera or enable Pi camera module
   - Ensure camera permissions are properly configured

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Satyam-Pokharel/Smart-Door-Lock-Using-AI.git
cd Smart-Door-Lock-Using-AI
```

### 2. Create Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=your_telegram_chat_id_here
```

### 5. Face Recognition Setup
Before first use, you need to register authorized faces:
```bash
cd src
python detection.py
```
This will capture 200 frames for face encoding and save them to `/home/satya/IOT/encoding/user.txt`

**Note**: Update the encoding path in `detection.py` to match your system path.

## 🚀 Usage

### Starting the Server
```bash
uvicorn main:app --host 0.0.0.0
```

The server will start on `http://0.0.0.0:8000`

### Accessing the Interface
1. Open your web browser and navigate to `http://raspberrypi.local:8000/static/index.html`
2. Login with the master password (default: "123" - change in `src/masterpassword.txt`)
3. The dashboard will show the live camera feed and door controls

### Default Credentials
- **Master Password**: `123` (stored in `src/masterpassword.txt`)
- **Emergency Password**: Same as master password

## 🔧 Configuration

### Master Password
Edit `src/masterpassword.txt` to change the master password:
```bash
echo "your_new_password" > src/masterpassword.txt
```

### SMS Configuration
The system uses Bitmoro SMS service. Update the API key in `server.py`:
```python
bitmoro = Bitmoro("your_bitmoro_api_key_here")
```

### Telegram Setup
1. Create a Telegram bot via @BotFather
2. Get your chat ID by messaging your bot and visiting: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Update the `.env` file with your credentials

## 📁 Project Structure

```
IOT/
├── encoding/
│   └── user.txt                 # Face recognition encodings
├── frontEnd/
│   ├── css/
│   │   └── index.css           # Styling
│   ├── js/
│   │   └── index.js            # Frontend logic
│   ├── index.html              # Main dashboard
│   └── register.html           # Registration page
├── src/
│   ├── __init__.py
│   ├── camera.py               # Camera handling (Singleton)
│   ├── detection.py            # Face recognition logic
│   ├── masterpassword.txt      # Master password storage
│   ├── motorController.py      # GPIO servo control
│   ├── server.py               # FastAPI application
│   └── stream.py               # Video streaming
├── Unauthorized/               # Unauthorized access photos
├── .env                        # Environment variables
├── main.py                     # Application entry point
└── requirement.txt             # Python dependencies
```

## 🔌 API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /emergency-unlock` - Emergency password unlock

### Door Control
- `GET /open-lock` - Unlock door (requires face recognition)
- `GET /close-lock` - Lock door
- `GET /status` - Get current door status

### Utilities
- `GET /forget-password` - Send password via SMS
- `WebSocket /camera` - Live camera feed

## 🛡️ Security Features

- **Session-based Authentication**: Secure cookie-based sessions
- **Face Recognition**: Authorized user verification before unlock
- **Unauthorized Access Logging**: Photos saved and sent to admin via Telegram
- **SMS Alerts**: Real-time notifications for all door events
- **Emergency Override**: Secure emergency access system

## 🔧 Troubleshooting

### Common Issues

1. **Camera not working**:
   ```bash
   # Check camera permissions
   sudo usermod -a -G video $USER
   # Restart and try again
   ```

2. **GPIO Permission denied**:
   ```bash
   sudo usermod -a -G gpio $USER
   ```

3. **Face recognition not working**:
   - Ensure good lighting conditions
   - Re-run the registration process
   - Check if encoding file exists and has proper permissions

4. **SMS/Telegram not working**:
   - Verify API credentials in `.env` file
   - Check internet connectivity
   - Validate phone number format

### Logs
Check application logs for debugging:
```bash
# Run with verbose logging
uvicorn main:app --host 0.0.0.0 --log-level debug
```

## 🎯 Development

### Adding New Features
1. Backend changes go in `src/server.py`
2. Frontend changes in `frontEnd/` directory
3. Face recognition logic in `src/detection.py`

### Testing
- Test face recognition: `python src/detection.py`
- Test motor control: Import and test `MotorController` class
- Test camera: Check camera feed via web interface

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Verify hardware connections
3. Ensure all dependencies are installed correctly

## ⚠️ Important Notes

- **Change default passwords** before deployment
- **Update file paths** in `detection.py` to match your system
- **Secure your Telegram bot token** and SMS API credentials
- **Test thoroughly** in a safe environment before production use

## 🔄 Auto-start (Optional)

To run the system automatically on boot, create a systemd service:

```bash
sudo nano /etc/systemd/system/smart-door-lock.service
```

Add the following content:
```ini
[Unit]
Description=Smart Door Lock Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/project/env/bin
ExecStart=/path/to/your/project/env/bin/uvicorn main:app --host 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable smart-door-lock.service
sudo systemctl start smart-door-lock.service
```

---

**Built with ❤️ for IoT Security**

Author
Satyam Pokharel
Email: satyampokharel9@gmail.com
GitHub: https://github.com/Satyam-Pokharel
