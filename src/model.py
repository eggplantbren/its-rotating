import numpy as np
import dnest4.builder as bd

# Load the data and put it in a dictionary
raw = np.loadtxt("gfl_new_data.txt")
data = { "x": raw[:,0],
         "y": raw[:,1],
         "v": raw[:,2],
         "sig_v": raw[:,3],
         "N": raw.shape[0] }

# Polar coordinates
data["r"] = np.sqrt(data["x"]**2 + data["y"]**2)
data["theta"] = np.arctan2(data["y"], data["x"])

# Create the model
model = bd.Model()

# Constant velocity dispersion
model.add_node(bd.Node("log_velocity_dispersion", bd.T(4.605, 2.0, 1.0)))
model.add_node(bd.Node("velocity_dispersion",
                            bd.Delta("exp(log_velocity_dispersion)")))

# Constant velocity offset
model.add_node(bd.Node("c_v_systematic", bd.T(0.0, 0.1, 1.0)))
model.add_node(bd.Node("v_systematic",
                    bd.Delta("c_v_systematic*velocity_dispersion")))

# Rotation amplitude
model.add_node(bd.Node("log_c_A", bd.T(-2.0, 1.0, 1.0)))
model.add_node(bd.Node("c_A", bd.Delta("exp(log_c_A)")))
model.add_node(bd.Node("A", bd.Delta("c_A*velocity_dispersion")))

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

