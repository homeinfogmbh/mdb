FILE_LIST = ./.installed_files.txt
ECHO = /bin/echo -e

install:
	install -m 755 ./crm.py /usr/local/lib/python3.4/dist-packages/homeinfo/

uninstall:
	@ while read FILE; do
		rm "${FILE}"
	done < ${FILE_LIST}

clean:
	@ rm -R ./build

check:
	@ find . -type f -name "*.py" -not -path "./build/*" -exec pep8 --hang-closing {} \;

pull:
	@ git pull

push:
	@ git push

all:	pull uninstall clean install
