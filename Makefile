# Makefile for setting up a virtual environment, installing dependencies, and building the binary

# Set the Python script filename
SCRIPT_NAME = main.py

# The name of the output binary 
OUTPUT_NAME = BullshitjobQuest

# The name of the generated folder 
DIST_DIR = dist

# The virtual environment folder 
VENV_DIR = venv

# The App icon
ICON_PATH = icon.ico

# Default target: Build the binary
all: venv build

# Create the virtual environment and install dependencies
venv:
	@echo "Creating virtual environment..."
	python -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(VENV_DIR)\Scripts\pip install -r requirements.txt

# Create the binary using PyInstaller
build:
	@echo "Building the binary..."
	$(VENV_DIR)\Scripts\python -m PyInstaller --onefile --windowed $(SCRIPT_NAME) --name $(OUTPUT_NAME) --icon=$(ICON_PATH)

# Clean the generated files (dist, build, .spec file, venv)
clean:
	@echo "Cleaning up generated files..."
	rmdir /s /q $(DIST_DIR)
	rmdir /s /q build
	del /f /q $(OUTPUT_NAME).spec
	rmdir /s /q $(VENV_DIR)

# Rebuild the binary from scratch (clean + build)
rebuild: clean venv build

# Show the usage information
help:
	@echo "Makefile targets:"
	@echo "  all         - Create virtual environment, install dependencies, and build the binary (default)"
	@echo "  venv        - Create the virtual environment and install dependencies"
	@echo "  build       - Build the binary"
	@echo "  clean       - Clean the generated files"
	@echo "  rebuild     - Clean and then build the binary"
	@echo "  help        - Show this help message"
