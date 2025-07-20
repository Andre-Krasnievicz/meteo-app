import streamlit as st
from datetime import datetime
from siphon.simplewebservice.wyoming import WyomingUpperAir
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units
from datetime import datetime
from pandas import DataFrame

def get_wyoming(dt: datetime, station: str, ICAO2WMO: dict) -> DataFrame:
    """Retorna DataFrame do sounding pelo código WMO ou ICAO."""
    queue = []
    if station.isdigit():
        queue.append(station)
    else:
        if station in ICAO2WMO:
            queue.append(ICAO2WMO[station])
        queue.append(station)

    for stn in queue:
        try:
            df = WyomingUpperAir.request_data(dt, stn)
            if not df.empty:
                return df
        except ValueError:
            continue
    raise ValueError(f"No sounding for {station} at {dt:%Y-%m-%d %HZ}")

def plot_T_Td(df: DataFrame, title: str | None = None) -> None:
    """Plota T (vermelho) e Td (azul) num Skew-T simplificado com figura maior."""
    p  = df['pressure'].values    * units(df.units['pressure'])
    T  = df['temperature'].values * units(df.units['temperature'])
    Td = df['dewpoint'].values    * units(df.units['dewpoint'])

    fig = plt.figure(figsize=(15, 10))
    skew = SkewT(fig)
    skew.plot(p,  T,  'r-', label='Temperatura')
    skew.plot(p, Td, 'b-', label='Ponto de orvalho')

    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-80, 40)
    skew.ax.set_xlabel('Temperatura (°C)')
    skew.ax.set_ylabel('Pressão (hPa)')
    skew.ax.legend()
    if title:
        plt.title(title)
    plt.grid(True)

    st.pyplot(fig)
