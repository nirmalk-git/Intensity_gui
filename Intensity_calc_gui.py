import PySimpleGUI as sg
import astropy.constants as cc
import astropy.units as unit
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# calculate the energy of single photon
def Photon_energy(wave) -> object:
    # the unit is in joules.
    Ph_E = (cc.h * cc.c / wave).to(unit.J)
    # gives the photon energy in joules.
    return Ph_E


def calc_flux(wave, well, pixel_area, time):
    # convert the photon intensity into light flux.
    # unit will be nW/cm2
    photon_energy = Photon_energy(wave)
    flux = (photon_energy * (well / qe) / pixel_area / time).to(unit.W / (unit.cm * unit.cm))
    return flux


first_column = [
    [sg.Text("Some text on Row 1")],
    # wavelength
    [sg.Text("Enter the wavelength (nm)", ), sg.InputText(key='wave', size=(10, 0))],
    # for displaying the results.
    [sg.Text("Energy of one photon = "), sg.Text("", size=(10, 0), key="Ph_E")],
    [sg.Button("Calculate photon energy")],
    # QE at wavelength
    [sg.Text("Enter QE at input wavelength"), sg.InputText(key='qe', size=(10, 0))],
    # Pixel size
    [sg.Text("Enter the pixel size (microns)"), sg.InputText(key='pix_size', size=(10, 0))],
    # FWC at LG
    [sg.Text("Enter the LG FWC (e)"), sg.InputText(key='fwc_l', size=(10, 0))],
    # FWC at HG
    [sg.Text("Enter the HG FWC (e)"), sg.InputText(key='fwc_h', size=(10, 0))],
    # Exposure time
    [sg.Text("Enter the Exposure time (s)"), sg.InputText(key='time', size=(10, 0))],
    # for displaying the results.
    [sg.Text("Flux at saturation for LG"), sg.Text("", size=(10, 0), key="lg_flux")],
    # for displaying the results.
    [sg.Text("Flux at saturation for HG"), sg.Text("", size=(10, 0), key="hg_flux")],
    # Cancel and OK
    [sg.Button("Calculate flux")],
    # PTC measurement points
    [sg.Text("PTC measurement points"), sg.InputText(key='N', size=(10, 0))],
    [sg.Text("LG minimum flux = "), sg.Text("", size=(10, 0), key="lg_min_flux")],
    [sg.Text("HG minimum flux = "), sg.Text("", size=(10, 0), key="hg_min_flux")],
    [sg.Button("Calculate min flux")],
    [sg.Button("Cancel")],
]


second_column = [
    [sg.Text("Some text on Row 1")],
]

layout = [
    [sg.Column(first_column),
     sg.VSeperator(),
     sg.Column(second_column),]
]
# Create the Window
window = sg.Window("PTC intensity estimation", layout, margins=(100, 100))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break

    if event == 'Calculate photon energy':
        # wave
        wave = float(values['wave']) * unit.nm
        # Energy of one photon
        Ph_E = Photon_energy(wave)
        window['Ph_E'].update(value=Ph_E)

    if event == 'Calculate flux':
        # wave
        wave = float(values['wave']) * unit.nm
        # QE
        qe = values['qe']
        qe = float(qe)
        # time
        time = float(values['time']) * unit.s
        # fwc lg
        fwc_l = float(values['fwc_l'])
        # fwc hg
        fwc_h = float(values['fwc_h'])
        # Pixel size
        pix_size = float(values['pix_size']) * unit.micron
        phot_h = fwc_h / qe
        phot_l = fwc_l / qe
        # area of the pixel
        Pixel_area = pix_size * pix_size
        # saturation flux for low gain
        flux_l = calc_flux(wave, fwc_l, Pixel_area, time)
        # saturation flux for high gain
        flux_h = calc_flux(wave, fwc_h, Pixel_area, time)
        window['lg_flux'].update(value=flux_l)
        window['hg_flux'].update(value=flux_h)
    if event == 'Calculate min flux':
        N = float(values['N'])
        lg_min_flux = flux_l/N
        hg_min_flux = flux_h/N
        window['lg_min_flux'].update(value=lg_min_flux)
        window['hg_min_flux'].update(value=hg_min_flux)


window.close()
