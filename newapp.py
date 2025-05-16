from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
from datetime import datetime
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)
CORS(app)

# Ensure static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/highlight', methods=['POST'])
def highlight_code():
    code = request.json.get('code', '')
    
    # Apply syntax highlighting
    highlighted_code = highlight(
        code,
        PythonLexer(),
        HtmlFormatter(style='monokai', noclasses=True)  # VS Code-like theme
    )
    
    return jsonify({"highlighted_code": highlighted_code})

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json['code']

    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"plot_{timestamp}.png"
    plot_path = os.path.join('static', filename)

    # Replace any 'plot.png' in user code with dynamic filename
    safe_code = code.replace('plot.png', filename)

    try:
        # Execute the code securely
        result = subprocess.run(
            ['python3', '-c', safe_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=100,
            check=False,
            text=True
        )

        return jsonify({
            "output": result.stdout,
            "error": result.stderr,
            "plot": filename if os.path.exists(plot_path) else None
        })

    except Exception as e:
        return jsonify({ "error": str(e) })

@app.route('/plot/<filename>')
def serve_plot(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)