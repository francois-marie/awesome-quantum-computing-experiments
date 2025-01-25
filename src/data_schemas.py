from dataclasses import dataclass
from typing import Optional

@dataclass
class ExperimentBase:
    article_title: str
    link: str
    year: int
    platform: str
    notes: Optional[str] = None

@dataclass
class QECExperiment(ExperimentBase):
    code_parameters: str
    code_name: str

@dataclass
class MSDExperiment(ExperimentBase):
    pass

@dataclass
class EntangledExperiment(ExperimentBase):
    entangled_state_error: float

@dataclass
class QubitCountExperiment(ExperimentBase):
    qubit_count: int 