import corner
import dnest4.classic as dn4
import matplotlib.pyplot as plt
import numpy as np

dn4.postprocess()

# Fonts
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 14
plt.rc("text", usetex=True)

posterior_sample = dn4.my_loadtxt("posterior_sample.txt")


fig = corner.corner(posterior_sample,
              labels=["$\\Sigma$ (km/s)", "$v_{\\rm sys}$ (km/s)",
                        "$A$ (km/s)", "$\phi$ (rad.)"],
              plot_contours=False, plot_density=False,
              data_kwargs={"alpha": 0.15, "ms": 0.75},
              label_kwargs=dict(fontsize=18))
plt.savefig("corner_rotation_gfl_priors.png", dpi=300)
plt.show()

## Version for the BJB priors
#fig = corner.corner(posterior_sample[:, np.array([1, 3, 5, 6])],
#              labels=["$\\Sigma$ (km/s)", "$v_{\\rm sys}$ (km/s)",
#                        "$A$ (km/s)", "$\phi$ (rad.)"],
#              plot_contours=False, plot_density=False,
#              data_kwargs={"alpha": 0.15, "ms": 0.75},
#              label_kwargs=dict(fontsize=18))
#plt.savefig("corner_rotation_bjb_priors.png", dpi=300)
#plt.show()

