import warnings
from utils import utils

warnings.filterwarnings('ignore')

df = utils.get_channel_info('vsauce1', './chromedriver')
print(df)
