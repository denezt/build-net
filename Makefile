PROGRAMS = boxes figlet cmatrix lolcat toilet trash-cli

.PHONY: install $(PROGRAMS)

install: $(PROGRAMS)
	@printf "\033[32mAll programs installed\033[0m\n"

$(PROGRAMS):
	@printf "\033[35mInstalling $@\033[0m\n"
	@sudo apt -y install $@
