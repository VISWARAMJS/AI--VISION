import tkinter as T
import re
import builtins
import sys
import io
from tkinter import filedialog

keywords = ["def", "class", "import", "if", "else", "return", "for",
            "while", "in", "try", "except", "finally", "with", "as",
            "lambda", "from", "elif", "pass", "break", "continue", "not", "and", "or"]

keyword_color = "cyan"
builtin_color = "red"
string_color = "green"
number_color = "yellow"
function_color = "magenta"

builtin_functions = [f for f in dir(builtins) if callable(getattr(builtins, f))]


def highlight_text(event=None):
    content = text_widget.get("1.0", T.END)
    for tag in ["keyword", "builtin", "string", "number", "function"]:
        text_widget.tag_remove(tag, "1.0", T.END)
    for kw in keywords:
        for match in re.finditer(rf"\b{kw}\b", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            text_widget.tag_add("keyword", start, end)
    text_widget.tag_config("keyword", foreground=keyword_color)
    for fn in builtin_functions:
        for match in re.finditer(rf"\b{fn}\b", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            text_widget.tag_add("builtin", start, end)
    text_widget.tag_config("builtin", foreground=builtin_color)
    for match in re.finditer(r'(\bdef\b\s+)(\w+)', content):
        start = f"1.0 + {match.start(2)} chars"
        end = f"1.0 + {match.end(2)} chars"
        text_widget.tag_add("function", start, end)
    text_widget.tag_config("function", foreground=function_color)
    for match in re.finditer(r'(\".*?\"|\'.*?\')', content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_widget.tag_add("string", start, end)
    text_widget.tag_config("string", foreground=string_color)
    for match in re.finditer(r'\b\d+(\.\d+)?\b', content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_widget.tag_add("number", start, end)
    text_widget.tag_config("number", foreground=number_color)


def auto_indent(event):
    line = text_widget.get("insert linestart", "insert")
    indent = re.match(r"^\s*", line).group()
    if line.strip().endswith(":"):
        indent += "    "
    text_widget.insert("insert", f"\n{indent}")
    return "break"


def run_code():
    code = text_widget.get("1.0", T.END)
    output_text.config(state="normal")
    output_text.delete("1.0", T.END)

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    old_input = builtins.input

    output_stream = io.StringIO()
    sys.stdout = output_stream
    sys.stderr = output_stream

    input_buffer = []
    input_index = 0
    waiting_for_input = False
    input_var = None

    def custom_input(prompt=""):
        nonlocal waiting_for_input, input_var, input_buffer, input_index

        output_text.insert(T.END, prompt)
        output_text.see(T.END)
        output_text.mark_set("input_start", T.END + "-1c")

        waiting_for_input = True
        input_var = []
        input_buffer = []
        input_index = len(output_text.get("1.0", T.END)) - 1

        def on_key(event):
            nonlocal input_buffer, input_index, waiting_for_input, input_var

            if not waiting_for_input:
                return

            if event.keysym == "BackSpace":
                if input_var:
                    input_var.pop()
                    output_text.delete("end-2c", "end-1c")
                return "break"
            elif event.keysym == "Return":
                return "break"
            elif len(event.char) == 1:
                input_var.append(event.char)
                output_text.insert(T.END, event.char)
                output_text.see(T.END)
                return "break"

        def on_enter(event):
            nonlocal waiting_for_input, input_var
            if waiting_for_input:
                waiting_for_input = False
                output_text.insert(T.END, "\n")
                output_text.see(T.END)
                window.after(10, lambda: None)  
            return "break"

        output_text.bind("<Key>", on_key)
        output_text.bind("<Return>", on_enter)

        while waiting_for_input:
            try:
                window.update()
            except T.TclError:
                break

        output_text.unbind("<Key>")
        output_text.unbind("<Return>")

        return "".join(input_var) if input_var else ""

    builtins.input = custom_input

    try:
     
        def write_to_both(text):
            output_stream.write(text)
            output_text.insert(T.END, text)
            output_text.see(T.END)

        class DualOutput:
            def write(self, text):
                output_stream.write(text)
                output_text.insert(T.END, text)
                output_text.see(T.END)

            def flush(self):
                output_stream.flush()

        sys.stdout = DualOutput()
        sys.stderr = DualOutput()

        exec(code, {})
    except Exception as e:
        print("Error:", e)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        builtins.input = old_input

    output_text.config(state="normal")
    output_text.see(T.END)


def open_file():
    path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if path:
        with open(path, "r") as file:
            content = file.read()
        text_widget.delete("1.0", T.END)
        text_widget.insert(T.END, content)
        highlight_text()


def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".py",
                                        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if path:
        with open(path, "w") as file:
            file.write(text_widget.get("1.0", T.END))

window = T.Tk()
window.title("V.R.M - PYTHON IDE")

window.minsize(800, 600)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

frame_top = T.Frame(window, bg="black")
frame_top.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

frame_top.grid_columnconfigure(0, weight=1)
frame_top.grid_columnconfigure(1, weight=1)
frame_top.grid_columnconfigure(2, weight=1)
frame_top.grid_columnconfigure(3, weight=1)

open_button = T.Button(frame_top, text="OPEN", command=open_file, bg="black", fg="cyan", font=("Consolas", 12))
open_button.grid(row=0, column=0, padx=5, pady=3, sticky="ew")

save_button = T.Button(frame_top, text="SAVE", command=save_file, bg="black", fg="cyan", font=("Consolas", 12))
save_button.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

run_button = T.Button(frame_top, text="RUN", command=run_code, bg="black", fg="cyan", font=("Consolas", 12))
run_button.grid(row=0, column=2, padx=5, pady=3, sticky="ew")

clear_button = T.Button(frame_top, text="CLEAR OUTPUT",
                        command=lambda: output_text.delete("1.0", T.END),
                        bg="black", fg="cyan", font=("Consolas", 12))
clear_button.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

paned_window = T.PanedWindow(window, orient=T.VERTICAL, bg="black", sashrelief=T.RAISED, sashwidth=5)
paned_window.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

editor_frame = T.Frame(paned_window, bg="black")
paned_window.add(editor_frame, height=400)

editor_frame.grid_rowconfigure(0, weight=1)
editor_frame.grid_columnconfigure(0, weight=1)
editor_frame.grid_columnconfigure(1, weight=0)

text_widget = T.Text(editor_frame, wrap="none", font=("Consolas", 18), bg="black", fg="white", insertbackground="white")
text_widget.grid(row=0, column=0, sticky="nsew")

v_scrollbar = T.Scrollbar(editor_frame, orient=T.VERTICAL, command=text_widget.yview)
v_scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.config(yscrollcommand=v_scrollbar.set)

h_scrollbar = T.Scrollbar(editor_frame, orient=T.HORIZONTAL, command=text_widget.xview)
h_scrollbar.grid(row=1, column=0, sticky="ew")
text_widget.config(xscrollcommand=h_scrollbar.set)

output_frame = T.Frame(paned_window, bg="black")
paned_window.add(output_frame, height=200)


output_frame.grid_rowconfigure(1, weight=1)
output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_columnconfigure(1, weight=0)


output_label = T.Label(output_frame, text="OUTPUT (Interactive)", bg="black", fg="cyan", font=("Consolas", 12))
output_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))


output_text = T.Text(output_frame, height=15, bg="black", fg="white", font=("Consolas", 13), insertbackground="white")
output_text.grid(row=1, column=0, sticky="nsew")


output_v_scroll = T.Scrollbar(output_frame, orient=T.VERTICAL, command=output_text.yview)
output_v_scroll.grid(row=1, column=1, sticky="ns")
output_text.config(yscrollcommand=output_v_scroll.set)


output_h_scroll = T.Scrollbar(output_frame, orient=T.HORIZONTAL, command=output_text.xview)
output_h_scroll.grid(row=2, column=0, sticky="ew")
output_text.config(xscrollcommand=output_h_scroll.set)

text_widget.bind("<KeyRelease>", highlight_text)
text_widget.bind("<Return>", auto_indent)
window.geometry("1000x700")
window.mainloop()
