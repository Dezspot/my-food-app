import flet as ft
import json
import os

DATA_FILE = "data.json"

products = {
    "chicken":   {"cal": 150, "p": 25, "f": 10, "c": 2},
    "rice":      {"cal": 370, "p": 8,  "f": 1,  "c": 85},
    "pasta":     {"cal": 350, "p": 12, "f": 2,  "c": 70},
    "buckwheat": {"cal": 350, "p": 13, "f": 2,  "c": 70},
    "tuna":      {"cal": 100, "p": 25, "f": 3,  "c": 0},
    "yoghurt":   {"cal": 670, "p": 28, "f": 26, "c": 70},
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

        def close_dialog(e=None):
            dialog.open = False
            page.update()

        def confirm(e):
            try:
                grams = float(grams_input.value)
                if grams <= 0:
                    raise ValueError
                data = products[product_name]
                total["cal"] += data["cal"] * grams / 100
                total["p"]   += data["p"]   * grams / 100
                total["f"]   += data["f"]   * grams / 100
                total["c"]   += data["c"]   * grams / 100
                save_data(total)
                close_dialog()
                update_ui()
            except Exception:
                grams_input.error_text = "Enter a valid number"
                grams_input.update()

        grams_input = ft.TextField(
            label=f"Grams of {product_name}",
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
                        ft.Button("🐔 Chicken",   on_click=lambda e: add_food("chicken")),
                        ft.Button("🍚 Rice",      on_click=lambda e: add_food("rice")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("🍝 Pasta",     on_click=lambda e: add_food("pasta")),
                        ft.Button("🌾 Buckwheat", on_click=lambda e: add_food("buckwheat")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("🐟 Tuna",      on_click=lambda e: add_food("tuna")),
                        ft.Button("🥛 Yoghurt",   on_click=lambda e: add_food("yoghurt")),
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