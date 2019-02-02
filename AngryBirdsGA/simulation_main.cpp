#include "simulation.h"
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

int main(int argc, char *argv[]) {
	if( argc > 1 ){
		ifstream file;
		file.open(argv[1], ios::in);

		if(file.is_open()){
  			int n_blocks = count(istreambuf_iterator<char>(file), 
            					  istreambuf_iterator<char>(), '\n');
  			file.clear();
  			file.seekg(0);

			int block_size = 6;
			float *v = new float[n_blocks*block_size];

			string line;
			string delimiter = " ";
			string value;
			size_t pos = 0;
			int value_count = 0;

			for (int i = 0; i < n_blocks; i++) {
				if(getline (file,line)){
					value_count = 0;
					while ((pos = line.find(delimiter)) != string::npos) {
		    			value = line.substr(0, pos);
		    			
		    			v[i*block_size+value_count] = atof(value.c_str());
		    			
		    			line.erase(0, pos + delimiter.length());
		    			value = "";
		    			pos = 0;
		    			value_count++;
					}
				} else {cerr << "Could not get line!"; } // end if
			}
			
			world_simulation(v, block_size, n_blocks);

			file.close();
		} else {
			cerr << "Cant open file";
		}

	} else {
		cerr << "No file especified";
	}

}