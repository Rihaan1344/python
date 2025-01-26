from flask import Flask, render_template, request, jsonify
import re


app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        data = request.get_json()
        eqn = data.get('equation')
        try:

            cleaned_eqn = re.sub(r'\b0+(\d)', r'\1', eqn) or eqn # Remove leading zeros
        except TypeError:
            cleaned_eqn = eqn

        response = {
                "message": f"{eval(cleaned_eqn)}"
        }
        return jsonify(response)
    return render_template("calc_template.html")

if __name__ == '__main__':
    app.run(debug=True)