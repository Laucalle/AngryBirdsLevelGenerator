CC=g++

obj/%.o: simulation.cpp simulation.h
	$(CC) -I./Box2D_v2.1.2/Box2D/ -static -c -o $@ $< -L./Box2D_v2.1.2/Box2D/Build/Box2D -lBox2D 

simulation_exec: simulation_main.cpp obj/simulation.o
	$(CC) -L./Box2D_v2.1.2/Box2D/Build/Box2D -o $@ $^ -I.  ./Box2D_v2.1.2/Box2D/Build/Box2D/libBox2D.a

.PHONY: clean

clean:
	rm -f obj/*.o *~ 