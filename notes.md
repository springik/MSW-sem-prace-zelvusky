# Techniky zpracování

## Rozostření a redukce šumu (Gaussův blur)

### Co to dělá?

- Pixely nahrádí průměrem
- Vlastně rozmaže snímek

### K čemu to je?

- Odstranění šumu
- Ať každé zrnko není želvuška

## Tresholding

### Co to dělá?

- Podle prahu převede pixely na extémy
- Řekněme jas nad 100 je bílá a rovná se a pod černá
- Tak tvoří binární masku

### K čemu to je?

- Zjístíme tak obrysy želvušek

Zkusíme použít Otsuovu metodu

## Morfologické operátory(Opravy bin. masky)

### Eroze

#### Co to dělá?

- Žere okraje bílých oblastí
- Pozře tečky šumu(zbývající)
- Zmenšuje i to užitečné(želvušky)

### Dilatace

#### Co to dělá?

- Nafoukne bílé oblasti
- Zacelí možné díry
- Spojí možné přerušení

### Kombinace

#### Otevření

- Eroze -> Dilatace

##### Co to dělá?

- Smaže menší šum a zpět zvětší objekty

#### Uzavření

- Dilatace -> Eroze

##### Co to dělá?

- Ucpe malé díry uvnitř želvušek

### Wateshed algoritmus

#### Co to dělá?

- Když si představíme binární obraz jako topologickou mapu, z lokálních minim "napustí vodu",kde se nám setkají hladiny z 2 různých údolí postavíme "hráz"
- Pokud se želvušky dotýkají Thresholdingem z nich uděláme jeden flek, díky tomuto je zase rozřízneme