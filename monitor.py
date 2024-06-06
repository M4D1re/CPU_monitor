import wmi
import psutil
import tkinter as tk

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information")
        self.root.geometry("800x800")

        self.cpu_label = tk.Label(root, text="CPU Information:")
        self.cpu_label.pack()

        self.cpu_info = tk.Text(root, height=15, width=70)
        self.cpu_info.pack()

        self.cpu_load_label = tk.Label(root, text="CPU Load per Core:")
        self.cpu_load_label.pack()

        self.cpu_load_text = tk.Text(root, height=20, width=70)
        self.cpu_load_text.pack()

        self.update_info()

    def get_cpu_info(self):
        c = wmi.WMI()
        cpu_data = ""
        try:
            for processor in c.Win32_Processor():
                cpu_data += "Processor Name: {}\n".format(processor.Name)
                cpu_data += "Current Clock Speed: {} MHz\n".format(processor.CurrentClockSpeed)
                cpu_data += "Max Clock Speed: {} MHz\n".format(processor.MaxClockSpeed)
                cpu_data += "Cores: {}\n".format(processor.NumberOfCores)
                cpu_data += "Threads: {}\n".format(processor.NumberOfLogicalProcessors)
                cpu_data += "--------------------\n"

            # Get per-core CPU usage
            core_usages = psutil.cpu_percent(percpu=True)
        except Exception as e:
            cpu_data += "Error retrieving CPU info: {}\n".format(e)
            core_usages = []
        return cpu_data, core_usages

    def update_info(self):
        cpu_data, core_usages = self.get_cpu_info()

        self.cpu_info.delete(1.0, tk.END)
        self.cpu_info.insert(tk.END, cpu_data)

        self.cpu_load_text.delete(1.0, tk.END)
        max_length = 50  # Maximum length for the bar

        for i, usage in enumerate(core_usages):
            bar_length = int(usage * max_length / 100)
            bar = "#" * bar_length + "-" * (max_length - bar_length)
            self.cpu_load_text.insert(tk.END, f"Core {i}: [{bar}] {usage:.2f}%\n")

        self.root.after(5000, self.update_info)  # Update every 5 seconds

def main():
    root = tk.Tk()
    app = SystemInfoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()