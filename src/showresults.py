import dnest4.classic as dn4
import matplotlib.pyplot as plt
import corner
dn4.postprocess()

# Fonts
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 14
plt.rc("text", usetex=True)
#plt.rcParams["axes.labelpad"] = 24

posterior_sample = dn4.my_loadtxt("posterior_sample.txt")
fig = corner.corner(posterior_sample,
              labels=["$\\Sigma$ (km/s)", "$v_{\\rm sys}$ (km/s)",
                        "$A$ (km/s)", "$\phi$"],
              plot_contours=False, plot_density=False,
              data_kwargs={"alpha": 0.15, "ms": 0.75},
              label_kwargs=dict(fontsize=18))
plt.savefig("corner_rotation_gfl_priors.png", dpi=300)
plt.show()

