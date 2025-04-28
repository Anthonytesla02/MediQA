import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")
        master.configure(bg="#f0f0f0")
        master.resizable(False, False)
        
        # Display variables
        self.current_expression = ""
        self.total_expression = ""
        
        # Configure display frame
        self.display_frame = tk.Frame(master, height=120, bg="#f0f0f0")
        self.display_frame.pack(pady=10)
        
        # Total expression display (shows the full calculation)
        self.total_expression_label = tk.Label(
            self.display_frame,
            text="",
            font=("Arial", 14),
            anchor=tk.E,
            bg="#f0f0f0",
            width=25,
            height=1
        )
        self.total_expression_label.pack(pady=(10, 0))
        
        # Current expression display (shows current input/result)
        self.current_expression_label = tk.Label(
            self.display_frame,
            text="0",
            font=("Arial", 24, "bold"),
            anchor=tk.E,
            bg="#f0f0f0",
            width=15,
            height=1
        )
        self.current_expression_label.pack(pady=(5, 10))
        
        # Configure buttons frame
        self.buttons_frame = tk.Frame(master, bg="#f0f0f0")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.create_buttons()
        
        # Bind keyboard events
        self.bind_keys()
    
    def bind_keys(self):
        """Bind keyboard keys to calculator functions"""
        self.master.bind("<Return>", lambda event: self.evaluate())
        self.master.bind("<Escape>", lambda event: self.clear())
        
        for key in "0123456789":
            self.master.bind(key, lambda event, digit=key: self.add_to_expression(digit))
        
        self.master.bind("+", lambda event: self.append_operator("+"))
        self.master.bind("-", lambda event: self.append_operator("-"))
        self.master.bind("*", lambda event: self.append_operator("×"))
        self.master.bind("/", lambda event: self.append_operator("÷"))
        self.master.bind(".", lambda event: self.add_to_expression("."))
        self.master.bind("<BackSpace>", lambda event: self.backspace())
    
    def create_buttons(self):
        """Create and place calculator buttons in the grid"""
        # Define button layout
        buttons = [
            ("C", 0, 0, "#ff9500", self.clear),
            ("±", 0, 1, "#a5a5a5", self.negate),
            ("%", 0, 2, "#a5a5a5", self.percentage),
            ("÷", 0, 3, "#ff9500", lambda: self.append_operator("÷")),
            
            ("7", 1, 0, "#d4d4d2", lambda: self.add_to_expression("7")),
            ("8", 1, 1, "#d4d4d2", lambda: self.add_to_expression("8")),
            ("9", 1, 2, "#d4d4d2", lambda: self.add_to_expression("9")),
            ("×", 1, 3, "#ff9500", lambda: self.append_operator("×")),
            
            ("4", 2, 0, "#d4d4d2", lambda: self.add_to_expression("4")),
            ("5", 2, 1, "#d4d4d2", lambda: self.add_to_expression("5")),
            ("6", 2, 2, "#d4d4d2", lambda: self.add_to_expression("6")),
            ("-", 2, 3, "#ff9500", lambda: self.append_operator("-")),
            
            ("1", 3, 0, "#d4d4d2", lambda: self.add_to_expression("1")),
            ("2", 3, 1, "#d4d4d2", lambda: self.add_to_expression("2")),
            ("3", 3, 2, "#d4d4d2", lambda: self.add_to_expression("3")),
            ("+", 3, 3, "#ff9500", lambda: self.append_operator("+")),
            
            ("0", 4, 0, "#d4d4d2", lambda: self.add_to_expression("0"), 2),
            (".", 4, 2, "#d4d4d2", lambda: self.add_to_expression(".")),
            ("=", 4, 3, "#ff9500", self.evaluate)
        ]
        
        # Create the buttons
        for button_data in buttons:
            if len(button_data) == 6:  # Special case for 0 button (spans 2 columns)
                text, row, col, color, command, columnspan = button_data
                button = tk.Button(
                    self.buttons_frame,
                    text=text,
                    font=("Arial", 18),
                    bg=color,
                    fg="white" if color != "#d4d4d2" else "black",
                    bd=0,
                    command=command
                )
                button.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="nsew")
            else:
                text, row, col, color, command = button_data
                button = tk.Button(
                    self.buttons_frame,
                    text=text,
                    font=("Arial", 18),
                    bg=color,
                    fg="white" if color != "#d4d4d2" else "black",
                    bd=0,
                    command=command
                )
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1)
    
    def add_to_expression(self, value):
        """Add a digit or decimal point to the current expression"""
        # If we start with a decimal point, add a leading zero
        if self.current_expression == "" and value == ".":
            self.current_expression = "0."
        # Prevent multiple decimal points in the same number
        elif value == "." and "." in self.current_expression:
            return
        # If current expression is just '0', replace it unless adding a decimal
        elif self.current_expression == "0" and value != ".":
            self.current_expression = value
        else:
            self.current_expression += value
        
        self.update_current_display()
    
    def append_operator(self, operator):
        """Append an operator to the expression"""
        if self.current_expression:
            # If last operation resulted in an error, clear it when starting a new operation
            if self.current_expression == "Error":
                self.clear()
                return
                
            # Update the total expression
            self.total_expression += self.current_expression + " " + operator + " "
            self.current_expression = ""
            
            self.update_total_display()
            self.update_current_display()
    
    def clear(self):
        """Clear all expressions and reset the calculator"""
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_display()
        self.update_total_display()
    
    def negate(self):
        """Change the sign of the current number"""
        if self.current_expression and self.current_expression != "Error":
            # Check if the current expression is a numeric value
            try:
                value = float(self.current_expression)
                # Avoid -0.0
                if value == 0:
                    return
                    
                self.current_expression = str(-value)
                # Convert to integer if it's a whole number
                if self.current_expression.endswith(".0"):
                    self.current_expression = self.current_expression[:-2]
                    
                self.update_current_display()
            except ValueError:
                pass  # Not a number, do nothing
    
    def percentage(self):
        """Convert the current number to a percentage (divide by 100)"""
        if self.current_expression and self.current_expression != "Error":
            try:
                value = float(self.current_expression)
                self.current_expression = str(value / 100)
                # Remove trailing zeros for cleaner display
                if self.current_expression.endswith(".0"):
                    self.current_expression = self.current_expression[:-2]
                self.update_current_display()
            except ValueError:
                pass
    
    def backspace(self):
        """Remove the last character from the current expression"""
        if self.current_expression and self.current_expression != "Error":
            self.current_expression = self.current_expression[:-1]
            self.update_current_display()
    
    def evaluate(self):
        """Evaluate the complete expression and display the result"""
        if not self.total_expression and not self.current_expression:
            return
            
        # If there's a current expression, add it to the total
        complete_expression = self.total_expression + self.current_expression
        
        # If expression ends with an operator, remove it
        if complete_expression and complete_expression[-1] in "+-×÷ ":
            complete_expression = complete_expression.rstrip("+-×÷ ")
        
        # Replace UI operators with Python operators
        complete_expression = complete_expression.replace("×", "*").replace("÷", "/")
        
        try:
            # Evaluate the expression
            result = str(eval(complete_expression))
            
            # Convert to integer if it's a whole number
            if result.endswith(".0"):
                result = result[:-2]
                
            # Update the displays
            self.total_expression = ""
            self.current_expression = result
            self.update_total_display()
            self.update_current_display()
            
        except ZeroDivisionError:
            self.current_expression = "Error"
            self.update_current_display()
            messagebox.showerror("Error", "Division by zero is not allowed")
            
        except Exception as e:
            self.current_expression = "Error"
            self.update_current_display()
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
    
    def update_current_display(self):
        """Update the current expression display"""
        if not self.current_expression:
            self.current_expression_label.config(text="0")
        else:
            # Limit display length to prevent overflow
            display_text = self.current_expression
            if len(display_text) > 15:
                # Try to use scientific notation for very large numbers
                try:
                    val = float(display_text)
                    if abs(val) > 10**12:
                        display_text = f"{val:.10e}"
                except:
                    # If not a simple number, just truncate
                    display_text = display_text[:15] + "..."
                
            self.current_expression_label.config(text=display_text)
    
    def update_total_display(self):
        """Update the total expression display"""
        self.total_expression_label.config(text=self.total_expression)


def main():
    # Create the main window
    root = tk.Tk()
    root.geometry("350x500")
    
    # Create the calculator
    calculator = Calculator(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
