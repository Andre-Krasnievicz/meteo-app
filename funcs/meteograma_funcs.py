import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from meteostat import Hourly
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from datetime import datetime
from typing import Union
import pytz

def get_data(station_id: str, start: datetime, end: datetime, local_tz: Union[str, pytz.BaseTzInfo]) -> DataFrame:
    # baixa dados horários
    data = Hourly(station_id, start, end)

    # pega somente temp e dew point
    df = data.fetch()[["temp","dwpt"]]

    # ajusta índice de UTC para horário local
    df = df.tz_localize("UTC").tz_convert(local_tz)

    return df

def plot_temp_td(df: DataFrame, place: str, start: datetime, end: datetime, tz) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df["temp"],  "r-", label="Temperatura (°C)")
    ax.plot(df.index, df["dwpt"], "b-", label="Ponto de orvalho (°C)")

    # limites e margens
    ax.set_xlim(df.index.min(), df.index.max())
    ax.margins(x=0)
    ax.set_ylim(10, 35)

    # eixo X: principais a cada 6 h, secundárias a cada 1 h
    ax.xaxis.set_major_locator(HourLocator(byhour=range(0,24,6), tz=tz))
    ax.xaxis.set_minor_locator(HourLocator(byhour=range(0,24,1), tz=tz))
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m %Hh", tz=tz))

    # eixo Y: principais a cada 5 °C, secundárias a cada 1 °C
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # grades
    ax.grid(which="major", linestyle="-", linewidth=0.8, alpha=0.7)
    ax.grid(which="minor", linestyle="--", linewidth=0.5, alpha=0.5)

    # título em DD/MM/AAAA ou intervalo
    if start.date() == end.date():
        title_date = start.strftime("%d/%m/%Y")
    else:
        title_date = f"{start.strftime('%d/%m/%Y')} a {end.strftime('%d/%m/%Y')}"
    ax.set_title(f"{place} — {title_date}")

    ax.set_xlabel("Data e Hora (Local)")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    st.pyplot(fig)