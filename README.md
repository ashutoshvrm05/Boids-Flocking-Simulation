# Boids-Flocking-Simulation

# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

Download the Zip file or close the repo in your device. Next, run the boids.py file. 

```bash
python3 boids.py
```

## 🧠 What is the Boids Algorithm?

A Video Illustration 

https://github.com/user-attachments/assets/907bd06e-0dec-4185-bcde-5d508a327c92

Developed by Craig Reynolds in 1986, the Boids (bird-oid objects) algorithm simulates the complex, organic movement of flocks of birds, schools of fish, or herds of sheep.
Instead of scripting the path of the flock as a whole, the algorithm gives each individual boid a simple set of rules and a limited field of view (Visibility Radius). The lifelike, synchronized swarming behavior that you see on screen is not programmed directly; it is an emergent property that arises naturally from the boids reacting to their immediate neighbors.

The Core Rules:

Every frame, each boid calculates its next move based on three distinct steering forces:

  2. Separation: Steer to avoid crowding or colliding with local flockmates.

  3. Alignment: Steer towards the average heading and velocity of local flockmates.

  4. Cohesion: Steer towards the average position (center of mass) of local flockmates.


## 🎛️ Parameter Tweaking & Emergent Behavior

By adjusting the weight (strength) of these rules and the boid's visibility radius, the simulation can model entirely different types of animals.

  1. Visibility Radius: Determines how far a boid can "see." A small radius creates many fragmented, independent sub-flocks. A large radius creates one massive, highly synchronized super-flock.
  2. Separation: This parameter defines how scattered a boid wants to be within it's visibility radius. Increase this and the boids repel each other.
  3. Cohesion: Higher cohesion means a higher tendency to form closter. It's the tendency of a boid to move to the center of a cluster (central tendency).
  4. Alignment: This parameter tells the boid to align itself to the average direction of motion (velocity) of other boids within it's visibility radius. A higher parameter value will make the boids look like a marching group, all moving in the same direction.

Some interesting emergent behavirous at different parameter setting.

  1. The "Panic" Swarm: If you set Separation to maximum and Cohesion to minimum, the flock structure breaks down entirely. The boids act like a scattered school of fish evading a predator, constantly repelling each other and refusing to group up.
  2. The "Black Hole": If you set Cohesion to maximum and Separation to zero, the boids will aggressively cluster into a single, dense, overlapping dot, losing all organic structure.
  3. The "Marching Band": High Alignment with moderate Separation and Cohesion results in a rigid, highly uniform flock that moves in lockstep, similar to migrating birds.

```python
    NUM_OF_BOIDS = 500
    SEPARATION_WEIGHT = 10
    ALIGNMENT_WEIGHT = 12
    COHESION_WEIGHT = 0.1
    VISIBILITY_RADIUS = 20
```
  Play around, and change the simulation parameter to simulate different stalk behavior.

## 🛠️ Components & Tech Stack

  1. Language: Python.
  2. Graphics & Rendering: [pygame](https://www.pygame.org/) (handling the game loop, surface rotation, and screen rendering).
  3. Mathematics: Custom Vector class handling 2D vector addition, subtraction, scalar multiplication, normalization, and magnitude calculations.
  4. Physics Integration: [Euler Integration](https://en.wikipedia.org/wiki/Euler_method
) is used to continuously update the velocity and position of the boids based on the applied steering forces frame-by-frame.

## 📚 What I Learned

Building this simulation was a deep dive into physics programming, algorithm optimization, and software architecture. Key takeaways include:

  1. Algorithmic Optimization (Spatial Partitioning): A naive approach to finding nearest neighbors requires every boid to check its distance against every other boid, resulting in a time complexity of $O(N^2)$. By implementing a Spatial Grid (dividing the screen into localized cells), I optimized the neighbor-search logic to roughly $O(N)$, allowing the simulation to render hundreds of boids smoothly at 60 FPS.
  2. Object-Oriented Programming (OOP): Structuring the project cleanly using classes for the Boid, the SpatialGrid, and the Vector math, ensuring encapsulation and readable code.
  3. Applied Kinematics & Linear Algebra: Translating raw vector math into fluid on-screen movement. This included handling edge-cases like zero-division errors in vector normalization, applying continuous forces to velocity rather than static position, and implementing boundary avoidance steering to keep the flock contained organically.

## 💡 Inspiration and Links

Check out this ammazing video by [SmarterEveryDay](https://www.youtube.com/@smartereveryday) - [I Didn't know Birds use Math in Murmurations! - Smarter Every Day 234](https://www.youtube.com/watch?v=4LWmRuB-uNU)

From where i Learned Spacial Positioning         - [Neat AI does Spatial Hash Boids](https://youtu.be/i0OHeCj7SOw?si=UyjyTzWsg-OuUxR_)

