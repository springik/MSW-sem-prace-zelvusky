Změna z THRESH_BINARY_INV na THRESH_BINARY
- želvušky jsou světlé mělo by fungovat lépe

Přidání CLAHE(Contrast Limited Adaptive Histogram Equalization)
- zbavení se odlesků pro zlepšení tresholdingu(doufám, že zmizí čáry jinak už jsem na konci sil)

Výsledkem bylo, že sice zmizely náhodné čáry, ale i želvušky.
Další kroky:
- zlehčení openingu(otevření)
- snížení hranice sure_foreground, aby je neignoroval watershed