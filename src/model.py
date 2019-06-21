import numpy as np
import dnest4.builder as bd

data = {"x": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        "y": np.array([-1.0, 2.0, -3.0, 3.9, 5.1]),
        "v": np.array([20.0, -40.0, 23.3, 39.2, -11.2]),
        "sig_v": np.array([1.0, 2.0, 0.5, 2.2, 1.2]),
        "N": 5}

# Create the model
model = bd.Model()

# Velocity dispersion
model.add_node(bd.Node("log_velocity_dispersion", bd.Normal(0.0, 10.0)))
model.add_node(bd.Node("velocity_dispersion",
                            bd.Delta("exp(log_velocity_dispersion)")))

# p(data | parameters)
for i in range(0, data["N"]):
    # This will be a bit slow but it doesn't matter
    stdev = "sqrt(pow(sig_v{index}, 2) + pow(velocity_dispersion, 2))"\
                .format(index=i)

    name = "v{index}".format(index=i)
    model.add_node(bd.Node(name, bd.Normal(0.0, stdev), observed=True))

# Create the C++ code
bd.generate_h(model, data)
bd.generate_cpp(model, data)

# Compile the C++ code so it's ready to go
import os
os.system("make")

