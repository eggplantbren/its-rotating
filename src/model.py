import numpy as np
import dnest4.builder as bd

# Load the data and put it in a dictionary
raw = np.loadtxt("gfl_new_data.txt")
data = { "x": raw[:,0],
         "y": raw[:,1],
         "v": raw[:,2],
         "sig_v": raw[:,3],
         "N": raw.shape[0] }

# Create the model
model = bd.Model()

# Constant velocity dispersion
model.add_node(bd.Node("log_velocity_dispersion", bd.T(4.605, 2.0, 1.0)))
model.add_node(bd.Node("velocity_dispersion",
                            bd.Delta("exp(log_velocity_dispersion)")))

# Constant velocity offset
model.add_node(bd.Node("c", bd.T(0.0, 0.1, 1.0)))
model.add_node(bd.Node("mu_v", bd.Delta("c*velocity_dispersion")))

# p(data | parameters)
for i in range(0, data["N"]):
    # This will be a bit slow but it doesn't matter
    stdev = "sqrt(pow(sig_v{index}, 2) + pow(velocity_dispersion, 2))"\
                .format(index=i)

    name = "v{index}".format(index=i)
    model.add_node(bd.Node(name, bd.Normal("mu_v", stdev), observed=True))

# Create the C++ code
bd.generate_h(model, data)
bd.generate_cpp(model, data)

# Compile the C++ code so it's ready to go
import os
os.system("make")

