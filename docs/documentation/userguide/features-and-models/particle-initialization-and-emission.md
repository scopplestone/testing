(sec:particle-initialization-and-emission)=
# Particle Initialization & Emission

The following section gives an overview of the available options regarding the definition of species and particle initialization
and emission. Simulation particles can be inserted initially within the computational domain and/or emitted at every time step.
First of all, the number of species is defined by

    Part-nSpecies=1
    Part-MaxParticleNumber=1000000

The maximum particle number is defined per core and should be chosen according to the number of simulation particles you expect,
including a margin to account for imbalances due transient flow features and/or the occurrence of new particles due to chemical
reactions. Example: A node of a HPC cluster has 2 CPUs, each has 12 cores. Thus, the node has 24 cores that share a total of
128GB RAM. Allocating 1000000 particles per core means, you can simulate up to 24 Million particles on a single node in this
example (assuming an even particle distribution). The limiting factor here is the amount of RAM available per node.

Regardless whether a standalone PIC, DSMC, or a coupled simulation is performed, the atomic mass [kg], the charge [C] and the
weighting factor $w$ [-] are required for each species.

    Part-Species1-MassIC=5.31352E-26
    Part-Species1-ChargeIC=0.0
    Part-Species1-MacroParticleFactor=5E2

Species that are not part of the initialization or emission but might occur as a result of e.g. chemical reactions should also be
defined with these parameters.

Due to the often repetitive definitions, the default value for a given parameter can be set using the wildcard `$`. Different
values for individual parameters can be specified by explicitly specifying the numbered parameter, irrespective of the ordering
in the parameter file.

    Part-Species1-Init1-VeloIC = 1.
    Part-Species$-Init$-VeloIC = 2.

Due to runtime considerations, the evaluation of the wildcard character is performed from left to right. Thus, a parameter like
`Part-Species1-Init$-VeloIC` will not work.

Different velocity distributions are available for the initialization/emission of particles.

| Distribution | Description                                             |
| ------------ | ------------------------------------------------------- |
| maxwell      | Maxwell-Boltzmann distribution                          |
| maxwell_lpn  | Maxwell-Boltzmann distribution for low particle numbers |
| WIP          | **WORK IN PROGRESS**                                    |

(sec:particle-insertion)=
## Initialization

At the beginning of a simulation, particles can be inserted using different initialization routines. Initialization regions are
defined per species and can overlap. First, the number of initialization conditions/regions has to be defined

    Part-Species1-nInits = 1

The type of the region is defined by the following parameter

    Part-Species1-Init1-SpaceIC = cell_local

Different `SpaceIC` are available and an overview is given in the table below.

|   Distribution  |                                    Description                                   |                   Reference                  |
| --------------- | -------------------------------------------------------------------------------- |  ------------------------------------------  |
|    cell_local   |         Particles are inserted in every cell at a constant number density        |                                              |
|       disc      |                     Particles are inserted on a circular disc                    |     Section {ref}`sec:particle-disk-init`    |
|     cylinder    | Particles are inserted in the given cylinder volume at a constant number density |   Section {ref}`sec:particle-cylinder-init`  |
| photon_cylinder |               Ionization of a background gas through photon impact               | Section {ref}`sec:particle-photo-ionization` |
|       WIP       |                               **WORK IN PROGRESS**                               |                                              |

Common parameters required for most of the insertion routines are given below. The drift velocity is defined by the direction
vector `VeloVecIC`, which is a unit vector, and a velocity magnitude [m/s]. The thermal velocity of particle is determined based
on the defined velocity distribution and the given translation temperature `MWTemperatureIC` [K]. Finally, the 'real' number
density is defined by `PartDensity` [1/m$^3$], from which the actual number of simulation particles will be determined (depending
on the chosen weighting factor).

    Part-Species1-Init1-VeloIC=1500
    Part-Species1-Init1-VeloVecIC=(/-1.0,0.0,0.0/)
    Part-Species1-Init1-velocityDistribution=maxwell_lpn
    Part-Species1-Init1-MWTemperatureIC=300.
    Part-Species1-Init1-PartDensity=1E20

In the case of molecules, the rotational and vibrational temperature [K] have to be defined. If electronic excitation is
considered, the electronic temperature [K] has to be defined

    Part-Species1-Init1-TempRot=300.
    Part-Species1-Init1-TempVib=300.
    Part-Species1-Init1-TempElec=300.

The parameters given so far are sufficient to define an initialization region for a molecular species using the `cell_local` option.
Additional options required for other insertion regions are described in the following.

(sec:particle-disk-init)=
### Circular Disc

To define the circular disc the following parameters are required:

    Part-Species1-Init1-SpaceIC               = disc
    Part-Species1-Init1-RadiusIC              = 1
    Part-Species1-Init1-BasePointIC           = (/ 0.0, 0.0, 0.0 /)
    Part-Species1-Init1-BaseVector1IC         = (/ 1.0, 0.0, 0.0 /)
    Part-Species1-Init1-BaseVector2IC         = (/ 0.0, 1.0, 0.0 /)
    Part-Species1-Init1-NormalIC              = (/ 0.0, 0.0, 1.0 /)

The first and second base vector span a plane, where a circle with the given radius will be defined at the base point.

(sec:particle-cylinder-init)=
### Cylinder

To define the cylinder the following parameters are required:

    Part-Species1-Init1-SpaceIC               = cylinder
    Part-Species1-Init1-RadiusIC              = 1
    Part-Species1-Init1-CylinderHeightIC      = 1
    Part-Species1-Init1-BasePointIC           = (/ 0.0, 0.0, 0.0 /)
    Part-Species1-Init1-BaseVector1IC         = (/ 1.0, 0.0, 0.0 /)
    Part-Species1-Init1-BaseVector2IC         = (/ 0.0, 1.0, 0.0 /)
    Part-Species1-Init1-NormalIC              = (/ 0.0, 0.0, 1.0 /)

The first and second base vector span a plane, where a circle with the given radius will be defined at the base point and then
extruded in the normal direction up to the cylinder height.

(sec:particle-photo-ionization)=
### Photo-ionization

A special case is the ionization of a background gas through photon impact, modelling a light pulse. The volume affected by the
light pulse is approximated by a cylinder, which is defined as described in Section {ref}`sec:particle-cylinder-init`. Additionally,
the SpaceIC has to be adapted and additional parameters are required:

    Part-Species1-Init1-SpaceIC                 = photon_cylinder
    Part-Species1-Init1-PulseDuration           = 1         ! [s]
    Part-Species1-Init1-WaistRadius             = 1E-6      ! [m]
    Part-Species1-Init1-WaveLength              = 1E-9      ! [m]
    Part-Species1-Init1-NbrOfPulses             = 1         ! [-], default = 1

The pulse duration and waist radius are utilized to define the spatial and temporal Gaussian profile of the intensity.
The number of pulses allows to consider multiple light pulses within a single simulation. To define the intensity of the light pulse,
either the average pulse power (energy of a single pulse times repetition rate), the pulse energy or the intensity amplitude have
to be provided.

    Part-Species1-Init1-Power                   = 1         ! [W]
    Part-Species1-Init1-RepetitionRate          = 1         ! [Hz]
    ! or
    Part-Species1-Init1-Energy                  = 1         ! [J]
    ! or
    Part-Species1-Init1-IntensityAmplitude      = 1         ! [W/m^2]

The intensity can be scaled with an additional factor to account for example for reflection or other effects:

    Part-Species1-Init1-EffectiveIntensityFactor    = 1         ! [-]

It should be noted that this initialization should be done with a particle species (i.e. not the background gas species) that is
also a product of the ionization reaction. The ionization reactions are defined as described in Section {ref}`sec:DSMC-chemistry` by

    DSMC-NumOfReactions = 1
    DSMC-Reaction1-ReactionType         = phIon
    DSMC-Reaction1-Reactants            = (/3,0,0/)
    DSMC-Reaction1-Products             = (/1,2,0/)
    DSMC-Reaction1-CrossSection         = 4.84E-24      ! [m^2]

The probability that an ionization event occurs is determined based on the given cross-section, which is usually given for a
certain wave length/photon energy. It should be noted that the background gas species should be given as the sole reactant and
electrons should be defined as the first and/or second product. Electrons will be emitted perpendicular to the light path defined
by the cylinder axis according to a cosine squared distribution.

Finally, the secondary electron emission through the impinging light pulse on a surface can also be modelled by an additional
insertion region (e.g. as an extra initialization for the same species). Additionally to the definition of the light pulse as
described above (pulse duration, waist radius, wave length, number of pulses, and power/energy/intensity), the following parameters
have to be set

    Part-Species1-Init2-SpaceIC               = photon_SEE_disc
    Part-Species1-Init2-velocityDistribution  = photon_SEE_energy
    Part-Species1-Init2-YieldSEE              = 0.1                 ! [-]
    Part-Species1-Init2-WorkFunctionSEE       = 2                   ! [eV]

The emission area is defined as a disc by the parameters introduced in Section {ref}`sec:particle-disk-init`. The yield controls
how many electrons are emitted per photon impact and their velocity distribution is defined by the work function. The scaling
factor defined by `EffectiveIntensityFactor` is not applied to this surface emission. Both emission regions can be sped-up if the
actual computational domain corresponds only to a quarter of the cylinder:

    Part-Species1-Init1-FirstQuadrantOnly       = T
    Part-Species1-Init2-FirstQuadrantOnly       = T

## Surface Flux

A surface flux enables the emission of particles at a boundary in order to simulate, e.g. a free-stream. They are defined
species-specifically and can overlap. First, the number of surface fluxes has to be given

    Part-Species1-nSurfaceFluxBCs=1

The surface flux is mapped to a certain boundary by giving its boundary number (e.g. `BC=1` corresponds to the previously defined
boundary `BC_OPEN`)

    Part-Species1-Surfaceflux1-BC=1

The remaining parameters such as flow velocity, temperature and number density are given analogously to the initial particle
insertion presented in Section {ref}`sec:particle-insertion`. An example to define the surface flux for a diatomic species is
given below

    Part-Species1-Surfaceflux1-VeloIC=1500
    Part-Species1-Surfaceflux1-VeloVecIC=(/-1.0,0.0,0.0/)
    Part-Species1-Surfaceflux1-velocityDistribution=maxwell_lpn
    Part-Species1-Surfaceflux1-MWTemperatureIC=300.
    Part-Species1-Surfaceflux1-PartDensity=1E20
    Part-Species1-Surfaceflux1-TempRot=300.
    Part-Species1-Surfaceflux1-TempVib=300.
    Part-Species1-Surfaceflux1-TempElec=300.

### Circular Inflow

The emission of particles from a surface flux can be limited to the area within a circle or a ring. The respective boundary has to
coincide or be parallel to the xy-, xz, or yz-planes. This allows to define inflow boundaries without specifically meshing the
geometrical feature, e.g. small orifices. The feature can be enabled per species and surface flux

    Part-Species1-Surfaceflux1-CircularInflow=TRUE

The normal direction of the respective boundary has to be defined by

    Part-Species1-Surfaceflux1-axialDir=1

Finally, the origin of the circle/ring on the surface and the radius have to be given. In the case of a ring, a maximal and minimal
radius is required (`-rmax` and `-rmin`, respectively), whereas for a circle only the input of maximal radius is sufficient.

    Part-Species1-Surfaceflux1-origin=(/5e-6,5e-6/)
    Part-Species1-Surfaceflux1-rmax=2.5e-6
    Part-Species1-Surfaceflux1-rmin=1e-6

The absolute coordinates are defined as follows for the respective normal direction.

| Normal Direction | Coordinates |
| :--------------: | :---------: |
|      x (=1)      |    (y,z)    |
|      y (=2)      |    (z,x)    |
|      z (=3)      |    (x,y)    |

Multiple circular inflows can be defined on a single boundary through multiple surface fluxes, e.g. to enable the simulation of
multiple inlets on a chamber wall.

### Adaptive Boundaries

Different adaptive boundaries can be defined as a part of a surface flux to model subsonic in- and outflows, where the emission is
adapted based on the prevalent conditions at the boundary. The modelling is based on the publications by {cite}`Farbar2014` and {cite}`Lei2017`.

    Part-Species1-Surfaceflux1-Adaptive=TRUE
    Part-Species1-Surfaceflux1-Adaptive-Type=1

An overview over the available types is given below.

 * `Type=1`: Constant static pressure and temperature inlet, defined as Type 1 in Ref. {cite}`Farbar2014`
 * `Type=2`: Constant static pressure outlet, defined as Type 1 in Ref. {cite}`Farbar2014`
 * `Type=3`: Constant mass flow and temperature inlet, where the given mass flow and sampled velocity are used to determine the
 number of particles for the surface flux. It requires the BC to be defined as `open`. Defined as Type 2 in Ref. {cite}`Farbar2014`
 * `Type=4`: Constant mass flow inlet and temperature inlet, where number of particles to be inserted is determined directly from
 the mass flow and the number of particles leaving the domain, $N_{\mathrm{in}}=N_{\dot{m}} + N_{\mathrm{out}}$. Defined as cf_3
 in Ref. {cite}`Lei2017`

Depending of the type of the chosen boundary type either the mass flow [kg/s] or the static pressure [Pa] have to be given

    Part-Species1-Surfaceflux1-Adaptive-Massflow=1.00E-14
    Part-Species1-Surfaceflux1-Adaptive-Pressure=10

The adaptive boundaries require the sampling of macroscopic properties such as flow velocity at the boundary. To compensate for
the statistical fluctuations, three possible sampling approaches are available. The first approach uses a relaxation factor
$f_{\mathrm{relax}}$, where the current value of the sampled variable $v^{n}$ is updated according to

$$v^{n}= (1-f_{\mathrm{relax}})\,v^{n-1} + f_{\mathrm{relax}} v^{\mathrm{samp}} $$

The relaxation factor $f_{\mathrm{relax}}$ is defined by

    AdaptiveBC-RelaxationFactor = 0.001

The second and third approach allows to sample over a certain number of iterations. If the truncated running average option is
enabled, the macroscopic properties will be continuously updated while the oldest sample will be replaced with the most recent.
If the truncated running average option is disabled, the macroscopic properties will be only updated every given number of
iterations, and the complete sample will be resetted afterwads. If a number of iterations is given, it will be used instead of
the first approach with the relaxation factor.

    AdaptiveBC-SamplingIteration      = 100
    AdaptiveBC-TruncateRunningAverage = T       ! DEFAULT: F

The adaptive particle emission can be combined with the circular inflow feature. In this context when the area of the actual
emission circle/ring is very small, it is preferable to utilize the `Type=4` constant mass flow condition. `Type=3` assumes an
open boundary and accounts for particles leaving the domain through that boundary already when determining the number of particles
to be inserted. As a result, this method tends to over predict the given mass flow, when the emission area is very small and large
sample size would be required to have enough particles that leave the domain through the emission area. For the `Type=4` method,
the actual number of particles leaving the domain through the circular inflow is counted and the mass flow adapted accordingly,
thus the correct mass flow can be reproduced.

Additionally, the `Type=4` method can be utilized in combination with a reflective boundary condition to model diffusion and
leakage (e.g. in vacuum tanks) based on a diffusion rate $Q$ [Pa m$^3$ s$^{-1}$]. The input mass flow [kg s$^{-1}$] for the
simulation is then determined by

$$\dot{m} = \frac{QM}{1000RT},$$

where $R=8.314$ J mol$^{-1}$K$^{-1}$ is the gas constant, $M$ the molar mass in [g mol$^{-1}$] and $T$ is the gas temperature [K].

To verify the resulting mass flow rate of an adaptive surface flux, the following option can be enabled

    CalcAdaptiveBCInfo = T

This will output a species-specific mass flow rate [kg s$^{-1}$] and the average pressure in the adjacent cells [Pa] for each
surface flux condition in the `PartAnalyze.csv`, which gives the current values for the time step. For the former, positive values
correspond to a net mass flux into the domain and negative values vice versa. It should be noted that while multiple adaptive
boundaries are possible, adjacent boundaries that share a mesh element should be avoided or treated carefully.

### Missing descriptions

ReduceNoise, DoForceFreeSurfaceFlux

DoPoissonRounding: {cite}`Tysanner2004`

AcceptReject, ARM_DmaxSampleN: {cite}`Garcia2006`

