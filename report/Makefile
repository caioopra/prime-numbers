# Makefile for LaTeX document compilation
# Author: Generated for prime numbers report
# Usage: make, make clean, make view, make help

# Variables
MAIN = main
TEX_FILES = $(wildcard *.tex)
BIB_FILES = $(wildcard *.bib)
PDF = $(MAIN).pdf
LATEX = pdflatex
BIBER = biber

# Default target
all: $(PDF)

# Main compilation target
$(PDF): $(TEX_FILES) $(BIB_FILES)
	@echo "Compiling LaTeX document..."
	$(LATEX) $(MAIN).tex
	@if [ -f $(MAIN).bcf ]; then \
		echo "Processing bibliography..."; \
		$(BIBER) $(MAIN); \
		echo "Recompiling with bibliography..."; \
		$(LATEX) $(MAIN).tex; \
		echo "Final compilation..."; \
		$(LATEX) $(MAIN).tex; \
	fi
	@echo "Compilation complete: $(PDF)"

# Force compilation target
compile:
	@echo "Compiling LaTeX document..."
	$(LATEX) $(MAIN).tex
	@if [ -f $(MAIN).bcf ]; then \
		echo "Processing bibliography..."; \
		$(BIBER) $(MAIN); \
		echo "Recompiling with bibliography..."; \
		$(LATEX) $(MAIN).tex; \
		echo "Final compilation..."; \
		$(LATEX) $(MAIN).tex; \
	fi
	@echo "Compilation complete: $(PDF)"

# Quick compilation (single pass, no bibliography)
quick:
	@echo "Quick compilation (single pass)..."
	$(LATEX) $(MAIN).tex

# Force full recompilation
rebuild: clean all

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.out *.run.xml *.toc *.lot *.lof
	@echo "Clean complete."

# Clean everything including PDF
clean-all: clean
	@echo "Removing PDF..."
	@rm -f $(PDF)

# View PDF (requires a PDF viewer)
view: $(PDF)
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(PDF); \
	elif command -v evince >/dev/null 2>&1; then \
		evince $(PDF) & \
	elif command -v okular >/dev/null 2>&1; then \
		okular $(PDF) & \
	else \
		echo "No PDF viewer found. Please open $(PDF) manually."; \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Compile the document (default)"
	@echo "  compile    - Force compilation regardless of file timestamps"
	@echo "  quick      - Quick compilation (single pass, no bibliography)"
	@echo "  rebuild    - Clean and recompile"
	@echo "  clean      - Remove auxiliary files"
	@echo "  clean-all  - Remove all generated files including PDF"
	@echo "  view       - Open PDF with system viewer"
	@echo "  help       - Show this help message"

# Phony targets
.PHONY: all compile quick rebuild clean clean-all view help

# Check for required tools
check-tools:
	@echo "Checking for required tools..."
	@command -v $(LATEX) >/dev/null 2>&1 || { echo "$(LATEX) not found!"; exit 1; }
	@command -v $(BIBER) >/dev/null 2>&1 || { echo "$(BIBER) not found!"; exit 1; }
	@echo "All required tools found."