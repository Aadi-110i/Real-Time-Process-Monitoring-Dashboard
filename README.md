# RealTime Process Monitoring Dashboard

A powerful and user-friendly system monitoring tool built with Python and PyQt6 that provides real-time insights into your system's performance and running processes.

## 🚀 Features

- **Real-time CPU Usage Monitoring**
  - Live CPU usage percentage tracking
  - Visual progress bar representation
  - Auto-refreshing metrics (3-second intervals)

- **Memory Usage Tracking**
  - Current memory utilization monitoring
  - Visual memory usage indicator
  - Percentage-based representation

- **Process Management**
  - Comprehensive list of all running processes
  - Process ID tracking
  - Per-process CPU and memory usage statistics
  - Sortable process list by any column

- **User Interface**
  - Modern dark theme design
  - Tabbed interface for organized information
  - Interactive controls for monitoring
  - Responsive and intuitive layout

## 🛠️ Requirements

- Python 3.x
- PyQt6
- psutil

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Haswanth2005/RealTime-Process-Monitoring-Dashboard.git
   cd RealTime-Process-Monitoring-Dashboard
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

To run the application:
```bash
python main.py
```

### Features and Controls:

1. **System Usage Tab**
   - Real-time CPU usage display
   - Memory usage monitoring
   - Visual progress bars

2. **Processes Tab**
   - List of all running processes
   - Sort by clicking column headers
   - Real-time updates

3. **Control Buttons**
   - Start Monitoring: Begin automatic updates
   - Stop Monitoring: Pause automatic updates
   - Refresh: Manual update of metrics

## 🔧 Technical Details

- **Update Frequency**: 3 seconds
- **Process Information**: 
  - Process ID
  - Process Name
  - CPU Usage (%)
  - Memory Usage (%)
- **UI Framework**: PyQt6
- **System Integration**: psutil

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyQt6 for the GUI framework
- psutil for system monitoring capabilities
