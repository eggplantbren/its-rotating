import numpy as np
import dnest4.builder as bd

# Load the data and put it in a dictionary
raw = np.loadtxt("gfl_new_data.txt")
data = { "x": raw[:,0],
         "y": raw[:,1],
         "r": raw[:,2],
         "theta": raw[:,3],
         "v": raw[:,4],
         "sig_v": raw[:,5],
         "N": raw.shape[0] }


# Polar coordinates
data["r"] = np.sqrt(data["x"]**2 + data["y"]**2)
data["theta"] = np.arctan2(data["y"], data["x"])

# Create the model
model = bd.Model()

# Constant velocity dispersion
model.add_node(bd.Node("velocity_dispersion",
                            bd.Uniform(0.0, 50)))

# Constant velocity offset
model.add_node(bd.Node("v_systematic",
                    bd.Uniform(-10.0, 10.0)))

# Rotation amplitude
model.add_node(bd.Node("A", bd.Uniform(0.0, 50.0)))

# Rotation angle
model.add_node(bd.Node("phi", bd.Uniform(0.0, 2.0*np.pi)))

# p(data | parameters)
for i in range(0, data["N"]):

    # 
    mean = "v_systematic + A*sin(theta{index} - phi)".format(index=i)

    # This will be a bit slow but it doesn't matter
    stdev = "sqrt(pow(sig_v{index}, 2) + pow(velocity_dispersion, 2))"\
                .format(index=i)

    name = "v{index}".format(index=i)
    model.add_node(bd.Node(name, bd.Normal(mean, stdev), observed=True))

# Create the C++ code
bd.generate_h(model, data)
bd.generate_cpp(model, data)

# Compile the C++ code so it's ready to go
import os
os.system("make")

