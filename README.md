# npp-epb

## Static Page Build

    pip3 install Jinja2
    python3 build.py
    chrome.exe index.html

## Hot Reloading Support

    pip3 install -r requirements.txt
    watchmedo auto-restart -p "*.py" -R python3 -- app.py
