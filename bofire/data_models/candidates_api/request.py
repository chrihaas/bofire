from typing import Optional

from pydantic import Field, model_validator

from bofire.data_models.base import BaseModel
from bofire.data_models.dataframes.api import Candidates, Experiments
from bofire.data_models.strategies.api import AnyStrategy


class CandidatesRequest(BaseModel):
    """Request model for generating candidates."""

    strategy_data: AnyStrategy = Field(description="Strategy data model")
    n_candidates: int = Field(
        default=1, gt=0, description="Number of candidates to generate"
    )
    experiments: Optional[Experiments] = Field(
        default=None, description="Experiments to provide to the strategy"
    )
    pendings: Optional[Candidates] = Field(
        default=None, description="Candidates that are pending to be executed"
    )

    @model_validator(mode="after")
    def validate_experiments(self):
        """Validates the experiments."""
        if self.experiments is not None:
            self.strategy_data.domain.validate_experiments(self.experiments.to_pandas())
        return self

    @model_validator(mode="after")
    def validate_pendings(self):
        """Validates that pendings are None."""
        if self.pendings is not None:
            raise ValueError("Pendings must be None for proposals.")
        return self
