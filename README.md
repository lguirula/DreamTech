# Dreamtech

Experiment description.

# Configuration

## Installation guide

1. **Clone the repository.**
    
    ```bash
    git clone https://github.com/lguirula/DreamTech.git
    cd DREAMTECH
    ```
    
2. **Create a Python virtual environment.**
    
    ```bash
    python -m venv env
    ```
    
3. **Activate the virtual environment and install the dependencies.**
    1. For Windows
        
        ```bash
        ./env/Scripts/Activate.ps1
        pip install -r requirements.txt
        ```
        
    2. For Linux / MacOS
        
        ```bash
        ./env/Scripts/activate
        pip install -r requirements.txt
        ```
        
4. **Run the program.**
    1. For the experiments:
        
        ```bash
        python .\menuBotones.py
        ```

    2. For PyQT5Designer:
        ```bash
        .\env\Scripts\designer.exe
        ```
        To generate .py file:
        ```bash
        python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
        ```

## Inputs

Since JSON is a data-only format, it doesn’t support comments. The turnaround was to put the comments as pseudo data, starting their names with underscores. That way, we can have easy access to the different options of a parameter.

```json
{
    "_this_is_a_comment": "data_label_1 options are this and that",
    "data_label_1": [],
    "data_label_2": ""
}
```

### **Program parameters**

- Detail 1.
- Detail 2.
