import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

fig, axs = plt.subplots(4, 4, figsize=(9, 9))

for i, df in enumerate(pd.read_csv('adv.csv', chunksize=10)):
    x, y = i//4, i%4
    axs[x, y].set_xticks([])
    axs[x, y].plot(df['avg']/df['n'])
    axs[x, y].plot(df['mine']/df['n'])
    # axs[x, y].plot(np.log1p(df['avg'] / df['n']))
    # axs[x, y].plot(np.log1p(df['mine'] / df['n']))
plt.show()