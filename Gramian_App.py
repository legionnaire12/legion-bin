import mysql.connector
from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='biosearc_test', password='D0f7znHyE8bsepB2',
                                 host='starbuck.asoshared.com',
                                 port='3306',
                                 database='biosearc_prices')
mycursor = cnx.cursor()

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField
from pyts.datasets import load_coffee

# Parameters
X, _, _, _ = load_coffee(return_X_y=True)

mycursor.execute("SELECT * FROM BTCTrainingNeutral")

myresult = mycursor.fetchall()
counter = 0
testlist2 = []

for tracker in myresult:
  counter += 1
  testlist = list(tracker[2:37]) #Strip index from what's taken from the database and convert it from a tuple to a list
  #if counter == 3: # Stops the loop after 3 iterations - FOR TESTING
  #  break
  for y in testlist: #Duplicates each of the terms in the list 8 times to fit the format of the GAD transform
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
    testlist2.append(y)
  
  Finallist = testlist2 + testlist[2:8] #The final version used for the GAD transform
  testlist2 =[]
  # Transform the time series into Gramian Angular Fields
  X[0] = Finallist 
  gasf = GramianAngularField(image_size=256, method='summation')
  X_gasf = gasf.fit_transform(X)
  gadf = GramianAngularField(image_size=256, method='difference')
  X_gadf = gadf.fit_transform(X)
  # Turn the Gramian Angular field into an image and then save it (currently using summation model)
  fig = plt.figure(figsize=(7, 7), frameon=False)
  grid = ImageGrid(fig, 111,
                 nrows_ncols=(1, 1),
                 axes_pad=0.15,
                 ngrids=None,
                 share_all=True,
                 label_mode="1",
                 )
  images = [X_gasf[0]]
  titles = ['']
  for image, title, ax in zip(images, titles, grid):
    im = ax.imshow(image, cmap='rainbow', origin='lower')
    ax.set_title(title, fontdict={'fontsize': 16})
    ax.axis('off')

  plt.tight_layout(pad=0)
  plt.show() 

#File saving code
  fig.savefig('/content/gdrive/My Drive/BTCdatasets/BTCTrainingNeutral/BTCTrainingNeutral' + str(counter) +'.png', dpi=fig.dpi)
