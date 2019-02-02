#include "simulation.h"
int main() {
	int n_blocks = 1;
	int block_size = 6;
	float *v = new float[n_blocks*block_size];
	for(int i = 0; i< n_blocks*block_size; i++){
		v[i] = 1;
	}
	world_simulation(v, block_size, n_blocks);
}