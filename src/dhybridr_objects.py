from dataclasses import dataclass, field, asdict
from typing import List, Tuple
import re

from utils import to_f_double as tfd
from utils import quote_string as qs
from utils import to_f_bool as tfb

@dataclass
class NodeConf:
    node_number: Tuple[int, ...] = field(default=(16, 16), metadata={"comment": "num of processes in each dimension"})

    def __str__(self) -> str:
        node_number_str = f"node_number(1:{len(self.node_number)})={self.node_number[0]},{self.node_number[1]}"
        return f"node_conf\n{{\n        {node_number_str},                ! {self.__dataclass_fields__['node_number'].metadata['comment']}\n}}"

@dataclass
class Time:
    dt: float = field(default=0.002, metadata={"comment": "time step"})
    niter: int = field(default=250000, metadata={"comment": "number of iterations"})
    t0: float = field(default=0.0, metadata={"comment": "initial time"})
    stiter: int = field(default=0, metadata={"comment": "starting iteration number"})
    c: float = field(default=100.0, metadata={"comment": "speed of light"})

    def __str__(self) -> str:
        return (
            f"time\n{{\n"
            f"        dt={tfd(self.dt)},                ! {self.__dataclass_fields__['dt'].metadata['comment']}\n"
            f"        niter={self.niter},                ! {self.__dataclass_fields__['niter'].metadata['comment']}\n"
            f"        t0={tfd(self.t0)},                ! {self.__dataclass_fields__['t0'].metadata['comment']}\n"
            f"        stiter={self.stiter},                ! {self.__dataclass_fields__['stiter'].metadata['comment']}\n"
            f"        c={tfd(self.c)},                ! {self.__dataclass_fields__['c'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class GridSpace:
    ncells: Tuple[int, ...] = field(default=(1024, 1024), metadata={"comment": "Grid size in number of cells in each dimension"})
    boxsize: Tuple[float, ...] = field(default=(512.0, 512.0), metadata={"comment": "Simulation box size in normalized units"})
    bdtype: Tuple[str, ...] = field(default=("per", "per", "per", "per"), metadata={"comment": "Boundary conditions for each dimension"})
    Te: float = field(default=1.0, metadata={"comment": "Electron temperature"})
    gamma: float = field(default=1.66667, metadata={"comment": "Adiabatic index"})

    def __str__(self) -> str:
        return (
            f"grid_space\n{{\n"
            f"        ncells(1:{len(self.ncells)})={','.join(map(str, self.ncells))},              ! {self.__dataclass_fields__['ncells'].metadata['comment']}\n"
            f"        boxsize(1:{len(self.boxsize)})={','.join(map(tfd, self.boxsize))},               ! {self.__dataclass_fields__['boxsize'].metadata['comment']}\n"
            f'        bdtype={','.join(map(qs, self.bdtype))},               ! {self.__dataclass_fields__['bdtype'].metadata['comment']}\n'
            f"        Te={tfd(self.Te)},                ! {self.__dataclass_fields__['Te'].metadata['comment']}\n"
            f"        gamma={tfd(self.gamma)},                ! {self.__dataclass_fields__['gamma'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class GlobalOutput:
    dodump: bool = field(default=True, metadata={"comment": "if true -> do dump"})
    ndump: int = field(default=500, metadata={"comment": "num of iter between dumps"})
    B0: float = field(default=3.05191e-7, metadata={"comment": "B field normalization (T)"})
    n0: float = field(default=1e6, metadata={"comment": "density normalization (m-3)"})
    units: str = field(default="NORM", metadata={"comment": '"NORM" (normalized) or "IS" (int. sys.)'})

    def __str__(self) -> str:
        return (
            f"global_output\n{{\n"
            f"        dodump={tfb(self.dodump)},                ! {self.__dataclass_fields__['dodump'].metadata['comment']}\n"
            f"        ndump={self.ndump},                ! {self.__dataclass_fields__['ndump'].metadata['comment']}\n"
            f"        B0={tfd(self.B0)},                ! {self.__dataclass_fields__['B0'].metadata['comment']}\n"
            f"        n0={tfd(self.n0)},                ! {self.__dataclass_fields__['n0'].metadata['comment']}\n"
            f'        units={qs(self.units)},                ! {self.__dataclass_fields__['units'].metadata['comment']}\n'
            f"}}"
        )

@dataclass
class Restart:
    do_restart: bool = field(default=False, metadata={"comment": "restarting previous simulation?"})
    save_restart: bool = field(default=True, metadata={"comment": "save restart info on disk?"})
    restart_step: int = field(default=5000, metadata={"comment": "num of iter between restart info dumps"})

    def __str__(self) -> str:
        return (
            f"restart\n{{\n"
            f"        do_restart={tfb(self.do_restart)},                ! {self.__dataclass_fields__['do_restart'].metadata['comment']}\n"
            f"        save_restart={tfb(self.save_restart)},                ! {self.__dataclass_fields__['save_restart'].metadata['comment']}\n"
            f"        restart_step={self.restart_step},                ! {self.__dataclass_fields__['restart_step'].metadata['comment']}\n"
            f"}}"
        )

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
    ct: Tuple[float, ...] = field(default=(1., 0., 425., 200., 1., 0.3), metadata={"comment": "Background magnetic field parameters"})

    def __str__(self) -> str:
        return (
            f"ext_emf\n{{\n"
            f"        Bx={qs(self.Bx)},                ! {self.__dataclass_fields__['Bx'].metadata['comment']}\n"
            f"        By={qs(self.By)},                ! {self.__dataclass_fields__['By'].metadata['comment']}\n"
            f"        Bz={qs(self.Bz)},                ! {self.__dataclass_fields__['Bz'].metadata['comment']}\n"
            f"        Ex={qs(self.Ex)},                ! {self.__dataclass_fields__['Ex'].metadata['comment']}\n"
            f"        Ey={qs(self.Ey)},                ! {self.__dataclass_fields__['Ey'].metadata['comment']}\n"
            f"        Ez={qs(self.Ez)},                ! {self.__dataclass_fields__['Ez'].metadata['comment']}\n"
            f"        input_name={qs(self.input_name)},                ! {self.__dataclass_fields__['input_name'].metadata['comment']}\n"
            f"        n_constants={self.n_constants},                ! {self.__dataclass_fields__['n_constants'].metadata['comment']}\n"
            f"        ct(1:{len(self.ct)})={','.join(map(tfd, self.ct))},                ! {self.__dataclass_fields__['ct'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class FieldDiag:
    dmp_efld: Tuple[bool, ...] = field(default=(False, False, True, True), metadata={"comment": "Dump electric field components"})
    dmp_bfld: Tuple[bool, ...] = field(default=(False, False, True, True), metadata={"comment": "Dump magnetic field components"})
    dmp_jfld: Tuple[bool, ...] = field(default=(False, False), metadata={"comment": "Dump current field components"})

    def __str__(self) -> str:
        return (
            f"field_diag\n{{\n"
            f"        dmp_efld(1:{len(self.dmp_efld)})={','.join(map(tfb, self.dmp_efld))},                ! {self.__dataclass_fields__['dmp_efld'].metadata['comment']}\n"
            f"        dmp_bfld(1:{len(self.dmp_bfld)})={','.join(map(tfb, self.dmp_bfld))},                ! {self.__dataclass_fields__['dmp_bfld'].metadata['comment']}\n"
            f"        dmp_jfld(1:{len(self.dmp_jfld)})={','.join(map(tfb, self.dmp_jfld))},                ! {self.__dataclass_fields__['dmp_jfld'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class Algorithm:
    ifsmooth: bool = field(default=True, metadata={"comment": "Smooth fields? default = true"})
    ifsmoothextfields: bool = field(default=True, metadata={"comment": "Smooth external fields? default = true"})
    filternpass: int = field(default=8, metadata={"comment": "Number of filter passes"})
    compensate: bool = field(default=True, metadata={"comment": "Use compensator in filter? default = true"})
    subniter: int = field(default=8, metadata={"comment": "Number of subiterations"})
    allowederror: float = field(default=1.0, metadata={"comment": "Allowed error in subiteration field calculation"})

    def __str__(self) -> str:
        return (
            f"algorithm\n{{\n"
            f"        ifsmooth={tfb(self.ifsmooth)},                ! {self.__dataclass_fields__['ifsmooth'].metadata['comment']}\n"
            f"        ifsmoothextfields={tfb(self.ifsmoothextfields)},                ! {self.__dataclass_fields__['ifsmoothextfields'].metadata['comment']}\n"
            f"        filternpass={self.filternpass},                ! {self.__dataclass_fields__['filternpass'].metadata['comment']}\n"
            f"        compensate={tfb(self.compensate)},                ! {self.__dataclass_fields__['compensate'].metadata['comment']}\n"
            f"        subniter={self.subniter},                ! {self.__dataclass_fields__['subniter'].metadata['comment']}\n"
            f"        allowederror={tfd(self.allowederror)},                ! {self.__dataclass_fields__['allowederror'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class LoadBalance:
    loadbalance: bool = field(default=False, metadata={"comment": "Do any load balance? default= true"})
    ifdynamicloadbalance: bool = field(default=False, metadata={"comment": "Do dynamic load balance? default = true"})
    dynamicloadbalancestep: int = field(default=500, metadata={"comment": "Number of iterations between dynamic load balance"})

    def __str__(self) -> str:
        return (
            f"loadbalance\n{{\n"
            f"        loadbalance={tfb(self.loadbalance)},                ! {self.__dataclass_fields__['loadbalance'].metadata['comment']}\n"
            f"        ifdynamicloadbalance={tfb(self.ifdynamicloadbalance)},                ! {self.__dataclass_fields__['ifdynamicloadbalance'].metadata['comment']}\n"
            f"        dynamicloadbalancestep={self.dynamicloadbalancestep},                ! {self.__dataclass_fields__['dynamicloadbalancestep'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class Particles:
    num_species: int = field(default=1, metadata={"comment": "Number of species"})
    part_sort_step: int = field(default=25, metadata={"comment": "Number of steps between sorting"})

    def __str__(self) -> str:
        return (
            f"particles\n{{\n"
            f"        num_species={self.num_species},                ! {self.__dataclass_fields__['num_species'].metadata['comment']}\n"
            f"        part_sort_step={self.part_sort_step},                ! {self.__dataclass_fields__['part_sort_step'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class Species:
    name: str = field(default="H+", metadata={"comment": "Species name"})
    dist: str = field(default="THERMAL", metadata={"comment": "Type of velocity distribution (THERMAL or ISO)"})
    num_par: Tuple[int, ...] = field(default=(10, 10), metadata={"comment": "Number of particles per cell"})
    spare_size: float = field(default=0.1, metadata={"comment": "% (0 to 1) of unused space in part vector"})
    ir: int = field(default=1, metadata={"comment": "Ionization ratio"})
    rqm: float = field(default=1.0, metadata={"comment": "Charge to mass ratio (inverse)"})
    vdrift: Tuple[float, ... ] = field(default=(0.0, 0.0, 0.0), metadata={"comment": "Drift velocity"})
    vth: float = field(default=0.1, metadata={"comment": "Thermal velocity"})
    kin_push: bool = field(default=True, metadata={"comment": "True -> kinetic push, false -> MHD"})
    ion_t: float = field(default=8.0, metadata={"comment": "Ionization time"})
    nsp: str = field(default="1.", metadata={"comment": "Species number density"})
    input_name: str = field(default="./input/vfld_init.unf", metadata={"comment": "Input file name for velocity field"})
    n_constants: int = field(default=5, metadata={"comment": "Number of constants in density definition"})
    ct: Tuple[float, ... ] = field(default=(1., 200., 1., 0.1, 0.1), metadata={"comment": "Density parameters"})
    follow: bool = field(default=True, metadata={"comment": "Follow particles? default=false"})

    def __str__(self) -> str:
        return (
            f"species\n{{\n"
            f"        name={qs(self.name)},                ! {self.__dataclass_fields__['name'].metadata['comment']}\n"
            f"        dist={qs(self.dist)},                ! {self.__dataclass_fields__['dist'].metadata['comment']}\n"
            f"        num_par(1:{len(self.num_par)})={','.join(map(tfd, self.num_par))},                ! {self.__dataclass_fields__['num_par'].metadata['comment']}\n"
            f"        spare_size={tfd(self.spare_size)},                ! {self.__dataclass_fields__['spare_size'].metadata['comment']}\n"
            f"        ir={self.ir},                ! {self.__dataclass_fields__['ir'].metadata['comment']}\n"
            f"        rqm={tfd(self.rqm)},                ! {self.__dataclass_fields__['rqm'].metadata['comment']}\n"
            f"        vdrift(1:{len(self.vdrift)})={','.join(map(tfd, self.vdrift))},                ! {self.__dataclass_fields__['vdrift'].metadata['comment']}\n"
            f"        vth={tfd(self.vth)},                ! {self.__dataclass_fields__['vth'].metadata['comment']}\n"
            f"        kin_push={tfb(self.kin_push)},                ! {self.__dataclass_fields__['kin_push'].metadata['comment']}\n"
            f"        ion_t={tfd(self.ion_t)},                ! {self.__dataclass_fields__['ion_t'].metadata['comment']}\n"
            f"        nsp={qs(self.nsp)},                ! {self.__dataclass_fields__['nsp'].metadata['comment']}\n"
            f"        input_name={qs(self.input_name)},                ! {self.__dataclass_fields__['input_name'].metadata['comment']}\n"
            f"        n_constants={self.n_constants},                ! {self.__dataclass_fields__['n_constants'].metadata['comment']}\n"
            f"        ct(1:{len(self.ct)})={','.join(map(str, self.ct))},                ! {self.__dataclass_fields__['ct'].metadata['comment']}\n"
            f"        follow={tfb(self.follow)},                ! {self.__dataclass_fields__['follow'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class BoundaryConditions:
    bdtype: Tuple[str, ... ] = field(default=("per", "per", "per", "per"), metadata={"comment": "Boundary conditions for each wall"})
    vth: float = field(default=0.0, metadata={"comment": "Thermal bath velocity (ignored for others)"})

    def __str__(self) -> str:
        return (
            f"boundary_conditions\n{{\n"
            f"        bdtype={','.join(map(qs, self.bdtype))},                ! {self.__dataclass_fields__['bdtype'].metadata['comment']}\n"
            f"        vth={tfd(self.vth)},                ! {self.__dataclass_fields__['vth'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class DiagSpecies:
    dmp_vfld: Tuple[bool, ... ] = field(default=(False, True), metadata={"comment": "Dump velocity field"})
    dmp_pfld: Tuple[bool, ... ] = field(default=(False, True), metadata={"comment": "Dump pressure field"})
    phasespaces: List[str] = field(default_factory=lambda: ["x3x2x1", "p1x1", "Etx1", "p2x1", "p3x1"], metadata={"comment": "Phase spaces to dump"})
    pres: Tuple[int, ... ] = field(default=(512, 512, 512), metadata={"comment": "Resolution for phase space (defaults to 512)"})
    xres: Tuple[int, ... ] = field(default=(256, 256), metadata={"comment": "Resolution for x space"})

    def __str__(self) -> str:
        return (
            f"diag_species\n{{\n"
            f"        dmp_vfld(1:{len(self.dmp_vfld)})={','.join(map(tfb, self.dmp_vfld))},                ! {self.__dataclass_fields__['dmp_vfld'].metadata['comment']}\n"
            f"        dmp_pfld(1:{len(self.dmp_pfld)})={','.join(map(tfb, self.dmp_pfld))},                ! {self.__dataclass_fields__['dmp_pfld'].metadata['comment']}\n"
            f"        phasespaces={','.join(map(qs,self.phasespaces))},                ! {self.__dataclass_fields__['phasespaces'].metadata['comment']}\n"
            f"        pres(1:{len(self.pres)})={','.join(map(str, self.pres))},                ! {self.__dataclass_fields__['pres'].metadata['comment']}\n"
            f"        xres(1:{len(self.xres)})={','.join(map(str, self.xres))},                ! {self.__dataclass_fields__['xres'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class RawDiag:
    raw_dump: bool = field(default=False, metadata={"comment": "Turn on or off raw dumps"})
    raw_ndump: int = field(default=1000, metadata={"comment": "Number of iterations between raw dumps"})
    raw_dump_fraction: float = field(default=1.0, metadata={"comment": "Fraction of raw dumps"})
    v_min: float = field(default=80.0, metadata={"comment": "Minimum velocity for raw dumps"})

    def __str__(self) -> str:
        return (
            f"raw_diag\n{{\n"
            f"        raw_dump={tfb(self.raw_dump)},                ! {self.__dataclass_fields__['raw_dump'].metadata['comment']}\n"
            f"        raw_ndump={self.raw_ndump},                ! {self.__dataclass_fields__['raw_ndump'].metadata['comment']}\n"
            f"        raw_dump_fraction={tfd(self.raw_dump_fraction)},                ! {self.__dataclass_fields__['raw_dump_fraction'].metadata['comment']}\n"
            f"        v_min={tfd(self.v_min)},                ! {self.__dataclass_fields__['v_min'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class TrackDiag:
    track_dump: bool = field(default=False, metadata={"comment": "Turn on or off track dumps (if on, follow=true)"})
    track_fields: bool = field(default=True, metadata={"comment": "Track fields in particle positions"})
    track_ndump: int = field(default=1000, metadata={"comment": "Number of iterations between track dumps"})
    track_nstore: int = field(default=5, metadata={"comment": "Values are stored every iteration if =1, every other iter if =2, etc"})
    track_info_file: str = field(default="./input/H+.tags", metadata={"comment": "Track information (particle tags to track)"})

    def __str__(self) -> str:
        return (
            f"track_diag\n{{\n"
            f"        track_dump={tfb(self.track_dump)},                ! {self.__dataclass_fields__['track_dump'].metadata['comment']}\n"
            f"        track_fields={tfb(self.track_fields)},                ! {self.__dataclass_fields__['track_fields'].metadata['comment']}\n"
            f"        track_ndump={self.track_ndump},                ! {self.__dataclass_fields__['track_ndump'].metadata['comment']}\n"
            f"        track_nstore={self.track_nstore},                ! {self.__dataclass_fields__['track_nstore'].metadata['comment']}\n"
            f"        track_info_file={qs(self.track_info_file)},                ! {self.__dataclass_fields__['track_info_file'].metadata['comment']}\n"
            f"}}"
        )

@dataclass
class DiagSpeciesTotal:
    dmp_vfld: Tuple[bool, ... ] = field(default=(False, False), metadata={"comment": "Dump total velocity field"})
    pres: Tuple[int, ... ] = field(default=(512, 512, 512), metadata={"comment": "Resolution for total phase space (defaults to 512)"})

    def __str__(self) -> str:
        return (
            f"diag_species_total\n{{\n"
            f"        dmp_vfld(1:{len(self.dmp_vfld)})={','.join(map(tfb, self.dmp_vfld))},                ! {self.__dataclass_fields__['dmp_vfld'].metadata['comment']}\n"
            f"        pres(1:{len(self.pres)})={self.pres[0]},{self.pres[1]},{self.pres[2]},                ! {self.__dataclass_fields__['pres'].metadata['comment']}\n"
            f"}}"
        )

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
                file.write(f"!---------- {section_name.replace('_', ' ')} ----------\n")
                file.write(f"{str(getattr(self, section_name))}\n")

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
    # create from default
    input_data = DHybridInput()
    print("Created default data:")
    print(input_data)
    # Output the data to a file
    input_data.to_file('input_default')

    # Create an instance from the input file
    input_data = DHybridInput.from_file('./templates/dHybridR/input/input')
    print("Loaded data from input file:")
    print(input_data)


    # Output the data back to a file
    output_filename = 'output'
    input_data.to_file(output_filename)
    print(f"Data has been written to {output_filename}")
