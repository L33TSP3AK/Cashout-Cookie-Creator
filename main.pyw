import sys
from PyQt5 import QtWidgets
from Config_Creator import Ui_DiamondDumper
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5 import QAxContainer
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QUrl, Qt, QTimer, pyqtSignal, pyqtSlot, QThread, QThreadPool, QBasicTimer, QTimerEvent, QMessageLogContext, QtMsgType, QRect
from PyQt5.QtWidgets import QApplication, QScrollArea, QLineEdit, QHBoxLayout, QShortcut, QMainWindow, QListWidget, QDockWidget, QPlainTextEdit, QLCDNumber, QWidget, QVBoxLayout, QTextBrowser, QFileDialog, QTextEdit, QComboBox, QPushButton, QMessageBox, QFrame, QInputDialog, QLabel, QCheckBox, QScrollBar, QDialogButtonBox, QDialog, QGridLayout, QMenu, QAction, QTabBar, QRadioButton, QSystemTrayIcon, QFormLayout, QProgressBar
from PyQt5.QtXml import QDomDocument
from PyQt5.QtGui import QDesktopServices, QTextCursor, QTextDocument, QColor, QCursor, QTextCharFormat, QIcon, QPainter, QTextOption
import requests
from requests.exceptions import RequestException, Timeout
import logging
import os
import time
from urllib.parse import urlparse
from PyQt5.QtGui import QFont


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super(SearchDialog, self).__init__(parent)
        self.setWindowTitle("Search")
        self.setGeometry(100, 100, 300, 100)
        
        self.search_label = QLabel("Find:")
        self.search_input = QLineEdit(self)
        
        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.accept)

        layout = QHBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        
        self.setLayout(layout)
    
    def get_search_term(self):
        return self.search_input.text()
    def set_result_count(self, count):
        self.result_label.setText(f"Occurrences: {count}")


class UserAgentComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMouseTracking(True)
        self.view().setMouseTracking(True)
        
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        
        self.current_index = -1
        
        # Set a custom font for the tooltip
        QToolTip.setFont(QFont('SansSerif', 10))

    def eventFilter(self, obj, event):
        if obj == self.view().viewport():
            if event.type() == Qt.QEvent.MouseMove:
                index = self.view().indexAt(event.pos())
                if index.isValid() and index.row() != self.current_index:
                    self.current_index = index.row()
                    self.hover_timer.start(2000)  # 2 seconds
                elif not index.isValid():
                    self.hide_tooltip()
            elif event.type() == Qt.QEvent.Leave:
                self.hide_tooltip()
        return super().eventFilter(obj, event)

    def showPopup(self):
        super().showPopup()
        self.view().viewport().installEventFilter(self)

    def hidePopup(self):
        super().hidePopup()
        self.view().viewport().removeEventFilter(self)
        self.hide_tooltip()

    def show_tooltip(self):
        if 0 <= self.current_index < self.count():
            item_text = self.itemText(self.current_index)
            QToolTip.showText(self.mapToGlobal(self.view().visualRect(self.model().index(self.current_index, 0)).bottomLeft()), 
                              item_text, 
                              self)

    def hide_tooltip(self):
        self.hover_timer.stop()
        self.current_index = -1
        QToolTip.hideText()

    def add_user_agents(self, user_agents):
        for agent in user_agents:
            self.addItem(agent)





class ProductInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CashOut Config Creator Product Information")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)

        # Set the base style
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: 1px solid #7F8C8D;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498DB;
                color: #ECF0F1;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QProgressBar {
                border: 2px solid #7F8C8D;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2ECC71;
            }
        """)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.product_name = QLabel("CashOut Cookie Creator")
        self.description = QTextEdit()
        self.description.setPlainText("A tool for managing and analyzing cookie data.")
        self.description.setReadOnly(True)

        self.repository_link = QLabel('<a href="https://github.com/L33TSP3AK/Cashout-Cookie-Creator">GitHub Repository</a>')
        self.repository_link.setOpenExternalLinks(True)

        self.developer_notes = QTextEdit()
        self.developer_notes.setPlainText("Developer Notes:\n- Version 1.4\n- Last updated: 2023-09-19\n- Known issues: **IN DEVELOPMENT**")
        self.developer_notes.setReadOnly(True)

        self.developer_info = QLabel("Developed By: @CashMoneyL33T")
        self.social_link = QLabel('<a href="https://t.me/CashMoneyL33T">Social Link</a>')
        self.social_link.setOpenExternalLinks(True)
        self.social_channel = QLabel('<a href="https://t.me/L33TSP3AK1337">Social Channel</a>')
        self.social_channel.setOpenExternalLinks(True)

        form_layout.addRow("Product:", self.product_name)
        form_layout.addRow("Description:", self.description)
        form_layout.addRow("Repository:", self.repository_link)
        form_layout.addRow("Developer Notes:", self.developer_notes)
        form_layout.addRow("Developer:", self.developer_info)
        form_layout.addRow("Social Link:", self.social_link)
        form_layout.addRow("Social Channel:", self.social_channel)

        layout.addLayout(form_layout)

        # Add Check for Updates button and progress bar
        update_layout = QHBoxLayout()
        self.check_updates_button = QPushButton("Check for Updates")
        self.check_updates_button.clicked.connect(self.check_for_updates)
        update_layout.addWidget(self.check_updates_button)

        self.update_progress = QProgressBar()
        self.update_progress.setRange(0, 0)  # Indeterminate progress
        self.update_progress.setVisible(False)
        update_layout.addWidget(self.update_progress)

        layout.addLayout(update_layout)

        self.update_status = QLabel("")
        layout.addWidget(self.update_status)

        # Add Join Us On Telegram button
        self.join_telegram_button = QPushButton("Join Us On Telegram")
        self.join_telegram_button.clicked.connect(self.open_telegram_channel)
        layout.addWidget(self.join_telegram_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def check_for_updates(self):
        # Implement your update checking logic here
        pass

    def open_telegram_channel(self):
        QDesktopServices.openUrl(QUrl("https://t.me/L33TSP3AK1337"))

    def check_for_updates(self):
        self.check_updates_button.setEnabled(False)
        self.update_progress.setVisible(True)
        self.update_status.setText("Checking for updates...")

        latest_version = self.get_latest_version()
        
        if latest_version:
            if latest_version > self.current_version:
                self.update_status.setText(f"An update is available. Latest version: {latest_version}")
            else:
                self.update_status.setText("You are using the latest version.")
        else:
            self.update_status.setText("Failed to check for updates. Please try again later.")

        self.update_progress.setVisible(False)
        self.check_updates_button.setEnabled(True)

    def update_check_complete(self, result):
        self.update_progress.setVisible(False)
        self.check_updates_button.setEnabled(True)

        if result == "up_to_date":
            self.update_status.setText("You are using the latest version.")
        elif result == "update_available":
            self.update_status.setText("An update is available. Please visit the GitHub repository.")
        else:
            self.update_status.setText("Failed to check for updates. Please try again later.")




    def get_latest_version(self):
        try:
            response = requests.get("https://api.github.com/repos/L33TSP3AK/Cashout-Cookie-Creator/releases/latest")
            response.raise_for_status()
            latest_release = response.json()
            return latest_release['tag_name'].lstrip('v')
        except Exception as e:
            print(f"Error fetching latest version: {e}")
            return None





class UpdateCheckerThread(QThread):
    update_result = pyqtSignal(str)

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version

    def run(self):
        try:
            # Fetch the latest release information from GitHub
            response = requests.get("https://api.github.com/repos/L33TSP3AK/Cashout-Cookie-Creator/releases/latest")
            response.raise_for_status()
            latest_release = response.json()

            # Extract the version number from the latest release tag
            latest_version = latest_release['tag_name'].lstrip('v')

            # Compare versions
            if version.parse(self.current_version) < version.parse(latest_version):
                self.update_result.emit("update_available")
            else:
                self.update_result.emit("up_to_date")
        except Exception as e:
            print(f"Error checking for updates: {e}")
            self.update_result.emit("error")







class RequestConfirmationDialog(QDialog):
    def __init__(self, domain, url, method, cookie_count, headers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Request Confirmation")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("You are about to send the following request:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Create a scroll area for the details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QLabel()
        scroll_area.setWidget(scroll_content)

        # Request details
        details_text = f"""
        <b>Domain:</b> {domain}<br>
        <b>URL:</b> {url}<br>
        <b>Method:</b> {method}<br>
        <b>Cookies:</b> {cookie_count} loaded<br><br>
        <b>Headers:</b><br>
        """

        for header, value in headers.items():
            details_text += f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{header}:</b> {value}<br>"

        scroll_content.setText(details_text)
        scroll_content.setTextFormat(Qt.RichText)
        scroll_content.setAlignment(Qt.AlignLeft)
        scroll_content.setFont(QFont("Arial", 10))
        scroll_content.setStyleSheet("background-color: #303030; color: #FFFFFF; padding: 10px; border-radius: 5px;")
        scroll_content.setWordWrap(True)

        layout.addWidget(scroll_area)

        # Buttons
        button_layout = QVBoxLayout()
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.accept)
        confirm_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)







class MainWindow(QtWidgets.QMainWindow, Ui_DiamondDumper):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This method is defined in the generated file
        self.load_cookies_button.clicked.connect(self.load_cookies_function)
        self.send_request_button.clicked.connect(self.send_request)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
        self.shortcut.activated.connect(self.open_search_dialog)
        self.enable_captures_checkBox.stateChanged.connect(self.enable_capture_frame)
        self.save_config_button.clicked.connect(self.save_config)
        self.current_cursor_position = 0
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon('cookie_creator.ico'))  # Set the tray icon
        self.tray_icon.show()
        self.toolButton.clicked.connect(self.show_product_info)
        if hasattr(self, 'parse_single_element_radiobutton'):
            self.parse_single_element_radiobutton.toggled.connect(self.parse_single_element_changed)
        if hasattr(self, 'parse_multiple_elements_radiobutton'):
            self.parse_multiple_elements_radiobutton.toggled.connect(self.parse_multiple_elements_changed)

        
        
    def setup_tray_icon(self):
        tray_menu = QMenu(self)

        # Open action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.show)

        # Minimize action
        minimize_action = QAction("Minimize", self)
        minimize_action.triggered.connect(self.hide)

        # Restore action
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.showNormal)

        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)

        # Close action
        close_action = QAction("Exit", self)
        close_action.triggered.connect(self.close)

        # Add actions to the tray menu
        tray_menu.addAction(open_action)
        tray_menu.addAction(minimize_action)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(about_action)
        tray_menu.addSeparator()  # Add a separator line
        tray_menu.addAction(close_action)

        # Set the context menu for the tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


    def show_product_info(self):
        dialog = ProductInfoDialog(self)
        dialog.exec_()



    def open_settings_dialog(self):
        # Implement the logic to open the settings dialog
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setGeometry(100, 100, 400, 300)
        settings_dialog.exec_()

    def show_about_dialog(self):
        # Implement the logic to show the about dialog
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About")
        about_dialog.setText("This is a sample application.")
        about_dialog.setStandardButtons(QMessageBox.Ok)
        about_dialog.exec_()

    def enable_capture_frame(self, state):
        # Enable or disable specific widgets based on the checkbox state
        self.capture_1_after.setEnabled(state == QtCore.Qt.Checked)
        self.capture_1_before.setEnabled(state == QtCore.Qt.Checked)
        self.capture_2_after.setEnabled(state == QtCore.Qt.Checked)
        self.capture_2_before.setEnabled(state == QtCore.Qt.Checked)
        self.capture_3_after.setEnabled(state == QtCore.Qt.Checked)
        self.capture_3_before.setEnabled(state == QtCore.Qt.Checked)
        pass

    def enable_capture_frame(self, state):
        is_enabled = state == QtCore.Qt.Checked
        
        # Enable or disable specific widgets based on the checkbox state
        self.capture_1_after.setEnabled(is_enabled)
        self.capture_1_before.setEnabled(is_enabled)
        self.capture_2_after.setEnabled(is_enabled)
        self.capture_2_before.setEnabled(is_enabled)
        self.capture_3_after.setEnabled(is_enabled)
        self.capture_3_before.setEnabled(is_enabled)
        
        # Enable/disable radio buttons based on checkbox state
        if hasattr(self, 'parse_single_element_radiobutton'):
            self.parse_single_element_radiobutton.setEnabled(is_enabled)
        if hasattr(self, 'parse_multiple_elements_radiobutton'):
            self.parse_multiple_elements_radiobutton.setEnabled(is_enabled)
        
        # Clear radio button selection when checkbox is unchecked
        if not is_enabled:
            if hasattr(self, 'parse_single_element_radiobutton'):
                self.parse_single_element_radiobutton.setChecked(False)
            if hasattr(self, 'parse_multiple_elements_radiobutton'):
                self.parse_multiple_elements_radiobutton.setChecked(False)
    
    def parse_single_element_changed(self, checked):
        if checked:
            self.parse_multiple_elements_radiobutton.setChecked(False)
    
    def parse_multiple_elements_changed(self, checked):
        if checked:
            self.parse_single_element_radiobutton.setChecked(False)


    def open_search_dialog(self):
        # Create and show the search dialog
        self.search_dialog = SearchDialog(self)

        # Center the dialog on the main window
        main_window_rect = self.geometry()
        dialog_rect = self.search_dialog.geometry()
        center_x = main_window_rect.x() + (main_window_rect.width() - dialog_rect.width()) // 2
        center_y = main_window_rect.y() + (main_window_rect.height() - dialog_rect.height()) // 2
        self.search_dialog.move(center_x, center_y)

        # Execute the dialog and check if it was accepted
        if self.search_dialog.exec_() == QDialog.Accepted:
            search_term = self.search_dialog.get_search_term()
            self.search_in_text_edit(search_term)

    def search_in_text_edit(self, search_term):
        # Clear previous highlights
        # Example: cursor = self.http_response_textEdit.textCursor()
        cursor.setPosition(0)
        self.http_response_textEdit.setTextCursor(cursor)

        # Highlight format
        format = QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))

        # Find all occurrences of the search term
        occurrences = 0
        # Example: while not cursor.isNull() and not cursor.atEnd():
        cursor = self.http_response_textEdit.document().find(search_term, cursor)
        if not cursor.isNull():
            occurrences += 1
            cursor.mergeCharFormat(format)

        # Update the result count in the search dialog
        if self.search_dialog:
            self.search_dialog.set_result_count(occurrences)

        # If occurrences are found, start searching from the beginning
        if occurrences > 0:
            self.find_next(search_term)

    def find_next(self, search_term):
        # Move the cursor to the current position
        # Example: cursor = self.http_response_textEdit.textCursor()
        cursor.setPosition(self.current_cursor_position)
        self.http_response_textEdit.setTextCursor(cursor)

        # Find the next occurrence
        cursor = self.http_response_textEdit.document().find(search_term, cursor)
        if not cursor.isNull():
            self.current_cursor_position = cursor.position()
            self.http_response_textEdit.setTextCursor(cursor)
        else:
            self.current_cursor_position = 0
        pass
        
        
        
        
        
        

########## Search Function in Response #############
    def open_search_dialog(self):
        # Create and show the search dialog
        search_dialog = SearchDialog(self)
        
        # Calculate the center position of the main window
        main_window_rect = self.geometry()
        dialog_rect = search_dialog.geometry()
        
        # Set the dialog's position to the center of the main window
        center_x = main_window_rect.x() + (main_window_rect.width() - dialog_rect.width()) // 2
        center_y = main_window_rect.y() + (main_window_rect.height() - dialog_rect.height()) // 2
        search_dialog.move(center_x, center_y)
        
        # Execute the dialog and check if it was accepted
        if search_dialog.exec_() == QDialog.Accepted:
            search_term = search_dialog.get_search_term()
            self.search_in_text_edit(search_term)
    
    def search_in_text_edit(self, search_term):
        # Clear previous highlights
        cursor = self.http_response_textEdit.textCursor()
        cursor.setPosition(0)
        self.http_response_textEdit.setTextCursor(cursor)

        # Highlight format
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))

        # Find all occurrences of the search term
        occurrences = 0
        while not cursor.isNull() and not cursor.atEnd():
            cursor = self.http_response_textEdit.document().find(search_term, cursor)
            if not cursor.isNull():
                occurrences += 1
                cursor.mergeCharFormat(format)



        # If occurrences are found, start searching from the beginning
        if occurrences > 0:
            self.find_next(search_term)

    def find_next(self, search_term):
        # Move the cursor to the current position
        cursor = self.http_response_textEdit.textCursor()
        cursor.setPosition(self.current_cursor_position)
        self.http_response_textEdit.setTextCursor(cursor)

        # Find the next occurrence
        cursor = self.http_response_textEdit.document().find(search_term, cursor)
        if not cursor.isNull():
            # Highlight the found text
            self.current_cursor_position = cursor.position()
            self.http_response_textEdit.setTextCursor(cursor)
        else:
            # Reset to start if no more occurrences
            self.current_cursor_position = 0
########################################################




########## Drag and Drop Function ##########
    def dragEnterEvent(self, event):
        # Accept the drag event if it contains URLs (files)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Handle the drop event to load the file
        if not self.validate_domain():
            return

        urls = event.mimeData().urls()
        if urls:
            file_name = urls[0].toLocalFile()
            if file_name.endswith('.txt'):
                self.load_cookies_from_file(file_name)


########################################################

    
    def send_request(self):
        # Get the URL and request type
        url = self.http_url_request_textedit.toPlainText().strip()
        request_type = self.get_or_post_combobox.currentText()
        valid_response_text = self.valid_response_text.toPlainText().strip()
    
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return
        
        # Parse the domain from the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
    
        # Get the cookies that were loaded from load_cookies_button
        cookie_count = self.total_cookies_lcdNumber.intValue()
    
        # Prepare headers
        headers = {}
        header_checkboxes = [
            ('User-Agent', self.user_agent_checkbox, self.user_agent_combobox),
            ('Accept', self.accept_checkbox, self.accept_combobox),
            ('Content-Type', self.content_type_checkbox, self.content_type_combobox),
            ('X-Akamai-Requested-Id', self.x_akamai_requested_id_checkbox, self.x_akamai_requested_id_combobox),
            ('Referer', self.referer_checkbox, self.referer_combobox),
            ('X-Content-Type-Options', self.x_content_checkbox, self.x_content_type_options_combobox),
            ('X-Requested-With', self.x_requested_with_checkbox, self.x_requested_with_combobox),
            ('CF-Access-Token', self.cf_access_token_checkbox, self.cf_access_token_combobox),
            ('CF-Access-Client-Id', self.cf_access_client_id_checkbox, self.cf_access_client_id_combobox),
            ('Sec-CH-UA', self.sec_ch_ua_checkbox, self.sec_ch_ua_combobox),
        ]
        
        for header_name, checkbox, combobox in header_checkboxes:
            if checkbox.isChecked():
                headers[header_name] = combobox.currentText().strip()
    
        # Show the confirmation dialog with headers
        confirm_dialog = RequestConfirmationDialog(domain, url, request_type, cookie_count, headers, self)
        if confirm_dialog.exec_() != QDialog.Accepted:
            return  # User cancelled the request
    
        try:
            # Create a session to handle cookies
            session = requests.Session()
    
            # Load cookies
            if hasattr(self, 'last_loaded_cookie_file'):
                cookie_domain = self.cookie_domain_edit.toPlainText().strip()
                with open(self.last_loaded_cookie_file, 'r') as file:
                    for line in file:
                        if cookie_domain in line:
                            parts = line.strip().split('\t')
                            if len(parts) >= 7:
                                session.cookies.set(parts[5], parts[6], domain=parts[0])
            else:
                logging.warning("No cookie file has been loaded.")
    
            # Prepare request kwargs
            request_kwargs = {
                'headers': headers,
                'timeout': 30,  # 30 seconds timeout
                'verify': True,  # SSL verification enabled by default
            }
    
            # Send the HTTP request based on the selected method
            if request_type == "GET":
                response = session.get(url, **request_kwargs)
            elif request_type == "POST":
                post_data = self.post_data_textedit.toPlainText()  # Assuming you have this text edit
                response = session.post(url, data=post_data, **request_kwargs)
            else:
                QMessageBox.warning(self, "Request Error", "Unsupported request type.")
                return
    
            # Handle content encoding
            response.encoding = response.apparent_encoding
    
            # Check for specific error responses
            error_messages = [
                "Please enable Cookies and reload the page",
                "Please turn JavaScript on and reload the page.",
                "Your connection needs to be verified before you can proceed"
            ]
    
            if any(msg in response.text for msg in error_messages):
                error_message = "Error - Update Your Headers\n\nSuggestion: Try modifying your User-Agent, Accept, or Content-Type headers."
                self.http_response_textEdit.setPlainText(error_message)
                QMessageBox.warning(self, "Error", error_message)
                return
    
            # Parse captures if enabled
            parsed_captures = []
            if self.enable_captures_checkBox.isChecked():
                response_text = response.text
                
                for i in range(1, 4):  # For capture_1, capture_2, and capture_3
                    before = getattr(self, f'capture_{i}_before').toPlainText().strip()
                    after = getattr(self, f'capture_{i}_after').toPlainText().strip()
                    if before and after:
                        try:
                            start = response_text.index(before) + len(before)
                            end = response_text.index(after, start)
                            captured_value = response_text[start:end].strip()
                            parsed_captures.append(f"Capture {i}: {captured_value}")
                        except ValueError:
                            parsed_captures.append(f"Capture {i}: Not found")
    
                # Determine which parsing method to use
                if self.parse_single_element_radiobutton.isChecked():
                    parsing_method = "Single Element"
                elif self.parse_multiple_elements_radiobutton.isChecked():
                    parsing_method = "Multiple Elements"
                else:
                    parsing_method = "No parsing method selected"
    
                # Display parsed captures in capture_value_response_textedit
                capture_response = f"Parsing Method: {parsing_method}\n\n"
                capture_response += "\n".join(parsed_captures)
                self.capture_value_response_textedit.setPlainText(capture_response)
    
            # Display the full response in the http_response_textEdit
            response_text = f"Status Code: {response.status_code}\n\nHeaders:\n"
            for key, value in response.headers.items():
                response_text += f"{key}: {value}\n"
            response_text += f"\nBody:\n{response.text}"
            self.http_response_textEdit.setPlainText(response_text)
    
            # Log the request (you might want to add more details)
            logging.info(f"Request sent to {url} with method {request_type}")
            if parsed_captures:
                logging.info(f"Parsed captures: {parsed_captures}")
    
        except requests.Timeout:
            QMessageBox.critical(self, "Request Error", "The request timed out. Please try again or check your internet connection.")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Request Error", f"An error occurred: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")
            logging.exception("Unexpected error in send_request")

################################ Cookies ##########################################

    def load_cookies_function(self):
        # Check if the domain is entered
        if not self.validate_domain():
            return

        # Open a file dialog to select a .txt file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Cookie File", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            self.load_cookies_from_file(file_name)

    def validate_domain(self):
        # Validate that the domain field is not empty
        domain = self.cookie_domain_edit.toPlainText().strip()
        if not domain:
            QMessageBox.warning(self, "Input Error", "Please enter a DOMAIN VALUE  before loading a file.")
            return False
        return True

    def load_cookies_from_file(self, file_name):
        try:
            # Read the file and count the lines matching the domain
            with open(file_name, 'r') as file:
                lines = file.readlines()
                domain = self.cookie_domain_edit.toPlainText().strip()
                matching_lines = [line for line in lines if domain in line]
    
            # Update the QLCDNumber with the number of matching lines
            num_matching_lines = len(matching_lines)
            self.total_cookies_lcdNumber.display(num_matching_lines)
    
            # Display a message box with the number of cookies found and the domain
            QMessageBox.information(
                self,
                "Cookies Found",
                f"Number of cookies found for domain '{domain}': {num_matching_lines}"
            )
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
################################################################################
############################  Config Loading Function#############################
    
    def load_config_function(self):
        # Create a message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Load Configuration")
        msg_box.setText("How do you want to load your configuration as?")
        
        # Add buttons for options
        project_button = msg_box.addButton("Project", QMessageBox.ActionRole)
        cash_button = msg_box.addButton("CA$H file", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        
        # Execute the message box and wait for user interaction
        msg_box.exec_()
        
        # Determine which button was clicked and perform the corresponding action
        if msg_box.clickedButton() == project_button:
            self.load_as_project()
        elif msg_box.clickedButton() == cash_button:
            self.load_as_cash_file()
        elif msg_box.clickedButton() == cancel_button:
            # Optional: Handle cancel action if needed
            pass
    
    def load_as_project(self):
        # Implement the logic to load configuration as a Project
        print("Loading configuration as Project...")
        # Add your loading logic here
    
    def load_as_cash_file(self):
        # Implement the logic to load configuration as a CA$H file
        print("Loading configuration as CA$H file...")
        # Add your loading logic here



########################## Config Saving Functions ##########################



    def save_config(self):
        # Get the configuration values from the UI
        project_name = self.save_config_textedit.toPlainText().strip()
        domain = self.cookie_domain_edit.toPlainText().strip()
        pars_after = self.capture_1_after.toPlainText().strip()
        pars_before = self.capture_1_before.toPlainText().strip()
        capture_1_before = self.capture_1_before.toPlainText().strip()
        capture_1_after = self.capture_1_after.toPlainText().strip()
        capture_2_before = self.capture_2_before.toPlainText().strip()
        capture_2_after = self.capture_2_after.toPlainText().strip()
        capture_3_before = self.capture_3_before.toPlainText().strip()
        capture_3_after = self.capture_3_after.toPlainText().strip()
        method = self.get_or_post_combobox.currentText().strip()
        url = self.http_url_request_textedit.toPlainText().strip()
        url_capture = self.url_capture_textedit.toPlainText().strip()
        response_valide = self.valid_response_text.toPlainText().strip()
    
        # Extract values from combo boxes
        user_agent = self.user_agent_combobox.currentText().strip()
        accept = self.accept_combobox.currentText().strip()
        content_type = self.content_type_combobox.currentText().strip()
        referer = self.referer_combobox.currentText().strip()
        x_content_type_options = self.x_content_type_options_combobox.currentText().strip()
        x_requested_with = self.x_requested_with_combobox.currentText().strip()
        creator = self.creator_config_textedit.toPlainText().strip()

        AddHeader1 = self.header_1_function.toPlainText().strip()
        AddHeader2 = self.header_2_function.toPlainText().strip()
        AddHeader3 = self.header_3_function.toPlainText().strip()
        AddHeader4 = self.header_4_function.toPlainText().strip()
        AddHeader5 = self.header_5_function.toPlainText().strip()
        Header1 = self.header_1_value.toPlainText().strip()
        Header2 = self.header_2_value.toPlainText().strip()
        Header3 = self.header_3_value.toPlainText().strip()
        Header4 = self.header_4_value.toPlainText().strip()
        Header5 = self.header_5_value.toPlainText().strip()
        
        
        
        # Prompt the user to choose how to save the configuration
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Save Configuration")
        msg_box.setText("How do you want to save your configuration?")
        project_button = msg_box.addButton("Project", QMessageBox.ActionRole)
        cash_button = msg_box.addButton("CA$H file", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Cancel)
        msg_box.exec_()
    
        # Determine which button was clicked and build the configuration content accordingly
        if msg_box.clickedButton() == project_button:
            config_content = f"""[Project Settings]
ProjectName={project_name}

[Request Settings]
Domain={domain}
ResponseValide={response_valide}
Header5={AddHeader5}={Header5}
Header4={AddHeader4}={Header4}
Header3={AddHeader3}={Header3}
Header2={AddHeader2}={Header2}
Header1={AddHeader1}={Header1}
AddHeader5=False
AddHeader4=False
AddHeader3=False
AddHeader2=False
AddHeader1=False
X-Requested-With={x_requested_with}
Referer={referer}
ContentType={content_type}
Accept={accept}
UserAgent={user_agent}
Body=
URL={url}
Method={method}

[Parser Settings]
ParsURL={url_capture}
ParsBefore={capture_1_before}
ParsAfter={capture_1_after}
UseParser=False
MethodParser=One
UseURL=False
"""
            self.save_to_file(config_content, "Project Files (*.proj)")
        elif msg_box.clickedButton() == cash_button:
            config_content = f"""[CA$H Settings]
ProjectName={project_name}

[Request Settings]
Domain={domain}
ResponseValide={response_valide}
Header5={Header5}
Header4={Header4}
Header3={Header3}
Header2={Header2}
Header1={Header1}
AddHeader5={AddHeader5}
AddHeader4={AddHeader4}
AddHeader3={AddHeader3}
AddHeader2={AddHeader2}
AddHeader1={AddHeader1}
X-Requested-With={x_requested_with}
Referer={referer}
ContentType={content_type}
Accept={accept}
UserAgent={user_agent}
Body=
URL={url}
Method={method}

[Parser Settings]
ParsURL={url_capture}
Capture1Before={capture_1_before}
Capture1After={capture_1_after}
Capture2Before={capture_2_before}
Capture2After={capture_2_after}
Capture3Before={capture_3_before}
Capture3After={capture_3_after}
UseParser=False
MethodParser=One
UseURL=False

[Security]
CreatorID={creator}
Checksum=
"""
            self.save_to_file(config_content, "CA$H Files (*.cash)")

    def save_to_file(self, content, file_filter):
        # Open a file dialog to save the file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", file_filter, options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(content)
            QMessageBox.information(self, "Saved", "Configuration saved successfully.")


    def save_as_project(self, config_text):
        # Open a file dialog to save as a project file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as Project", "", "Project Files (*.proj);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(config_text)
            QMessageBox.information(self, "Saved", "Configuration saved as a project file.")
    
    def save_as_cash_file(self, config_text):
        # Open a file dialog to save as a CA$H file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as CA$H File", "", "CA$H Files (*.cash);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(config_text)
            QMessageBox.information(self, "Saved", "Configuration saved as a CA$H file.")
########################################################################




################## TOOL BUTTON  DEV DIALOG WINDOW ##########################
    def openDialog(self):
        # Open the dialog window
        dialog = CustomDialog(self)
        dialog.exec_()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the dialog window
        self.setWindowTitle("Dialog with Tabs")
        self.setGeometry(100, 100, 400, 300)

        # Create a QVBoxLayout
        layout = QVBoxLayout(self)

        # Create a QTabWidget
        tabWidget = QTabWidget(self)

        # Create the first page
        firstPage = QWidget()
        firstPageLayout = QVBoxLayout()
        firstPageLayout.addWidget(QLabel("This is the first page."))
        firstPage.setLayout(firstPageLayout)

        # Create the second page
        secondPage = QWidget()
        secondPageLayout = QVBoxLayout()
        
        # Developer contact information
        contactLabel = QLabel("Developer Contact: developer@example.com")
        secondPageLayout.addWidget(contactLabel)

        # Version number
        versionLabel = QLabel("Version: 1.0.0")
        secondPageLayout.addWidget(versionLabel)

        # Update button
        updateButton = QPushButton("Check for Updates")
        updateButton.clicked.connect(self.checkForUpdates)
        secondPageLayout.addWidget(updateButton)

        secondPage.setLayout(secondPageLayout)

        # Add pages to the tab widget
        tabWidget.addTab(firstPage, "Page 1")
        tabWidget.addTab(secondPage, "Page 2")

        # Add the tab widget to the dialog layout
        layout.addWidget(tabWidget)

    def checkForUpdates(self):
        # Placeholder function for update logic
        print("Checking for updates...")
########################################################################

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()