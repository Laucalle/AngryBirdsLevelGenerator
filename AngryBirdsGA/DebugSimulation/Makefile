IDIR =../Box2D_v2.1.2/Box2D/
CC=g++
CFLAGS=-I$(IDIR)

LDIR =../Box2D_v2.1.2/Box2D/Build/Box2D

LIBS=-lm

_DEPS = simulation.h

_OBJ = hellomake.o hellofunc.o 
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


obj/%.o: ../simulation.cpp ../simulation.h
	$(CC) -I../Box2D_v2.1.2/Box2D/ -static -c -o $@ $< -L../Box2D_v2.1.2/Box2D/Build/Box2D -lBox2D 

example: Simulation_debug_main.cpp obj/simulation.o
	$(CC) -L../Box2D_v2.1.2/Box2D/Build/Box2D -o $@ $^ -I..  ../Box2D_v2.1.2/Box2D/Build/Box2D/libBox2D.a

.PHONY: clean

clean:
	rm -f obj/*.o *~ 