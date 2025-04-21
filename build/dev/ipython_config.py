c = get_config()  # noqa: F821

# Autoreload modules
c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = ["%autoreload 2"]
