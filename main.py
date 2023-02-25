from res import params, visual
from tests import test_single as single
from tests import test_single_noise as noise

if __name__ == '__main__':
    # single.run_tests(phasespace=True, makegif=False)
    # noise.run_tests(phasespace=True, makegif=False)

    noise.phase_space = True
    noise.make_gif = False
    visual.show_xw = False
    visual.show_xyw = True

    # for sigma in [1e-3, 1e-5, 1e-7, 1e-9]:
    for sigma in [1e-150, 1e-250, 1e-300]:
        params.sigma = sigma
        noise.laser_off()
