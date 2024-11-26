# # import sys
# # from PyQt5.QtWidgets import (
# #     QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
# #     QLineEdit, QComboBox, QListWidget, QHBoxLayout, QWidget, QMessageBox
# # )

# # class IssueTracker(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Cross-Platform Issue Tracker")
# #         self.setGeometry(100, 100, 600, 400)

# #         # Main layout
# #         self.layout = QVBoxLayout()

# #         # Input fields for adding issues
# #         self.issue_input = QLineEdit(self)
# #         self.issue_input.setPlaceholderText("Enter issue description")
# #         self.layout.addWidget(self.issue_input)

# #         self.project_input = QLineEdit(self)
# #         self.project_input.setPlaceholderText("Enter project name")
# #         self.layout.addWidget(self.project_input)

# #         self.assignee_input = QLineEdit(self)
# #         self.assignee_input.setPlaceholderText("Enter assignee name")
# #         self.layout.addWidget(self.assignee_input)

# #         self.status_selector = QComboBox(self)
# #         self.status_selector.addItems(["Open", "In Progress", "Resolved"])
# #         self.layout.addWidget(self.status_selector)

# #         # Button to add an issue
# #         self.add_issue_button = QPushButton("Add Issue", self)
# #         self.add_issue_button.clicked.connect(self.add_issue)
# #         self.layout.addWidget(self.add_issue_button)

# #         # List to display issues
# #         self.issue_list = QListWidget(self)
# #         self.layout.addWidget(self.issue_list)

# #         # Set main layout
# #         container = QWidget()
# #         container.setLayout(self.layout)
# #         self.setCentralWidget(container)

# #         # Storage for issues
# #         self.issues = []

# #     def add_issue(self):
# #         issue_desc = self.issue_input.text().strip()
# #         project = self.project_input.text().strip()
# #         assignee = self.assignee_input.text().strip()
# #         status = self.status_selector.currentText()

# #         if not issue_desc or not project or not assignee:
# #             QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
# #             return

# #         # Save the issue as a dictionary
# #         issue = {
# #             "description": issue_desc,
# #             "project": project,
# #             "assignee": assignee,
# #             "status": status
# #         }
# #         self.issues.append(issue)

# #         # Update the issue list display
# #         self.update_issue_list()

# #         # Clear input fields
# #         self.issue_input.clear()
# #         self.project_input.clear()
# #         self.assignee_input.clear()

# #     def update_issue_list(self):
# #         self.issue_list.clear()
# #         for issue in self.issues:
# #             issue_text = (f"[{issue['project']}] {issue['description']} - Assigned to: {issue['assignee']}"
# #                           f" | Status: {issue['status']}")
# #             self.issue_list.addItem(issue_text)

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     tracker = IssueTracker()
# #     tracker.show()
# #     sys.exit(app.exec_())



# import sys
# import csv
# from datetime import datetime, date
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
#     QLineEdit, QComboBox, QListWidget, QHBoxLayout, QWidget, QMessageBox,
#     QDateEdit
# )
# from PyQt5.QtCore import QDate

# class IssueTracker(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Cross-Platform Issue Tracker")
#         self.setGeometry(100, 100, 800, 600)

#         # Main layout
#         self.layout = QVBoxLayout()

#         # Input fields for adding issues
#         self.issue_input = QLineEdit(self)
#         self.issue_input.setPlaceholderText("Enter issue description")
#         self.layout.addWidget(self.issue_input)

#         self.project_input = QLineEdit(self)
#         self.project_input.setPlaceholderText("Enter project name")
#         self.layout.addWidget(self.project_input)

#         self.assignee_input = QLineEdit(self)
#         self.assignee_input.setPlaceholderText("Enter assignee name")
#         self.layout.addWidget(self.assignee_input)

#         self.status_selector = QComboBox(self)
#         self.status_selector.addItems(["Open", "In Progress", "Resolved"])
#         self.layout.addWidget(self.status_selector)

#         self.priority_selector = QComboBox(self)
#         self.priority_selector.addItems(["High", "Medium", "Low"])
#         self.layout.addWidget(self.priority_selector)

#         self.deadline_input = QDateEdit(self)
#         self.deadline_input.setCalendarPopup(True)
#         self.deadline_input.setDisplayFormat("yyyy-MM-dd")
#         self.deadline_input.setDate(QDate.currentDate())
#         self.layout.addWidget(self.deadline_input)

#         # Search bar
#         self.search_bar = QLineEdit(self)
#         self.search_bar.setPlaceholderText("Search issues...")
#         self.search_bar.textChanged.connect(self.filter_issues)
#         self.layout.addWidget(self.search_bar)

#         # Button to add an issue
#         self.add_issue_button = QPushButton("Add Issue", self)
#         self.add_issue_button.clicked.connect(self.add_issue)
#         self.layout.addWidget(self.add_issue_button)

#         # List to display issues
#         self.issue_list = QListWidget(self)
#         self.issue_list.itemClicked.connect(self.edit_or_delete_issue)
#         self.layout.addWidget(self.issue_list)

#         # Button to save issues to CSV
#         self.save_button = QPushButton("Save Issues")
#         self.save_button.clicked.connect(self.save_issues_to_file)
#         self.layout.addWidget(self.save_button)

#         # Set main layout
#         container = QWidget()
#         container.setLayout(self.layout)
#         self.setCentralWidget(container)

#         # Storage for issues
#         self.issues = []

#         # Load issues from file on startup
#         self.load_issues_from_file()

#     def add_issue(self):
#         """Add a new issue to the tracker."""
#         issue_desc = self.issue_input.text().strip()
#         project = self.project_input.text().strip()
#         assignee = self.assignee_input.text().strip()
#         status = self.status_selector.currentText()
#         priority = self.priority_selector.currentText()
#         deadline = self.deadline_input.date().toPyDate()

#         if not issue_desc or not project or not assignee:
#             QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
#             return

#         # Save the issue as a dictionary
#         issue = {
#             "description": issue_desc,
#             "project": project,
#             "assignee": assignee,
#             "status": status,
#             "priority": priority,
#             "deadline": deadline
#         }
#         self.issues.append(issue)

#         # Update the issue list display
#         self.update_issue_list()

#         # Clear input fields
#         self.issue_input.clear()
#         self.project_input.clear()
#         self.assignee_input.clear()
#         self.status_selector.setCurrentIndex(0)
#         self.priority_selector.setCurrentIndex(0)
#         self.deadline_input.setDate(QDate.currentDate())

#     def update_issue_list(self, issues=None):
#         """Update the displayed issue list."""
#         self.issue_list.clear()
#         if issues is None:
#             issues = self.issues

#         for issue in issues:
#             is_overdue = issue["deadline"] < datetime.now().date()
#             overdue_style = " (Overdue)" if is_overdue else ""
#             issue_text = (f"[{issue['project']}] {issue['description']} - Assigned to: {issue['assignee']}"
#                           f" | Status: {issue['status']} | Priority: {issue['priority']}"
#                           f" | Deadline: {issue['deadline']}{overdue_style}")
#             self.issue_list.addItem(issue_text)

#     def filter_issues(self):
#         """Filter issues based on the search bar input."""
#         keyword = self.search_bar.text().lower()
#         filtered_issues = [
#             issue for issue in self.issues
#             if keyword in issue["description"].lower()
#             or keyword in issue["project"].lower()
#             or keyword in issue["assignee"].lower()
#             or keyword in issue["status"].lower()
#             or keyword in issue["priority"].lower()
#         ]
#         self.update_issue_list(filtered_issues)

#     def edit_or_delete_issue(self, item):
#         """Prompt the user to edit or delete the selected issue."""
#         issue_index = self.issue_list.row(item)
#         issue = self.issues[issue_index]

#         response = QMessageBox.question(
#             self, "Edit or Delete", f"Do you want to edit or delete this issue?\n\n{item.text()}",
#             QMessageBox.Edit | QMessageBox.Delete | QMessageBox.Cancel
#         )

#         if response == QMessageBox.Edit:
#             self.issue_input.setText(issue["description"])
#             self.project_input.setText(issue["project"])
#             self.assignee_input.setText(issue["assignee"])
#             self.status_selector.setCurrentText(issue["status"])
#             self.priority_selector.setCurrentText(issue["priority"])
#             self.deadline_input.setDate(issue["deadline"])
#             self.issues.pop(issue_index)
#         elif response == QMessageBox.Delete:
#             self.issues.pop(issue_index)
#             self.update_issue_list()

#     def load_issues_from_file(self):
#         """Load issues from a CSV file at startup."""
#         try:
#             with open("issues.csv", "r") as file:
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     issue = {
#                         "description": row["description"],
#                         "project": row["project"],
#                         "assignee": row["assignee"],
#                         "status": row["status"],
#                         "priority": row["priority"],
#                         "deadline": datetime.strptime(row["deadline"], "%Y-%m-%d").date()
#                     }
#                     self.issues.append(issue)
#             self.update_issue_list()
#         except FileNotFoundError:
#             pass
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"An error occurred while loading issues: {str(e)}")

#     def save_issues_to_file(self):
#         """Save issues to a CSV file."""
#         try:
#             with open("issues.csv", "w", newline="") as file:
#                 writer = csv.DictWriter(file, fieldnames=["description", "project", "assignee", "status", "priority", "deadline"])
#                 writer.writeheader()
#                 for issue in self.issues:
#                     writer.writerow({
#                         "description": issue["description"],
#                         "project": issue["project"],
#                         "assignee": issue["assignee"],
#                         "status": issue["status"],
#                         "priority": issue["priority"],
#                         "deadline": issue["deadline"].strftime("%Y-%m-%d") if isinstance(issue["deadline"], date) else issue["deadline"]
#                     })
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"An error occurred while saving issues: {str(e)}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     tracker = IssueTracker()
#     tracker.show()
#     sys.exit(app.exec_())





import sys
import csv
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QHBoxLayout, QWidget, QMessageBox,
    QDateEdit, QDialog, QFormLayout, QTableWidget, QTableWidgetItem
)

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
        self.setGeometry(100, 100, 800, 600)

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

        # Table to display issues
        self.issue_table = QTableWidget(self)
        self.issue_table.setColumnCount(6)
        self.issue_table.setHorizontalHeaderLabels(["Description", "Project", "Assignee", "Status", "Priority", "Deadline"])
        self.issue_table.verticalHeader().setVisible(False)
        self.issue_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.issue_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.issue_table.setSelectionMode(QTableWidget.SingleSelection)
        self.issue_table.setSortingEnabled(True)
        self.issue_table.itemDoubleClicked.connect(self.edit_issue)
        self.layout.addWidget(self.issue_table)

        # Add issue button
        self.add_issue_button = QPushButton("Add Issue", self)
        self.add_issue_button.clicked.connect(self.add_issue)
        self.layout.addWidget(self.add_issue_button)

        # Edit issue button
        self.edit_issue_button = QPushButton("Edit Issue", self)
        self.edit_issue_button.clicked.connect(self.edit_issue)
        self.edit_issue_button.setEnabled(False)
        self.layout.addWidget(self.edit_issue_button)

        # Delete issue button
        self.delete_issue_button = QPushButton("Delete Issue", self)
        self.delete_issue_button.clicked.connect(self.delete_issue)
        self.delete_issue_button.setEnabled(False)
        self.layout.addWidget(self.delete_issue_button)

        # Set main layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Storage for issues
        self.issues = []

        # Load issues from file on startup
        self.load_issues()

    def add_issue(self):
        issue_desc = self.search_bar.text().strip()
        project = "New Project"
        assignee = "Unassigned"
        status = "Open"
        priority = "Medium"
        deadline = datetime.now().date() + timedelta(days=7)

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

        # Clear search bar
        self.search_bar.clear()

    def edit_issue(self):
        selected_row = self.issue_table.currentRow()
        if selected_row >= 0:
            issue = self.issues[selected_row]
            dialog = EditIssueDialog(issue, self)
            if dialog.exec_() == QDialog.Accepted:
                self.update_issue_list()

    def delete_issue(self):
        selected_row = self.issue_table.currentRow()
        if selected_row >= 0:
            self.issue_table.removeRow(selected_row)
            del self.issues[selected_row]
            self.update_issue_list()

    def update_issue_list(self):
        self.issue_table.setRowCount(len(self.issues))

        for row, issue in enumerate(self.issues):
            description_item = QTableWidgetItem(issue["description"])
            project_item = QTableWidgetItem(issue["project"])
            assignee_item = QTableWidgetItem(issue["assignee"])
            status_item = QTableWidgetItem(issue["status"])
            priority_item = QTableWidgetItem(issue["priority"])
            deadline_item = QTableWidgetItem(issue["deadline"].strftime("%Y-%m-%d"))

            if datetime.now().date() > issue["deadline"]:
                description_item.setBackground(Qt.red)
                project_item.setBackground(Qt.red)
                assignee_item.setBackground(Qt.red)
                status_item.setBackground(Qt.red)
                priority_item.setBackground(Qt.red)
                deadline_item.setBackground(Qt.red)

            self.issue_table.setItem(row, 0, description_item)
            self.issue_table.setItem(row, 1, project_item)
            self.issue_table.setItem(row, 2, assignee_item)
            self.issue_table.setItem(row, 3, status_item)
            self.issue_table.setItem(row, 4, priority_item)
            self.issue_table.setItem(row, 5, deadline_item)

        self.issue_table.sortItems(5, Qt.DescendingOrder)

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
