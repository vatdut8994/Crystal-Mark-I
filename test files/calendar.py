import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QTextFormat, QTextCharFormat

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # Create the calendar widget
        calendar = QCalendarWidget(self)
        
        # Remove the header
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        
        # Set the background color to black
        palette = calendar.palette()
        palette.setColor(palette.Window, QColor(0, 0, 0))
        calendar.setPalette(palette)
        
        # Set the foreground color to white
        palette.setColor(palette.Text, QColor(255, 255, 255))
        calendar.setPalette(palette)
        
        # Set the selected date's background color to green
        format = QTextCharFormat()
        format.setBackground(QColor(170, 222, 175))
        calendar.setDateTextFormat(calendar.selectedDate(), format)
        
        # Get the dates of the current month
        month = calendar.monthShown()
        year = calendar.yearShown()
        current_date = QDate.currentDate()
        days_in_month = QDate(current_date).daysInMonth()
        dates_in_month = [QDate(year, month, day) for day in range(1, days_in_month + 1)]
        start_date = QDate(current_date.year(), current_date.month(), 1)
        end_date = QDate(current_date.year(), current_date.month(), current_date.daysInMonth())
        
        # Set the background color of the current month's dates to green
        for date in dates_in_month:
            format = QTextCharFormat()
            format.setBackground(QColor(0, 255, 0))
            calendar.setDateTextFormat(date, format)
        
        # Set the background color of the dates which are not part of the month to blue
        for date in (calendar.dateRange(calendar.minimumDate(), calendar.maximumDate()) - set(dates_in_month)):
            format = QTextCharFormat()
            format.setBackground(QColor(0, 0, 255))
            calendar.setDateTextFormat(date, format)
        
        # Set the background color of the weekdays to red
        for i in range(7):
            format = QTextFormat()
            format.setBackground(QColor(255, 0, 0))
            calendar.setWeekdayTextFormat(i, format)
        
        # Set the calendar widget as the central widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(calendar)
        self.setCentralWidget(central_widget)
        
app = QApplication(sys.argv)
window = CalendarWindow()
window.show()
sys.exit(app.exec_())
