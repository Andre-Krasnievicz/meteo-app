# 🌤️ App Meteorológico com Streamlit

Este projeto é um aplicativo interativo desenvolvido com **Streamlit** para visualização de dois tipos de diagramas meteorológicos:

- 🌡️ **Diagrama Skew-T** (radiossondagem)
- 📈 **Meteograma T–Td** (dados horários)

O app permite ao usuário explorar visualmente dados meteorológicos de diferentes localidades e datas, com foco em análise termodinâmica da atmosfera.

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Python 3.12
- `pip`
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run Home.py
