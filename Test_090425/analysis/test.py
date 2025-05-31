import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6, 6), constrained_layout=True)
fig.suptitle("VISIBLE TITLE", y=0.95, fontsize=20)
fig.text(0.5, 0.5, "Test plot", ha='center')
plt.show()
