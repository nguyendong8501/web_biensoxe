# ImageReade

Insert Tesseract file path in main.py (line 54):

```python
# Example: r'D:\TesseractOCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_exe>'
```

# Start Flask webserver
## UNIX
```'bash
python3 main.py
```

## Windows
```bash
python main.py
```

PS: The webserver will start on the port 5000

