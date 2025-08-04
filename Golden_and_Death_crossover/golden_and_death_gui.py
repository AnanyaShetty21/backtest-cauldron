import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLineEdit, QDateEdit, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
import pandas as pd
from dhanhq import dhanhq

def golden_death(client_id, access_token, ticker, to_date, from_date):
    dhan = dhanhq(client_id, access_token)
    df_full = pd.read_csv("midcap_symbol_with_security_ids.csv")
    id = df_full.loc[df_full['Symbol']==ticker.upper(), 'SEM_SMST_SECURITY_ID']
    id = id.values[0]
    dhan_historical_data = dhan.historical_daily_data(security_id=str(id), exchange_segment='NSE_EQ', instrument_type='EQUITY', from_date=from_date, to_date=to_date)    
    df = pd.DataFrame(dhan_historical_data['data'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
    df['timestamp'] = df['timestamp'] + pd.DateOffset(days=1) # for some reason the above conversion was offsetting the day by one 
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
    golden_locs = []
    death_locs = []
    for i in range(1, len(df)):
        if(df.iloc[i]['EMA50']>df.iloc[i]['EMA200'] and df.iloc[i-1]['EMA50']<df.iloc[i-1]['EMA200']):
            golden_locs.append(str(df.iloc[i]['timestamp']).split()[0])
        elif(df.iloc[i]['EMA50']<df.iloc[i]['EMA200'] and df.iloc[i-1]['EMA50']>df.iloc[i-1]['EMA200']):
            death_locs.append(str(df.iloc[i]['timestamp']).split()[0])

    return golden_locs, death_locs

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Golden and Death Crossovers")
        layout = QVBoxLayout()
        self.client_id = QLineEdit()
        self.client_id.setEchoMode(QLineEdit.Password)
        self.access_token = QLineEdit()
        self.access_token.setEchoMode(QLineEdit.Password)
        self.ticker = QLineEdit()
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.submit_button = QPushButton("Submit")
        self.submit_button.setEnabled(False)
        self.golden_list = QListWidget()
        self.death_list = QListWidget()
        self.golden_data = []
        self.death_data = []

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Client ID: "))
        row1.addWidget(self.client_id)
        row1.addWidget(QLabel("Access token: "))
        row1.addWidget(self.access_token)
        row1.addWidget(QLabel("Ticker: "))
        row1.addWidget(self.ticker)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("From date:"))
        row2.addWidget(self.from_date)
        row2.addWidget(QLabel("To date:"))
        row2.addWidget(self.to_date)
        row2.setContentsMargins(250, 0, 250, 0)
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(self.submit_button)
        layout.addLayout(row3)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Golden crossover dates "))
        row4.addWidget(QLabel("Death crossover dates "))
        layout.addLayout(row4)

        row5 = QHBoxLayout()
        row5.addWidget(self.golden_list)
        row5.addWidget(self.death_list)
        layout.addLayout(row5)

        self.setLayout(layout)
        self.connect_signals()

    def validate(self):
        is_valid = all([self.client_id.text().strip(), self.access_token.text().strip(), self.ticker.text().strip(), self.from_date.date()<self.to_date.date()])
        self.submit_button.setEnabled(is_valid)

    def connect_signals(self):
        lineEdits = [self.client_id, self.access_token, self.ticker]
        dateEdits = [self.from_date, self.to_date]
        for item in lineEdits:
            item.textChanged.connect(self.validate)
        for item in dateEdits:
            item.dateChanged.connect(self.validate)
        self.submit_button.clicked.connect(self.on_submit)

    def on_submit(self):
        client_id = self.client_id.text().strip()
        access_token = self.access_token.text().strip()
        ticker = self.ticker.text().strip()
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")

        try:
            self.golden_data, self.death_data = golden_death(client_id, access_token, ticker, to_date, from_date)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch data: {e}\n")
            self.golden_data = []
            self.death_data = []

        self.golden_list.clear()
        self.death_list.clear()

        self.golden_list.addItems(self.golden_data)
        self.death_list.addItems(self.death_data)

    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = GUI()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())