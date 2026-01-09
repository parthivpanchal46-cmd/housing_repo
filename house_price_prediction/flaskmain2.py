from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# import sklearn
# print("Loaded sklearn version:", sklearn.__version__)

app = Flask(__name__)

# Load trained regression model
loaded_model = joblib.load("linear_regression_housing.pkl")

# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("housing.html")

# -------------------------------
# Predict API
# -------------------------------
# @app.route("/predict", methods=["GET", "POST"])
# def predict():

#     area = bedrooms = bathrooms = age_of_house = None

#     # 🔹 1. Query Params (GET - Postman)
#     if request.args.get("area"):
#         area = request.args.get("area")
#         bedrooms = request.args.get("bedrooms")
#         bathrooms = request.args.get("bathrooms")
#         age_of_house = request.args.get("age_of_house")

#     # 🔹 2. JSON Body (POST - Postman)
#     elif request.is_json:
#         data = request.get_json()
#         area = data.get("area")
#         bedrooms = data.get("bedrooms")
#         bathrooms = data.get("bathrooms")
#         age_of_house = data.get("age_of_house")

#     # 🔹 3. HTML Form (POST)
#     else:
#         area = request.form.get("area")
#         bedrooms = request.form.get("bedrooms")
#         bathrooms = request.form.get("bathrooms")
#         age_of_house = request.form.get("age_of_house")

#     # 🔹 Validation
#     if None in [area, bedrooms, bathrooms, age_of_house]:
#         return jsonify({"error": "Missing input fields"}), 400

#     # 🔹 Prediction
#     features = np.array([[ 
#         float(area),
#         int(bedrooms),
#         int(bathrooms),
#         int(age_of_house)
#     ]])

#     prediction = loaded_model.predict(features)[0]

#     # 🔹 JSON response (Postman)
#     if request.is_json or request.args:
#         return jsonify({
#             "area": float(area),
#             "bedrooms": int(bedrooms),
#             "bathrooms": int(bathrooms),
#             "age_of_house": int(age_of_house),
#             "predicted_price": round(float(prediction), 2)
#         })

#     # 🔹 HTML response
#     return render_template(
#         "housing.html",
#         prediction=f"🏠 Predicted Price: {round(float(prediction), 2)}"
#     )


# # -------------------------------
# # Run App
# # -------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)



@app.route("/predict", methods=["GET", "POST"])
def predict():

    # 🔹 Read from all possible sources safely
    data = {}

    # 1️⃣ Query Params
    if request.args:
        data = request.args

    # 2️⃣ JSON Body
    elif request.is_json:
        data = request.get_json()

    # 3️⃣ form-data / HTML form
    else:
        data = request.form

    # 🔹 Extract fields
    area = data.get("area")
    bedrooms = data.get("bedrooms")
    bathrooms = data.get("bathrooms")
    age_of_house = data.get("age_of_house")

    # 🔹 Validation
    if not all([area, bedrooms, bathrooms, age_of_house]):
        return jsonify({"error": "Missing input fields"}), 400

    # 🔹 Prediction
    features = [[
        float(area),
        int(bedrooms),
        int(bathrooms),
        int(age_of_house)
    ]]

    prediction = loaded_model.predict(features)[0]

    # 🔹 JSON response (Postman)
    if request.args or request.is_json:
        return jsonify({
            "area": float(area),
            "bedrooms": int(bedrooms),
            "bathrooms": int(bathrooms),
            "age_of_house": int(age_of_house),
            "predicted_price": round(float(prediction), 2)
        })

    # 🔹 HTML response
    return render_template(
        "housing.html",
        prediction=f"🏠 Predicted Price: {round(float(prediction), 2)}"
    )

if __name__ == "__main__":
    app.run(debug=True)


# Output ==> show in chrome ,in write json ,in write params, but not in write body form-data