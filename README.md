# Zelda Game

This is a Zelda-inspired game made using Pygame and Python.

## Getting Started

To get started, you'll need to clone repo and create a virtual environment and install the required packages. Here are the steps:

1. **clone the repository"**
```bash
git clone https://github.com/FluffyRudy/zelda.git
```

2. **Create a virtual environment:**
Open a terminal and navigate to the directory where you cloned the repository. Then, run the following command to create a new virtual environment:
This will create a new virtual environment named `venv`.
```bash
cd zelda
python3 -m venv .env
```

3. **Activate the virtual environment:**

Depending on your operating system, activate virtual environment:
- **Linux/macOS:**

  ```
  source venv/bin/activate
  ```

- **Windows:**

  ```
  venv\Scripts\activate
  ```

4. **Install the required packages:**

Once the virtual environment is activated, you can install the required packages by running the following command:
```bash
pip install -r requirements.txt
```

5. **Running the game**

```bash
python3 main.py
```