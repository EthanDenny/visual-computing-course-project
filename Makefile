default:
	mkdir -p bin
	gcc  -fPIC -shared -o bin/speedylib.so src/speedylib.c
