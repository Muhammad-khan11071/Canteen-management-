from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
from data_manager import MASTER_FILE, RECORD_FILE

app = Flask(__name__)


def get_todays_items():
    # 1. Get Today's Date in our conventional format (DD-MM-YY)
    today = datetime.now().strftime("%d-%m-%y")

    try:
        # Read records
        records_df = pd.read_csv(RECORD_FILE)

        # Find row for today
        todays_record = records_df[records_df["date"] == today]

        if todays_record.empty:
            return []

        # Extract IDs string "1 2 3" -> list [1, 2, 3]
        ids_str = str(todays_record.iloc[0]["item_ids"])
        # Handle cases where IDs might be separated by space or comma
        ids_str = ids_str.replace(",", " ")
        item_ids = [int(x) for x in ids_str.split()]

        # Read Main Menu
        menu_df = pd.read_csv(MASTER_FILE)

        # Filter menu to only include these IDs
        todays_menu = menu_df[menu_df["id"].isin(item_ids)].to_dict("records")

        return todays_menu

    except Exception as e:
        print(f"Error: {e}")
        return []


@app.route("/")
def home():
    items = get_todays_items()
    # If using actual today and it's empty, we pass the date to show user
    today_date = datetime.now().strftime("%B %d, %Y")
    return render_template("index.html", items=items, date=today_date)


@app.route("/upvote", methods=["POST"])
def upvote():
    try:
        data = request.json
        item_id = int(data.get("id"))
        action = data.get("action")  # We will send 'add' or 'remove'

        # Load CSV
        df = pd.read_csv(MASTER_FILE)

        mask = df["id"] == item_id
        if mask.any():
            current_votes = df.loc[mask, "upvotes"].values[0]

            # Logic to Add or Remove
            if action == "add":
                new_votes = current_votes + 1
            elif action == "remove":
                new_votes = max(0, current_votes - 1)  # Prevent negative votes
            else:
                return jsonify({"success": False, "error": "Invalid action"})

            df.loc[mask, "upvotes"] = new_votes

            # Save back to CSV
            df.to_csv(MASTER_FILE, index=False)

            return jsonify({"success": True, "new_count": int(new_votes)})

        return jsonify({"success": False, "error": "Item not found"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
