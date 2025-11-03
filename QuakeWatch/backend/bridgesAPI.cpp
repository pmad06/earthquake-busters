/*
#include <string>

using namespace std;

#include "Bridges.h"
#include "DataSource.h"
#include "data_src/EarthquakeUSGS.h"


using namespace bridges;

int max_quakes = 100;

// This program fragment illustrates how to access the USGS earthquake data
int main(int argc, char **argv) {

	// create Bridges object
	Bridges bridges (1, "dhiv06_",
		"1183465480984");
	// set title
	bridges.setTitle("Accessing USGIS Earthquake Data (USGIS Data)");

	// read the earth quake  data
	DataSource ds (&bridges);
	vector<EarthquakeUSGS> eq_list = ds.getEarthquakeUSGSData(max_quakes);

	// print the first few quake records
	for (int k = 0; k < 10; k++) {
		cout << "Earthquake " << k << ": \n";
		const auto& eq = eq_list[k];
		cout << "\tMagnitude:" << eq.getMagnitude() << endl
		<< "\tDate:" << eq.getDateStr() << endl
		<< "\tLocation: " <<  eq.getLocation() << endl
		<< "\tLat/Long:"  << eq.getLatit() << "," <<
		eq.getLongit() << endl;
	}


	return 0;
}*/