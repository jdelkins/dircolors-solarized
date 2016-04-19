OUT = dircolors.16dark dircolors.16light dircolors.256dark dircolors.256light dircolors.16Mdark dircolors.16Mlight
PYTHON = python

all: $(OUT)

dircolors.16dark: dircolors.in transform.py
	$(PYTHON) transform.py 16 dark

dircolors.16light: dircolors.in transform.py
	$(PYTHON) transform.py 16 light

dircolors.256dark: dircolors.in transform.py
	$(PYTHON) transform.py 256 dark

dircolors.256light: dircolors.in transform.py
	$(PYTHON) transform.py 256 light

dircolors.16Mdark: dircolors.in transform.py
	$(PYTHON) transform.py 16M dark

dircolors.16Mlight: dircolors.in transform.py
	$(PYTHON) transform.py 16M light

clean:
	rm $(OUT)
	sudo rm -rf test-directory
	rm -rf __pycache__

test-directory: test-directory.tar.bz2
	sudo rm -rf test-directory
	sudo tar xvjf test-directory.tar.bz2
	cd test-directory && sudo chmod a+t directory+t directory+t-o+w && sudo chmod 777 directory777 && sudo chmod o+w directory+t-o+w && sudo rm file3.hardlink; sudo ln file3 file3.hardlink && sudo chmod g+s setgid-g+s && sudo chmod u+s setuid-u+s

.PHONY: all clean
