import ROOT as rt
import numpy as np
import pdg # the official PDG API

class DatabasePDG(rt.TDatabasePDG):
    """
    This class is basically a combination of ROOT's TDatabasePDG,
    and the official PDG API. Amazingly, I have found *both* to be
    incomplete; for example TDatabasePDG lacks particles such as
    f_0(500) (PDGID=9000221), but the official pdg API also has
    issues for uu_1 (PDGID=2203). Combining them hopefully mitigates
    this issue.
    """

    # This code is quite hacky! - Jan

    def __init__(self):
        super().__init__()
        self.pdg_api = pdg.connect()

    def GetParticle(self,pdg_id:int):

        particle_root = None # particle returned by TDatabasePDG
        particle_pdg = None # particle returned by official PDG API

        try:
            particle_root = super().GetParticle(pdg_id)
        except:
            pass

        try:
            particle_class = "" # "ParticleClass" like "meson" or "lepton", possibly leaving blank for now
            try:
                particle_class = particle_root.ParticleClass()
            except:
                pass

            particle_pdg_raw = self.pdg_api.get_particle_by_mcid(pdg_id)
            # convert this into a TParticlePDG -- we'll do an imperfect
            # conversion since there are certain fields we won't use.

            anti_particle = 0
            if('bar' in particle_pdg_raw.name):
                anti_particle = 1

            try:
                lifetime = particle_pdg_raw.lifetime
                is_stable = False
                if(lifetime is None):
                    is_stable = True
                elif(np.isinf(particle_pdg_raw.lifetime)):
                    is_stable = True
            except: # for particles like the f_0(500), we may trigger the except -- assume such particles are unstable. #NOTE: Therefore referencing this lifetime is not recommended!
                lifetime = 0.
                is_stable = False

            mass = 0.
            try:
                if(particle_pdg_raw.mass is not None):
                    mass = particle_pdg_raw.mass
            except:
                pass

            width = 0.
            try:
                if(particle_pdg_raw.width is not None):
                    width = particle_pdg_raw.width
            except:
                pass

            particle_pdg = rt.TParticlePDG(
                particle_pdg_raw.name,
                particle_pdg_raw.name,
                mass,
                is_stable,
                width,
                particle_pdg_raw.charge / 3., # TParticlePDG gives charge in units of \e|/3
                particle_class, # "ParticleClass" like "meson" or "lepton", leaving blank for now
                pdg_id,
                anti_particle,
                0
            )
        except:
            pass

        if(particle_pdg is not None):
            return particle_pdg
        return particle_root

    def GetCharge(self,pdg_id:int):
        """
        Simplified function for getting charge.
        In practice, using this is much faster than
        a full particle lookup using GetParticle()
        followed by a call to Charge().
        """
        try:
            particle = super().GetParticle(pdg_id)
            return particle.Charge()
        except:
            particle = self.pdg_api.get_particle_by_mcid(pdg_id)
            return particle.charge / 3. # division by 3 to match TDatabasePDG behaviour

######################################################################
# Some old code below, relatively clunky stuff for plotting information
# on particles and labeling them nicely. This should ultimately be
# updated or removed. -Jan
######################################################################
# Map PDG codes to particle names, with ROOT/Latex formatting.
pdg_names = {
    0 : 'None',
    1 : 'd',
    2 : 'u',
    3 : 's',
    4 : 'c',
    5 : 'b',
    6 : 't',
    -1 : '#bar{d}',
    -2 : '#bar{u}',
    -3 : '#bar{s}',
    -4 : '#bar{c}',
    -5 : '#bar{b}',
    -6 : '#bar{t}',
    11 : 'e^{-}',
    12 : '#nu_{e}',
    13 : '#mu^{-}',
    14 : '#nu_{#mu}',
    15 : '#tau^{-}',
    16 : '#tau_{e}',
    -11 : 'e^{+}',
    -12 : '#bar{#nu_{e}}',
    -13 : '#mu^{+}',
    -14 : '#bar{#nu_{#mu}}',
    -15 : '#tau^{+}',
    -16 : '#bar{#nu_{#tau}}',
    9 : 'g',
    21 : 'g',
    22 : '#gamma',
    23 : 'Z^{0}',
    24 : 'W^{+}',
    -24 : 'W^{-}',
    25 : 'h^{0}',
    111 : '#pi^{0}',
    211 : '#pi^{+}',
    -211 : '#pi^{-}',
    130 : 'K^{0}_{L}',
    310 : 'K^{0}_{S}',
    311 : 'K^{0}',
    321 : 'K^{+}',
    -321 : 'K^{-}',
    411 : 'D^{+}',
    -411 : 'D^{-}',
    421 : 'D^{0}',
    511 : 'B^{0}',
    521 : 'B^{+}',
    -521 : 'B^{-}',
    2212 : 'p',
    2112 : 'n',
    -2212: '#bar{p}',
    -2112: '#bar{n}'
}

# Map PDG codes to more convenient values, for plotting
pdg_plotcodes = {
    1 : 1,
    2 : 3,
    3 : 5,
    4 : 7,
    5 : 9,
    6 : 11,
    -1 : 2,
    -2 : 4,
    -3 : 6,
    -4 : 8,
    -5 : 10,
    -6 : 12,
    11 : 14,
    12 : 20,
    13 : 16,
    14 : 22,
    15 : 18,
    16 : 24,
    -11 : 15,
    -12 : 21,
    -13 : 17,
    -14 : 23,
    -15 : 19,
    -16 : 25,
    9 : 13,
    21 : 13,
    22 : 26,
    23 : 27,
    24 : 28,
    -24 : 29,
    25 : 30,
    111 : 31,
    211 : 32,
    -211 : 33,
    130 : 34,
    310 : 35,
    311 : 36,
    321 : 37,
    -321 : 38,
    411 : 39,
    -411 : 40,
    421 : 41,
    511 : 42,
    521 : 43,
    -521 : 44,
    2212 : 45,
    2112 : 46
}

def FillPdgHist(hist,codes):
    for code in codes:
        try: code = pdg_plotcodes[int(code)]
        except: code = -1
        hist.Fill(code)
    return