NAME=Uncertainty_2015
BIBDIR=.
BIBFILES=./Uncertainty_2015.bib

# Write stdout here
#OUTPUT=/dev/null
OUTPUT=$(NAME).out

# Use these commands
PDFLATEX=pdflatex
BIBTEX=bibtex
RM=/bin/rm
ECHO=/usr/bin/printf

# Use these compile flags
LATEXFLAGS=-halt-on-error -interaction=batchmode
BIBTEXFLAGS=

PASS='\033[00;32mPASS\033[00m\n'
FAIL="\033[00;31mFAIL\033[00m\n"

.PHONY: clean

all: $(NAME).pdf

$(NAME).pdf: $(NAME).tex $(BIBFILES)
	@$(RM) -f $(OUTPUT) 2> /dev/null || true
	@$(ECHO) "$(PDFLATEX) $(LATEXFLAGS) $(NAME).tex... "
	@($(PDFLATEX) $(LATEXFLAGS) $(NAME).tex > $(OUTPUT) && $(ECHO) $(PASS)) || $(ECHO) $(FAIL) 
	@$(ECHO) "$(BIBTEX) $(NAME).aux... "
	@($(BIBTEX) $(BIBTEXFLAGS) $(NAME).aux >> $(OUTPUT) && $(ECHO) $(PASS)) || $(ECHO) $(FAIL)
	@$(ECHO) "$(PDFLATEX) $(NAME).tex... "
	@($(PDFLATEX) $(LATEXFLAGS) $(NAME).tex > $(OUTPUT) && $(ECHO) $(PASS)) || $(ECHO) $(FAIL)
	@$(ECHO) "$(PDFLATEX) $(NAME).tex... "
	@($(PDFLATEX) $(LATEXFLAGS) $(NAME).tex > $(OUTPUT) && $(ECHO) $(PASS)) || $(ECHO) $(FAIL)
	@$(ECHO) "$(NAME).pdf successfully created.\n"

clean:
	@$(RM) -f $(NAME).log $(NAME).out *aux *bbl *blg 

nuke: clean
	@$(RM) -f $(NAME).pdf

pdf: all clean

