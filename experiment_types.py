from dataclasses import dataclass


@dataclass
class ExperimentResult:
    """
    This class is used to store the results of an experiment.
    """
    temperature: float
    response_length: int
    llm_answer: str
    correct_answer: str
    llm_name: str
    question_id: int
    top_p: float
    prompt_name: str
    doubt_injection_prob: float
    injection_string: str
