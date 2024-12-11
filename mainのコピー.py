import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import json
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# 車両形式の辞書
CAR_TYPES = {
    "ク": "制御車",
    "モ": "電動車",
    "ロ": "グリーン車",
    "ハ": "普通車",
    "ネ": "寝台車",
    "シ": "食堂車",
    "ユ": "郵便車",
    "ニ": "荷物車",
    "エ": "救援車",
    "ヤ": "職用車",
    "ル": "配給車",
    "キ": "気動車"
}

# 車両タイプの色
CAR_TYPE_COLORS = {
    "制御車": "orange",
    "電動車": "blue",
    "グリーン車": "green",
    "普通車": "grey",
    "寝台車": "darkblue",
    "食堂車": "brown",
    "郵便車": "cyan",
    "荷物車": "darkgreen",
    "救援車": "red",
    "職用車": "purple",
    "配給車": "pink",
    "気動車": "yellow"
}

class TrainManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("鉄道車両編成管理システム")
        self.root.geometry("1600x900")
        self.series_data = {}
        self.retired_data = []

        self.create_menu()
        self.create_main_ui()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新規作成", command=self.new_project)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_command(label="読み込み", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        self.root.config(menu=menubar)

    def create_main_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 系列リストボックス
        self.series_listbox = tk.Listbox(main_frame, height=35, width=40, font=("Helvetica", 12))
        self.series_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.series_listbox.bind("<Double-1>", self.open_series_window)

        # 系列操作ボタン
        series_btn_frame = tk.Frame(main_frame)
        series_btn_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(series_btn_frame, text="系列追加", command=self.add_series).pack(fill=tk.X, pady=5)
        tk.Button(series_btn_frame, text="系列削除", command=self.delete_series).pack(fill=tk.X, pady=5)
        tk.Button(series_btn_frame, text="廃車リスト", command=self.show_retired_list).pack(fill=tk.X, pady=5)

        # 凡例
        legend_frame = tk.Frame(self.root)
        legend_frame.pack(fill=tk.X, padx=5, pady=5)
        for label, color in CAR_TYPE_COLORS.items():
            tk.Label(legend_frame, text=label, bg=color, width=15, relief=tk.RIDGE).pack(side=tk.LEFT, padx=2, pady=2)

    def new_project(self):
        if messagebox.askyesno("確認", "現在のデータを破棄して新規作成しますか？"):
            self.series_data = {}
            self.retired_data = []
            self.update_series_list()

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            data = {"series": self.series_data, "retired": self.retired_data}
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("保存完了", "データを保存しました。")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.series_data = data.get("series", {})
            self.retired_data = data.get("retired", [])
            self.update_series_list()
            messagebox.showinfo("読み込み完了", "データを読み込みました。")

    def update_series_list(self):
        self.series_listbox.delete(0, tk.END)
        for series_name in self.series_data.keys():
            self.series_listbox.insert(tk.END, series_name)

    def add_series(self):
        series_name = simpledialog.askstring("系列追加", "系列名を入力してください:")
        if series_name and series_name not in self.series_data:
            self.series_data[series_name] = {"formations": [], "description": "", "photos": []}
            self.update_series_list()

    def delete_series(self):
        selected = self.series_listbox.curselection()
        if selected:
            series_name = self.series_listbox.get(selected[0])
            if messagebox.askyesno("確認", f"系列「{series_name}」を削除しますか？"):
                del self.series_data[series_name]
                self.update_series_list()

    def open_series_window(self, event):
        selected = self.series_listbox.curselection()
        if selected:
            series_name = self.series_listbox.get(selected[0])
            series_data = self.series_data[series_name]
            SeriesWindow(self.root, series_name, series_data, self.retired_data)

    def show_retired_list(self):
        RetiredWindow(self.root, self.retired_data)

class SeriesWindow:
    def __init__(self, parent, series_name, series_data, retired_data):
        self.series_name = series_name
        self.series_data = series_data
        self.retired_data = retired_data

        self.window = tk.Toplevel(parent)
        self.window.title(f"系列: {series_name}")
        self.window.geometry("1400x900")

        self.create_ui()

    def create_ui(self):
        # 編成リストボックス
        self.formation_listbox = tk.Listbox(self.window, height=25, width=50, font=("Helvetica", 12))
        self.formation_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.formation_listbox.bind("<Double-1>", self.open_formation_window)

        # 編成操作ボタン
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Button(btn_frame, text="編成追加", command=self.add_formation).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="編成削除", command=self.delete_formation).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="編成コピー", command=self.copy_formation).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="アルバム編集", command=self.edit_album).pack(fill=tk.X, pady=5)

        # 解説テキスト
        tk.Label(btn_frame, text="解説:").pack(anchor="w", pady=5)
        self.series_description = tk.Text(btn_frame, height=10, width=40, font=("Helvetica", 12))
        self.series_description.pack(fill=tk.X, pady=5)
        self.series_description.insert(tk.END, self.series_data.get("description", ""))
        self.series_description.bind("<FocusOut>", self.save_description)

        self.update_formation_list()

    def update_formation_list(self):
        self.formation_listbox.delete(0, tk.END)
        for formation in self.series_data.get("formations", []):
            self.formation_listbox.insert(tk.END, formation["name"])

    def add_formation(self):
        formation_name = simpledialog.askstring("編成追加", "編成名を入力してください:")
        if formation_name:
            self.series_data["formations"].append({
                "name": formation_name,
                "cars": [],
                "photos": [],
                "description": ""
            })
            self.update_formation_list()

    def delete_formation(self):
        selected = self.formation_listbox.curselection()
        if selected:
            formation_name = self.formation_listbox.get(selected[0])
            if messagebox.askyesno("確認", f"編成「{formation_name}」を削除しますか？"):
                del self.series_data["formations"][selected[0]]
                self.update_formation_list()

    def copy_formation(self):
        selected = self.formation_listbox.curselection()
        if selected:
            formation = self.series_data["formations"][selected[0]]
            new_formation = formation.copy()
            new_formation["name"] += " (コピー)"
            self.series_data["formations"].append(new_formation)
            self.update_formation_list()

    def open_formation_window(self, event):
        selected = self.formation_listbox.curselection()
        if selected:
            formation = self.series_data["formations"][selected[0]]
            FormationWindow(self.window, formation, self.retired_data)

    def edit_album(self):
        AlbumWindow(self.window, self.series_data)

    def save_description(self, event):
        self.series_data["description"] = self.series_description.get("1.0", tk.END).strip()

class AlbumWindow:
    def __init__(self, parent, series_data):
        self.series_data = series_data

        self.window = tk.Toplevel(parent)
        self.window.title(f"アルバム: {self.series_data.get('name', '')}")
        self.window.geometry("800x600")

        self.create_ui()

    def create_ui(self):
        # 写真リストボックス
        self.photo_listbox = tk.Listbox(self.window, height=30, width=50, font=("Helvetica", 12))
        self.photo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        # 写真操作ボタン
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Button(btn_frame, text="写真追加", command=self.add_photo).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="写真削除", command=self.delete_photo).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="写真プレビュー", command=self.preview_photo).pack(fill=tk.X, pady=5)

        self.update_photo_list()

    def update_photo_list(self):
        self.photo_listbox.delete(0, tk.END)
        for photo in self.series_data.get("photos", []):
            self.photo_listbox.insert(tk.END, photo)

    def add_photo(self):
        file_paths = filedialog.askopenfilenames(title="写真を選択", filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_paths:
            self.series_data["photos"].extend(file_paths)
            self.update_photo_list()

    def delete_photo(self):
        selected = self.photo_listbox.curselection()
        if selected:
            photo = self.photo_listbox.get(selected[0])
            self.series_data["photos"].remove(photo)
            self.update_photo_list()

    def preview_photo(self):
        selected = self.photo_listbox.curselection()
        if selected:
            photo_path = self.photo_listbox.get(selected[0])
            if os.path.exists(photo_path):
                PreviewWindow(self.window, photo_path)
            else:
                messagebox.showerror("エラー", "選択された写真が見つかりません。")

class PreviewWindow:
    def __init__(self, parent, photo_path):
        self.photo_path = photo_path

        self.window = tk.Toplevel(parent)
        self.window.title("写真プレビュー")
        self.window.geometry("600x600")

        # 画像表示
        try:
            img = Image.open(photo_path)
            img.thumbnail((600, 600))
            self.photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.window, image=self.photo)
            label.pack()
        except Exception as e:
            messagebox.showerror("エラー", f"画像を開く際にエラーが発生しました: {e}")
            self.window.destroy()

class FormationWindow:
    def __init__(self, parent, formation, retired_data):
        self.formation = formation
        self.retired_data = retired_data

        self.window = tk.Toplevel(parent)
        self.window.title(f"編成: {formation['name']}")
        self.window.geometry("1000x800")

        self.create_ui()

    def create_ui(self):
        self.car_listbox = tk.Listbox(self.window, height=25, width=50, font=("Helvetica", 12))
        self.car_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.car_listbox.bind("<Double-1>", self.edit_car)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Button(btn_frame, text="車両追加", command=self.add_car).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="車両削除", command=self.delete_car).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="写真を読み込む", command=self.attach_photo).pack(fill=tk.X, pady=5)

        # 写真リストボックス
        self.photo_listbox = tk.Listbox(self.window, height=10, width=50, font=("Helvetica", 12))
        self.photo_listbox.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.photo_listbox.image_refs = []  # 画像の参照を保持するリスト

        tk.Label(btn_frame, text="解説:").pack(anchor="w", pady=5)
        self.formation_description = tk.Text(btn_frame, height=15, width=40, font=("Helvetica", 12))
        self.formation_description.pack(fill=tk.X, pady=5)
        self.formation_description.insert(tk.END, self.formation["description"])
        self.formation_description.bind("<FocusOut>", self.save_formation_description)

        self.update_car_list()

def attach_photo(self):
    try:
        print("写真追加ボタンが押されました。")
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not file_path:
            print("ファイルが選択されませんでした。")
            return

        print(f"選択されたファイルパス: {file_path}")
        img = Image.open(file_path)
        img.thumbnail((400, 300))
        photo = ImageTk.PhotoImage(img)

        if "photos" not in self.formation:
            self.formation["photos"] = []

        self.formation["photos"].append({"path": file_path, "image": photo})
        index = len(self.formation["photos"]) - 1
        self.photo_listbox.insert(tk.END, f"写真 {index + 1}")
        self.photo_listbox.image_refs.append(photo)
        print("写真が正常に追加されました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        messagebox.showerror("エラー", f"写真を追加中にエラーが発生しました: {e}")


        try:
            img = Image.open(file_path)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)

            self.formation["photos"].append({"path": file_path, "image": photo})
            index = len(self.formation["photos"]) - 1
            self.photo_listbox.insert(tk.END, f"写真 {index + 1}")
            self.photo_listbox.image_refs.append(photo)

        except Exception as e:
            messagebox.showerror("エラー", f"画像を読み込めませんでした: {e}")

class CarWindow:
    def __init__(self, parent, formation, update_callback, car=None, index=None):
        self.formation = formation
        self.update_callback = update_callback
        self.car = car
        self.index = index

        self.window = tk.Toplevel(parent)
        self.window.title("車両編集" if car else "車両追加")
        self.window.geometry("500x700")

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 車両名
        tk.Label(frame, text="車両名:").pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.name_entry.pack(fill=tk.X, pady=5)
        if self.car:
            self.name_entry.insert(tk.END, self.car.get("name", ""))

        # 車両タイプ（タグ）
        tk.Label(frame, text="車両タイプ (1〜6個):").pack(anchor="w", pady=5)
        self.type_frame = tk.Frame(frame)
        self.type_frame.pack(fill=tk.X, pady=5)

        self.selected_types = self.car.get("tags", []) if self.car else []
        self.type_vars = []
        self.update_type_buttons()

        tk.Button(frame, text="タグ編集", command=self.edit_tags).pack(pady=5)

        # ステータス項目
        status_fields = [
            ("加速度 (m/s²)", "acceleration"),
            ("減速度 (m/s²)", "deceleration"),
            ("出力 (kW)", "power_kw"),
            ("制御方式", "control_method")
        ]

        self.status_entries = {}
        for label_text, key in status_fields:
            tk.Label(frame, text=label_text + ":").pack(anchor="w", pady=5)
            entry = tk.Entry(frame, font=("Helvetica", 12))
            entry.pack(fill=tk.X, pady=5)
            if self.car:
                entry.insert(tk.END, str(self.car.get(key, "")))
            self.status_entries[key] = entry

        # 車両解説
        tk.Label(frame, text="車両解説:").pack(anchor="w", pady=5)
        self.description_text = tk.Text(frame, height=5, font=("Helvetica", 12))
        self.description_text.pack(fill=tk.BOTH, pady=5)
        if self.car:
            self.description_text.insert(tk.END, self.car.get("description", ""))

        # 保存ボタン
        tk.Button(frame, text="保存", command=self.save_car).pack(pady=10)

    def update_type_buttons(self):
        for widget in self.type_frame.winfo_children():
            widget.destroy()
        for t in self.selected_types:
            tk.Label(self.type_frame, text=t, bg=CAR_TYPE_COLORS.get(t, "grey"), fg="white", padx=5, pady=2, relief=tk.RIDGE).pack(side=tk.LEFT, padx=2, pady=2)

    def edit_tags(self):
        edit_window = tk.Toplevel(self.window)
        edit_window.title("車両タイプ選択")
        edit_window.geometry("300x400")

        tk.Label(edit_window, text="車両タイプを選択してください (最大6個):").pack(anchor="w", pady=5)

        # 選択可能なタイプをリストボックスで表示
        listbox = tk.Listbox(edit_window, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        for code, name in CAR_TYPES.items():
            listbox.insert(tk.END, f"{code}: {name}")
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 既に選択されているタイプを選択
        existing_indices = [list(CAR_TYPES.values()).index(t) for t in self.selected_types if t in CAR_TYPES.values()]
        for idx in existing_indices:
            listbox.selection_set(idx)

        def save_tags():
            selected_indices = listbox.curselection()
            selected = [list(CAR_TYPES.values())[i] for i in selected_indices]
            if len(selected) > 6:
                messagebox.showerror("エラー", "車両タイプは最大6個まで選択できます。")
                return
            self.selected_types = selected
            self.update_type_buttons()
            edit_window.destroy()

        tk.Button(edit_window, text="保存", command=save_tags).pack(pady=5)

    def save_car(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("エラー", "車両名を入力してください。")
            return

        tags = self.selected_types
        if len(tags) == 0:
            messagebox.showerror("エラー", "少なくとも1つの車両タイプを選択してください。")
            return
        elif len(tags) > 6:
            messagebox.showerror("エラー", "車両タイプは最大6個まで選択できます。")
            return

        # ステータス項目の取得
        try:
            acceleration = float(self.status_entries["acceleration"].get())
            deceleration = float(self.status_entries["deceleration"].get())
            power_kw = float(self.status_entries["power_kw"].get())
            control_method = self.status_entries["control_method"].get().strip()
        except ValueError:
            messagebox.showerror("エラー", "ステータス項目には数値を入力してください。")
            return

        description = self.description_text.get("1.0", tk.END).strip()

        # 色の設定（最初のタグの色を使用）
        color = CAR_TYPE_COLORS.get(tags[0], "black")

        car_data = {
            "name": name,
            "tags": tags,
            "color": color,
            "acceleration": acceleration,
            "deceleration": deceleration,
            "power_kw": power_kw,
            "control_method": control_method,
            "description": description
        }

        if self.car and self.index is not None:
            # 編集の場合
            self.formation["cars"][self.index] = car_data
        else:
            # 追加の場合
            self.formation["cars"].append(car_data)

        self.update_callback()
        self.window.destroy()

class RetiredWindow:
    def __init__(self, parent, retired_data):
        self.retired_data = retired_data

        self.window = tk.Toplevel(parent)
        self.window.title("廃車リスト")
        self.window.geometry("500x400")

        self.create_ui()

    def create_ui(self):
        tk.Label(self.window, text="廃車一覧").pack(anchor="w", padx=5, pady=5)
        self.retired_listbox = tk.Listbox(self.window, height=20, width=50, font=("Helvetica", 12))
        self.retired_listbox.pack(fill=tk.BOTH, padx=5, pady=5)

        for retired_car in self.retired_data:
            self.retired_listbox.insert(tk.END, retired_car["name"])

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="廃車追加", command=self.add_retired_car).pack(fill=tk.X, pady=5)

    def add_retired_car(self):
        car_name = simpledialog.askstring("廃車追加", "廃車車両名を入力してください:")
        if car_name:
            self.retired_data.append({"name": car_name})
            self.retired_listbox.insert(tk.END, car_name)

class FormationWindow:
    def __init__(self, parent, formation, retired_data):
        self.formation = formation
        self.retired_data = retired_data

        self.window = tk.Toplevel(parent)
        self.window.title(f"編成: {formation['name']}")
        self.window.geometry("1200x800")

        self.create_ui()

    def create_ui(self):
        # 車両リストボックス
        self.car_listbox = tk.Listbox(self.window, height=30, width=60, font=("Helvetica", 12))
        self.car_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.car_listbox.bind("<Double-1>", self.edit_car)

        # 車両操作ボタン
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Button(btn_frame, text="車両追加", command=self.add_car).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="車両削除", command=self.delete_car).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="車両コピー", command=self.copy_car).pack(fill=tk.X, pady=5)

        # 解説テキスト
        tk.Label(btn_frame, text="解説:").pack(anchor="w", pady=5)
        self.formation_description = tk.Text(btn_frame, height=10, width=40, font=("Helvetica", 12))
        self.formation_description.pack(fill=tk.X, pady=5)
        self.formation_description.insert(tk.END, self.formation.get("description", ""))
        self.formation_description.bind("<FocusOut>", self.save_formation_description)

        self.update_car_list()

    def update_car_list(self):
        self.car_listbox.delete(0, tk.END)
        for car in self.formation.get("cars", []):
            display_name = f"{car['name']} ({', '.join(car.get('tags', []))})"
            self.car_listbox.insert(tk.END, display_name)
            self.car_listbox.itemconfig(tk.END, {'fg': car.get("color", "black")})

    def add_car(self):
        CarWindow(self.window, self.formation, self.update_car_list)

    def delete_car(self):
        selected = self.car_listbox.curselection()
        if selected:
            if messagebox.askyesno("確認", "選択された車両を削除しますか？"):
                del self.formation["cars"][selected[0]]
                self.update_car_list()

    def copy_car(self):
        selected = self.car_listbox.curselection()
        if selected:
            car = self.formation["cars"][selected[0]]
            new_car = car.copy()
            new_car["name"] += " (コピー)"
            self.formation["cars"].append(new_car)
            self.update_car_list()

    def edit_car(self, event):
        selected = self.car_listbox.curselection()
        if selected:
            car = self.formation["cars"][selected[0]]
            CarWindow(self.window, self.formation, self.update_car_list, car, selected[0])

    def save_formation_description(self, event):
        self.formation["description"] = self.formation_description.get("1.0", tk.END).strip()

class CarWindow:
    def __init__(self, parent, formation, update_callback, car=None, index=None):
        self.formation = formation
        self.update_callback = update_callback
        self.car = car
        self.index = index

        self.window = tk.Toplevel(parent)
        self.window.title("車両編集" if car else "車両追加")
        self.window.geometry("500x700")

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 車両名
        tk.Label(frame, text="車両名:").pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.name_entry.pack(fill=tk.X, pady=5)
        if self.car:
            self.name_entry.insert(tk.END, self.car.get("name", ""))

        # 車両タイプ（タグ）
        tk.Label(frame, text="車両タイプ (1〜6個):").pack(anchor="w", pady=5)
        self.type_frame = tk.Frame(frame)
        self.type_frame.pack(fill=tk.X, pady=5)

        self.selected_types = self.car.get("tags", []) if self.car else []
        self.type_vars = []
        self.update_type_buttons()

        tk.Button(frame, text="タグ編集", command=self.edit_tags).pack(pady=5)

        # ステータス項目
        status_fields = [
            ("加速度 (m/s²)", "acceleration"),
            ("減速度 (m/s²)", "deceleration"),
            ("出力 (kW)", "power_kw"),
            ("制御方式", "control_method")
        ]

        self.status_entries = {}
        for label_text, key in status_fields:
            tk.Label(frame, text=label_text + ":").pack(anchor="w", pady=5)
            entry = tk.Entry(frame, font=("Helvetica", 12))
            entry.pack(fill=tk.X, pady=5)
            if self.car:
                entry.insert(tk.END, str(self.car.get(key, "")))
            self.status_entries[key] = entry

        # 車両解説
        tk.Label(frame, text="車両解説:").pack(anchor="w", pady=5)
        self.description_text = tk.Text(frame, height=5, font=("Helvetica", 12))
        self.description_text.pack(fill=tk.BOTH, pady=5)
        if self.car:
            self.description_text.insert(tk.END, self.car.get("description", ""))

        # 保存ボタン
        tk.Button(frame, text="保存", command=self.save_car).pack(pady=10)

    def update_type_buttons(self):
        for widget in self.type_frame.winfo_children():
            widget.destroy()
        for t in self.selected_types:
            tk.Label(self.type_frame, text=t, bg=CAR_TYPE_COLORS.get(t, "grey"), fg="white", padx=5, pady=2, relief=tk.RIDGE).pack(side=tk.LEFT, padx=2, pady=2)

    def edit_tags(self):
        edit_window = tk.Toplevel(self.window)
        edit_window.title("車両タイプ選択")
        edit_window.geometry("300x400")

        tk.Label(edit_window, text="車両タイプを選択してください (最大6個):").pack(anchor="w", pady=5)

        # 選択可能なタイプをリストボックスで表示
        listbox = tk.Listbox(edit_window, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        for code, name in CAR_TYPES.items():
            listbox.insert(tk.END, f"{code}: {name}")
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 既に選択されているタイプを選択
        existing_indices = [i for i, (k, v) in enumerate(CAR_TYPES.items()) if v in self.selected_types]
        for idx in existing_indices:
            listbox.selection_set(idx)

        def save_tags():
            selected_indices = listbox.curselection()
            selected = [list(CAR_TYPES.values())[i] for i in selected_indices]
            if len(selected) > 6:
                messagebox.showerror("エラー", "車両タイプは最大6個まで選択できます。")
                return
            self.selected_types = selected
            self.update_type_buttons()
            edit_window.destroy()

        tk.Button(edit_window, text="保存", command=save_tags).pack(pady=5)

    def save_car(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("エラー", "車両名を入力してください。")
            return

        tags = self.selected_types
        if len(tags) == 0:
            messagebox.showerror("エラー", "少なくとも1つの車両タイプを選択してください。")
            return
        elif len(tags) > 6:
            messagebox.showerror("エラー", "車両タイプは最大6個まで選択できます。")
            return

        # ステータス項目の取得
        try:
            acceleration = float(self.status_entries["acceleration"].get())
            deceleration = float(self.status_entries["deceleration"].get())
            power_kw = float(self.status_entries["power_kw"].get())
            control_method = self.status_entries["control_method"].get().strip()
        except ValueError:
            messagebox.showerror("エラー", "ステータス項目には数値を入力してください。")
            return

        description = self.description_text.get("1.0", tk.END).strip()

        # 色の設定（最初のタグの色を使用）
        color = CAR_TYPE_COLORS.get(tags[0], "black")

        car_data = {
            "name": name,
            "tags": tags,
            "color": color,
            "acceleration": acceleration,
            "deceleration": deceleration,
            "power_kw": power_kw,
            "control_method": control_method,
            "description": description
        }

        if self.car and self.index is not None:
            # 編集の場合
            self.formation["cars"][self.index] = car_data
        else:
            # 追加の場合
            self.formation["cars"].append(car_data)

        self.update_callback()
        self.window.destroy()

class RetiredWindow:
    def __init__(self, parent, retired_data):
        self.retired_data = retired_data

        self.window = tk.Toplevel(parent)
        self.window.title("廃車リスト")
        self.window.geometry("500x400")

        self.create_ui()

    def create_ui(self):
        tk.Label(self.window, text="廃車一覧").pack(anchor="w", padx=5, pady=5)
        self.retired_listbox = tk.Listbox(self.window, height=20, width=50, font=("Helvetica", 12))
        self.retired_listbox.pack(fill=tk.BOTH, padx=5, pady=5)

        for retired_car in self.retired_data:
            self.retired_listbox.insert(tk.END, retired_car["name"])

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="廃車追加", command=self.add_retired_car).pack(fill=tk.X, pady=5)

    def add_retired_car(self):
        car_name = simpledialog.askstring("廃車追加", "廃車車両名を入力してください:")
        if car_name:
            self.retired_data.append({"name": car_name})
            self.retired_listbox.insert(tk.END, car_name)

class PreviewWindow:
    def __init__(self, parent, photo_path):
        self.photo_path = photo_path

        self.window = tk.Toplevel(parent)
        self.window.title("写真プレビュー")
        self.window.geometry("600x600")

        # 画像表示
        try:
            img = Image.open(photo_path)
            img.thumbnail((600, 600))
            self.photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.window, image=self.photo)
            label.pack()
        except Exception as e:
            messagebox.showerror("エラー", f"画像を開く際にエラーが発生しました: {e}")
            self.window.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainManagerApp(root)
    root.mainloop()
