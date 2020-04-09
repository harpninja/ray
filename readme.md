# Ray Tracer
A Python version of [Ray Tracing in One Weekend](https://github.com/RayTracing/raytracing.github.io)by Peter Shirley.
This code generates fewer spheres than the original.  This is noted in main.py.
A few points:
* I have followed the original C++ variable names and other things as much as possible.
* Albedo in the code is actually a colour, rather than a simple reflectance.
* Attenuation seems really superfluous to be passing around, until you get to Dielectric and realise it is actually intended for something.
* This took longer than one weekend.

### Run
python main.py
