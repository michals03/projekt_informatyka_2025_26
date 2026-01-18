import sys
import datetime
from typing import List, Optional, Dict
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox, QSlider, QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt, QPointF, QTimer, QRectF
from PyQt5.QtGui import (QPainter, QColor, QPen, QPainterPath, QFont, QLinearGradient, QRadialGradient, QBrush)

COLORS = {
    'CIECZ_A': QColor(255, 80, 80),
    'CIECZ_B': QColor(80, 80, 255),
    'NIEDOGRZANY': QColor(140, 100, 255),
    'GOTOWY': QColor(50, 255, 50),
    'TLO': QColor(40, 40, 45),
    'RURA_PUSTA': QColor(60, 60, 65)
}
STYLESHEET = """
    QWidget { background-color: #2b2b2b; color: #e0e0e0; font-family: 'Arial', sans-serif; font-size: 14px; }
    QTabWidget::pane { border: 1px solid #444; }
    QTabBar::tab { background: #3a3a3a; color: #ccc; padding: 10px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
    QTabBar::tab:selected { background: #555; color: white; font-weight: bold; }
    QGroupBox { border: 1px solid #555; border-radius: 8px; margin-top: 20px; font-weight: bold; color: #aaa; }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
    QLineEdit { background-color: #3a3a3a; border: 1px solid #555; border-radius: 4px; padding: 4px; color: #fff; font-weight: bold; }
    QPushButton { background-color: #444; border: none; border-radius: 5px; padding: 8px; font-weight: bold; color: white; }
    QPushButton:hover { background-color: #555; }
    QPushButton#BtnStart { background-color: #2e7d32; }
    QPushButton#BtnStart:hover { background-color: #4caf50; }
    QPushButton#BtnReset { background-color: #c62828; }
    QPushButton#BtnReset:hover { background-color: #e53935; }
    QTextEdit { background-color: #1e1e1e; border: 1px solid #555; font-family: 'Consolas', monospace; }
"""
class Rura:
    def __init__(self, punkty: List[tuple], grubosc: int = 12):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.czy_plynie = False
        self.kolor_cieczy = COLORS['NIEDOGRZANY']

    def ustaw_przeplyw(self, plynie: bool, kolor: QColor = None):
        self.czy_plynie = plynie
        if kolor:
            self.kolor_cieczy = kolor

    def draw(self, painter: QPainter):
        if len(self.punkty) < 2:
            return
        
        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)
        pen_bg = QPen(COLORS['RURA_PUSTA'], self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen_bg)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        
        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)
            painter.drawPath(path)
            pen_h = QPen(self.kolor_cieczy.lighter(150), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_h)
            painter.drawPath(path)

class Pompa:
    def __init__(self, x: int, y: int, nazwa: str = ""):
        self.x = x
        self.y = y
        self.nazwa = nazwa
        self.aktywna = False
        self.rozmiar = 20  
        self.kat = 0

    def aktualizuj(self):
        if self.aktywna:
            self.kat = (self.kat + 10) % 360

    def draw(self, painter: QPainter):
        kolor = QColor(50, 255, 50) if self.aktywna else QColor(200, 50, 50)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(kolor)
        painter.drawEllipse(QPointF(self.x, self.y), self.rozmiar, self.rozmiar)
        
        if self.aktywna:
            painter.save()
            painter.translate(self.x, self.y)
            painter.rotate(self.kat)
            painter.setPen(QPen(Qt.black, 3))
            r = self.rozmiar - 6
            painter.drawLine(-r, 0, r, 0)
            painter.drawLine(0, -r, 0, r)
            painter.restore()
        else:
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            rect = QRectF(self.x - self.rozmiar, self.y - self.rozmiar, self.rozmiar*2, self.rozmiar*2)
            painter.drawText(rect, Qt.AlignCenter, "P")

class Mieszadlo:
    def __init__(self, x: int, y: int, dlugosc: int = 40):
        self.x = x
        self.y = y
        self.dlugosc = dlugosc
        self.kat = 0
        self.aktywne = False

    def aktualizuj(self):
        if self.aktywne:
            self.kat = (self.kat + 15) % 360

    def draw(self, painter: QPainter):
        painter.save()
        painter.translate(self.x, self.y)
        painter.setPen(QPen(QColor(180, 180, 180), 4))
        painter.drawLine(0, -130, 0, 0)
        painter.rotate(self.kat)
        painter.setPen(QPen(QColor(200, 200, 200), 6, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(-self.dlugosc//2, 0, self.dlugosc//2, 0)
        painter.drawLine(0, -self.dlugosc//2, 0, self.dlugosc//2)
        painter.restore()

class Grzalka:
    def __init__(self, x: int, y: int, width: int = 100):
        self.x = x
        self.y = y
        self.width = width
        self.aktywna = False

    def draw(self, painter: QPainter, clip_rect: QRectF = None):
        if self.aktywna:
            painter.save()
            if clip_rect:
                painter.setClipRect(clip_rect)
            glow = QRadialGradient(self.x, self.y - 10, 60)
            glow.setColorAt(0, QColor(255, 50, 0, 150))
            glow.setColorAt(1, QColor(255, 50, 0, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(self.x - 60), int(self.y - 70), 120, 120)
            painter.restore()
        kolor = QColor(255, 80, 80) if self.aktywna else QColor(100, 100, 100)
        painter.setPen(QPen(kolor, 3, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        start_x = self.x - self.width / 2
        path.moveTo(start_x, self.y)
        steps = 12
        step_w = self.width / steps
        for i in range(steps):
            off = -12 if i % 2 == 0 else 0
            path.lineTo(start_x + (i + 1) * step_w, self.y + off)
        painter.drawPath(path)

class Zbiornik:
    def __init__(self, x, y, width=80, height=120, nazwa="", kolor_cieczy=COLORS['NIEDOGRZANY'], 
                 pojemnosc=200, text_x_offset=0, text_y_offset=-35, 
                 info_x_offset=None, info_y_offset=None, temperatura_start=20.0, pokaz_temp=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.nazwa = nazwa
        self.pojemnosc = float(pojemnosc)
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0
        self.aktualny_kolor = kolor_cieczy
        self.temperatura = temperatura_start
        self.pokaz_temp = pokaz_temp
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        self.info_x_offset = info_x_offset
        self.info_y_offset = info_y_offset
        self.outlet_bottom = (x + width/2, y + height)
        self.inlet_top = (x + width/2, y)

    def czy_pusty(self) -> bool:
        return self.aktualna_ilosc <= 0.1

    def czy_pelny(self) -> bool:
        return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def dodaj_ciecz(self, ilosc: float) -> float:
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc: float) -> float:
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto
    
    def ustaw_poziom_manualnie(self, ilosc: float):
        self.aktualna_ilosc = max(0.0, min(float(ilosc), self.pojemnosc))
        self.aktualizuj_poziom()

    def aktualizuj_poziom(self):
        self.poziom = max(0.0, min(1.0, self.aktualna_ilosc / self.pojemnosc))

    def get_rect(self) -> QRectF:
        return QRectF(self.x, self.y, self.width, self.height)

    def get_wolne_miejsce(self) -> float:
        return self.pojemnosc - self.aktualna_ilosc
    
    def draw(self, painter: QPainter):
        bg_grad = QLinearGradient(self.x, self.y, self.x + self.width, self.y)
        bg_grad.setColorAt(0, QColor(60, 60, 60, 100))
        bg_grad.setColorAt(0.5, QColor(80, 80, 80, 50))
        bg_grad.setColorAt(1, QColor(60, 60, 60, 100))
        
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QBrush(bg_grad))
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

        if self.poziom > 0:
            h = self.height * self.poziom
            y_start = self.y + self.height - h
            
            liq_grad = QLinearGradient(self.x, y_start, self.x + self.width, y_start)
            c = self.aktualny_kolor
            liq_grad.setColorAt(0, c.darker(120))
            liq_grad.setColorAt(0.5, c)
            liq_grad.setColorAt(1, c.darker(120))
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(liq_grad))
            painter.drawRect(int(self.x + 2), int(y_start), int(self.width - 4), int(h - 1))
            
            if self.info_x_offset is None:
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Arial", 10, QFont.Bold))
                tekst = f"{self.aktualna_ilosc:.1f}L"
                if self.pokaz_temp:
                    tekst += f"\n{int(self.temperatura)}°C"
                painter.drawText(QRectF(self.x, y_start - 45, self.width, 40), Qt.AlignCenter, tekst)

        painter.setPen(QPen(QColor(180, 180, 180), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(int(self.x + self.text_x_offset), int(self.y + self.text_y_offset), self.nazwa)

        if self.info_x_offset is not None and self.aktualna_ilosc > 0.1:
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 9))
            tekst = f"Obj: {self.aktualna_ilosc:.1f} L"
            if self.pokaz_temp:
                tekst += f"\nTemp: {int(self.temperatura)} °C"
            painter.drawText(QRectF(self.x + self.info_x_offset, self.y + self.info_y_offset, 120, 50), 
                             Qt.AlignLeft | Qt.AlignTop, tekst)

class WidokRaportow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.raport = QTextEdit()
        self.raport.setReadOnly(True)
        layout.addWidget(QLabel("Podsumowanie Ostatniego Procesu:"))
        layout.addWidget(self.raport)
        self.setLayout(layout)

    def generuj_raport(self, dane: Dict):
        tekst = f"""
RAPORT KOŃCOWY PROCESU
======================
Data: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PARAMETRY WEJŚCIOWE:
- Surowiec A: {dane['a']} L
- Surowiec B: {dane['b']} L
- Temp. Cel:  {dane['cel_temp']} °C

WYNIKI:
- Temp. Końcowa: {dane['koniec_temp']} °C
- Status: {dane['status']}
- Zbiornik Docelowy: {dane['dest']}
======================    """
        self.raport.setText(tekst)

class WidokSystemu(QWidget):
    def __init__(self, raport_widget: WidokRaportow):
        super().__init__()
        self.raport_widget = raport_widget
        self.setMinimumSize(1000, 700)
        self.running = False
        self.stan_procesu = "STOP" 
        self.czas_mieszania = 0
        self.wymagane_mieszanie = 100
        self.docelowo_a = 0
        self.docelowo_b = 0
        self.wlane_a = 0.0
        self.wlane_b = 0.0
        self.temp_docelowa = 60.0
        self.timer = QTimer()
        self.timer.timeout.connect(self.cykl_automatyki)
        self.init_ui_elements()
        self.init_layout()

    def init_ui_elements(self):
        self.zb_a = Zbiornik(100, 80, nazwa="Surowiec 1", kolor_cieczy=COLORS['CIECZ_A'], pojemnosc=300, text_x_offset=90, text_y_offset=20, temperatura_start=0.0, pokaz_temp=False)
        self.zb_a.aktualna_ilosc = 200
        self.zb_a.aktualizuj_poziom()
        
        self.zb_b = Zbiornik(700, 80, nazwa="Surowiec 2", kolor_cieczy=COLORS['CIECZ_B'], pojemnosc=300, text_x_offset=90, text_y_offset=20, temperatura_start=0.0, pokaz_temp=False)
        self.zb_b.aktualna_ilosc = 200
        self.zb_b.aktualizuj_poziom()
        
        self.zb_c = Zbiornik(400, 250, width=140, height=160, nazwa="Mieszalnik", kolor_cieczy=COLORS['NIEDOGRZANY'], pojemnosc=250, text_x_offset=150, text_y_offset=20, info_x_offset=150, info_y_offset=50) 
        self.zb_d = Zbiornik(280, 500, width=140, height=140, nazwa="Zbiornik D", kolor_cieczy=COLORS['NIEDOGRZANY'], pojemnosc=300, text_x_offset=-80, text_y_offset=20, pokaz_temp=False)
        self.zb_e = Zbiornik(520, 500, width=140, height=140, nazwa="Zbiornik E", kolor_cieczy=COLORS['GOTOWY'], pojemnosc=300, text_x_offset=150, text_y_offset=20, pokaz_temp=False)
        
        self.zbiorniki = [self.zb_a, self.zb_b, self.zb_c, self.zb_d, self.zb_e]

        self.pompa1 = Pompa(140, 235)
        self.pompa2 = Pompa(740, 235)
        self.pompa3 = Pompa(470, 455)
        self.mieszadlo = Mieszadlo(470, 360)
        self.grzalka = Grzalka(470, 400, width=100)

        y_poziom = 235
        x_wlot_a, x_wlot_b = 430, 510
        
        p_a = self.zb_a.outlet_bottom
        self.rura_a = Rura([p_a, (p_a[0], y_poziom), (x_wlot_a, y_poziom), (x_wlot_a, 250)])
        
        p_b = self.zb_b.outlet_bottom
        self.rura_b = Rura([p_b, (p_b[0], y_poziom), (x_wlot_b, y_poziom), (x_wlot_b, 250)])
        
        p_c_out = self.zb_c.outlet_bottom
        y_split = 485
        x_target_d, x_target_e = 350, 590
        
        self.rura_out_common = Rura([p_c_out, (p_c_out[0], y_split)])
        self.rura_out_left = Rura([(p_c_out[0], y_split), (x_target_d, y_split), (x_target_d, 500)])
        self.rura_out_right = Rura([(p_c_out[0], y_split), (x_target_e, y_split), (x_target_e, 500)])
        
        self.rury = [self.rura_a, self.rura_b, self.rura_out_common, self.rura_out_left, self.rura_out_right]

    def init_layout(self):
        self.panel_receptura = QGroupBox("1. Parametry Procesu", self)
        self.panel_receptura.setGeometry(20, 650, 350, 200)
        l_rec = QVBoxLayout()
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("A (L) :"))
        self.inp_ilosc_a = QLineEdit("30")
        row1.addWidget(self.inp_ilosc_a)
        row1.addWidget(QLabel("B (L):"))
        self.inp_ilosc_b = QLineEdit("30")
        row1.addWidget(self.inp_ilosc_b)
        l_rec.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Temp. docelowa (°C):"))
        self.inp_temp = QLineEdit("0")
        row2.addWidget(self.inp_temp)
        l_rec.addLayout(row2)
        
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("START")
        self.btn_start.setObjectName("BtnStart")
        self.btn_start.clicked.connect(self.start_procesu)
        
        self.btn_reset = QPushButton("RESET")
        self.btn_reset.setObjectName("BtnReset")
        self.btn_reset.clicked.connect(self.reset_procesu)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_reset)
        l_rec.addLayout(btn_layout)
        
        self.lbl_status = QLabel("Stan: GOTOWY")
        self.lbl_status.setFont(QFont("Arial", 12, QFont.Bold))
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: #00bcd4; margin-top: 5px;")
        l_rec.addWidget(self.lbl_status)
        self.panel_receptura.setLayout(l_rec)

        self.panel_magazyn = QGroupBox("2. Magazyn", self)
        self.panel_magazyn.setGeometry(600, 650, 380, 200)
        l_mag = QVBoxLayout()
        
        self.lbl_slider_a = QLabel(f"Poziom A: {int(self.zb_a.aktualna_ilosc)}L")
        l_mag.addWidget(self.lbl_slider_a)
        self.slider_a = QSlider(Qt.Horizontal)
        self.slider_a.setRange(0, 300)
        self.slider_a.setValue(200)
        self.slider_a.valueChanged.connect(self.zmien_poziom_a)
        l_mag.addWidget(self.slider_a)
        
        self.lbl_slider_b = QLabel(f"Poziom B: {int(self.zb_b.aktualna_ilosc)}L")
        l_mag.addWidget(self.lbl_slider_b)
        self.slider_b = QSlider(Qt.Horizontal)
        self.slider_b.setRange(0, 300)
        self.slider_b.setValue(200)
        self.slider_b.valueChanged.connect(self.zmien_poziom_b)
        l_mag.addWidget(self.slider_b)
        
        self.btn_clean = QPushButton("Opróżnij Cały System")
        self.btn_clean.clicked.connect(self.wyczysc_system)
        l_mag.addWidget(self.btn_clean)
        self.panel_magazyn.setLayout(l_mag)

    def zmien_poziom_a(self, value):
        if not self.running:
            self.zb_a.ustaw_poziom_manualnie(value)
            self.lbl_slider_a.setText(f"Poziom A: {value}L")
            self.update()

    def zmien_poziom_b(self, value):
        if not self.running:
            self.zb_b.ustaw_poziom_manualnie(value)
            self.lbl_slider_b.setText(f"Poziom B: {value}L")
            self.update()

    def wyczysc_system(self):
        if not self.running:
            for zb in [self.zb_c, self.zb_d, self.zb_e]:
                zb.aktualna_ilosc = 0
                zb.aktualizuj_poziom()
            
            self.zb_c.temperatura = 0.0
            self.zb_c.aktualny_kolor = COLORS['NIEDOGRZANY']
            self.zb_d.aktualny_kolor = COLORS['NIEDOGRZANY']
            self.zb_e.aktualny_kolor = COLORS['GOTOWY']
            
            self.update()

    def oblicz_kolor_dla_temperatury(self, temp: float) -> QColor:
        return COLORS['NIEDOGRZANY'] if temp < 80.0 else COLORS['GOTOWY']

    def start_procesu(self):
        if self.running:
            return
        
        try:
            val_a = float(self.inp_ilosc_a.text())
            val_b = float(self.inp_ilosc_b.text())
            temp_target = float(self.inp_temp.text())
            
            if val_a <= 0 and val_b <= 0:
                raise ValueError("Podaj dodatnie ilości surowców.")
            
            if self.zb_a.aktualna_ilosc < val_a or self.zb_b.aktualna_ilosc < val_b:
                raise ValueError("Niewystarczająca ilość surowca w magazynie.")
            
            wolne_miejsce = self.zb_c.get_wolne_miejsce()
            if (val_a + val_b) > wolne_miejsce:
                raise ValueError(f"Przepełnienie mieszalnika! Wolne miejsce: {wolne_miejsce:.1f}L")

            self.docelowo_a = val_a
            self.docelowo_b = val_b
            self.wlane_a = 0
            self.wlane_b = 0
            self.temp_docelowa = temp_target
            self.zb_c.temperatura = 0.0
            self.zb_c.aktualny_kolor = COLORS['NIEDOGRZANY']
            
            self.slider_a.setEnabled(False)
            self.slider_b.setEnabled(False)
            
            self.stan_procesu = "DOZOWANIE"
            self.running = True
            self.timer.start(50) 
            self.lbl_status.setText("Stan: DOZOWANIE")
            
        except ValueError as e: 
            QMessageBox.critical(self, "Błąd Walidacji", str(e))

    def reset_procesu(self):
        self.running = False
        self.timer.stop()
        self.stan_procesu = "STOP"
        self.pompa1.aktywna = False
        self.pompa2.aktywna = False
        self.pompa3.aktywna = False
        self.mieszadlo.aktywne = False
        self.grzalka.aktywna = False
        
        for r in self.rury:
            r.ustaw_przeplyw(False)
            
        self.slider_a.setEnabled(True)
        self.slider_b.setEnabled(True)
        self.lbl_status.setText("Stan: ZATRZYMANO")
        self.update()

    def cykl_automatyki(self):
        if not self.running:
            return
        SPEED = 1.5 
        if self.stan_procesu == "DOZOWANIE":
            done_a = self.obsluz_dozowanie(self.zb_a, self.wlane_a, self.docelowo_a, self.pompa1, self.rura_a, COLORS['CIECZ_A'], SPEED)
            if not done_a: self.wlane_a += min(SPEED, self.docelowo_a - self.wlane_a)
            
            done_b = self.obsluz_dozowanie(self.zb_b, self.wlane_b, self.docelowo_b, self.pompa2, self.rura_b, COLORS['CIECZ_B'], SPEED)
            if not done_b: self.wlane_b += min(SPEED, self.docelowo_b - self.wlane_b)

            self.slider_a.setValue(int(self.zb_a.aktualna_ilosc))
            self.slider_b.setValue(int(self.zb_b.aktualna_ilosc))
            
            if done_a and done_b: 
                self.stan_procesu = "MIESZANIE" 
                self.czas_mieszania = self.wymagane_mieszanie
                self.lbl_status.setText("Stan: GRZANIE I MIESZANIE")

        elif self.stan_procesu == "MIESZANIE":
            self.mieszadlo.aktywne = True
            self.mieszadlo.aktualizuj()
            
            if self.zb_c.temperatura < self.temp_docelowa:
                self.grzalka.aktywna = True
                self.zb_c.temperatura += 0.3
            else:
                self.grzalka.aktywna = False
                self.zb_c.temperatura = self.temp_docelowa
            self.zb_c.aktualny_kolor = self.oblicz_kolor_dla_temperatury(self.zb_c.temperatura)
            
            if self.czas_mieszania > 0:
                self.czas_mieszania -= 1

            if self.czas_mieszania <= 0 and self.zb_c.temperatura >= self.temp_docelowa:
                self.mieszadlo.aktywne = False
                self.grzalka.aktywna = False
                self.stan_procesu = "OPROZNIANIE"
                self.lbl_status.setText("Stan: OPRÓŻNIANIE")

        elif self.stan_procesu == "OPROZNIANIE":
            kolor_produktu = self.zb_c.aktualny_kolor
            temp_final = self.zb_c.temperatura
            target_tank = self.zb_e if temp_final >= 80.0 else self.zb_d
            
            if not self.zb_c.czy_pusty() and not target_tank.czy_pelny():
                amt = self.zb_c.usun_ciecz(SPEED * 2)
                target_tank.dodaj_ciecz(amt)
                target_tank.aktualny_kolor = kolor_produktu
                
                self.pompa3.aktywna = True
                self.pompa3.aktualizuj()
                self.rura_out_common.ustaw_przeplyw(True, kolor_produktu)
                
                if target_tank == self.zb_e:
                    self.rura_out_right.ustaw_przeplyw(True, kolor_produktu)
                    self.rura_out_left.ustaw_przeplyw(False)
                else:
                    self.rura_out_left.ustaw_przeplyw(True, kolor_produktu)
                    self.rura_out_right.ustaw_przeplyw(False)
            else:
                self.koniec_procesu(temp_final)

        self.update()

    def obsluz_dozowanie(self, zrodlo: Zbiornik, wlane: float, cel: float, pompa: Pompa, rura: Rura, kolor, speed) -> bool:
        if wlane < cel:
            potrzeba = cel - wlane
            wolne_c = self.zb_c.get_wolne_miejsce()
            amt = min(speed, potrzeba, wolne_c)
            
            if amt > 0.01:
                pobrano = zrodlo.usun_ciecz(amt)
                self.zb_c.dodaj_ciecz(pobrano)
                pompa.aktywna = True
                pompa.aktualizuj()
                rura.ustaw_przeplyw(True, kolor)
                return False
        
        pompa.aktywna = False
        rura.ustaw_przeplyw(False)
        return True

    def koniec_procesu(self, temp_final):
        self.pompa3.aktywna = False
        self.rura_out_common.ustaw_przeplyw(False)
        self.rura_out_left.ustaw_przeplyw(False)
        self.rura_out_right.ustaw_przeplyw(False)
        self.stan_procesu = "KONIEC"
        self.lbl_status.setText("Stan: KONIEC")
        self.running = False
        self.timer.stop()
        self.slider_a.setEnabled(True)
        self.slider_b.setEnabled(True)
        
        dest_name = "Zbiornik E " if temp_final >= 80 else "Zbiornik D "
        self.raport_widget.generuj_raport({
            'a': self.docelowo_a, 
            'b': self.docelowo_b, 
            'cel_temp': self.temp_docelowa,
            'koniec_temp': int(temp_final), 
            'status': 'ZAKOŃCZONY', 
            'dest': dest_name
        })
        QMessageBox.information(self, "Proces Zakończony", f"Temperatura: {int(temp_final)}°C\nProdukt trafił do: {dest_name}")

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        for r in self.rury:
            r.draw(p)
            
        rect_c = self.zb_c.get_rect()
        
        for z in self.zbiorniki:
            z.draw(p)
        self.grzalka.draw(p, clip_rect=rect_c)
        self.pompa1.draw(p)
        self.pompa2.draw(p)
        self.pompa3.draw(p)
        self.mieszadlo.draw(p)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System SCADA ")
        self.setFixedSize(1020, 950)
        self.setStyleSheet(STYLESHEET)
        
        self.tabs = QTabWidget()
        self.ekran_raportow = WidokRaportow()
        self.ekran_instalacji = WidokSystemu(self.ekran_raportow)
        
        self.tabs.addTab(self.ekran_instalacji, " Instalacja ")
        self.tabs.addTab(self.ekran_raportow, " Raporty ")
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = MainWindow()
    okno.show()
    sys.exit(app.exec_())