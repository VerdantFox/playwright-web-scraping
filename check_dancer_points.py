"""check_dancer_points: Check dancer points with the World Swing Dance Council site."""
from typing import Union
from playwright.sync_api import Playwright, sync_playwright, TimeoutError
import json
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def points_route() -> dict:
    """Return the points for a dancer as JSON (flask converts dictionary to JSON)."""
    name_or_id = request.args.get("name_or_id")
    return (
        check_points(name_or_id) if name_or_id else {"error": "No name or ID provided."}
    )


def check_points_inner(
    playwright: Playwright, name_or_id: str
) -> dict[str, Union[int, str, None]]:
    """Check dancer points with the World Swing Dance Council site."""
    # Set up playwright
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.worldsdc.com/registry-points/")
    # Search for dancer
    i_frame = page.frame_locator('iframe[name="myiFrame"]')
    search_bar = i_frame.get_by_placeholder("Search by Name or WSDC #")
    search_bar.click()
    search_bar.fill(name_or_id)
    search_results = i_frame.locator(".tt-selectable")
    try:
        search_results.first.click(timeout=1000)
    except TimeoutError:
        return {"error": "No results found."}
    # Scrape results
    results = i_frame.locator("#lookup_results")
    name_and_id = results.locator("h1").inner_text()
    name, dancer_id = name_and_id.split(" (")
    dancer_id = dancer_id.strip(")")
    lower_level = results.locator(".lead").first.locator(".label-success").inner_text()
    upper_level_loc = results.locator(".lead").first.locator(".label-warning")
    upper_level = upper_level_loc.inner_text() if upper_level_loc.is_visible() else None
    div_and_points = results.locator("h3").first.inner_text()
    highest_pointed_division, points_in_division, _ = div_and_points.split(" ")
    # Clean up playwright
    context.close()
    browser.close()
    return {
        "name": name,
        "id": int(dancer_id),
        "lower_level": lower_level,
        "upper_level": upper_level,
        "highest_pointed_division": highest_pointed_division,
        "points_in_division": int(points_in_division),
    }


def check_points(name_or_id: str) -> dict[str, Union[int, str, None]]:
    """Check dancer points with the World Swing Dance Council site."""
    with sync_playwright() as playwright:
        return check_points_inner(playwright, name_or_id)


if __name__ == "__main__":  # pragma: no cover
    name_or_id = input("Name or ID: ")
    results = check_points(name_or_id)
    print(json.dumps(results, indent=4))
