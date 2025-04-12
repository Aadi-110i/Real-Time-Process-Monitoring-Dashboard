import sys
import psutil
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QTimer

class ProcessMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Real-Time Process Monitoring Dashboard")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout()

        # CPU & Memory Usage Labels
        self.cpu_label = QLabel("CPU Usage: ")
        self.memory_label = QLabel("Memory Usage: ")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)

        # Table for Processes
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(3)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %"])
        layout.addWidget(self.process_table)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_process_list)
        layout.addWidget(self.refresh_button)

        # Timer for Auto-Refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_process_list)
        self.timer.start(2000)  # Updates every 2 seconds

        self.setLayout(layout)
        self.update_process_list()  # Initial Load

    def update_process_list(self):
        """Fetch and display the system process list"""
        self.cpu_label.setText(f"CPU Usage: {psutil.cpu_percent()}%")
        self.memory_label.setText(f"Memory Usage: {psutil.virtual_memory().percent}%")

        processes = list(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']))
        self.process_table.setRowCount(len(processes))

        for row, proc in enumerate(processes):
            self.process_table.setItem(row, 0, QTableWidgetItem(str(proc.info['pid'])))
            self.process_table.setItem(row, 1, QTableWidgetItem(proc.info['name']))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(proc.info['cpu_percent'])))

# Run the Application
app = QApplication(sys.argv)
window = ProcessMonitor()
window.show()
sys.exit(app.exec())
