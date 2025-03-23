import psutil
import sys

from PyQt6.QtWidgets import (
QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,

QTableWidget, QTableWidgetItem, QTabWidget, QProgressBar,
QHBoxLayout)

from PyQt6. QtCore import QTimer, Qt

from PyQt6.QtGui import QFont



class ProcessM(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle(" Monitoring dashboard ")
        self.setGeometry(300, 300, 900, 500)
        #background black
        self.setStyleSheet(" background-color: #121212")

        # Main Layout
        main_layout = QVBoxLayout()

        #ui part
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # System Usage Tab
        self.usage_tab = QWidget()
        self.usage_layout = QVBoxLayout()

        self.cpu_label = QLabel("🖥️ CPU Usage: 0%")
        self.memory_label = QLabel("💾 Memory Usage: 0%")

        # Font Styling
        self.cpu_label.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        self.memory_label.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))

        self.cpu_bar = QProgressBar()
        self.memory_bar = QProgressBar()

        self.cpu_bar.setFormat("%p% ⚡")
        self.memory_bar.setFormat("%p% 🚀")

        self.usage_layout.addWidget(self.cpu_label)
        self.usage_layout.addWidget(self.cpu_bar)
        self.usage_layout.addWidget(self.memory_label)
        self.usage_layout.addWidget(self.memory_bar)
        self.usage_tab.setLayout(self.usage_layout)
        self.tabs.addTab(self.usage_tab, " System Usage")

        # Process List Tab
        self.process_tab = QWidget()
        self.process_table = QTableWidget()
        self.process_layout = QVBoxLayout()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["Process ID", "Process Name ", "CPU", "Memory"])

        self.process_table.setSortingEnabled(True)
        self.process_layout.addWidget(self.process_table)
        self.process_tab.setLayout(self.process_layout)

        self.tabs.addTab(self.process_tab," Processes ")

        # Control Buttons
        self.button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.start_button = QPushButton("▶ Start Monitoring ")
        self.stop_button = QPushButton("⏸ Stop Monitoring ")

        self.refresh_button.clicked.connect(self.update_process_list)
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)

        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)

        # Timer for Auto-Refresh
        self.timer = QTimer(self)
        #timeout.connect(self.update_process_list)
        self.timer.timeout.connect(self.update_process_list)

        #updates every 2 sec
        self.timer.start(3000)

        self.update_process_list()  # Initial Load

    def update_process_list(self):
        """Fetch and display system usage and processes"""
        cpu_usage = int(psutil.cpu_percent())
        memory_usage = int(psutil.virtual_memory().percent)

        self.cpu_label.setText(f"🖥 CPU Usage: {cpu_usage}%")
        self.memory_label.setText(f" Memory Usage: {memory_usage}%")

        self.cpu_bar.setValue(cpu_usage)
        self.memory_bar.setValue(memory_usage)

        processes = list(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']))
        self.process_table.setRowCount(len(processes))

        for row, proc in enumerate(processes):
            process_id =proc.info.get('pid','N/A')
            self.process_table.setItem(row, 0, QTableWidgetItem(str(process_id)))
            self.process_table.setItem(row, 1, QTableWidgetItem(proc.info['name']))
            self.process_table.setItem(row, 2, QTableWidgetItem(f"{proc.info['cpu_percent']:.2f}%"))
            self.process_table.setItem(row, 3, QTableWidgetItem(f"{proc.info['memory_percent']:.2f}%"))

#restarts in every 3sec gap
    def start_monitoring(self):
        self.timer.start(3000)

    # Stop the auto-refresh
    def stop_monitoring(self):
        self.timer.stop()


# Run the Application
app = QApplication(sys.argv)
window = ProcessM()
window.show()
sys.exit(app.exec())
