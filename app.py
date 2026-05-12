from flask import Flask, render_template, request
import csv
import re

app = Flask(__name__)

PER_PAGE = 50

@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    message = ""
    headers = []

    complaint_no = request.form.get("complaint_no", "").strip().lower()
    customer_name = request.form.get("customer_name", "").strip().lower()

    page = int(request.form.get("page", 1))
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    all_results = []

    if request.method == "POST":
        if not complaint_no and not customer_name:
            message = "⚠️ Please enter at least one field"
        else:
            with open("data.csv", mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                # Get ALL headers dynamically
                headers = [h.strip() for h in reader.fieldnames]

                for row in reader:
                    # Clean row keys + handle missing values
                    clean_row = {k.strip(): (v if v is not None else "") for k, v in row.items()}

                    comp = re.sub(r'\s+', ' ', str(clean_row.get("Complain No", ""))).strip().lower()
                    cust = re.sub(r'\s+', ' ', str(clean_row.get("Customer Name", ""))).strip().lower()

                    if (not complaint_no or complaint_no in comp) and \
                       (not customer_name or customer_name in cust):

                        all_results.append(clean_row)

            total = len(all_results)

            # ✅ Pagination
            results = all_results[start:end]

            if not results:
                message = "❌ No records found"

            return render_template(
                "index.html",
                results=results,
                headers=headers,
                message=message,
                page=page,
                total=total,
                complaint_no=complaint_no,
                customer_name=customer_name
            )

    return render_template("index.html", results=[], headers=[], message=message, page=1, total=0)


if __name__ == "__main__":
    app.run(debug=True)