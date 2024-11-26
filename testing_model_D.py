import sys
import csv
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QListWidget, QHBoxLayout, QWidget, QMessageBox,
    QDateEdit, QCheckBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

class EditIssueDialog(QDialog):
    def __init__(self, issue, parent=None):
        super().__init__(parent)
        self.issue = issue

        self.setWindowTitle("Edit Issue")
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()
        self.setLayout(layout)

        self.description_input = QLineEdit(self)
        self.description_input.setText(issue["description"])
        layout.addRow("Description:", self.description_input)

        self.project_input = QLineEdit(self)
        self.project_input.setText(issue["project"])
        layout.addRow("Project:", self.project_input)

        self.assignee_input = QLineEdit(self)
        self.assignee_input.setText(issue["assignee"])
        layout.addRow("Assignee:", self.assignee_input)

        self.status_selector = QComboBox(self)
        self.status_selector.addItems(["Open", "In Progress", "Resolved"])
        self.status_selector.setCurrentText(issue["status"])
        layout.addRow("Status:", self.status_selector)

        self.priority_selector = QComboBox(self)
        self.priority_selector.addItems(["High", "Medium", "Low"])
        self.priority_selector.setCurrentText(issue["priority"])
        layout.addRow("Priority:", self.priority_selector)

        self.deadline_input = QDateEdit(self)
        self.deadline_input.setDisplayFormat("yyyy-MM-dd")
        self.deadline_input.setDate(issue["deadline"])
        layout.addRow("Deadline:", self.deadline_input)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

    def save(self):
        self.issue["description"] = self.description_input.text()
        self.issue["project"] = self.project_input.text()
        self.issue["assignee"] = self.assignee_input.text()
        self.issue["status"] = self.status_selector.currentText()
        self.issue["priority"] = self.priority_selector.currentText()
        self.issue["deadline"] = self.deadline_input.date().toPyDate()

        self.accept()

class IssueTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross-Platform Issue Tracker")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search issues...")
        self.search_bar.textChanged.connect(self.update_issue_list)
        self.layout.addWidget(self.search_bar)

        # Filter dropdowns
        self.status_filter = QComboBox(self)
        self.status_filter.addItems(["All", "Open", "In Progress", "Resolved"])
        self.status_filter.currentIndexChanged.connect(self.update_issue_list)
        self.layout.addWidget(self.status_filter)

        self.priority_filter = QComboBox(self)
        self.priority_filter.addItems(["All", "High", "Medium", "Low"])
        self.priority_filter.currentIndexChanged.connect(self.update_issue_list)
        self.layout.addWidget(self.priority_filter)

        # Input fields for adding issues
        self.issue_input = QLineEdit(self)
        self.issue_input.setPlaceholderText("Enter issue description")
        self.layout.addWidget(self.issue_input)

        self.project_input = QLineEdit(self)
        self.project_input.setPlaceholderText("Enter project name")
        self.layout.addWidget(self.project_input)

        self.assignee_input = QLineEdit(self)
        self.assignee_input.setPlaceholderText("Enter assignee name")
        self.layout.addWidget(self.assignee_input)

        self.status_selector = QComboBox(self)
        self.status_selector.addItems(["Open", "In Progress", "Resolved"])
        self.layout.addWidget(self.status_selector)

        self.priority_selector = QComboBox(self)
        self.priority_selector.addItems(["High", "Medium", "Low"])
        self.layout.addWidget(self.priority_selector)

        self.deadline_input = QDateEdit(self)
        self.deadline_input.setDisplayFormat("yyyy-MM-dd")
        self.layout.addWidget(self.deadline_input)

        # Button to add an issue
        self.add_issue_button = QPushButton("Add Issue", self)
        self.add_issue_button.clicked.connect(self.add_issue)
        self.layout.addWidget(self.add_issue_button)

        # List to display issues
        self.issue_list = QListWidget(self)
        self.layout.addWidget(self.issue_list)

        # Set main layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Storage for issues
        self.issues = []

        # Load issues from file on startup
        self.load_issues()

    def add_issue(self):
        issue_desc = self.issue_input.text().strip()
        project = self.project_input.text().strip()
        assignee = self.assignee_input.text().strip()
        status = self.status_selector.currentText()
        priority = self.priority_selector.currentText()
        deadline = self.deadline_input.date().toPyDate()

        if not issue_desc or not project or not assignee:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        # Save the issue as a dictionary
        issue = {
            "description": issue_desc,
            "project": project,
            "assignee": assignee,
            "status": status,
            "priority": priority,
            "deadline": deadline
        }
        self.issues.append(issue)

        # Update the issue list display
        self.update_issue_list()

        # Clear input fields
        self.issue_input.clear()
        self.project_input.clear()
        self.assignee_input.clear()
        self.priority_selector.setCurrentIndex(0)
        self.deadline_input.setDate(datetime.now().date())

    def update_issue_list(self):
        self.issue_list.clear()
        for issue in self.issues:
            if self.search_bar.text() and self.search_bar.text() not in issue["description"]:
                continue
            if self.status_filter.currentText() != "All" and self.status_filter.currentText() != issue["status"]:
                continue
            if self.priority_filter.currentText() != "All" and self.priority_filter.currentText() != issue["priority"]:
                continue

            issue_text = (f"[{issue['project']}] {issue['description']} - Assigned to: {issue['assignee']}"
                          f" | Status: {issue['status']} | Priority: {issue['priority']}"
                          f" | Deadline: {issue['deadline'].strftime('%Y-%m-%d')}")
            item = QListWidgetItem(issue_text)
            if datetime.now().date() > issue["deadline"]:
                item.setBackground(Qt.red)
            self.issue_list.addItem(item)

    def load_issues(self):
        try:
            with open("issues.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    issue = {
                        "description": row["description"],
                        "project": row["project"],
                        "assignee": row["assignee"],
                        "status": row["status"],
                        "priority": row["priority"],
                        "deadline": datetime.strptime(row["deadline"], "%Y-%m-%d").date()
                    }
                    self.issues.append(issue)
            self.update_issue_list()
        except FileNotFoundError:
            pass

    def save_issues(self):
        with open("issues.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["description", "project", "assignee", "status", "priority", "deadline"])
            writer.writeheader()
            for issue in self.issues:
                writer.writerow(issue)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = IssueTracker()
    tracker.show()
    sys.exit(app.exec_())