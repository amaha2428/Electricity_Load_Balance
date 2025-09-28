# Electricity_Load_Balance




# ☀️ SolarSize Nigeria

**SolarSize Nigeria** is an interactive Streamlit web app designed to help Nigerian households and small businesses calculate their daily energy consumption, size a solar power system accurately, optimize load based on budget and priority, and find local vendors.

---

## 🚀 Features

- 🔌 **Electrical Load Calculator**  
  Select from common or custom appliances to calculate daily, monthly, and total energy usage.

- ☀️ **Solar System Sizing**  
  Automatically estimates required solar panel capacity (`kWp`), battery storage (`kWh`), and recommends optimal solar panels.

- ⚖️ **Load Optimization**  
  Allows users to prioritize appliances (High, Medium, Low) and fit systems into budget constraints.

- 🏪 **Vendor Finder**  
  Suggests reliable solar vendors based on your location and system type. Also allows new vendors to register.

- 📊 **Visualizations**  
  Pie charts, bar plots, and cost breakdowns help users understand energy distribution and financial impact.

---

## 🖥️ Live Demo

🌐 [View Deployed App on Streamlit Cloud](https://solar-size.streamlit.app/)

---

## 🧰 Tech Stack

- Python 🐍
- Streamlit 🎈
- Pandas & NumPy 📊
- Plotly Express & Graph Objects 📈

---

## 📦 Installation & Local Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/solar-size-app.git
cd solar-size-app
````

### 2. Install Dependencies

Make sure you have Python 3.8+ installed. Then:

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run solar_app_prototype.py
```

---

## 🧮 How It Works

### 🏠 Load Calculator

Calculates daily energy usage with:

$$
\text{kWh} = \frac{\text{Power (W)} \times \text{Hours}}{1000}
$$

### ☀️ Solar Sizing

Determines required solar capacity with:

$$
\text{Solar kWp} = \frac{\text{Daily kWh}}{\text{Solar Irradiance} \times \text{Efficiency}}
$$

Battery sizing:

$$
\text{Battery kWh} = \text{Daily kWh} \times \text{Autonomy Days}
$$

### ⚖️ Load Optimization

Filters appliances by priority and finds the best-fit system for a given budget, with ROI and savings estimates.

---

## 📂 Project Structure

```
solar-size-app/
│
├── solar_app_prototype.py    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Optional: Ignore __pycache__, .DS_Store etc.
```

---

## 💡 Future Improvements

* ✅ Persistent storage for vendor registration
* 🔋 Add support for different battery types and depth-of-discharge
* 📡 Integration with Google Maps for vendor location
* 🧾 PDF or CSV report generation
* 🛑 User authentication and admin backend

---

## 🙌 Acknowledgements

Built by [God’spower Amaha](mailto:amahagodspower@gmail.com)
• Data and AI for a brighter future.

---

## 📜 License

This project is open-source and free to use under the MIT License.

````
