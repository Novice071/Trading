#daten beschaffen
import yfinance as yf

# Beispiel: Daten für Apple (AAPL) herunterladen
data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Zeige die ersten Zeilen der heruntergeladenen Daten an
print(data.head())

#Momentum berechnen
# Berechne das Momentum (z.B. 12-Monats-Momentum, ca. 252 Handelstage)
data['Momentum'] = data['Close'].pct_change(periods=252)  # 252 Handelstage im Jahr

# Zeige die ersten Zeilen mit berechnetem Momentum
print(data[['Close', 'Momentum']].head())

#Erstelle Handelssignale
# Erstelle ein Signal basierend auf dem Momentum
data['Signal'] = 0
data.loc[data['Momentum'] > 0, 'Signal'] = 1  # Kaufsignal bei positivem Momentum
data.loc[data['Momentum'] <= 0, 'Signal'] = -1  # Verkaufssignal bei negativem Momentum

# Zeige die ersten Zeilen mit den Handelssignalen
print(data[['Close', 'Momentum', 'Signal']].tail())

#Simuliere Strategie Performance
# Berechne die täglichen Renditen
data['Daily_Return'] = data['Close'].pct_change()

# Berechne die Strategie-Performance
data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']

# Berechne die kumulierten Renditen
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()
data['Cumulative_Market_Return'] = (1 + data['Daily_Return']).cumprod()

# Zeige die kumulierten Renditen
print(data[['Cumulative_Strategy_Return', 'Cumulative_Market_Return']].tail())


#Visualiserung
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.plot(data['Cumulative_Strategy_Return'], label='Momentum Strategy')
plt.plot(data['Cumulative_Market_Return'], label='Market Returns')
plt.title('Momentum Strategy vs Market Returns')
plt.legend()
plt.show()

#Daten bereinigen
# Entferne Zeilen, in denen das Momentum nicht berechnet werden konnte
data = data.dropna(subset=['Momentum'])

# Dann kannst du das Signal und die Strategie-Performance neu berechnen
data['Signal'] = 0
data.loc[data['Momentum'] > 0, 'Signal'] = 1
data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()
data['Cumulative_Market_Return'] = (1 + data['Daily_Return']).cumprod()

# Plot erneut erstellen
plt.figure(figsize=(12, 8))
plt.plot(data['Cumulative_Strategy_Return'], label='Momentum Strategy')
plt.plot(data['Cumulative_Market_Return'], label='Market Returns')
plt.title('Momentum Strategy vs Market Returns')
plt.legend()
plt.show()
