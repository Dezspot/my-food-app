import flet as ft
import json
import os

DATA_FILE = "data.json"

products = {
    "chicken":   {"cal": 150, "p": 20, "f": 15, "c": 2},
    "rice":      {"cal": 370, "p": 8,  "f": 1,  "c": 85},
    "pasta":     {"cal": 350, "p": 12, "f": 2,  "c": 70},
    "buckwheat": {"cal": 350, "p": 13, "f": 2,  "c": 70},
    "tuna":      {"cal": 100, "p": 25, "f": 2,  "c": 0, "unit": "pcs"},
    "yoghurt":   {"cal": 670, "p": 28, "f": 26, "c": 70, "unit": "pcs"},
    "egg":       {"cal": 80,  "p": 6,  "f": 5,  "c": 1, "unit": "pcs"},
    "bread":     {"cal": 85,  "p": 4,  "f": 1,  "c": 15, "unit": "pcs"},
    "banana":    {"cal": 100, "p": 1,  "f": 1,  "c": 25, "unit": "pcs"},
}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"cal": 0, "p": 0, "f": 0, "c": 0}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def main(page: ft.Page):
    page.title = "My Food"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    total = load_data()

    result_text = ft.Text(
        f"Kcal: {int(total['cal'])}  "
        f"P: {int(total['p'])}  "
        f"F: {int(total['f'])}  "
        f"C: {int(total['c'])}",
        size=20,
    )

    def update_ui():
        result_text.value = (
            f"Kcal: {int(total['cal'])}  "
            f"P: {int(total['p'])}  "
            f"F: {int(total['f'])}  "
            f"C: {int(total['c'])}"
        )
        page.update()

    def add_food(product_name):
        data = products[product_name]
        unit = data["unit"]
        label = f"Pieces of {product_name} (pcs)" if unit == "pcs" else f"Grams of {product_name} (g)"

        def close_dialog(e=None):
            dialog.open = False
            page.update()

        def confirm(e):
            try:
                amount = float(grams_input.value)
                if amount <= 0:
                    raise ValueError
                multiplier = amount if unit == "pcs" else amount / 100
                total["cal"] += data["cal"] * multiplier
                total["p"]   += data["p"]   * multiplier
                total["f"]   += data["f"]   * multiplier
                total["c"]   += data["c"]   * multiplier
                save_data(total)
                close_dialog()
                update_ui()
            except Exception:
                grams_input.error_text = "Enter a valid number"
                grams_input.update()

        grams_input = ft.TextField(
            label=label,
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
            on_submit=confirm,
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Add {product_name.capitalize()}"),
            content=ft.Container(content=grams_input, width=250),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Add", on_click=confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def reset(e):
        total["cal"] = total["p"] = total["f"] = total["c"] = 0
        save_data(total)
        update_ui()

    page.add(
        ft.Column(
            [
                ft.Text("🍽 My Food", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                ft.Row(
                    [
                        ft.Button("🍗 Chicken", on_click=lambda e: add_food("chicken")),
                        ft.Button("🍚 Rice", on_click=lambda e: add_food("rice")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("🍝 Pasta", on_click=lambda e: add_food("pasta")),
                        ft.Button("🌾 Buckwheat", on_click=lambda e: add_food("buckwheat")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("🐟 Tuna", on_click=lambda e: add_food("tuna")),
                        ft.Button("🥛 Yoghurt", on_click=lambda e: add_food("yoghurt")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                 ft.Row(
                    [
                        ft.Button("🥚 Egg", on_click=lambda e: add_food("egg")),
                        ft.Button("🍞 Bread", on_click=lambda e: add_food("bread")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    [
                        ft.Button("🍌 Banana", on_click=lambda e: add_food("banana")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Divider(),
                result_text,
                ft.Divider(),

                ft.Button("RESET", on_click=reset),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )
    )

ft.run(main)