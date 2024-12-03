import bofire.data_models.candidates_api.api as candidates_api
from bofire.data_models.dataframes.api import (
    Candidates,
    ExperimentOutputValue,
    ExperimentRow,
    Experiments,
)
from bofire.data_models.strategies.api import RandomStrategy, SoboStrategy
from tests.bofire.data_models.specs.dataframes import specs as dataframes
from tests.bofire.data_models.specs.specs import Specs
from tests.bofire.data_models.specs.strategies import specs as strategies


specs = Specs([])


specs.add_valid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(RandomStrategy).obj(),
        "n_candidates": 1,
        "experiments": None,
        "pendings": None,
    },
)


specs.add_invalid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(SoboStrategy).obj(),
        "n_candidates": 1,
        "experiments": Experiments(
            rows=[
                ExperimentRow(
                    inputs={
                        "i5": 1,
                        "i6": 2,
                        "i7": 3,
                    },
                    outputs={
                        "o1": ExperimentOutputValue(value=1),
                        "o2": ExperimentOutputValue(value=2),
                    },
                ),
                ExperimentRow(
                    inputs={
                        "i5": 2,
                        "i6": 3,
                        "i7": 4,
                    },
                    outputs={
                        "o1": ExperimentOutputValue(value=2),
                        "o2": ExperimentOutputValue(value=3),
                    },
                ),
            ]
        ),
        "pendings": None,
    },
    error=ValueError,
    message="Extra inputs are not permitted",
)


specs.add_invalid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(RandomStrategy).obj(),
        "n_candidates": 1,
        "experiments": None,
        "pendings": dataframes.valid(Candidates).obj(),
    },
    error=ValueError,
    message="Extra inputs are not permitted",
)


specs.add_invalid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(RandomStrategy).obj(),
        "n_candidates": 1,
        "experiments": None,
        "pendings": None,
        "state": "INVALID",
    },
    error=ValueError,
    message="Input should be 'CREATED', 'CLAIMED', 'FAILED' or 'FINISHED'",
)


specs.add_invalid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(RandomStrategy).obj(),
        "n_candidates": 1,
        "experiments": None,
        "pendings": None,
        "state": candidates_api.ProposalStateEnum.FAILED,
        "error_message": 500,
    },
    error=ValueError,
    message="Input should be a valid string",
)


specs.add_invalid(
    candidates_api.CandidatesProposal,
    lambda: {
        "strategy_data": strategies.valid(RandomStrategy).obj(),
        "n_candidates": 1,
        "experiments": None,
        "pendings": None,
        "last_updated_at": "INVALID",
    },
    error=ValueError,
    message="Input should be a valid datetime or date",
)
