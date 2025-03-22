import sys
import psutil
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Real-Time Process Monitoring Dashboard")
        self.setGeometry(200, 200, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Process Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Process Name", "CPU Usage (%)", "Memory Usage (%)"])
        self.layout.addWidget(self.table)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for a process...")
        self.search_bar.textChanged.connect(self.update_table)
        self.layout.addWidget(self.search_bar)

        # Kill Process Input & Button
        self.kill_input = QLineEdit()
        self.kill_input.setPlaceholderText("Enter PID to kill")
        self.layout.addWidget(self.kill_input)

        self.kill_button = QPushButton("Kill Process")
        self.kill_button.clicked.connect(self.kill_process)
        self.layout.addWidget(self.kill_button)

        # CPU & Memory Usage Graphs
        self.cpu_series = QLineSeries()
        self.memory_series = QLineSeries()

        self.chart = QChart()
        self.chart.addSeries(self.cpu_series)
        self.chart.addSeries(self.memory_series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("CPU & Memory Usage Over Time")

        self.chart_view = QChartView(self.chart)
        self.layout.addWidget(self.chart_view)

        # Timer to update data every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 1000ms = 1 second

        # Store data points for graph
        self.time_counter = 0
        self.cpu_usage_data = []
        self.memory_usage_data = []

    def update_data(self):
        """ Updates the process table and CPU/Memory usage graph """
        self.update_table()

        # Get CPU & Memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Append data
        self.cpu_usage_data.append((self.time_counter, cpu_usage))
        self.memory_usage_data.append((self.time_counter, memory_usage))
        self.time_counter += 1

        # Update Graph
        self.cpu_series.clear()
        self.memory_series.clear()

        for time, value in self.cpu_usage_data[-20:]:
            self.cpu_series.append(time, value)

        for time, value in self.memory_usage_data[-20:]:
            self.memory_series.append(time, value)

    def update_table(self):
        """ Updates the process list table dynamically """
        self.table.setRowCount(0)
        search_text = self.search_bar.text().lower()

        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                memory = proc.info['memory_percent']

                # Filter based on search text
                if search_text and search_text not in name.lower():
                    continue

                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(pid)))
                self.table.setItem(row_position, 1, QTableWidgetItem(name))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"{cpu:.2f}"))
                self.table.setItem(row_position, 3, QTableWidgetItem(f"{memory:.2f}"))

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def kill_process(self):
        """ Kills a process based on user input PID """
        pid_text = self.kill_input.text()
        if not pid_text.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a valid PID.")
            return

        pid = int(pid_text)
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            QMessageBox.information(self, "Success", f"Process {pid} terminated.")
            self.update_table()  # Refresh table after killing process
        except psutil.NoSuchProcess:
            QMessageBox.warning(self, "Error", "Process not found.")
        except psutil.AccessDenied:
            QMessageBox.warning(self, "Error", "Access Denied! Run as administrator.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessMonitor()
    window.show()
    sys.exit(app.exec())
