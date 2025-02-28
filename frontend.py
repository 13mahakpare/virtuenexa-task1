import tkinter as tk
from tkinter import messagebox
from backend import get_weather, save_history, get_saved_cities
from PIL import Image, ImageTk  # Import for handling images
import requests  # Missing import for API calls
import webbrowser
# Global variable to store the weather window reference
weather_window = None  

# Main window setup
root = tk.Tk()
root.title("Weatherly")
root.geometry("500x400")

# 🔹 Function to Load & Set Background
def set_background(image_path):
    global bg_photo
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1550, 800), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label.config(image=bg_photo)  # Update the label's image

# 🔹 Default Home Page Background
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)
set_background("home.png")  # Default background

# 🔹 Fetch Weather & Update Background
def get_weather_action():
    city = city_entry.get()
    
    # 🔹 Fetch weather data using backend function
    weather = get_weather(city)
    
    if "error" in weather:
        messagebox.showerror("Error", weather["error"])
    else:
        show_result(city, weather)
        
        # 🔹 Change Background Based on Weather
        weather_condition = weather["description"].lower()
        if "clear" in weather_condition:
            set_background("sunny.jpg")
        elif "cloud" in weather_condition or "mist" in weather_condition or "fog" in weather_condition:
            set_background("cloudy.jpg")
        elif "rain" in weather_condition or "drizzle" in weather_condition or "thunderstorm" in weather_condition:
            set_background("rainy.jpg")
        elif "snow" in weather_condition:
            set_background("snow.jpeg")
        else:
            set_background("default.jpg")  # Fallback background

# 🔹 Display weather results
def show_result(city, weather):
    """Display the live weather result in a new window with a save button."""
    result_window = tk.Toplevel(root)
    result_window.title(f"Weather in {city}")
    result_window.geometry("350x300")
    result_window.configure(bg="lightblue")

    result_text = (
        f"City: {weather['city']}\n"
        f"Temperature: {weather['temperature']}°C\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Description: {weather['description']}"
    )

    label = tk.Label(result_window, text=result_text, font=("Arial", 12), bg="lightblue")
    label.pack(pady=20)

    # Save button inside the weather window
    save_button = tk.Button(result_window, text="Save City", font=("Arial", 10), bg="green", fg="white",
                            command=lambda: save_city(city, result_window))
    save_button.pack(pady=10)
    
    # 🔹 Clickable link function
    def open_weather_link():
        url = f"https://openweathermap.org/find?q={city}"  # OpenWeatherMap search page for the city
        webbrowser.open(url)

    # 🔹 Clickable link label (bottom-right corner)
    link_label = tk.Label(result_window, text="For more details, click here", fg="blue", cursor="hand2", 
                          bg="lightblue", font=("Arial", 10, "underline"))
    link_label.place(relx=0.98, rely=0.98, anchor="se")  # Bottom-right corner placement
    link_label.bind("<Button-1>", lambda e: open_weather_link())  # Open link when clicked

    return result_window

    return result_window  # Keeps the window open

# 🔹 Save City to History
def save_city(city, window):
    """Save the city and notify the user."""
    save_history(city)
    messagebox.showinfo("Saved", f"{city} has been saved to history.")

# 🔹 Show Saved Cities
def show_saved_cities():
    """Open a new window to display saved city names."""
    history_window = tk.Toplevel(root)
    history_window.title("Saved Cities")
    history_window.geometry("400x300")
    history_window.configure(bg="lightblue")

    history_label = tk.Label(history_window, text="Click on a city to view its weather", font=("Arial", 14, "bold"), bg="lightblue")
    history_label.pack(pady=10)

    history_listbox = tk.Listbox(history_window, width=30, height=10)
    history_listbox.pack(pady=5)

    cities = get_saved_cities()
    
    if not cities:
        history_listbox.insert(tk.END, "No saved cities")
    else:
        for city in cities:
            history_listbox.insert(tk.END, city)

    history_listbox.bind("<Double-Button-1>", lambda event: on_city_selected(event, history_listbox))

# 🔹 Show Weather When a Saved City is Clicked
def on_city_selected(event, listbox):
    """Fetch and display live weather when a saved city is clicked."""
    selected_index = listbox.curselection()
    if selected_index:
        city = listbox.get(selected_index)
        weather = get_weather(city)
        if "error" in weather:
            messagebox.showerror("Error", weather["error"])
        else:
            show_result(city, weather)

# 🔹 Centered Frame for Search Box
search_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
search_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centering the search box

# 🔹 City Entry Field (Wider, Shorter & Rounded)
city_entry = tk.Entry(search_frame, font=("Arial", 14), fg="gray", width=30, relief="flat", bd=0)
city_entry.insert(0, "Search City")  # Default placeholder text
city_entry.pack(side="left", padx=10, ipady=5)

# Remove placeholder on click
def on_entry_click(event):
    if city_entry.get() == "Search City":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

# Restore placeholder if empty
def on_focus_out(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Search City")
        city_entry.config(fg="gray")

city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focus_out)

# 🔹 Load & Resize Search Icon (For Design Only)
search_icon_img = Image.open("searchicon.png")  # Ensure "searchicon.png" exists
search_icon_img = search_icon_img.resize((30, 30), Image.Resampling.LANCZOS)
search_icon = ImageTk.PhotoImage(search_icon_img)

# 🔹 Label for Search Icon (Just for Looks)
search_icon_label = tk.Label(search_frame, image=search_icon, bg="white")
search_icon_label.pack(side="right", padx=5)

# 🔹 Centered 'Get Weather' Button (Now Works)
get_weather_button = tk.Button(root, text="Get Weather", font=("verdana", 12, "bold"), bg="#00ADB5", fg="white",
                               relief="flat", padx=20, pady=5, command=get_weather_action)
get_weather_button.place(relx=0.5, rely=0.6, anchor="center")  # Centering the button

# 🔹 Centered 'View Saved' Button (Above the Bottom)
view_saved_button = tk.Button(root, text="View Saved", font=("verdana", 12, "bold"), bg="#393E46", fg="white",
                              relief="flat", padx=20, pady=5, command=show_saved_cities)
view_saved_button.place(relx=0.5, rely=0.93, anchor="center")  # Adjusted for visibility

# 🔹 "Contact Us" in Bottom-Right Corner (No Background)
contact_label = tk.Label(root, text="Contact Us", fg="blue", cursor="hand2",
                         font=("Arial", 10, "underline"))
contact_label.place(relx=0.98, rely=0.98, anchor="se")

# Run application
root.mainloop()
