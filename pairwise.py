import models.pip 
import adaptived.pairwiseiplot as adaptive


def main(p=100,ip=0.1,g=10):
    s = models.pip.model_pip(p,ip,g)
    adaptive.draw_array(s)
    return s

