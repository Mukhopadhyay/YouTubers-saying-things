import warnings
from utils import utils

# Avoiding selenium warnings
warnings.filterwarnings('ignore')

# Calling the method
df = utils.get_channel_info('vsauce1', './chromedriver')

# Printing the dataframe
print(df)
