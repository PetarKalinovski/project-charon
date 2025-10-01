from strands import tool
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config_loader import load_config
import json
from datetime import datetime
from src.utils.callback_hanlder_subagents import log_to_session


@tool
def add_sleep_data(
    date: str, sleep_duration: int, sleep_quality: str, notes: str
) -> str:
    """
    Add sleep data to the sleep tracking file.
    Args:
        date (str): Date of the sleep record in YYYY-MM-DD format.
        sleep_duration (int): Duration of sleep in minutes.
        sleep_quality (str): Quality of sleep (e.g., "good", "average", "poor").
        notes (str): Additional notes about the sleep.
    Returns:
        str: Confirmation message indicating the sleep data has been added.
    """
    config = load_config()

    sleep_dir = config.big_boss_orchestrator_agent.sleep_tracking_file

    with open(sleep_dir) as file:
        data = json.load(file)

    new_sleep_entry = {
        "date": date,
        "total_sleep_time": sleep_duration,
        "sleep_quality": sleep_quality,
        "notes": notes,
    }

    log_to_session(f"Adding new sleep entry: {new_sleep_entry}")

    data["sleep_sessions"].append(new_sleep_entry)

    try:
        with open(sleep_dir, "w") as file:
            json.dump(data, file, indent=4)

        log_to_session(f"Sleep data written to {sleep_dir}")
        last_week_end_str = data["weekly_summary"][-1]["week_end"]
        last_week_end = datetime.strptime(last_week_end_str, "%Y-%m-%d")
        if (datetime.now() - last_week_end).days >= 7:
            log_to_session("Weekly summary needs to be updated.")
            return f"Sleep data added {new_sleep_entry}. But weekly summary is not updated. Please run the weekly summary tool to update it."

        return f"Sleep data added: {new_sleep_entry}"
    except Exception as e:
        log_to_session(f"Error writing to sleep tracking file: {e}")
        return f"Error adding sleep data. {e}"


@tool
def get_sleep_data() -> str:
    """
    Retrieve sleep data from the sleep tracking file.
    Returns:
        str: JSON string containing the sleep data.
    """
    config = load_config()
    sleep_dir = config.big_boss_orchestrator_agent.sleep_tracking_file

    try:
        with open(sleep_dir) as file:
            data = json.load(file)
        return json.dumps(data, indent=4)
    except FileNotFoundError:
        log_to_session(f"Sleep tracking file not found at {sleep_dir}")
        return "Sleep tracking file not found."
    except json.JSONDecodeError:
        log_to_session("Error decoding JSON from sleep tracking file.")
        return "Error decoding sleep tracking data."


# "week_start": "2025-07-31",
#             "average_duration": 450,
#             "average_quality": "good",
#             "notes": "Overall good sleep quality with consistent duration."


@tool
def update_weekly_summary(
    week_start: str,
    week_end: str,
    average_duration: int,
    average_quality: str,
    notes: str,
) -> str:
    """
    Update the weekly summary in the sleep tracking file.
    Args:
        week_start (str): Start date of the week in YYYY-MM-DD format.
        weel_end (str): End date of the week in YYYY-MM-DD format.
        average_duration (int): Average sleep duration in minutes.
        average_quality (str): Average sleep quality for the week.
        notes (str): Additional notes for the weekly summary.
    Returns:
        str: Confirmation message indicating the weekly summary has been updated.
    """
    config = load_config()
    sleep_dir = config.big_boss_orchestrator_agent.sleep_tracking_file
    try:
        with open(sleep_dir) as file:
            data = json.load(file)

        new_weekly_summary = {
            "week_start": week_start,
            "average_duration": average_duration,
            "average_quality": average_quality,
            "notes": notes,
        }
        log_to_session(f"Updating weekly summary: {new_weekly_summary}")
        data["weekly_summary"].append(new_weekly_summary)

        with open(sleep_dir, "w") as file:
            json.dump(data, file, indent=4)
        log_to_session(f"Weekly summary updated: {new_weekly_summary}")

        return f"Weekly summary updated: {new_weekly_summary}"
    except Exception as e:
        log_to_session(f"Error updating weekly summary: {e}")
        return f"Error updating weekly summary. {e}"
