from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    fortune_proc = subprocess.run(['fortune'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    fortune_output = fortune_proc.stdout

    cowsay_proc = subprocess.run(['cowsay'], input=fortune_output, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cowsay_output = cowsay_proc.stdout
    return f"<pre>{cowsay_output}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5043)


