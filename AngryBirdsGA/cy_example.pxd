
cdef extern from  "simulation.h":
	void world_simulation(float* k, int block_data, int n_blocks)
	