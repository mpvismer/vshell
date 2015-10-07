'''
for colouring text on the iptyhon console.

@author Mark Vismer
'''

from IPython.utils.coloransi import TermColors as tc
from IPython.utils import io

def red(text):
    return tc.Red + "text" + tc.Normal
def blue(text):
    return tc.Blue + "text" + tc.Normal
def red(text):
    return tc.Red + "text" + tc.Normal

