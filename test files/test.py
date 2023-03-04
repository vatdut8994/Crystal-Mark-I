# calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QBrush, QColor, QTextCharFormat, QPalette
from PyQt5.QtCore import Qt, QDate


class CustomCalendarWidget(QCalendarWidget):
    def paintCell(self, painter, rect, date):
        if date.month() == self.monthShown() and date.year() == self.yearShown():
            # This is a date in the current month, set the background color to white
            background_color = QColor(255, 255, 255)
        else:
            # This is a date not in the current month, set the background color to light gray
            background_color = QColor(200, 200, 200)

        # Set the background color for the cell
        painter.fillRect(rect, QBrush(background_color))

        # Call the parent implementation of paintCell to draw the text
        super().paintCell(painter, rect, date)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Calendar Example")

calendar = CustomCalendarWidget()
# calendar.setGridVisible(True)

calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

# Set the background color for the entire window
window.setStyleSheet("background-color: black;color: white;")



current_date = QDate.currentDate()
start_date = QDate(current_date.year(), current_date.month(), 1)
end_date = QDate(current_date.year(), current_date.month(), current_date.daysInMonth())

date = start_date
brush = QBrush(QColor(14, 29, 39))
format = QTextCharFormat()
format.setBackground(brush)

while date <= end_date:
    calendar.setDateTextFormat(date, format)
    date = date.addDays(1)



format = QTextCharFormat()
format.setForeground(QBrush(Qt.white))

# Set the text color
palette = calendar.palette()
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
calendar.setPalette(palette)

# Set the selected date background color
brush = QBrush(QColor(170, 222, 175))
format = QTextCharFormat()
format.setBackground(brush)
calendar.setDateTextFormat(calendar.selectedDate(), format)

# Remove red text
format = QTextCharFormat()
format.setForeground(QBrush(Qt.white))
format.setBackground(QBrush(QColor(24, 38, 41)))
calendar.setWeekdayTextFormat(Qt.Monday, format)
calendar.setWeekdayTextFormat(Qt.Tuesday, format)
calendar.setWeekdayTextFormat(Qt.Wednesday, format)
calendar.setWeekdayTextFormat(Qt.Thursday, format)
calendar.setWeekdayTextFormat(Qt.Friday, format)
calendar.setWeekdayTextFormat(Qt.Saturday, format)
calendar.setWeekdayTextFormat(Qt.Sunday, format)

brush = QBrush(QColor(200, 200, 200))

# Create a text format with the brush as the foreground
format = QTextCharFormat()
format.setForeground(brush)

# Set the format for the not-part-of-the-month dates
# calendar.setNotationTextFormat(QTextCharFormat(), format)

layout = QVBoxLayout()
layout.addWidget(calendar)

central_widget = QWidget()
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

window.show()
sys.exit(app.exec_())
