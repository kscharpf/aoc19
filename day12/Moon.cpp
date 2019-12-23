#include <math.h>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <sstream>

using namespace std;

class Moon {
	public :
		Moon(int x, int y, int z) {
			pos.push_back(x);
			pos.push_back(y);
			pos.push_back(z);
			vel.push_back(0);
			vel.push_back(0);
			vel.push_back(0);
		}

		Moon(const Moon &rhs) {
			pos.push_back(rhs.pos[0]);
			pos.push_back(rhs.pos[1]);
			pos.push_back(rhs.pos[2]);
			pos.push_back(rhs.vel[0]);
			pos.push_back(rhs.vel[1]);
			pos.push_back(rhs.vel[2]);
		}

		Moon &operator=(const Moon &rhs) {
			pos.push_back(rhs.pos[0]);
			pos.push_back(rhs.pos[1]);
			pos.push_back(rhs.pos[2]);
			pos.push_back(rhs.vel[0]);
			pos.push_back(rhs.vel[1]);
			pos.push_back(rhs.vel[2]);

			return *this;
		}

		static void gravity(Moon &moon1, Moon &moon2) {
			for(size_t i=0; i<moon1.pos.size(); i++) {
				if(moon1.pos[i] > moon2.pos[i]) {
					moon1.vel[i]--;
					moon2.vel[i]++;
				} else if(moon1.pos[i] < moon2.pos[i]) {
					moon1.vel[i]++;
					moon2.vel[i]--;
				}
			}
		}

		int energy(const std::vector<int> &v) const {
			int s = 0;
			for (auto &x : v) {
				s += abs(x);
			}
			return s;
		}

		int potential_energy() const {
			return energy(pos);
		}

		int kinetic_energy() const {
			return energy(vel);
		}

		int total_energy() const {
			return potential_energy() * kinetic_energy();
		}

		void update() {
			for(size_t i=0; i<pos.size(); i++) {
				pos[i] += vel[i];
			}
		}

		std::pair<uint64_t, uint64_t> pos_vel_for_dim(const int dim) const {
			return std::make_pair<uint64_t, uint64_t>(pos[dim], vel[dim]);
		}

		bool operator==(const Moon &rhs) const {
			return pos[0] == rhs.pos[0] && pos[1] == rhs.pos[1] && pos[2] == rhs.pos[2] &&
				vel[0] == rhs.vel[0] && vel[1] == rhs.vel[1] && vel[2] == rhs.vel[2];
		}

		friend ostream & operator<<(ostream &os, const Moon &m) {
			os << "pos <" << (m.pos[0]) << "," << (m.pos[1]) << "," << (m.pos[2]) << ">";
			os << "vel <" << (m.vel[0]) << "," << (m.vel[1]) << "," << (m.vel[2]) << ">";
			return os;
		}

		size_t hashCode() const {
			size_t hash = 37;
			hash = 17*hash + pos[0];
			hash = 17*hash + pos[1];
			hash = 17*hash + pos[2];
			hash = 17*hash + vel[0];
			hash = 17*hash + vel[1];
			hash = 17*hash + vel[2];
			return hash;
		}

		std::string str() const {
			std::stringstream ss;
			ss << pos[0] << "," << pos[1] << "," << pos[2];
			ss << vel[0] << "," << vel[1] << "," << vel[2];
			return ss.str();
		}

	private:
		std::vector<int> pos;
		std::vector<int> vel;
};

uint64_t gcd(uint64_t a, uint64_t b) {
	if(a == 0) return b;
	return gcd(b % a, a);
}

uint64_t lcm(uint64_t a, uint64_t b) {
	return (a*b)/gcd(a,b);
}


int main() {
	std::vector<Moon *> moons;
	moons.push_back(new Moon(5,4,4));
	moons.push_back(new Moon(-11,-11,-3));
	moons.push_back(new Moon(0,7,0));
	moons.push_back(new Moon(-13,2,10));
	//moons.push_back(new Moon(-1,0,2));
	//moons.push_back(new Moon(2,-10,-7));
	//moons.push_back(new Moon(4,-8,8));
	//moons.push_back(new Moon(3,5,-1));
	//moons.push_back(new Moon(-8,10,0));
	//moons.push_back(new Moon(5,5,10));
	//moons.push_back(new Moon(2,-7,3));
	//moons.push_back(new Moon(9,-8,-3));
	//
	std::vector<bool> allDims;
	allDims.push_back(false);
	allDims.push_back(false);
	allDims.push_back(false);

	std::string first_x;
	std::string first_y;
	std::string first_z;
	bool matched_x = false;
	bool matched_y = false;
	bool matched_z = false;
	int x_timestep = 0;
	int y_timestep = 0;
	int z_timestep = 0;
	for(int timestep = 0; ; timestep++) {

		if(timestep % 1000000 == 0) {
			cout << "=================================" << endl;
			cout << "Timestep " << timestep << endl;
			cout << "=================================" << endl;
			for(int i=0; i<4; i++) {
				cout << "Moon["<<i<<"]: " << (*moons[i]) << std::endl;
			}
		}

		std::string s_x;
		std::string s_y;
		std::string s_z;

		std::stringstream ss_x;
		std::stringstream ss_y;
		std::stringstream ss_z;

		for(int i=0; i<4; i++) {
			auto x = moons[i]->pos_vel_for_dim(0);
			ss_x << x.first << "," << x.second;
			auto y = moons[i]->pos_vel_for_dim(1);
			ss_y << y.first << "," << y.second;
			auto z = moons[i]->pos_vel_for_dim(2);
			ss_z << z.first << "," << z.second;
		};
		s_x = ss_x.str();
		s_y = ss_y.str();
		s_z = ss_z.str();

		if(timestep == 0) {
			first_x = s_x;
			first_y = s_y;
			first_z = s_z;
		} 

		if(timestep > 0) {
			if(s_x == first_x && x_timestep == 0) {
				cout << "Matched x at timestep " << timestep << endl;
				x_timestep = timestep;
				matched_x = true;
			}
			if(s_y == first_y && y_timestep == 0) {
				cout << "Matched y at timestep " << timestep << endl;
				y_timestep = timestep;
				matched_y = true;
			}
			if(s_z == first_z && z_timestep == 0) {
				cout << "Matched z at timestep " << timestep << endl;
				z_timestep = timestep;
				matched_z = true;
			}
			if(matched_x && matched_y && matched_z) {
				cout << "Repeat is " << lcm(x_timestep, lcm(y_timestep, z_timestep)) << endl;
				break;
			}
			
		}
		if(timestep == 1000) {
			int sum = 0;
			for(int i=0; i<4; i++) {
				sum += moons[i]->total_energy();
			}
			cout << "total energy after 1000 steps: " << sum << std::endl;
		}
		for(int i=0; i<3; i++) {
			for(int j=i+1; j<4; j++) {
				Moon::gravity(*moons[i],*moons[j]);
			}
		}
		for(int i=0; i<4; i++) {
			moons[i]->update();
		}
	}

	return 0;
}
