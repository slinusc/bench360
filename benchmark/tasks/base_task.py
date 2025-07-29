from abc import ABC, abstractmethod

class BaseTask(ABC):
    """
    Abstract base class for all NLP tasks.
    """

    @abstractmethod
    def generate_prompts(self, num_examples: int):
        """
        Should return a list of prompts and reference answers.
        """
        pass

    @abstractmethod
    def quality_metrics(self, generated: str, reference):
        """
        Should return a dictionary of task-specific evaluation metrics.
        """
        pass
