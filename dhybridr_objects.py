from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict, Any
import re

@dataclass
class NodeConf:
    node_number: Tuple[int, int] = field(default=(16, 16), metadata={"comment": "num of processes in each dimension"})

@dataclass
class Time:
    dt: float = field(default=0.002, metadata={"comment": "time step"})
    niter: int = field(default=250000, metadata={"comment": "number of iterations"})
    t0: float = field(default=0.0, metadata={"comment": "initial time"})
    stiter: int = field(default=0, metadata={"comment": "starting iteration number"})
    c: float = field(default=100.0, metadata={"comment": "speed of light"})

@dataclass
class GridSpace:
    ncells: Tuple[int, int] = field(default=(1024, 1024), metadata={"comment": "Grid size in number of cells in each dimension"})
    boxsize: Tuple[float, float] = field(default=(512.0, 512.0), metadata={"comment": "Simulation box size in normalized units"})
    bdtype: Tuple[str, str, str, str] = field(default=("per", "per", "per", "per"), metadata={"comment": "Boundary conditions for each dimension"})
    Te: float = field(default=1.0, metadata={"comment": "Electron temperature"})
    gamma: float = field(default=1.66667, metadata={"comment": "Adiabatic index"})

@dataclass
class GlobalOutput:
    dodump: bool = field(default=True, metadata={"comment": "if true -> do dump"})
    ndump: int = field(default=500, metadata={"comment": "num of iter between dumps"})
    B0: float = field(default=3.05191e-7, metadata={"comment": "B field normalization (T)"})
    n0: float = field(default=1e6, metadata={"comment": "density normalization (m-3)"})
    units: str = field(default="NORM", metadata={"comment": '"NORM" (normalized) or "IS" (int. sys.)'})

@dataclass
class Restart:
    do_restart: bool = field(default=False, metadata={"comment": "restarting previous simulation?"})
    save_restart: bool = field(default=True, metadata={"comment": "save restart info on disk?"})
    restart_step: int = field(default=5000, metadata={"comment": "num of iter between restart info dumps"})

@dataclass
class ExtEmf:
    Bx: str = field(default="0.", metadata={"comment": "External Bx field"})
    By: str = field(default="0.", metadata={"comment": "External By field"})
    Bz: str = field(default="0.", metadata={"comment": "External Bz field"})
    Ex: str = field(default="0", metadata={"comment": "External Ex field"})
    Ey: str = field(default="0", metadata={"comment": "External Ey field"})
    Ez: str = field(default="0", metadata={"comment": "External Ez field"})
    input_name: str = field(default="./input/Bfld_init.unf", metadata={"comment": "Input file name for external EM field"})
    n_constants: int = field(default=6, metadata={"comment": "Number of constants"})
    ct: Tuple[float, float, float, float, float, float] = field(default=(1., 0., 425., 200., 1., 0.3), metadata={"comment": "Background magnetic field parameters"})

@dataclass
class FieldDiag:
    dmp_efld: Tuple[bool, bool, bool, bool] = field(default=(False, False, True, True), metadata={"comment": "Dump electric field components"})
    dmp_bfld: Tuple[bool, bool, bool, bool] = field(default=(False, False, True, True), metadata={"comment": "Dump magnetic field components"})
    dmp_jfld: Tuple[bool, bool] = field(default=(False, False), metadata={"comment": "Dump current field components"})

@dataclass
class Algorithm:
    ifsmooth: bool = field(default=True, metadata={"comment": "Smooth fields? default = true"})
    ifsmoothextfields: bool = field(default=True, metadata={"comment": "Smooth external fields? default = true"})
    filternpass: int = field(default=8, metadata={"comment": "Number of filter passes"})
    compensate: bool = field(default=True, metadata={"comment": "Use compensator in filter? default = true"})
    subniter: int = field(default=8, metadata={"comment": "Number of subiterations"})
    allowederror: float = field(default=1.0, metadata={"comment": "Allowed error in subiteration field calculation"})

@dataclass
class LoadBalance:
    loadbalance: bool = field(default=False, metadata={"comment": "Do any load balance? default= true"})
    ifdynamicloadbalance: bool = field(default=False, metadata={"comment": "Do dynamic load balance? default = true"})
    dynamicloadbalancestep: int = field(default=500, metadata={"comment": "Number of iterations between dynamic load balance"})

@dataclass
class Particles:
    num_species: int = field(default=1, metadata={"comment": "Number of species"})
    part_sort_step: int = field(default=25, metadata={"comment": "Number of steps between sorting"})

@dataclass
class Species:
    name: str = field(default="H+", metadata={"comment": "Species name"})
    dist: str = field(default="THERMAL", metadata={"comment": "Type of velocity distribution (THERMAL or ISO)"})
    num_par: Tuple[int, int] = field(default=(10, 10), metadata={"comment": "Number of particles per cell"})
    spare_size: float = field(default=0.1, metadata={"comment": "% (0 to 1) of unused space in part vector"})
    ir: int = field(default=1, metadata={"comment": "Ionization ratio"})
    rqm: float = field(default=1.0, metadata={"comment": "Charge to mass ratio (inverse)"})
    vdrift: Tuple[float, float, float] = field(default=(0.0, 0.0, 0.0), metadata={"comment": "Drift velocity"})
    vth: float = field(default=0.1, metadata={"comment": "Thermal velocity"})
    kin_push: bool = field(default=True, metadata={"comment": "True -> kinetic push, false -> MHD"})
    ion_t: float = field(default=8.0, metadata={"comment": "Ionization time"})
    nsp: str = field(default="1.", metadata={"comment": "Species number density"})
    input_name: str = field(default="./input/vfld_init.unf", metadata={"comment": "Input file name for velocity field"})
    n_constants: int = field(default=5, metadata={"comment": "Number of constants in density definition"})
    ct: Tuple[float, float, float, float, float] = field(default=(1., 200., 1., 0.1, 0.1), metadata={"comment": "Density parameters"})
    follow: bool = field(default=True, metadata={"comment": "Follow particles? default=false"})

@dataclass
class BoundaryConditions:
    bdtype: Tuple[str, str, str, str] = field(default=("per", "per", "per", "per"), metadata={"comment": "Boundary conditions for each wall"})
    vth: float = field(default=0.0, metadata={"comment": "Thermal bath velocity (ignored for others)"})

@dataclass
class DiagSpecies:
    dmp_vfld: Tuple[bool, bool] = field(default=(False, True), metadata={"comment": "Dump velocity field"})
    dmp_pfld: Tuple[bool, bool] = field(default=(False, True), metadata={"comment": "Dump pressure field"})
    phasespaces: List[str] = field(default_factory=lambda: ["x3x2x1", "p1x1", "Etx1", "p2x1", "p3x1"], metadata={"comment": "Phase spaces to dump"})
    pres: Tuple[int, int, int] = field(default=(512, 512, 512), metadata={"comment": "Resolution for phase space (defaults to 512)"})
    xres: Tuple[int, int] = field(default=(256, 256), metadata={"comment": "Resolution for x space"})

@dataclass
class RawDiag:
    raw_dump: bool = field(default=False, metadata={"comment": "Turn on or off raw dumps"})
    raw_ndump: int = field(default=1000, metadata={"comment": "Number of iterations between raw dumps"})
    raw_dump_fraction: float = field(default=1.0, metadata={"comment": "Fraction of raw dumps"})
    v_min: float = field(default=80.0, metadata={"comment": "Minimum velocity for raw dumps"})

@dataclass
class TrackDiag:
    track_dump: bool = field(default=False, metadata={"comment": "Turn on or off track dumps (if on, follow=true)"})
    track_fields: bool = field(default=True, metadata={"comment": "Track fields in particle positions"})
    track_ndump: int = field(default=1000, metadata={"comment": "Number of iterations between track dumps"})
    track_nstore: int = field(default=5, metadata={"comment": "Values are stored every iteration if =1, every other iter if =2, etc"})
    track_info_file: str = field(default="./input/H+.tags", metadata={"comment": "Track information (particle tags to track)"})

@dataclass
class DiagSpeciesTotal:
    dmp_vfld: Tuple[bool, bool] = field(default=(False, False), metadata={"comment": "Dump total velocity field"})
    pres: Tuple[int, int, int] = field(default=(512, 512, 512), metadata={"comment": "Resolution for total phase space (defaults to 512)"})

@dataclass
class DHybridInput:
    node_conf: NodeConf = field(default_factory=NodeConf)
    time: Time = field(default_factory=Time)
    grid_space: GridSpace = field(default_factory=GridSpace)
    global_output: GlobalOutput = field(default_factory=GlobalOutput)
    restart: Restart = field(default_factory=Restart)
    ext_emf: ExtEmf = field(default_factory=ExtEmf)
    field_diag: FieldDiag = field(default_factory=FieldDiag)
    algorithm: Algorithm = field(default_factory=Algorithm)
    loadbalance: LoadBalance = field(default_factory=LoadBalance)
    particles: Particles = field(default_factory=Particles)
    species: Species = field(default_factory=Species)
    boundary_conditions: BoundaryConditions = field(default_factory=BoundaryConditions)
    diag_species: DiagSpecies = field(default_factory=DiagSpecies)
    raw_diag: RawDiag = field(default_factory=RawDiag)
    track_diag: TrackDiag = field(default_factory=TrackDiag)
    diag_species_total: DiagSpeciesTotal = field(default_factory=DiagSpeciesTotal)

    def to_file(self, filename: str):
        with open(filename, 'w') as file:
            file.write(f"! dHybrid input file v 2.2\n! Created for Keyan Gootkin's pysim module\n")
            for section_name, section in asdict(self).items():
                section_meta = getattr(self, section_name).__dataclass_fields__
                file.write(f"!---------- {section_name.replace('_', ' ')} ----------\n")
                file.write(f"{section_name}\n{{\n")
                for key, value in section.items():
                    if isinstance(value, tuple) or isinstance(value, list):
                        value = ','.join(map(str, value))
                    comment = section_meta[key].metadata.get("comment", "")
                    file.write(f"    {key}={value}, {'!' + comment if comment else ''}\n")
                file.write(f"}}\n")

    @staticmethod
    def from_file(filename: str):
        def parse_value(value):
            if ',' in value:
                value = value.split(',')
                if all(re.match(r'^-?\d+$', v) for v in value):
                    return tuple(map(int, value))
                elif all(re.match(r'^-?\d+(\.\d+)?$', v) for v in value):
                    return tuple(map(float, value))
                else:
                    return tuple(value)
            if value in ['.true.', '.false.']:
                return value == '.true.'
            if re.match(r'^-?\d+$', value):
                return int(value)
            if re.match(r'^-?\d+(\.\d+)?$', value):
                return float(value)
            return value.strip('"')

        sections = {}
        current_section = None

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('!') or not line:
                    continue
                if line.endswith('{'):
                    current_section = line[:-1].strip()
                    sections[current_section] = {}
                elif line.endswith('}'):
                    current_section = None
                elif current_section:
                    key, value = map(str.strip, line.rstrip(',').split('='))
                    sections[current_section][key] = parse_value(value)

        return DHybridInput(
            node_conf=NodeConf(**sections.get('node_conf', {})),
            time=Time(**sections.get('time', {})),
            grid_space=GridSpace(**sections.get('grid_space', {})),
            global_output=GlobalOutput(**sections.get('global_output', {})),
            restart=Restart(**sections.get('restart', {})),
            ext_emf=ExtEmf(**sections.get('ext_emf', {})),
            field_diag=FieldDiag(**sections.get('field_diag', {})),
            algorithm=Algorithm(**sections.get('algorithm', {})),
            loadbalance=LoadBalance(**sections.get('loadbalance', {})),
            particles=Particles(**sections.get('particles', {})),
            species=Species(**sections.get('species', {})),
            boundary_conditions=BoundaryConditions(**sections.get('boundary_conditions', {})),
            diag_species=DiagSpecies(**sections.get('diag_species', {})),
            raw_diag=RawDiag(**sections.get('raw_diag', {})),
            track_diag=TrackDiag(**sections.get('track_diag', {})),
            diag_species_total=DiagSpeciesTotal(**sections.get('diag_species_total', {})),
        )

if __name__ == "__main__":
    # Create an instance from the input file
    input_data = DHybridInput.from_file('./templates/dHybridR/input/input')
    print("Loaded data from input file:")
    print(input_data)

    # Output the data back to a file
    output_filename = 'output'
    input_data.to_file(output_filename)
    print(f"Data has been written to {output_filename}")
