import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QDialog, QTextEdit, QDateEdit
from datetime import datetime

class Event:
    def __init__(self, name, date, description):
        self.name = name
        self.date = date
        self.description = description

class Character:
    def __init__(self, name, periods):
        self.name = name
        self.periods = periods

class Period:
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

class HistorianDatabase:
    def __init__(self):
        self.events = []
        self.characters = []
        self.periods = []

    def add_event(self, name, date, description):
        event = Event(name, date, description)
        self.events.append(event)

    def add_character(self, name, periods):
        character = Character(name, periods)
        self.characters.append(character)

    def add_period(self, name, start_date, end_date):
        period = Period(name, start_date, end_date)
        self.periods.append(period)

    def search_event(self, keyword):
        result = []
        for event in self.events:
            if keyword.lower() in event.name.lower():
                result.append(event)
        return result

class EventDetailsDialog(QDialog):
    def __init__(self, event, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Olay Detayları")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.name_label = QLabel(f"<b>Olay Adı:</b> {event.name}")
        self.date_label = QLabel(f"<b>Tarih:</b> {event.date.strftime('%d/%m/%Y')}")
        self.description_label = QLabel(f"<b>Açıklama:</b> {event.description}")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.description_label)

        self.setLayout(self.layout)

class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Etkinlik Ekle")

        layout = QVBoxLayout()

        self.name_label = QLabel("Etkinlik Adı:")
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        self.date_label = QLabel("Tarih:")
        self.date_edit = QDateEdit()
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_edit)

        self.description_label = QLabel("Açıklama:")
        self.description_edit = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_edit)

        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_event)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_event(self):
        name = self.name_edit.text()
        date_str = self.date_edit.date().toString("dd/MM/yyyy")
        description = self.description_edit.toPlainText()

        if not name or not date_str or not description:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Geçersiz tarih formatı. Lütfen 'dd/mm/yyyy' formatında girin.")
            return

        self.parent().db.add_event(name, date, description)
        QMessageBox.information(self, "Bilgi", "Etkinlik başarıyla eklendi.")
        self.accept()

class AddCharacterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Kişi Ekle")

        layout = QVBoxLayout()

        self.name_label = QLabel("Kişi Adı:")
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        self.periods_label = QLabel("Dönemler:")
        self.periods_edit = QLineEdit()
        layout.addWidget(self.periods_label)
        layout.addWidget(self.periods_edit)

        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_character)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_character(self):
        name = self.name_edit.text()
        periods_str = self.periods_edit.text()

        if not name or not periods_str:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        periods = []
        for period_str in periods_str.split(','):
            period_parts = period_str.strip().split('-')
            if len(period_parts) != 3:
                QMessageBox.warning(self, "Uyarı", "Geçersiz dönem formatı. Lütfen 'Dönem Adı - Başlangıç Tarihi - Bitiş Tarihi' formatında girin.")
                return
            period_name = period_parts[0].strip()
            start_date_str = period_parts[1].strip()
            end_date_str = period_parts[2].strip()
            try:
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
            except ValueError:
                QMessageBox.warning(self, "Uyarı", "Geçersiz tarih formatı. Lütfen 'dd/mm/yyyy' formatında girin.")
                return
            periods.append(Period(period_name, start_date, end_date))

        self.parent().db.add_character(name, periods)
        QMessageBox.information(self, "Bilgi", "Kişi başarıyla eklendi.")
        self.accept()

class HistorianApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HistorianDatabase()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tarihçi - Tarihi Olaylar Veritabanı')
        self.setGeometry(700, 250, 800, 600)

        self.layout = QVBoxLayout()

        self.search_label = QLabel('Olay Ara:')
        self.search_edit = QLineEdit()
        self.search_button = QPushButton('Ara')
        self.search_edit.setStyleSheet("QLineEdit { padding: 5px; }")
        self.search_button.setStyleSheet("QPushButton { padding: 5px; background-color: green;border-radius:5px; padding: 19px 30px; color: white; font-family: Arial; font-size: 17px; font-weight: bold; }") 
        self.search_button.clicked.connect(self.search_event)

        self.event_list = QListWidget()
        self.event_list.itemDoubleClicked.connect(self.show_event_details)

        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_edit)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.event_list)

        self.add_event_button = QPushButton('Etkinlik Ekle')
        self.add_event_button.setStyleSheet("QPushButton { padding: 5px; background-color: orange;border-radius:5px; padding: 19px 30px; color: white; font-family: Arial; font-size: 17px;font-weight: bold;}")  
        self.add_event_button.clicked.connect(self.add_event_dialog)
        self.layout.addWidget(self.add_event_button)

        self.add_character_button = QPushButton('Kişi Ekle')
        self.add_character_button.setStyleSheet("QPushButton { padding: 5px; background-color: orange;padding: 19px 30px;border-radius:5px; color: white; font-family: sans-serif;font-size: 17px;font-weight: bold; }")  
        self.add_character_button.clicked.connect(self.add_character_dialog)
        self.layout.addWidget(self.add_character_button)

        self.show_characters_button = QPushButton('Kişileri Göster')
        self.show_characters_button.setStyleSheet(
            "QPushButton { padding: 5px; background-color: orange; padding: 19px 30px;border-radius:5px; color: white; font-family: sans-serif; font-size: 17px;font-weight: bold;}") 
        self.show_characters_button.clicked.connect(self.show_characters)
        self.layout.addWidget(self.show_characters_button)

        self.setLayout(self.layout)

        self.add_sample_data()

    def add_sample_data(self):
        self.db.add_event('Fransız Devrimi', datetime(1789, 7, 14), 'Fransa Krallığına son verildi.')
        self.db.add_event('Amerikan Bağımsızlık Bildirgesi', datetime(1776, 7, 4), 'ABD\'nin bağımsızlığını ilan etti.')
        self.db.add_event('İlk İnsanın Ay\'a Ayak Basması', datetime(1969, 7, 20), 'Neil Armstrong, Ay\'a ayak bastı.')
        self.db.add_event('Berlin Duvarı Yıkıldı', datetime(1989, 11, 9), 'Almanya\'nın birleşmesini simgeleyen Berlin Duvarı yıkıldı.')
        self.db.add_event('İspanya İç Savaşı Başladı', datetime(1936, 7, 17), 'Franco liderliğindeki Milliyetçi Hareket, İspanya İç Savaşı\'nı başlattı.')
        self.db.add_event('İlk Demokratik Seçimler Güney Afrika\'da Yapıldı', datetime(1994, 4, 27), 'Nelson Mandela, Güney Afrika\'nın ilk siyahî başkanı seçildi.')
        self.db.add_event('Leonardo da Vinci Mona Lisa\'yı Yarattı', datetime(1503, 8, 21), 'Leonardo da Vinci, ünlü tablosu Mona Lisa\'yı yarattı.')
        self.db.add_event('Hiroşima\'ya Atom Bombası Atıldı', datetime(1945, 8, 6), 'ABD, Hiroşima\'ya ilk atom bombasını attı.')
        self.db.add_event('Louis Pasteur, Kuduz Aşısını Buldu', datetime(1885, 7, 6), 'Louis Pasteur, kuduz aşısını buldu ve ilk kez bir insan üzerinde denedi.')
        self.db.add_event('İlk Dünya Kadınlar Günü Kutlandı', datetime(1909, 3, 8), 'Clara Zetkin tarafından önerilen Uluslararası Kadınlar Günü kutlandı.')

        for event in self.db.events:
            self.event_list.addItem(f'{event.name}\n- Tarih: {event.date.strftime("%d/%m/%Y")}\n- Açıklama: {event.description}\n\n')

    def search_event(self):
        keyword = self.search_edit.text()
        if keyword.strip() != '':
            results = self.db.search_event(keyword)
            if results:
                self.event_list.clear()
                for event in results:
                    self.event_list.addItem(f'{event.name}\n- Tarih: {event.date.strftime("%d/%m/%Y")}\n- Açıklama: {event.description}\n\n')
            else:
                QMessageBox.warning(self, 'Uyarı', 'Eşleşen olay bulunamadı.')
        else:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir arama kelimesi girin.')

    def show_event_details(self, item):
        event_name = item.text().split(' - ')[0]
        for event in self.db.events:
            if event.name == event_name:
                dialog = EventDetailsDialog(event, self)
                dialog.exec_()

    def show_historical_leaders(self):
        sorted_characters = sorted(self.db.characters, key=lambda character: character.periods[0].start_date)
        leaders_text = "Tarihi Liderler:\n"
        for character in sorted_characters:
            periods_text = "\n".join([
                                         f"    - {period.name}: {period.start_date.strftime('%d/%m/%Y')} - {period.end_date.strftime('%d/%m/%Y')}"
                                         for period in character.periods])
            leaders_text += f"- {character.name}:\n{periods_text}\n"
        QMessageBox.information(self, 'Tarihi Liderler', leaders_text)

    def add_event_dialog(self):
        dialog = AddEventDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.event_list.clear()
            for event in self.db.events:
                self.event_list.addItem(f'{event.name}\n- Tarih: {event.date.strftime("%d/%m/%Y")}\n- Açıklama: {event.description}\n\n')

    def add_character_dialog(self):
        dialog = AddCharacterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, 'Bilgi', 'Kişi başarıyla eklendi.')

    def show_characters(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Kişiler")
        dialog.setGeometry(800, 320, 600, 400) 

        layout = QVBoxLayout()
        characters_label = QLabel("Kişiler:")
        characters_list = QListWidget()

        for character in self.db.characters:
            periods_text = "\n".join(
                [f"- {period.name}: {period.start_date.strftime('%d/%m/%Y')} - {period.end_date.strftime('%d/%m/%Y')}"
                 for period in character.periods])
            characters_list.addItem(f"{character.name}:\n{periods_text}\n")

        layout.addWidget(characters_label)
        layout.addWidget(characters_list)
        dialog.setLayout(layout)

        leaders_list = [
            "Mustafa Kemal Atatürk - Kurtuluş Savaşı (1919/05/19 - 1923/07/24)",
            "Napolyon Bonapart - Napolyon Savaşları (1799/11/09 - 1815/06/22)",
            "Gandhi - Hint Bağımsızlık Hareketi (1915/01/09 - 1947/08/15)",
            "Adolf Hitler - Nazi Almanyası (1933/01/30 - 1945/04/30)",
            "Mao Zedong - Çin Devrimi (1949/10/01 - 1976/09/09)",
            "Winston Churchill - II. Dünya Savaşı (1939/09/01 - 1945/09/02)",
            "Joseph Stalin - Sovyetler Birliği Dönemi (1922/04/03 - 1953/03/05)",
            "Queen Victoria - Victorian Çağı (1837/06/20 - 1901/01/22)",
            "Martin Luther King Jr. - Sivil Haklar Hareketi (1955/12/01 - 1968/04/04)",
            "Cleopatra - Mısır Hükümdarlığı (-51/01/01 - -30/08/12)",
            "Elizabeth I - Elizabeth Dönemi (1558/11/17 - 1603/03/24)",
            "Nelson Mandela - Güney Afrika Başkanlığı (1994/05/10 - 1999/06/14)",
            "Julius Caesar - Roma İmparatorluğu (-100/07/12 - -44/03/15)",
            "Mahatma Gandhi - Hindistan Bağımsızlık Hareketi (1915/01/09 - 1948/01/30)",
            "Catherine the Great - Rus İmparatorluğu (1762/07/09 - 1796/11/17)"
        ]
        for leader in leaders_list:
            characters_list.addItem(leader)

        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistorianApp()
    window.show()
    sys.exit(app.exec_())
