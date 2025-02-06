# **Art Letters** 🎨

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://art-letters.streamlit.app)

**Create unique art using letters.**

This interactive **Streamlit** app allows you to enter letters, style their edges,
color enclosed polygons, and download the result as a **PNG with a transparent background**.

---

## **Features**

✅ **Interactive polygon selection** – Click on any polygon to change its color.  
✅ **Custom edge styling** – Adjust color, width, and curvature of edges.  
✅ **Random color generation** – Instantly apply random colors to all polygons.  
✅ **Transparent PNG export** – Save high-quality images with adjustable resolution.  

---

## **Installation**

This project is managed with [Poetry](https://python-poetry.org/).  
To set up the environment, run:

```bash
git clone https://github.com/killian31/art-letters.git
cd art-letters
poetry install
```

If you don’t have Poetry installed, first install it using:

```bash
pip install poetry  # or follow https://python-poetry.org/docs/#installation
```

## Running the App

Once installed, start the Streamlit app by running:

```bash
poetry run streamlit run app.py
```
