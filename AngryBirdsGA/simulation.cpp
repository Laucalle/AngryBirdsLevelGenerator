#include "simulation.h"
#include <iostream>
#include <cstdio>
#include <vector>
#include "Box2D/Box2D.h"

std::vector<float> world_simulation(float* k, int block_data, int n_blocks)
{

	// Define the gravity vector.
	b2Vec2 gravity(0.0f, -4.905f);

	// Do we want to let bodies sleep?
	bool doSleep = true;

	// Construct a world object, which will hold and simulate the rigid bodies.
	b2World world(gravity, doSleep);

	// Define the ground body.
	// TODO: find correct ground position
	b2BodyDef groundBodyDef;
	groundBodyDef.position.Set(0.0f, -13.5f); 

	// Call the body factory which allocates memory for the ground body
	// from a pool and creates the ground box shape (also from a pool).
	// The body is also added to the world.
	b2Body* groundBody = world.CreateBody(&groundBodyDef);

	// Define the ground box shape.
	b2PolygonShape groundBox;

	// The extents are the half-widths of the box.
	groundBox.SetAsBox(50.0f, 10.0f);

	// Add the ground fixture to the ground body.
	groundBody->CreateFixture(&groundBox, 0.0f);


	// DYNAMICS /////////////////////////////////////////////////////////////
	std::vector<b2Body*> bodies_ref;
	std::vector<std::pair<float,float> > prev_positions;
	for (int i = 0; i < n_blocks; i++) {
		// Define properties

		// Define the dynamic body. We set its position and call the body factory.
		b2BodyDef bodyDef;
		bodyDef.type = b2_dynamicBody;
		bodyDef.position.Set(k[i*block_data], k[i*block_data+1]);
		prev_positions.push_back(std::pair<float,float>(k[i*block_data], k[i*block_data+1]));
		b2Body* body = world.CreateBody(&bodyDef);

		body->SetTransform(body->GetPosition(), k[i*block_data+4]*(b2_pi/180));

		// Define another box shape for our dynamic body.
		b2PolygonShape dynamicBox;
		//std::cerr << " " << k[i*block_data+2] << " " << k[i*block_data+3] << std::endl;
		dynamicBox.SetAsBox(k[i*block_data+2], k[i*block_data+3]);
		
		// Define the dynamic body fixture.
		b2FixtureDef fixtureDef;
		fixtureDef.shape = &dynamicBox;

		// Set the box density to be non-zero, so it will be dynamic.
		fixtureDef.density = 1.0f;

		// Override the default friction.
		fixtureDef.friction = k[i*block_data+5];

		// Add the shape to the body.
		body->CreateFixture(&fixtureDef);
		bodies_ref.push_back(body);


	}

//////////////////////////////////////7



	// Prepare for simulation. Typically we use a time step of 1/60 of a
	// second (60Hz) and 10 iterations. This provides a high quality simulation
	// in most game scenarios.
	float32 timeStep = 1.0f / 60.0f;
	int32 velocityIterations = 100;
	int32 positionIterations = 100;
	
	std::vector<float> body_instant_vel(bodies_ref.size());
	// This is our little game loop.
	int num_iter = 60;
	for (int32 i = 0; i < num_iter; ++i)
	{
		// Instruct the world to perform a single step of simulation.
		// It is generally best to keep the time step and iterations fixed.
		world.Step(timeStep, velocityIterations, positionIterations);

		// Clear applied body forces.
		world.ClearForces();

		// Now print the position and angle of the body.

		for (int j = 0;  j < bodies_ref.size(); j++){
			b2Vec2 position = bodies_ref[j]->GetPosition();
			float32 angle = bodies_ref[j]->GetAngle();
			//printf("Block %d: %4.2f %4.2f %4.2f\n", j, position.x, position.y, angle);
			if( i > 0 ){
				body_instant_vel[j]+= std::sqrt((position.x - prev_positions[j].first) * (position.x - prev_positions[j].first)
				                      + (position.y -prev_positions[j].second) * (position.y - prev_positions[j].second) ) / timeStep;
			}
			prev_positions[j].first = position.x;
			prev_positions[j].second = position.y;
		}
	}

	for (int j = 0;  j < body_instant_vel.size(); j++){
		body_instant_vel[j] /= num_iter; 
		std::cout << body_instant_vel[j] << std::endl;
	}

	return body_instant_vel;
	
	// When the world destructor is called, all bodies and joints are freed. This can
	// create orphaned pointers, so be careful about your world management.
}
